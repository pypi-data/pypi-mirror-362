"""reaction_info_extractor_clean.py

Single-file, maintainable CLI tool that pulls **enzyme-reaction performance data**
from chemistry PDFs using Google Gemini (text-only *and* vision) - now with
**true figure-image extraction** mirroring the enzyme-lineage workflow.

Key June 2025 additions
=======================
1. **Figure image helper** - locates the figure caption, then exports the first
   image **above** that caption using PyMuPDF (fitz). This PNG is sent to
   Gemini Vision for metric extraction.
2. **GeminiClient.generate()** now accepts an optional `image_b64` arg and
   automatically switches to a *vision* invocation when provided.
3. **extract_metrics_for_enzyme()** chooses between three tiers:

      * *Table* -> caption + following rows (text-only)
      * *Figure* -> image bytes (vision) *or* caption fallback
      * *Other* -> page-level text

   If the vision route fails (no JSON), it gracefully falls back to caption
   text so the pipeline never crashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from base64 import b64encode, b64decode
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple

import fitz  # PyMuPDF - for image extraction
import google.generativeai as genai  # type: ignore
import pandas as pd
from PyPDF2 import PdfReader
import io

###############################################################################
# 1 - CONFIG & CONSTANTS
###############################################################################

@dataclass
class Config:
    """Centralised tunables so tests can override them easily."""

    model_name: str = "gemini-2.5-flash"
    location_temperature: float = 0.0
    extract_temperature: float = 0.0
    model_reaction_temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 12288
    pdf_cache_size: int = 8
    retries: int = 2

@dataclass
class CompoundMapping:
    """Mapping between compound identifiers and IUPAC names."""
    identifiers: List[str]
    iupac_name: str
    common_names: List[str] = field(default_factory=list)
    compound_type: str = "unknown"
    source_location: Optional[str] = None

###############################################################################
# 2 - LOGGING
###############################################################################

LOGGER = logging.getLogger("reaction_info_extractor")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(levelname)s [%(name)s] %(message)s"))
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)

# --- Debug dump helper ----------------------------------------------------
def _dump(text: str | bytes, path: Path | str) -> None:
    """Write `text` / `bytes` to `path`, creating parent dirs as needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if isinstance(text, (bytes, bytearray)) else "w"
    with p.open(mode) as fh:
        fh.write(text)

###############################################################################
# 3 - PDF UTILITIES
###############################################################################

def extract_text_by_page(path: Optional[Path]) -> List[str]:
    if path is None:
        return []
    reader = PdfReader(str(path))
    pages: List[str] = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception as exc:  # pragma: no cover
            LOGGER.warning("PyPDF2 failed on a page: %s", exc)
            pages.append("")
    return pages

###############################################################################
# 4 - GEMINI WRAPPER (text & vision)
###############################################################################

def get_model(cfg: Config):
    """Configure API key and return a `GenerativeModel` instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("Set the GEMINI_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(cfg.model_name)

# Bounded LRU caches to store prompt/image content by hash (prevents memory leaks)

class LRUCache:
    """Simple LRU cache implementation."""
    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self.cache = OrderedDict()
    
    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: str) -> None:
        if key in self.cache:
            # Update existing
            self.cache.move_to_end(key)
        else:
            # Add new, evict oldest if needed
            if len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)
        self.cache[key] = value
    
    def __len__(self) -> int:
        return len(self.cache)

# Global bounded caches
_PROMPT_CACHE = LRUCache(maxsize=1000)
_IMAGE_CACHE = LRUCache(maxsize=500)  # Images are larger, so smaller cache

def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics for debugging."""
    return {
        "gemini_cache_info": _cached_gemini_call.cache_info(),
        "prompt_cache_size": len(_PROMPT_CACHE),
        "image_cache_size": len(_IMAGE_CACHE),
    }

@lru_cache(maxsize=1000)
def _cached_gemini_call(
    model_name: str,
    prompt_hash: str,
    image_hash: Optional[str],
    temperature: float,
    max_retries: int,
) -> str:
    """Pure cached function for Gemini API calls using only hash keys.
    
    Args:
        model_name: Name of the Gemini model
        prompt_hash: SHA256 hash of the prompt
        image_hash: SHA256 hash of the image (if any)
        temperature: Temperature for generation
        max_retries: Maximum number of retries
    
    Returns:
        Raw response text from Gemini
    """
    # Retrieve actual content from LRU cache
    prompt = _PROMPT_CACHE.get(prompt_hash)
    image_b64 = _IMAGE_CACHE.get(image_hash) if image_hash else None
    
    if prompt is None:
        raise RuntimeError(f"Prompt content not found for hash {prompt_hash}")
    
    # Configure API key (this is idempotent)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("Set the GEMINI_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    
    # Create model instance (not cached since it's lightweight)
    model = genai.GenerativeModel(model_name)
    
    for attempt in range(1, max_retries + 1):
        try:
            # Handle image if provided
            if image_b64:
                # Decode base64 string to bytes for Gemini API
                image_bytes = b64decode(image_b64)
                parts = [prompt, {"mime_type": "image/png", "data": image_bytes}]
            else:
                parts = [prompt]
            
            resp = model.generate_content(
                parts,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": 24576,  # Increased 3x from 8192
                }
            )
            # Track token usage if available
            try:
                if hasattr(resp, 'usage_metadata'):
                    input_tokens = getattr(resp.usage_metadata, 'prompt_token_count', 0)
                    output_tokens = getattr(resp.usage_metadata, 'candidates_token_count', 0)
                    if input_tokens or output_tokens:
                        try:
                            from .wrapper import add_token_usage
                            add_token_usage('reaction_info_extractor', input_tokens, output_tokens)
                        except ImportError:
                            pass  # wrapper not available
            except Exception:
                pass  # token tracking is best-effort
            
            return resp.text.strip()
        except Exception as exc:
            if attempt == max_retries:
                raise
            time.sleep(2 ** attempt)
    
    # Should never reach here
    raise RuntimeError("Max retries exceeded")

def _normalize_prompt_for_caching(prompt: str) -> str:
    """Normalize prompt for better cache hit rates by removing boilerplate and collapsing whitespace."""
    # Remove common boilerplate lines that don't affect the core query
    lines = prompt.split('\n')
    normalized_lines = []
    
    for line in lines:
        # Skip timestamp and debug lines
        if any(skip in line.lower() for skip in ['timestamp:', 'length:', 'characters', '===', '***']):
            continue
        # Skip lines that are just separators
        if line.strip() and not line.strip().replace('=', '').replace('-', '').replace('*', ''):
            continue
        # Collapse whitespace but preserve structure
        normalized_lines.append(' '.join(line.split()))
    
    # Join and collapse multiple newlines
    normalized = '\n'.join(normalized_lines)
    normalized = re.sub(r'\n\s*\n+', '\n\n', normalized)
    
    return normalized.strip()

def generate_json_with_retry(
    model,
    prompt: str,
    schema_hint: str | None = None,
    *,
    max_retries: int = 2,
    temperature: float = 0.0,
    debug_dir: str | Path | None = None,
    tag: str = 'gemini',
    image_b64: Optional[str] = None,
):
    """Call Gemini with retries & exponential back-off, returning parsed JSON."""
    # Generate cache keys based on normalized prompt and image content
    normalized_prompt = _normalize_prompt_for_caching(prompt)
    prompt_hash = hashlib.sha256(normalized_prompt.encode()).hexdigest()
    image_hash = hashlib.sha256(image_b64.encode()).hexdigest() if image_b64 else None
    
    # Log prompt details
    LOGGER.info("=== GEMINI API CALL: %s ===", tag.upper())
    LOGGER.info("Prompt length: %d characters", len(prompt))
    LOGGER.info("Prompt hash: %s", prompt_hash[:16])
    if image_hash:
        LOGGER.info("Image hash: %s", image_hash[:16])
    LOGGER.info("First 500 chars of prompt:\n%s\n...(truncated)", prompt[:500])
    
    # Save full prompt to debug directory if provided
    if debug_dir:
        debug_path = Path(debug_dir)
        debug_path.mkdir(parents=True, exist_ok=True)
        prompt_file = debug_path / f"{tag}_prompt_{int(time.time())}.txt"
        _dump(f"=== PROMPT FOR {tag.upper()} ===\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\nLength: {len(prompt)} characters\nHash: {prompt_hash}\n{'='*80}\n\n{prompt}",
              prompt_file)
        LOGGER.info("Full prompt saved to: %s", prompt_file)
    
    try:
        # Store content in bounded LRU caches for the cached function to retrieve
        _PROMPT_CACHE.put(prompt_hash, prompt)
        if image_hash and image_b64:
            _IMAGE_CACHE.put(image_hash, image_b64)
        
        # Check if this will be a cache hit
        cache_info_before = _cached_gemini_call.cache_info()
        
        # Use cached Gemini call (only with hash keys)
        LOGGER.info("Calling cached Gemini API...")
        raw = _cached_gemini_call(
            model_name=model.model_name,
            prompt_hash=prompt_hash,
            image_hash=image_hash,
            temperature=temperature,
            max_retries=max_retries,
        )
        
        # Log cache performance
        cache_info_after = _cached_gemini_call.cache_info()
        if cache_info_after.hits > cache_info_before.hits:
            LOGGER.info("✓ Cache HIT for prompt hash %s", prompt_hash[:16])
        else:
            LOGGER.info("✗ Cache MISS for prompt hash %s", prompt_hash[:16])
        
        # Log response
        LOGGER.info("Gemini response length: %d characters", len(raw))
        LOGGER.info("First 500 chars of response:\n%s\n...(truncated)", raw[:500])
        
        # Save full response to debug directory
        if debug_dir:
            response_file = debug_path / f"{tag}_response_{int(time.time())}.txt"
            _dump(f"=== RESPONSE FOR {tag.upper()} ===\nTimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\nLength: {len(raw)} characters\nHash: {prompt_hash}\n{'='*80}\n\n{raw}",
                  response_file)
            LOGGER.info("Full response saved to: %s", response_file)

        # Remove common Markdown fences more carefully
        if raw.startswith("```json"):
            raw = raw[7:].strip()  # Remove ```json
        elif raw.startswith("```"):
            raw = raw[3:].strip()  # Remove ```
        
        if raw.endswith("```"):
            raw = raw[:-3].strip()  # Remove trailing ```
        
        
        # Simple JSON parsing approach
        # Try direct parsing first
        LOGGER.debug(f"Raw JSON length: {len(raw)}")
        LOGGER.debug(f"Raw JSON first 200 chars: {raw[:200]}")
        LOGGER.debug(f"Raw JSON last 200 chars: {raw[-200:]}")
        
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as e:
            LOGGER.error(f"JSON parsing failed at position {e.pos}: {e}")
            LOGGER.error(f"Character at error: {repr(raw[e.pos] if e.pos < len(raw) else 'END')}")
            LOGGER.error(f"Context: {repr(raw[max(0, e.pos-20):e.pos+20])}")
            
            # Count braces and quotes for debugging
            open_braces = raw.count('{')
            close_braces = raw.count('}')
            quotes = raw.count('"')
            LOGGER.error(f"Braces: {open_braces} open, {close_braces} close. Quotes: {quotes}")
            
            # If that fails, try to extract JSON from the response using a simpler method
            try:
                # Look for the JSON object start and end
                start_idx = raw.find('{')
                if start_idx == -1:
                    raise json.JSONDecodeError("No JSON object found", raw, 0)
                
                # Find the matching closing brace by counting
                brace_count = 0
                end_idx = -1
                for i in range(start_idx, len(raw)):
                    if raw[i] == '{':
                        brace_count += 1
                    elif raw[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                
                if end_idx == -1:
                    raise json.JSONDecodeError("No matching closing brace found", raw, 0)
                
                json_str = raw[start_idx:end_idx]
                LOGGER.debug(f"Extracted JSON string: {json_str[:200]}...")
                parsed = json.loads(json_str)
                
            except json.JSONDecodeError:
                # Final fallback - try to use eval as a last resort (unsafe but functional)
                try:
                    # Replace problematic characters and try to parse as Python dict
                    safe_raw = raw.replace('null', 'None').replace('true', 'True').replace('false', 'False')
                    start_idx = safe_raw.find('{')
                    if start_idx == -1:
                        raise ValueError("No dict found")
                    
                    brace_count = 0
                    end_idx = -1
                    for i in range(start_idx, len(safe_raw)):
                        if safe_raw[i] == '{':
                            brace_count += 1
                        elif safe_raw[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_idx = i + 1
                                break
                    
                    if end_idx == -1:
                        raise ValueError("No matching closing brace found")
                    
                    dict_str = safe_raw[start_idx:end_idx]
                    parsed = eval(dict_str)  # This is unsafe but we trust our own generated content
                    LOGGER.warning("Used eval() fallback for JSON parsing")
                    
                except Exception:
                    # If all else fails, return empty dict
                    LOGGER.error("All JSON parsing methods failed")
                    if '[]' in raw:
                        parsed = []
                    else:
                        raise json.JSONDecodeError("No JSON structure found in response", raw, 0)
        
        LOGGER.info("Successfully parsed JSON response")
        return parsed
    except Exception as exc:
        LOGGER.error("Cached Gemini call failed: %s", exc)
        raise


###############################################################################
# 5 - PROMPTS (unchanged except for brevity)
###############################################################################

PROMPT_FIND_LOCATIONS = dedent("""
You are an expert reader of protein engineering manuscripts.
Given the following article captions and section titles, identify most promising locations
(tables or figures) that contain reaction performance data (yield, TON, TTN, ee, 
activity, etc.) for enzyme variants. Use your best judgement to include location showing full evolution lineage data.

IMPORTANT: Some papers have multiple enzyme lineages/campaigns with different 
performance data locations. Pay careful attention to:
- The caption text to identify which campaign/lineage the data is for
- Enzyme name prefixes that indicate different campaigns
- Different substrate/product types mentioned in captions

Respond with a JSON array where each element contains:
- "location": the identifier (e.g. "Table S1", "Figure 3", "Table 2")
- "type": one of "table", "figure"
- "confidence": your confidence score (0-100)
- "caption": the exact caption text for this location
- "reason": brief explanation (including if this is for a specific lineage/campaign)
- "lineage_hint": any indication of which enzyme group this data is for (or null)
- "campaign_clues": specific text in the caption that indicates the campaign (enzyme names, substrate types, etc.)

Tables are generally preferred over figures unless you are convinced that only the figure you find have complete lineage reaction matrix information. Some table don't have performance data, check provided context of the specific table.
Do not include too much sources, just return 2 or 3 sources.
Adjust confidence comparing all locations you will be returning, only rank figure the highest when you are absolutely certain table won't contain complete information.
When returning confidence scores, be more accurate and avoid scores that are too close together.
Respond ONLY with **minified JSON**. NO markdown fences.

Example:
[{"location": "Table S1", "type": "table", "confidence": 95, "caption": "Table S1. Detailed information...", "reason": "Complete performance metrics", "lineage_hint": "first enzyme family", "campaign_clues": "PYS lineage, pyrrolidine synthesis"}]
""")

PROMPT_EXTRACT_METRICS = dedent("""
You are given either (a) the PNG image of a figure panel, or (b) the caption /
text excerpt that contains numeric reaction performance data for an enzyme.

Extract ONLY the performance metrics, NOT substrate/product names or reaction conditions.

Return a JSON object with the following keys (use **null** only if the value is not mentioned at all):
  * "yield"              - yield as percentage with ONE decimal place precision
  * "ttn"               - turnover number (total turnovers)
  * "ton"               - turnover number if TTN not available
  * "selectivity"       - ee or er value with unit (e.g., "98% ee", ">99:1 er")
  * "conversion"        - conversion percentage if different from yield
  * "tof"               - turnover frequency (turnovers per time unit) if provided
  * "activity"          - specific activity if provided (with unit)
  * "other_metrics"     - dictionary of any other performance metrics with their units
  * "notes"             - any performance-related notes

IMPORTANT: 
- Extract ALL performance metrics provided, even if they use different units.
- Do NOT extract substrate/product names - these will come from SI
- Do NOT extract reaction conditions (temperature, pH, time, solvent)
- If the table shows different reactions (e.g., pyrrolidine vs indoline), note this in "notes"
- If you find conflicting values between bar graphs and text, or multiple sources for the same enzyme, ONLY use the most complete and reliable source (typically the primary figure/table being analyzed)

Respond ONLY with **minified JSON**. NO markdown fences, no commentary.
""")

PROMPT_EXTRACT_FIGURE_METRICS_BATCH = dedent("""
STEP 1: First, identify ALL X-axis labels in the figure
- Read each X-axis label from left to right
- List exactly what text appears under each bar/data point
- Note: Labels may be abbreviated or use different naming conventions

STEP 2: Match X-axis labels to target enzyme variants
- Compare each X-axis label against the target enzyme list below
- Look for partial matches, abbreviations, or similar naming patterns
- If an X-axis label doesn't match any target enzyme, still include it for completeness

STEP 3: Identify Y-axis scales and what they measure
- Look at the Y-axis labels and tick marks to understand what each axis measures
- If there are multiple Y-axes (left and right), read the axis labels and units
- Note the minimum and maximum values on each axis scale
- Identify which visual elements (bars, dots, lines) correspond to which axis

STEP 4: Extract values for each matched variant
- For each X-axis position, identify which visual elements belong to that position
- LEFT Y-axis (bars): Measure bar height against the left scale by reading tick marks
- RIGHT Y-axis (dots): Measure dot position against the right scale by reading tick marks
- CRITICAL: Read actual scale values from the axis labels and tick marks
- Verify: taller bars should have higher values, higher dots should have higher values

Target enzymes to find and extract:
{enzyme_names}

Instructions:
1. First, list ALL X-axis labels you can see in the figure
2. Match each X-axis label to the target enzyme variants
3. For matched variants, extract both bar heights (left Y-axis) and dot positions (right Y-axis)
4. Return data only for variants that have clear X-axis labels and are matched to targets

Return JSON with the identified enzyme variant names as keys containing:
  * "x_axis_label" - the exact text from the X-axis for this variant
  * "yield" - percentage from left Y-axis bar height measurement
  * "ttn" - turnover number from right Y-axis dot position measurement
  * "ton" - if TTN not available
  * "selectivity" - if shown
  * "conversion" - if different from yield
  * "tof" - if provided
  * "activity" - if provided
  * "other_metrics" - other metrics
  * "notes" - REQUIRED: Describe the X-axis label, bar position, and dot position (e.g., "X-axis shows P411-CIS, leftmost bar is very short, dot is at bottom")

CRITICAL: Return ONLY valid JSON in this exact format:
{{"enzyme_name": {{"x_axis_label": "label", "yield": number, "ttn": number, "notes": "description"}}}}

Rules:
- Use double quotes for all strings
- No markdown, no commentary, no explanations
- All values must be properly formatted
- Ensure JSON is complete and valid
- Do not truncate or cut off the response
- IMPORTANT: When extracting data, prioritize the most complete source that shows data for ALL variants. If there are conflicting values between different sources (e.g., bar graph vs text values), use the source that provides complete data for all target enzymes and ignore partial or conflicting values from other sources
""")

# Removed substrate scope IUPAC extraction - now handled in model reaction only

PROMPT_FIND_MODEL_REACTION_LOCATION = dedent("""
You are an expert reader of chemistry manuscripts.
Given the following text sections, identify where the MODEL REACTION information is located.

The model reaction is the STANDARD reaction used to evaluate all enzyme variants 
(not the substrate scope). Look for:

- Sections titled "Model Reaction", "Standard Reaction", "General Procedure"
- Text describing the reaction conditions used for enzyme evolution/screening
- Sections describing which substrates were used as the benchmark
- Compound numbers (e.g., "6a", "7a") used in the model reaction

Also identify where the IUPAC names for these specific compounds are listed.

Respond with a JSON object containing:
{
  "model_reaction_location": {
    "location": "section name or description",
    "confidence": 0-100,
    "reason": "why this contains the model reaction",
    "compound_ids": ["list", "of", "compound", "IDs", "if", "found"]
  },
  "conditions_location": {
    "location": "where reaction conditions are described",
    "confidence": 0-100
  },
  "iupac_location": {
    "location": "where IUPAC names are listed (usually SI compound characterization)",
    "confidence": 0-100,
    "compound_section_hint": "specific section to look for compound IDs"
  }
}

Respond ONLY with **minified JSON**. NO markdown fences, no commentary.
""")

PROMPT_MODEL_REACTION = dedent("""
Extract the model/standard reaction used to evaluate enzyme variants in this paper.

This is the reaction used for directed evolution screening, NOT the substrate scope.
Look for terms like "model reaction", "standard substrate", "benchmark reaction", 
or the specific reaction mentioned in enzyme screening/evolution sections.

CRITICAL STEPS FOR IUPAC NAMES:
1. First identify the compound IDs used in the model reaction (e.g., "6a", "7a")
2. Then search the provided context for these compound IDs to find their IUPAC names
3. Look for sections with "Compound 6a", "Product 7a", or similar patterns
4. The IUPAC names are usually given after the compound ID in parentheses or after a colon

CRITICAL FOR SUBSTRATE CONCENTRATION:
- Look carefully in FIGURES and figure captions for substrate concentration information
- Figures often show detailed reaction conditions that may not be in the main text
- Identify the ACTUAL SUBSTRATES being transformed (not reducing agents or cofactors)
- Common pattern: "[X] mM [substrate name]" or "[substrate]: [X] mM"
- DO NOT confuse reducing agents (dithionite, NADH, etc.) with actual substrates
- The substrate is the molecule being chemically transformed by the enzyme

Return a JSON object with:
  * "substrate_list" - Array of substrate identifiers as used in the paper (e.g., ["5", "6a"])
  * "substrate_iupac_list" - Array of IUPAC names for ALL substrates/reagents
  * "product_list" - Array of product identifiers as used in the paper (e.g., ["7a"])
  * "product_iupac_list" - Array of IUPAC names for ALL products formed
  * "reaction_substrate_concentration" - Concentration of actual substrate(s) being transformed, NOT reducing agents like dithionite
  * "cofactor" - Any cofactors used (e.g., "NADH", "NADPH", "FAD", "heme", etc.) or null if none
  * "reaction_temperature" - reaction temperature (e.g., "25°C", "room temperature")
  * "reaction_ph" - reaction pH
  * "reaction_buffer" - buffer system (e.g., "50 mM potassium phosphate")
  * "reaction_other_conditions" - other important conditions (enzyme loading, reducing agents like dithionite, time, anaerobic, etc.)

IMPORTANT: 
- Extract the reaction used for ENZYME EVOLUTION/SCREENING (not substrate scope)
- Substrate concentration = concentration of chemicals being transformed, NOT reducing agents (dithionite, NADH, etc.)
- Maintain correspondence: substrate_list[i] should map to substrate_iupac_list[i], same for products
- If a compound ID has no IUPAC name found, still include it in the list with null in the IUPAC list
- For IUPAC names, look for the SYSTEMATIC chemical names, NOT common/trivial names
- Search the provided context for systematic names - they typically:
  * Use numerical locants (e.g., "prop-2-enoate" not "acrylate")
  * Follow IUPAC nomenclature rules
  * May be found in compound characterization sections
- If you find a common name in the reaction description, search the context for its systematic equivalent
- Look for the exact systematic names as written in the compound characterization
- Do NOT include stereochemistry prefixes like (1R,2S) unless they are part of the compound name in the SI

Respond ONLY with **minified JSON**. NO markdown fences, no commentary.
""")

PROMPT_ANALYZE_LINEAGE_GROUPS = dedent("""
You are analyzing enzyme performance data from a protein engineering manuscript.
Based on the performance data locations and enzyme names, determine if there are 
distinct enzyme lineage groups that were evolved for different purposes.

Look for patterns such as:
- Different tables/figures for different enzyme groups
- Enzyme naming patterns that suggest different lineages
- Different reaction types mentioned in notes or captions
- Clear separations in how variants are organized

Return a JSON object with:
{
  "has_multiple_lineages": true/false,
  "lineage_groups": [
    {
      "group_id": "unique identifier you assign",
      "data_location": "where this group's data is found",
      "enzyme_pattern": "naming pattern or list of enzymes",
      "reaction_type": "what reaction this group catalyzes",
      "evidence": "why you grouped these together"
    }
  ],
  "confidence": 0-100
}

If only one lineage exists, return has_multiple_lineages: false with a single group.

Respond ONLY with **minified JSON**.
""")

PROMPT_FIND_LINEAGE_MODEL_REACTION = dedent("""
For the enzyme group with performance data in {location}, identify the specific 
model reaction used to screen/evaluate these variants.

Context about this group:
{group_context}

Look for:
- References to the specific substrate/product used for this enzyme group
- Text near the performance data location describing the reaction
- Connections between the enzyme names and specific substrates
- Any mention of "screened with", "tested against", "substrate X was used"

Return:
{{
  "substrate_ids": ["list of substrate IDs for this group"],
  "product_ids": ["list of product IDs for this group"],
  "confidence": 0-100,
  "evidence": "text supporting this substrate/product assignment"
}}

Respond ONLY with **minified JSON**.
""")

PROMPT_COMPOUND_MAPPING = dedent("""
Extract compound identifiers and their IUPAC names from the provided sections.

Look for ALL compounds mentioned, including:
1. Compounds with explicit IUPAC names in the text
2. Common reagents where you can provide standard IUPAC names
3. Products that may not be explicitly characterized

CRITICAL - NO HALLUCINATION:
- Extract IUPAC names EXACTLY as written in the source
- DO NOT modify, correct, or "improve" any chemical names
- If a name is written as "benzyl-2-phenylcyclopropane-1-carboxylate", keep it exactly
- Only provide standard IUPAC names for common reagents if not found in text
- If no IUPAC name is found for a compound, return null for iupac_name
- Include ALL compounds found or referenced

IMPORTANT - ONE NAME PER COMPOUND:
- Return ONLY ONE IUPAC name per compound identifier
- If multiple names are found for the same compound, choose the one most likely to be the IUPAC name:
  1. Names explicitly labeled as "IUPAC name:" in the text
  2. Names in compound characterization sections
  3. The most systematic/complete chemical name
- Do NOT return multiple IUPAC names in a single iupac_name field

Return as JSON:
{
  "compound_mappings": [
    {
      "identifier": "compound identifier",
      "iupac_name": "complete IUPAC name",
      "common_names": ["any alternative names"],
      "compound_type": "substrate/product/reagent/other",
      "source_location": "where found or inferred"
    }
  ]
}
""")

###############################################################################
# 6 - EXTRACTION ENGINE
###############################################################################

class ReactionExtractor:
    _FIG_RE = re.compile(r"(?:supplementary\s+)?fig(?:ure)?\s+s?\d+[a-z]?", re.I)
    _TAB_RE = re.compile(r"(?:supplementary\s+)?tab(?:le)?\s+s?\d+[a-z]?", re.I)

    def __init__(self, manuscript: Path, si: Optional[Path], cfg: Config, debug_dir: Optional[Path] = None, 
                 campaign_filter: Optional[str] = None, all_campaigns: Optional[List[str]] = None):
        self.manuscript = manuscript
        self.si = si
        self.cfg = cfg
        self.model = get_model(cfg)
        self.debug_dir = debug_dir
        self.campaign_filter = campaign_filter  # Filter for specific campaign
        self.all_campaigns = all_campaigns or []  # List of all campaigns for context
        
        # Cache for extracted figures to avoid redundant extractions (bounded to prevent memory leaks)
        self._figure_cache = LRUCache(maxsize=100)  # Figures are large, so smaller cache
        self._model_reaction_locations_cache = LRUCache(maxsize=50)
        
        # Cache for compound mappings to avoid repeated API calls (bounded to prevent memory leaks)
        self._compound_mapping_cache = LRUCache(maxsize=1000)
        self._compound_mapping_text_cache = LRUCache(maxsize=500)  # Cache text extractions too
        
        # Cache for reaction locations to avoid repeated API calls (bounded to prevent memory leaks)
        self._reaction_locations_cache = LRUCache(maxsize=50)
        
        # Create debug directory if specified
        if self.debug_dir:
            self.debug_dir = Path(self.debug_dir)
            self.debug_dir.mkdir(parents=True, exist_ok=True)
            LOGGER.info("Debug output will be saved to: %s", self.debug_dir)
        
        if self.campaign_filter:
            LOGGER.info("Filtering extraction for campaign: %s", self.campaign_filter)

        # Preload text pages
        LOGGER.info("Reading PDFs…")
        self.ms_pages = extract_text_by_page(manuscript)
        self.si_pages = extract_text_by_page(si)
        self.all_pages = self.ms_pages + self.si_pages

        # Keep open fitz Docs for image extraction
        self.ms_doc = fitz.open(str(manuscript))
        self.si_doc = fitz.open(str(si)) if si else None

    # ------------------------------------------------------------------
    # 6.1 Find locations (unchanged)
    # ------------------------------------------------------------------

    def _collect_captions_and_titles(self) -> str:
        # Pattern to match Table or Figure with optional leading whitespace and page numbers
        # This catches all variations including "Supplementary Table", "Table S 2", "Figure S1", etc.
        # Also handles cases where there's whitespace or page numbers before the caption
        cap_pattern = re.compile(r"^[\s\d]*\s*(Supplementary\s+Table|Table|Figure).*", re.I | re.M)
        captions: List[str] = []
        
        # Process each page individually to avoid TOC entries
        for page_idx, page_text in enumerate(self.all_pages):
            # Skip if this looks like a TOC page
            if self._is_toc_page(page_text):
                LOGGER.debug("Skipping TOC page %d for caption collection", page_idx + 1)
                continue
                
            # Find all figure/table captions with more context
            for match in cap_pattern.finditer(page_text):
                caption_line = match.group(0).strip()
                
                # Skip if this looks like a TOC entry (has page number at end or dots)
                if re.search(r'\.{3,}|\.{2,}\s*\d+\s*$|\s+\d+\s*$', caption_line):
                    LOGGER.debug("Skipping TOC-style entry: %s", caption_line[:50])
                    continue
                
                caption_start = match.start()
                
                # For tables, include much more content after the caption to show actual table data
                # For figures, include substantial content to show what the figure contains
                is_table = 'table' in match.group(1).lower()
                # Increase context for figures to ensure we capture descriptive text
                max_chars = 8000 if is_table else 3000
                
                # Get context including text before and after the caption
                # Include some text before to help identify the location
                context_before = max(0, caption_start - 200)
                context_after = min(len(page_text), caption_start + max_chars)
                
                # Extract the full context
                full_context = page_text[context_before:context_after].strip()
                
                # Find the actual caption text (not just the "Figure X" part)
                # Look for text after the figure/table identifier that forms the caption
                caption_text = page_text[caption_start:context_after]
                
                # Try to find the end of the caption (usually ends with a period before next paragraph)
                caption_end_match = re.search(r'^[^\n]+\.[^\n]*(?:\n\n|\n(?=[A-Z]))', caption_text)
                if caption_end_match:
                    actual_caption = caption_text[:caption_end_match.end()].strip()
                else:
                    # Fallback: take first few lines
                    lines = caption_text.split('\n')
                    actual_caption = '\n'.join(lines[:3]).strip()
                
                # Ensure we have meaningful content, not just the figure number
                if len(actual_caption) > 20:  # More than just "Figure S23."
                    # For the prompt, include the full context to help identify what's in the figure
                    caption_with_context = f"{actual_caption}\n\n[Context around figure/table:]\n{full_context}"
                    captions.append(caption_with_context)
            
        # Also look for SI section titles
        si_titles = re.findall(r"^S\d+\s+[A-Z].{3,80}", "\n".join(self.si_pages), re.M)
        
        result = "\n".join(captions + si_titles)
        LOGGER.debug("Collected %d captions/titles, total length: %d chars", 
                    len(captions) + len(si_titles), len(result))
        
        # Log first few captions for debugging
        if captions:
            LOGGER.debug("First few captions: %s", captions[:3])
            
        return result

    def find_reaction_locations(self) -> List[Dict[str, Any]]:
        """Find all locations containing reaction performance data."""
        # Create cache key based on campaign filter
        cache_key = f"locations_{self.campaign_filter or 'all'}"
        
        # Check cache first
        cached_result = self._reaction_locations_cache.get(cache_key)
        if cached_result is not None:
            LOGGER.info("Using cached reaction locations for campaign: %s", self.campaign_filter or 'all')
            return cached_result
        
        # Add campaign context - always provide context to help model understanding
        campaign_context = ""
        if self.campaign_filter:
            campaigns_warning = ""
            if self.all_campaigns:
                campaigns_warning = f"""
            ALL CAMPAIGNS IN THIS PAPER:
            {chr(10).join([f"- {campaign}" for campaign in self.all_campaigns])}

            CRITICAL WARNING: Do NOT confuse campaigns! Each campaign uses completely different substrates.
            Be extremely careful to only extract data for the {self.campaign_filter} campaign.
            """
            
            campaign_context = f"""
            IMPORTANT: You are looking for performance data specifically for the {self.campaign_filter} campaign.
            Only return locations that contain data for this specific campaign.
            Ignore locations that contain data for other campaigns.
            {campaigns_warning}

            """
        else:
            # Even for single campaigns, provide context about what to look for
            campaign_context = f"""
            IMPORTANT: You are looking for performance data showing enzyme evolution progression.
            Look for locations that contain actual performance metrics (yield, TTN, TON, activity, etc.) 
            for multiple enzyme variants, not just mutation lists or method descriptions.

            Tables may only contain mutation information without performance data - check the actual 
            table content below the caption to verify if performance metrics are present.
            Figures with evolutionary lineage data often contain the actual performance matrix.

            """
        
        prompt = campaign_context + PROMPT_FIND_LOCATIONS + "\n\n" + self._collect_captions_and_titles()
        try:
            data = generate_json_with_retry(
                self.model,
                prompt,
                temperature=self.cfg.location_temperature,
                debug_dir=self.debug_dir,
                tag="find_locations"
            )
            # Handle both single dict (backwards compatibility) and list
            result = []
            if isinstance(data, dict):
                result = [data]
            elif isinstance(data, list):
                result = data
            else:
                LOGGER.error("Expected list or dict from Gemini, got: %s", type(data))
                result = []
            
            # Cache the result
            self._reaction_locations_cache.put(cache_key, result)
            LOGGER.info("Cached reaction locations for campaign: %s", self.campaign_filter or 'all')
            
            return result
        except Exception as e:
            LOGGER.error("Failed to find reaction locations: %s", e)
            return []

    def _get_base_location(self, location: str) -> str:
        """Extract the base location identifier (e.g., 'Table S1' from 'Table S1' or 'S41-S47').
        
        This helps group related locations that likely share the same model reaction.
        """
        # Common patterns for locations
        patterns = [
            (r'Table\s+S\d+', 'table'),
            (r'Figure\s+S\d+', 'figure'),
            (r'Table\s+\d+', 'table'),
            (r'Figure\s+\d+', 'figure'),
            (r'S\d+(?:-S\d+)?', 'supp'),  # Supplementary pages like S41-S47
        ]
        
        for pattern, loc_type in patterns:
            match = re.search(pattern, location, re.I)
            if match:
                return match.group(0)
        
        # Default: use the location as-is
        return location

    def analyze_lineage_groups(self, locations: List[Dict[str, Any]], enzyme_df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze if there are distinct lineage groups based on different locations.
        
        Key principle: Different locations (tables/figures) indicate different model reactions.
        """
        # Group locations by their base identifier
        location_groups = {}
        
        for loc in locations:
            location_id = loc['location']
            base_location = self._get_base_location(location_id)
            
            if base_location not in location_groups:
                location_groups[base_location] = []
            location_groups[base_location].append(loc)
        
        # Each unique base location represents a potential lineage group
        lineage_groups = []
        
        for base_loc, locs in location_groups.items():
            # Use the location with highest confidence as primary
            primary_loc = max(locs, key=lambda x: x.get('confidence', 0))
            
            # Create a group for this location
            group = {
                'group_id': base_loc,
                'data_location': primary_loc['location'],
                'all_locations': [l['location'] for l in locs],
                'lineage_hint': primary_loc.get('lineage_hint', ''),
                'caption': primary_loc.get('caption', ''),
                'confidence': primary_loc.get('confidence', 0)
            }
            lineage_groups.append(group)
        
        # Multiple distinct base locations = multiple model reactions
        has_multiple = len(location_groups) > 1
        
        LOGGER.info("Location-based lineage analysis: %d distinct base locations found", 
                   len(location_groups))
        for group in lineage_groups:
            LOGGER.info("  - %s: %s", group['group_id'], group['data_location'])
        
        return {
            'has_multiple_lineages': has_multiple,
            'lineage_groups': lineage_groups,
            'confidence': 95
        }
    
    def find_lineage_model_reaction(self, location: str, group_context: str, model_reaction_locations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Find the model reaction for a specific lineage group.
        Returns early if no relevant text is found to avoid unnecessary API calls."""
        
        # Gather relevant text near this location
        page_text = self._page_with_reference(location) or ""
        
        # Early exit if no text found for this location
        if not page_text or len(page_text.strip()) < 100:
            LOGGER.info("No sufficient text found for location %s, skipping lineage-specific extraction", location)
            return {}
        
        # Also check manuscript introduction for model reaction info
        intro_text = "\n\n".join(self.ms_pages[:3]) if self.ms_pages else ""
        
        # Quick relevance check - look for reaction-related keywords
        reaction_keywords = ["substrate", "product", "reaction", "compound", "synthesis", "procedure", "method"]
        combined_text = (page_text + intro_text).lower()
        if not any(keyword in combined_text for keyword in reaction_keywords):
            LOGGER.info("No reaction-related keywords found for location %s, skipping lineage extraction", location)
            return {}
        
        # Build the prompt with location and context
        prompt = PROMPT_FIND_LINEAGE_MODEL_REACTION.format(
            location=location,
            group_context=group_context
        )
        prompt += f"\n\nText near {location}:\n{page_text[:3000]}"
        prompt += f"\n\nManuscript introduction:\n{intro_text[:3000]}"
        
        # If we have model reaction locations, include text from those locations too
        text_added = False
        if model_reaction_locations:
            # Add text from model reaction location
            if model_reaction_locations.get("model_reaction_location", {}).get("location"):
                model_loc = model_reaction_locations["model_reaction_location"]["location"]
                model_text = self._get_text_around_location(model_loc)
                if model_text:
                    prompt += f"\n\nText from {model_loc} (potential model reaction location):\n{model_text[:3000]}"
                    text_added = True
            
            # Add text from conditions location (often contains reaction details)
            if model_reaction_locations.get("conditions_location", {}).get("location"):
                cond_loc = model_reaction_locations["conditions_location"]["location"]
                cond_text = self._get_text_around_location(cond_loc)
                if cond_text:
                    prompt += f"\n\nText from {cond_loc} (reaction conditions):\n{cond_text[:3000]}"
                    text_added = True
        
        # If we didn't find any model reaction locations and the page text is sparse, skip
        if not text_added and len(page_text.strip()) < 500:
            LOGGER.info("Insufficient context for lineage model reaction extraction at %s", location)
            return {}
        
        try:
            LOGGER.info("Attempting lineage-specific model reaction extraction for %s", location)
            data = generate_json_with_retry(
                self.model,
                prompt,
                temperature=self.cfg.model_reaction_temperature,
                debug_dir=self.debug_dir,
                tag=f"lineage_model_reaction_{location.replace(' ', '_')}"
            )
            
            # Validate the response has useful information
            if isinstance(data, dict) and (data.get('substrate_ids') or data.get('product_ids')):
                LOGGER.info("Lineage model reaction extraction successful for %s", location)
                return data
            else:
                LOGGER.info("Lineage model reaction extraction returned empty results for %s", location)
                return {}
                
        except Exception as e:
            LOGGER.error("Failed to find model reaction for lineage at %s: %s", location, e)
            return {}

    # ------------------------------------------------------------------
    # 6.2 Figure / Table context helpers
    # ------------------------------------------------------------------

    def _is_toc_page(self, page_text: str) -> bool:
        """Detect if a page is a Table of Contents page."""
        # Look for common TOC indicators
        toc_indicators = [
            "table of contents",
            "contents",
            r"\.{5,}",  # Multiple dots (common in TOCs)
            r"\d+\s*\n\s*\d+\s*\n\s*\d+",  # Multiple page numbers in sequence
        ]
        
        # Count how many TOC-like patterns we find
        toc_score = 0
        text_lower = page_text.lower()
        
        # Check for explicit TOC title
        if "table of contents" in text_lower or (
            "contents" in text_lower and text_lower.index("contents") < 200
        ):
            toc_score += 3
        
        # Check for multiple figure/table references with page numbers
        figure_with_page = re.findall(r'figure\s+[sS]?\d+.*?\.{2,}.*?\d+', text_lower)
        table_with_page = re.findall(r'table\s+[sS]?\d+.*?\.{2,}.*?\d+', text_lower)
        
        if len(figure_with_page) + len(table_with_page) > 5:
            toc_score += 2
        
        # Check for many dotted lines
        if len(re.findall(r'\.{5,}', page_text)) > 3:
            toc_score += 1
            
        return toc_score >= 2

    def _page_with_reference(self, ref_id: str) -> Optional[str]:
        for page in self.all_pages:
            if ref_id.lower() in page.lower():
                return page
        return None

    # ---- Table text helper - now returns full page ----
    def _extract_table_context(self, ref: str) -> str:
        page = self._page_with_reference(ref)
        if not page:
            return ""
        # Return the entire page content for better table extraction
        return page

    # ---- Figure caption helper (text fallback) ----
    def _extract_figure_caption(self, ref: str) -> str:
        page = self._page_with_reference(ref)
        if not page:
            return ""
        m = re.search(rf"({re.escape(ref)}[\s\S]{{0,800}}?\.)", page, re.I)
        if m:
            return m.group(1)
        for line in page.split("\n"):
            if ref.lower() in line.lower():
                return line
        return page[:800]

    def _ensure_rgb_pixmap(self, pix: fitz.Pixmap) -> fitz.Pixmap:
        """Ensure pixmap is in RGB colorspace for PIL compatibility."""
        if pix.alpha:  # RGBA -> RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        elif pix.colorspace and pix.colorspace.name not in ["DeviceRGB", "DeviceGray"]:
            # Convert unsupported colorspaces (CMYK, LAB, etc.) to RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        return pix

    # ---- NEW: Page image helper for both figures and tables ----
    def _extract_page_png(self, ref: str, extract_figure_only: bool = True) -> Optional[str]:
        """Export the page containing the reference as PNG.
        If extract_figure_only=True, extracts just the figure above the caption.
        If False, extracts the entire page (useful for tables).
        Returns a base64-encoded PNG or None."""
        LOGGER.debug("_extract_page_png called with ref='%s', extract_figure_only=%s", ref, extract_figure_only)
        
        # Check cache first
        cache_key = f"{ref}_{extract_figure_only}"
        cached_result = self._figure_cache.get(cache_key)
        if cached_result is not None:
            LOGGER.debug("Using cached figure for %s", ref)
            return cached_result
        
        # For table extraction, use multi-page approach
        if not extract_figure_only:
            pages_with_ref = self._find_pages_with_reference(ref)
            if pages_with_ref:
                LOGGER.debug(f"Found {len(pages_with_ref)} pages containing {ref}")
                return self._extract_multiple_pages_png(pages_with_ref, ref)
            return None

        # For figure extraction, search both documents for actual figure captions
        docs = list(filter(None, [self.ms_doc, self.si_doc]))
        LOGGER.debug("Searching for '%s' in %d documents", ref, len(docs))
        
        for doc_idx, doc in enumerate(docs):
            doc_name = "MS" if doc_idx == 0 else "SI"
            LOGGER.debug("Searching in %s document with %d pages", doc_name, doc.page_count)
            
            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                page_text = page.get_text()
                LOGGER.debug("Checking page %d of %s document (text length: %d chars)", 
                           page_number + 1, doc_name, len(page_text))
                
                # Skip Table of Contents pages
                if self._is_toc_page(page_text):
                    LOGGER.debug("Skipping page %d - detected as Table of Contents", page_number + 1)
                    continue
                
                # Look for figure caption pattern more flexibly
                # Normalize the reference to handle variations
                figure_num = ref.replace('Figure', '').replace('figure', '').strip()
                
                # Extract main figure number from subfigure (e.g., "1C" -> "1")
                main_figure_num = re.match(r'^(\d+)', figure_num)
                if main_figure_num:
                    main_figure_num = main_figure_num.group(1)
                else:
                    main_figure_num = figure_num
                
                # Create a flexible pattern that handles various spacing and formatting
                # This pattern looks for "Figure" (case insensitive) followed by optional spaces
                # then the figure number, then any of: period, colon, space+capital letter, or end of line
                # Also match at the beginning of a line to catch captions
                flexible_pattern = rf"(?i)(?:^|\n)\s*figure\s*{re.escape(main_figure_num)}(?:\.|:|(?=\s+[A-Z])|\s*$)"
                
                LOGGER.debug("Looking for figure caption '%s' with flexible pattern: %s", 
                           main_figure_num, flexible_pattern)
                
                caption_found = False
                cap_rect = None
                
                # Search for all matches of the flexible pattern
                for match in re.finditer(flexible_pattern, page_text, re.MULTILINE):
                    LOGGER.debug("Found potential figure caption: %s at position %d", match.group(0), match.start())
                    # Check if this is likely an actual caption (not just a reference)
                    match_start = match.start()
                    match_end = match.end()
                    
                    # Get surrounding context
                    context_start = max(0, match_start - 50)
                    context_end = min(len(page_text), match_end + 100)
                    context = page_text[context_start:context_end]
                    
                    # Check if this looks like a real caption (not just a reference)
                    # Look for words that typically precede figure references
                    preceding_text = page_text[max(0, match_start-20):match_start].lower()
                    if any(word in preceding_text for word in ['see ', 'in ', 'from ', 'shown in ', 'refer to ']):
                        LOGGER.debug("Skipping reference preceded by: %s", preceding_text.strip())
                        continue
                    
                    # Check if there's descriptive text after the figure number
                    remaining_text = page_text[match_end:match_end+100].strip()
                    
                    # For actual captions, there should be substantial descriptive text
                    if len(remaining_text) < 20:
                        LOGGER.debug("Skipping potential reference: insufficient text after (%d chars)", len(remaining_text))
                        continue
                        
                    # Check if the remaining text looks like a caption (contains descriptive words)
                    # Expanded list of caption keywords to be more inclusive
                    first_words = remaining_text[:50].lower()
                    caption_keywords = ['detailed', 'representative', 'shows', 'comparison', 
                                      'illustrates', 'demonstrates', 'results', 'data',
                                      'chromatogram', 'spectra', 'analysis', 'site-directed',
                                      'mutagenesis', 'mutants', 'evolution', 'directed',
                                      'screening', 'reaction', 'variant', 'enzyme', 'protein',
                                      'activity', 'performance', 'yield', 'selectivity',
                                      'characterization', 'optimization', 'development',
                                      'structure', 'domain', 'crystal', 'model']
                    if not any(word in first_words for word in caption_keywords):
                        LOGGER.debug("Skipping: doesn't look like caption text: %s", first_words)
                        continue
                    
                    # Found actual figure caption, get its position
                    caption_text = match.group(0)
                    text_instances = page.search_for(caption_text, quads=False)
                    if text_instances:
                        cap_rect = text_instances[0]
                        caption_found = True
                        LOGGER.info("Found actual caption for %s: '%s' with following text: '%s...'", 
                                  ref, caption_text, remaining_text[:50])
                        break
                
                if not caption_found:
                    # Debug: show what figure-related text is actually on this page
                    figure_mentions = [line.strip() for line in page_text.split('\n') 
                                     if 'figure' in line.lower() and main_figure_num.lower() in line.lower()]
                    if figure_mentions:
                        LOGGER.debug("Page %d has figure mentions but no caption match: %s", 
                                   page_number, figure_mentions[:3])
                    
                    # For supplementary figures, also check for "supplementary" mentions
                    if 'supplementary' in ref.lower():
                        supp_mentions = [line.strip() for line in page_text.split('\n')
                                       if 'supplementary' in line.lower() and 'figure' in line.lower()]
                        if supp_mentions:
                            LOGGER.warning("Found supplementary figure mentions on page %d but no caption match. First 3: %s", 
                                         page_number + 1, supp_mentions[:3])
                    continue
                
                if extract_figure_only:
                    # Extract only the area above the caption (the actual figure)
                    # This excludes caption text and focuses on visual elements
                    LOGGER.info("Extracting figure area above caption for %s", ref)
                    
                    # Get the page dimensions
                    page_rect = page.rect
                    
                    # Extract the area above the caption
                    if cap_rect:
                        # Extract from top of page to top of caption
                        figure_rect = fitz.Rect(0, 0, page_rect.width, cap_rect.y0)
                        LOGGER.debug("Extracting figure area: %s (caption at y=%f)", figure_rect, cap_rect.y0)
                    else:
                        # If no caption found, use top 80% of page
                        figure_rect = fitz.Rect(0, 0, page_rect.width, page_rect.height * 0.8)
                        LOGGER.debug("No caption found, using top 80% of page: %s", figure_rect)
                    
                    # Extract the figure area only
                    mat = fitz.Matrix(5.0, 5.0)  # 5x zoom for better quality
                    pix = page.get_pixmap(matrix=mat, clip=figure_rect)
                    pix = self._ensure_rgb_pixmap(pix)
                    img_bytes = pix.tobytes("png")
                    
                    # Save PNG to debug directory if available
                    if self.debug_dir:
                        timestamp = int(time.time())
                        png_file = self.debug_dir / f"figure_{ref.replace(' ', '_')}_{timestamp}.png"
                        with open(png_file, 'wb') as f:
                            f.write(img_bytes)
                        LOGGER.info("Saved figure page to: %s", png_file)
                    
                    result = b64encode(img_bytes).decode()
                    # Cache the result
                    self._figure_cache.put(cache_key, result)
                    return result
                else:
                    # Extract the entire page as an image
                    mat = fitz.Matrix(5.0, 5.0)  # 5x zoom for better quality
                    pix = page.get_pixmap(matrix=mat)
                    pix = self._ensure_rgb_pixmap(pix)
                    img_bytes = pix.tobytes("png")
                    
                    # Save PNG to debug directory if available
                    if self.debug_dir:
                        timestamp = int(time.time())
                        png_file = self.debug_dir / f"page_{ref.replace(' ', '_')}_{timestamp}.png"
                        with open(png_file, 'wb') as f:
                            f.write(img_bytes)
                        LOGGER.info("Saved page image to: %s", png_file)
                    
                    result = b64encode(img_bytes).decode()
                    # Cache the result
                    self._figure_cache.put(cache_key, result)
                    return result
        
        # Fallback: If no caption found, try to find any page that mentions this figure
        LOGGER.info("No figure caption found for '%s', trying fallback search", ref)
        
        for doc_idx, doc in enumerate(docs):
            doc_name = "MS" if doc_idx == 0 else "SI"
            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                page_text = page.get_text()
                
                # Look for any mention of the figure reference
                if re.search(rf'\b{re.escape(ref)}\b', page_text, re.IGNORECASE):
                    LOGGER.info("Found '%s' mentioned on page %d of %s document (fallback)", 
                               ref, page_number + 1, doc_name)
                    
                    # Extract the entire page as the figure might be on this page
                    mat = fitz.Matrix(5.0, 5.0)  # 5x zoom for better quality
                    pix = page.get_pixmap(matrix=mat)
                    pix = self._ensure_rgb_pixmap(pix)
                    img_bytes = pix.tobytes("png")
                    
                    # Save PNG to debug directory if available
                    if self.debug_dir:
                        timestamp = int(time.time())
                        png_file = self.debug_dir / f"fallback_{ref.replace(' ', '_')}_{timestamp}.png"
                        with open(png_file, 'wb') as f:
                            f.write(img_bytes)
                        LOGGER.info("Saved fallback page image to: %s", png_file)
                    
                    result = b64encode(img_bytes).decode()
                    # Cache the result
                    self._figure_cache.put(cache_key, result)
                    return result
        
        LOGGER.warning("_extract_page_png returning None for '%s' - figure not found in any document", ref)
        return None
    
    def _find_pages_with_reference(self, ref: str) -> List[Tuple[fitz.Document, int]]:
        """Find all pages containing the reference across documents.
        Prioritizes pages with actual captions over just references.
        Returns list of (document, page_number) tuples."""
        pages_found = []
        caption_pages = []
        
        for doc in filter(None, [self.ms_doc, self.si_doc]):
            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                page_text = page.get_text()
                
                # Skip Table of Contents pages
                if self._is_toc_page(page_text):
                    LOGGER.debug("Skipping TOC page %d in _find_pages_with_reference", page_number + 1)
                    continue
                
                # Check for actual figure caption first
                if ref.lower().startswith('figure'):
                    figure_num = ref.replace('Figure ', '').replace('figure ', '')
                    
                    # Extract main figure number from subfigure (e.g., "1C" -> "1")
                    main_figure_num = re.match(r'^(\d+)', figure_num)
                    if main_figure_num:
                        main_figure_num = main_figure_num.group(1)
                    else:
                        main_figure_num = figure_num
                    
                    caption_patterns = [
                        rf"^Figure\s+{re.escape(main_figure_num)}\.",
                        rf"^Figure\s+{re.escape(main_figure_num)}:",
                        rf"^Figure\s+{re.escape(main_figure_num)}\s+[A-Z]"
                    ]
                    
                    for pattern in caption_patterns:
                        if re.search(pattern, page_text, re.MULTILINE | re.IGNORECASE):
                            caption_pages.append((doc, page_number))
                            break
                
                # Fallback to any mention of the reference
                if ref.lower() in page_text.lower():
                    pages_found.append((doc, page_number))
        
        # Return caption pages first, then other pages
        return caption_pages + [p for p in pages_found if p not in caption_pages]
    
    def _extract_multiple_pages_png(self, pages: List[Tuple[fitz.Document, int]], ref: str = "unknown") -> Optional[str]:
        """Extract multiple pages as a combined PNG image."""
        if not pages:
            return None
            
        # Sort pages by document and page number
        pages.sort(key=lambda x: (id(x[0]), x[1]))
        
        # Extract the range of pages including one page after
        all_images = []
        for i, (doc, page_num) in enumerate(pages):
            # Add the current page
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
            pix = doc.load_page(page_num).get_pixmap(matrix=mat)
            pix = self._ensure_rgb_pixmap(pix)
            all_images.append(pix)
            
            # Only extract the page containing the reference (removed next page logic)
        
        if not all_images:
            return None
            
        # If only one page, return it directly
        if len(all_images) == 1:
            pix = self._ensure_rgb_pixmap(all_images[0])
            img_bytes = pix.tobytes("png")
            
            # Save debug file if available
            if self.debug_dir:
                timestamp = int(time.time())
                png_file = self.debug_dir / f"page_{ref.replace(' ', '_')}_{timestamp}.png"
                with open(png_file, 'wb') as f:
                    f.write(img_bytes)
                LOGGER.info("Saved multi-page image to: %s", png_file)
            
            return b64encode(img_bytes).decode()
            
        # Combine multiple pages vertically
        if not all_images:
            return None
            
        if len(all_images) == 1:
            pix = self._ensure_rgb_pixmap(all_images[0])
            return b64encode(pix.tobytes("png")).decode()
            
        # Calculate dimensions for combined image
        total_height = sum(pix.height for pix in all_images)
        max_width = max(pix.width for pix in all_images)
        
        LOGGER.info(f"Combining {len(all_images)} pages into single image ({max_width}x{total_height})")
        
        # Create a new document with a single page that can hold all images
        output_doc = fitz.open()
        
        # Create a page with the combined dimensions
        # Note: PDF pages have a max size, so we scale if needed
        max_pdf_dimension = 14400  # PDF max is ~200 inches at 72 DPI
        scale = 1.0
        if total_height > max_pdf_dimension or max_width > max_pdf_dimension:
            scale = min(max_pdf_dimension / total_height, max_pdf_dimension / max_width)
            total_height = int(total_height * scale)
            max_width = int(max_width * scale)
            LOGGER.warning(f"Scaling down by {scale:.2f} to fit PDF limits")
        
        page = output_doc.new_page(width=max_width, height=total_height)
        
        # Insert each image into the page
        y_offset = 0
        for i, pix in enumerate(all_images):
            # Center each image horizontally
            x_offset = (max_width - pix.width * scale) / 2
            
            # Create rect for image placement
            rect = fitz.Rect(x_offset, y_offset, 
                           x_offset + pix.width * scale, 
                           y_offset + pix.height * scale)
            
            # Insert the image
            page.insert_image(rect, pixmap=pix)
            y_offset += pix.height * scale
            
        # Convert the page to a pixmap
        # Limit zoom factor to avoid creating excessively large images
        # Gemini has limits on image size (approx 20MB or 20 megapixels)
        zoom = 5.0
        estimated_pixels = (max_width * zoom) * (total_height * zoom)
        max_pixels = 20_000_000  # 20 megapixels
        
        if estimated_pixels > max_pixels:
            # Calculate appropriate zoom to stay under limit
            zoom = min(5.0, (max_pixels / (max_width * total_height)) ** 0.5)
            LOGGER.warning(f"Reducing zoom from 5.0 to {zoom:.2f} to stay under {max_pixels/1e6:.1f} megapixel limit")
        
        mat = fitz.Matrix(zoom, zoom)
        combined_pix = page.get_pixmap(matrix=mat)
        combined_pix = self._ensure_rgb_pixmap(combined_pix)
        
        # Convert to PNG and return
        img_bytes = combined_pix.tobytes("png")
        
        # Check final size
        final_size_mb = len(img_bytes) / (1024 * 1024)
        if final_size_mb > 20:
            LOGGER.warning(f"Combined image is {final_size_mb:.1f}MB, may be too large for vision API")
        output_doc.close()
        
        # Save debug file if available
        if self.debug_dir:
            timestamp = int(time.time())
            png_file = self.debug_dir / f"combined_pages_{ref.replace(' ', '_')}_{timestamp}.png"
            with open(png_file, 'wb') as f:
                f.write(img_bytes)
            LOGGER.info("Saved combined multi-page image to: %s", png_file)
        
        return b64encode(img_bytes).decode()

    # ------------------------------------------------------------------
    # 6.3 Extract metrics in batch
    # ------------------------------------------------------------------
    
    def _validate_location_exists(self, ref: str) -> bool:
        """Verify that the referenced location actually exists in the document."""
        # Search for the actual reference in both manuscript and SI documents
        docs_to_check = [self.ms_doc]
        if self.si_doc:
            docs_to_check.append(self.si_doc)
            
        for doc in docs_to_check:
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Look for table references like "Table 1", "Table S1", etc.
                if re.search(rf'\b{re.escape(ref)}\b', text, re.IGNORECASE):
                    return True
        
        return False

    def _validate_context(self, snippet: str, enzyme_list: List[str], ref: str) -> bool:
        """Validate that the context contains meaningful content for extraction."""
        if not snippet or len(snippet.strip()) < 50:
            LOGGER.warning("Insufficient context for extraction from %s - skipping", ref)
            return False
        
        # Check if context actually mentions the enzymes we're looking for
        enzyme_mentions = sum(1 for enzyme in enzyme_list if enzyme.lower() in snippet.lower())
        if enzyme_mentions == 0:
            LOGGER.warning("No enzyme mentions found in context for %s - skipping", ref)
            return False
        
        # Check for performance-related keywords
        performance_keywords = ['yield', 'selectivity', 'conversion', 'ee', 'er', 'ttn', 'ton', 'tof', '%', 'percent']
        has_performance_data = any(keyword in snippet.lower() for keyword in performance_keywords)
        
        if not has_performance_data:
            LOGGER.warning("No performance metrics found in context for %s - skipping", ref)
            return False
        
        LOGGER.info("Context validated for %s: %d chars, %d enzyme mentions", ref, len(snippet), enzyme_mentions)
        return True

    def _validate_response(self, data: Dict, enzyme_list: List[str], ref: str) -> bool:
        """Validate that the response contains meaningful data for the requested enzymes."""
        if not data or not isinstance(data, dict):
            LOGGER.warning("Invalid response format from %s - skipping", ref)
            return False
        
        # Check if we got data for at least one enzyme
        enzymes_with_data = 0
        for enzyme in enzyme_list:
            enzyme_data = data.get(enzyme, {})
            if isinstance(enzyme_data, dict) and enzyme_data:
                # Check if there's at least one non-null metric
                metrics = ['yield', 'ttn', 'ton', 'selectivity', 'conversion', 'tof', 'activity']
                has_metric = any(enzyme_data.get(metric) is not None for metric in metrics)
                if has_metric:
                    enzymes_with_data += 1
        
        if enzymes_with_data == 0:
            LOGGER.warning("No valid metrics found in response from %s - skipping", ref)
            return False
        
        LOGGER.info("Response validated for %s: %d enzymes with data", ref, enzymes_with_data)
        return True

    def extract_metrics_batch(self, enzyme_list: List[str], ref: str) -> List[Dict[str, Any]]:
        """Extract performance metrics for multiple enzymes from the identified location in batch."""
        LOGGER.info("extract_metrics_batch called with ref='%s' for %d enzymes", ref, len(enzyme_list))
        ref_lc = ref.lower()
        image_b64: Optional[str] = None
        
        # First, validate that the location actually exists in the document
        if not self._validate_location_exists(ref):
            LOGGER.warning("Location %s not found in document - skipping", ref)
            return []
        
        # Add campaign context if available
        campaign_context = ""
        if self.campaign_filter:
            campaign_context = f"\n\nIMPORTANT: You are extracting data for the {self.campaign_filter} campaign.\nOnly extract data that is relevant to this specific campaign.\n"
        
        if self._TAB_RE.search(ref_lc):
            # For tables, try to extract the page as an image first
            image_b64 = self._extract_page_png(ref, extract_figure_only=False)
            if not image_b64:
                LOGGER.debug("No page image found for %s - using full page text", ref)
                snippet = self._extract_table_context(ref)
        elif self._FIG_RE.search(ref_lc):
            # For figures, extract just the figure image (same logic as compound mapping)
            LOGGER.debug("Attempting to extract figure image for '%s'", ref)
            image_b64 = self._extract_page_png(ref, extract_figure_only=True)
            if not image_b64:
                LOGGER.warning("Failed to extract figure image for '%s' - falling back to caption text", ref)
                snippet = self._extract_figure_caption(ref)
                LOGGER.debug("Caption extraction result: %s", 
                           f"'{snippet[:100]}...'" if snippet else "empty")
            else:
                LOGGER.info("Successfully extracted figure image for '%s'", ref)
                # If figure is found, ignore text information - use image only
                snippet = ""
        else:
            snippet = self._page_with_reference(ref) or ""

        # For figures with images, skip text validation and proceed with image extraction
        if image_b64 and self._FIG_RE.search(ref_lc):
            LOGGER.info("Using figure image for %s - ignoring text context", ref)
        elif not image_b64 and not self._validate_context(snippet, enzyme_list, ref):
            return []

        # Create enhanced enzyme descriptions with parent/mutation context
        if hasattr(self, 'enzyme_df') and self.enzyme_df is not None:
            enzyme_descriptions = []
            for enzyme in enzyme_list:
                # Find this enzyme in the dataframe
                enzyme_row = None
                if 'enzyme_id' in self.enzyme_df.columns:
                    enzyme_row = self.enzyme_df[self.enzyme_df['enzyme_id'] == enzyme]
                elif 'enzyme' in self.enzyme_df.columns:
                    enzyme_row = self.enzyme_df[self.enzyme_df['enzyme'] == enzyme]
                
                if enzyme_row is not None and len(enzyme_row) > 0:
                    row = enzyme_row.iloc[0]
                    parent = row.get('parent_enzyme_id', '')
                    mutations = row.get('mutations', '')
                    
                    desc = f"- {enzyme}"
                    if parent and str(parent).strip() and str(parent) != 'nan':
                        desc += f" (parent: {parent})"
                    if mutations and str(mutations).strip() and str(mutations) != 'nan':
                        desc += f" (mutations: {mutations})"
                    enzyme_descriptions.append(desc)
                else:
                    enzyme_descriptions.append(f"- {enzyme}")
            enzyme_names = "\n".join(enzyme_descriptions)
        else:
            enzyme_names = "\n".join([f"- {enzyme}" for enzyme in enzyme_list])
        
        if image_b64:
            # Use batch extraction prompt for image analysis
            location_context = f"\n\nIMPORTANT: You are extracting data from {ref}, which has been identified as the PRIMARY LOCATION containing the most reliable performance data for these enzymes.\n"
            prompt = campaign_context + location_context + PROMPT_EXTRACT_FIGURE_METRICS_BATCH.format(enzyme_names=enzyme_names)
            LOGGER.info("Gemini Vision: extracting metrics for %d enzymes from %s…", len(enzyme_list), ref)
            tag = f"extract_metrics_batch_vision"
        else:
            # Add enzyme names to prompt for batch extraction with explicit format requirement
            format_example = '{"enzyme1": {"yield": "99.0%", "ttn": null, ...}, "enzyme2": {"yield": "85.0%", ...}}'
            prompt = campaign_context + PROMPT_EXTRACT_METRICS + f"\n\nExtract performance data for ALL these enzyme variants:\n{enzyme_names}\n\nReturn a JSON object with enzyme names as keys, each containing the metrics.\nExample format: {format_example}\n\n=== CONTEXT ===\n" + snippet[:4000]
            LOGGER.info("Gemini: extracting metrics for %d enzymes from %s…", len(enzyme_list), ref)
            tag = f"extract_metrics_batch"

        try:
            data = generate_json_with_retry(
                self.model,
                prompt,
                temperature=self.cfg.extract_temperature,
                debug_dir=self.debug_dir,
                tag=tag,
                image_b64=image_b64
            )
            
            # Validate response has meaningful data
            if not self._validate_response(data, enzyme_list, ref):
                # If figure extraction failed and we have a figure, try falling back to text
                if image_b64 and self._FIG_RE.search(ref_lc):
                    LOGGER.warning("Figure extraction from %s returned empty results - falling back to text", ref)
                    snippet = self._extract_figure_caption(ref)
                    if self._validate_context(snippet, enzyme_list, ref):
                        # Retry with text extraction
                        format_example = '{"enzyme1": {"yield": "99.0%", "ttn": null, ...}, "enzyme2": {"yield": "85.0%", ...}}'
                        prompt = campaign_context + PROMPT_EXTRACT_METRICS + f"\n\nExtract performance data for ALL these enzyme variants:\n{enzyme_names}\n\nReturn a JSON object with enzyme names as keys, each containing the metrics.\nExample format: {format_example}\n\n=== CONTEXT ===\n" + snippet[:4000]
                        LOGGER.info("Gemini: retrying with text extraction for %d enzymes from %s…", len(enzyme_list), ref)
                        
                        data = generate_json_with_retry(
                            self.model,
                            prompt,
                            temperature=self.cfg.extract_temperature,
                            debug_dir=self.debug_dir,
                            tag=f"extract_metrics_batch_text_fallback",
                            image_b64=None
                        )
                        
                        # Validate the text extraction response
                        if not self._validate_response(data, enzyme_list, ref):
                            return []
                    else:
                        return []
                else:
                    return []
            
            # Handle the response format - expecting a dict with enzyme names as keys
            results = []
            if isinstance(data, dict):
                for enzyme in enzyme_list:
                    enzyme_data = data.get(enzyme, {})
                    if not isinstance(enzyme_data, dict):
                        enzyme_data = {"error": "No data found"}
                    
                    # Normalize keys
                    # No need to rename - we now use "yield" directly
                    if "TTN" in enzyme_data and "ttn" not in enzyme_data:
                        enzyme_data["ttn"] = enzyme_data.pop("TTN")
                    
                    # Add metadata
                    enzyme_data["enzyme"] = enzyme
                    enzyme_data["location_ref"] = ref
                    enzyme_data["used_image"] = bool(image_b64)
                    results.append(enzyme_data)
            else:
                # Fallback if response format is unexpected
                LOGGER.warning("Unexpected response format from batch extraction")
                for enzyme in enzyme_list:
                    results.append({
                        "enzyme": enzyme,
                        "location_ref": ref,
                        "used_image": bool(image_b64),
                        "error": "Invalid response format"
                    })
                    
        except Exception as e:
            LOGGER.warning("Failed to extract metrics batch: %s", e)
            results = []
            for enzyme in enzyme_list:
                results.append({
                    "enzyme": enzyme,
                    "location_ref": ref,
                    "used_image": bool(image_b64),
                    "error": str(e)
                })
        
        return results

    # Removed extract_iupac_names - substrate scope IUPAC extraction no longer needed

    # ------------------------------------------------------------------
    # 6.4 Model reaction with location finding
    # ------------------------------------------------------------------

    def find_model_reaction_locations(self, enzyme_variants: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """Find locations for model reaction scheme, conditions, and IUPAC names."""
        # Create cache key based on campaign filter and enzyme variants
        cache_key = f"{self.campaign_filter}_{hash(tuple(sorted(enzyme_variants)) if enzyme_variants else ())}"
        
        # Check cache first
        cached_result = self._model_reaction_locations_cache.get(cache_key)
        if cached_result is not None:
            LOGGER.info("Using cached model reaction locations for campaign: %s", self.campaign_filter)
            return cached_result
        
        # Collect all text including section titles, captions, and schemes
        all_text = self._collect_captions_and_titles()
        
        # Also add first few pages of main text and SI
        ms_preview = "\n".join(self.ms_pages[:5])[:5000]
        si_preview = "\n".join(self.si_pages[:10])[:5000] if self.si_pages else ""
        
        # Add enzyme context if provided
        enzyme_context = ""
        if enzyme_variants and self.campaign_filter:
            campaigns_context = ""
            if self.all_campaigns:
                campaigns_context = f"""
ALL CAMPAIGNS IN THIS PAPER:
{chr(10).join([f"- {campaign}" for campaign in self.all_campaigns])}

CRITICAL WARNING: Do NOT confuse campaigns! Each campaign uses completely different substrates:
- Different campaigns may use similar enzyme names but different substrates
- Be extremely careful to only extract data for the {self.campaign_filter} campaign
- Ignore data from other campaigns even if they seem similar
"""
            
            enzyme_context = f"""
IMPORTANT CONTEXT:
You are looking for the model reaction used specifically for these enzyme variants:
{', '.join(enzyme_variants[:10])}{'...' if len(enzyme_variants) > 10 else ''}

These variants belong to campaign: {self.campaign_filter}
{campaigns_context}
Focus on finding the model reaction that was used to evaluate THESE specific variants.
Different campaigns may use different model reactions.
"""
        
        prompt = enzyme_context + PROMPT_FIND_MODEL_REACTION_LOCATION + "\n\n=== CAPTIONS AND SECTIONS ===\n" + all_text + "\n\n=== MANUSCRIPT TEXT PREVIEW ===\n" + ms_preview + "\n\n=== SI TEXT PREVIEW ===\n" + si_preview
        
        try:
            data = generate_json_with_retry(
                self.model,
                prompt,
                temperature=self.cfg.location_temperature,
                debug_dir=self.debug_dir,
                tag="find_model_reaction_locations"
            )
            if not isinstance(data, dict):
                LOGGER.error("Expected dict from Gemini, got: %s", type(data))
                return None
            
            # Cache the result
            self._model_reaction_locations_cache.put(cache_key, data)
            LOGGER.info("Cached model reaction locations for campaign: %s", self.campaign_filter)
            
            return data
        except Exception as e:
            LOGGER.error("Failed to find model reaction locations: %s", e)
            return None

    def _get_text_around_location(self, location: str) -> Optional[str]:
        """Extract text around a given location identifier."""
        location_lower = location.lower()
        
        # Handle compound locations like "Figure 2 caption and Section I"
        # Extract the first figure/table/scheme reference
        figure_match = re.search(r"(figure|scheme|table)\s*\d+", location_lower)
        if figure_match:
            primary_location = figure_match.group(0)
            # Try to find this primary location first
            for page_text in self.all_pages:
                if primary_location in page_text.lower():
                    idx = page_text.lower().index(primary_location)
                    start = max(0, idx - 500)
                    end = min(len(page_text), idx + 3000)
                    return page_text[start:end]
        
        # Search in all pages for exact match
        for page_text in self.all_pages:
            if location_lower in page_text.lower():
                # Find the location and extract context around it
                idx = page_text.lower().index(location_lower)
                start = max(0, idx - 500)
                end = min(len(page_text), idx + 3000)
                return page_text[start:end]
        
        # If not found in exact form, try pattern matching
        # For scheme/figure references
        if re.search(r"(scheme|figure|table)\s*\d+", location_lower):
            pattern = re.compile(location.replace(" ", r"\s*"), re.I)
            for page_text in self.all_pages:
                match = pattern.search(page_text)
                if match:
                    start = max(0, match.start() - 500)
                    end = min(len(page_text), match.end() + 3000)
                    return page_text[start:end]
        
        return None

    def _get_extended_text_around_location(self, location: str, before: int = 2000, after: int = 10000) -> Optional[str]:
        """Extract extended text around a given location identifier."""
        location_lower = location.lower()
        
        # Search in all pages
        for i, page_text in enumerate(self.all_pages):
            if location_lower in page_text.lower():
                # Find the location
                idx = page_text.lower().index(location_lower)
                
                # Collect text from multiple pages if needed
                result = []
                
                # Start from current page
                start = max(0, idx - before)
                result.append(page_text[start:])
                
                # Add subsequent pages up to 'after' characters
                chars_collected = len(page_text) - start
                page_idx = i + 1
                
                while chars_collected < after + before and page_idx < len(self.all_pages):
                    next_page = self.all_pages[page_idx]
                    chars_to_take = min(len(next_page), after + before - chars_collected)
                    result.append(next_page[:chars_to_take])
                    chars_collected += chars_to_take
                    page_idx += 1
                
                return "\n".join(result)
        
        return None

    def _extract_sections_by_title(self, sections: List[str], max_chars_per_section: int = 5000) -> str:
        """Extract text from sections with specific titles."""
        extracted_text = []
        
        for section_title in sections:
            pattern = re.compile(rf"{re.escape(section_title)}.*?(?=\n\n[A-Z]|\Z)", re.I | re.S)
            
            # Search in all pages
            for page in self.all_pages:
                match = pattern.search(page)
                if match:
                    section_text = match.group(0)[:max_chars_per_section]
                    extracted_text.append(f"=== {section_title} ===\n{section_text}")
                    break
        
        return "\n\n".join(extracted_text)

    def _extract_compound_mappings_from_text(
        self,
        extraction_text: str,
        compound_ids: List[str] = None,
        tag_suffix: str = "",
        campaign_filter: Optional[str] = None,
    ) -> Dict[str, CompoundMapping]:
        """Helper function to extract compound mappings from provided text."""
        prompt = PROMPT_COMPOUND_MAPPING
        if campaign_filter:
            prompt += f"\n\nIMPORTANT: Focus on compound information relevant to the {campaign_filter} campaign/reaction system."
        if compound_ids:
            prompt += "\n\nCOMPOUNDS TO MAP: " + ", ".join(sorted(compound_ids))
        prompt += "\n\nTEXT:\n" + extraction_text
        
        tag = f"compound_mapping_{tag_suffix}" if tag_suffix else "compound_mapping"
        
        try:
            data = generate_json_with_retry(
                self.model,
                prompt,
                temperature=self.cfg.model_reaction_temperature,
                debug_dir=self.debug_dir,
                tag=tag,
            )
            
            mappings = {}
            for item in data.get("compound_mappings", []):
                # Handle both old format (with identifiers list) and new format (with identifier string)
                identifiers = item.get("identifiers", [])
                if not identifiers and item.get("identifier"):
                    identifiers = [item.get("identifier")]
                
                mapping = CompoundMapping(
                    identifiers=identifiers,
                    iupac_name=item.get("iupac_name", ""),
                    common_names=item.get("common_names", []),
                    compound_type=item.get("compound_type", "unknown"),
                    source_location=item.get("source_location")
                )
                
                # Create lookup entries for all identifiers and common names
                for identifier in mapping.identifiers + mapping.common_names:
                    if identifier:
                        mappings[identifier.lower().strip()] = mapping
            
            return mappings
            
        except Exception as exc:
            LOGGER.error("Failed to extract compound mappings: %s", exc)
            return {}

    def _extract_compound_mappings_with_figures(
        self,
        text: str,
        compound_ids: List[str],
        figure_images: Dict[str, str],
        tag_suffix: str = "",
        campaign_filter: Optional[str] = None,
    ) -> Dict[str, CompoundMapping]:
        """Extract compound mappings using multimodal approach with figures."""
        # Enhanced prompt for figure-based extraction
        prompt = """You are analyzing chemical figures and manuscript text to identify compound IUPAC names.

TASK: Find the IUPAC names for these specific compound identifiers: """ + ", ".join(sorted(compound_ids)) + """

Use your best knowledge, Look carefully in:
1. The chemical structures shown in figures - infer IUPAC names from drawn structures
2. Figure captions that may define compounds
3. Text that refers to these compound numbers
4. Reaction schemes showing transformations"""

        if campaign_filter:
            campaigns_warning = ""
            if self.all_campaigns:
                campaigns_warning = f"""
ALL CAMPAIGNS IN THIS PAPER:
{chr(10).join([f"- {campaign}" for campaign in self.all_campaigns])}

CRITICAL WARNING: Do NOT confuse campaigns! Each campaign uses completely different substrates.
"""
            
            prompt += f"""

IMPORTANT CAMPAIGN CONTEXT: Focus on compound information relevant to the {campaign_filter} campaign/reaction system.
{campaigns_warning}
Different campaigns may use different numbering systems for compounds.
Do NOT include compound information from other campaigns."""

        prompt += """

IMPORTANT:
- Only provide IUPAC names you can determine from the figures or text
- If a structure is clearly shown in a figure, derive the IUPAC name from it

Return as JSON:
{
  "compound_mappings": [
    {
      "identifier": "compound identifier", 
      "iupac_name": "IUPAC name",
      "common_names": ["common names if any"],
      "compound_type": "substrate/product/reagent",
      "source_location": "where found (e.g., Figure 3, manuscript text)"
    }
  ]
}

TEXT FROM MANUSCRIPT:
""" + text
        
        # Prepare multimodal content
        content_parts = [prompt]
        
        # Add figure images
        if figure_images:
            for fig_ref, fig_base64 in figure_images.items():
                try:
                    img_bytes = b64decode(fig_base64)
                    # Format image for Gemini API
                    image_part = {"mime_type": "image/png", "data": img_bytes}
                    content_parts.append(f"\n[Figure: {fig_ref}]")
                    content_parts.append(image_part)
                    LOGGER.info("Added figure %s to multimodal compound mapping", fig_ref)
                except Exception as e:
                    LOGGER.warning("Failed to add figure %s: %s", fig_ref, e)
        
        tag = f"compound_mapping_{tag_suffix}" if tag_suffix else "compound_mapping"
        
        try:
            # Log multimodal call
            LOGGER.info("=== GEMINI MULTIMODAL API CALL: COMPOUND_MAPPING_WITH_FIGURES ===")
            LOGGER.info("Text prompt length: %d characters", len(prompt))
            LOGGER.info("Number of images: %d", len(content_parts) - 1)
            LOGGER.info("Compounds to find: %s", ", ".join(sorted(compound_ids)))
            
            # Save debug info
            if self.debug_dir:
                prompt_file = self.debug_dir / f"{tag}_prompt_{int(time.time())}.txt"
                with open(prompt_file, 'w') as f:
                    f.write(f"=== PROMPT FOR {tag.upper()} ===\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Text length: {len(prompt)} characters\n")
                    f.write(f"Images included: {len(content_parts) - 1}\n")
                    for fig_ref in figure_images.keys():
                        f.write(f"  - {fig_ref}\n")
                    f.write("="*80 + "\n\n")
                    f.write(prompt)
                LOGGER.info("Full prompt saved to: %s", prompt_file)
            
            # Make multimodal API call with increased token limit
            response = self.model.generate_content(
                content_parts,
                generation_config={
                    "temperature": 0.0,
                    "max_output_tokens": 24576,  # Increased 3x for compound mapping
                }
            )
            
            # Track token usage if available
            try:
                if hasattr(response, 'usage_metadata'):
                    input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0)
                    output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0)
                    if input_tokens or output_tokens:
                        try:
                            from .wrapper import add_token_usage
                            add_token_usage('reaction_info_extractor', input_tokens, output_tokens)
                        except ImportError:
                            pass  # wrapper not available
            except Exception:
                pass  # token tracking is best-effort
            
            raw_text = response.text.strip()
            
            # Log response
            LOGGER.info("Gemini multimodal response length: %d characters", len(raw_text))
            
            if self.debug_dir:
                response_file = self.debug_dir / f"{tag}_response_{int(time.time())}.txt"
                with open(response_file, 'w') as f:
                    f.write(f"=== RESPONSE FOR {tag.upper()} ===\n")
                    f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Length: {len(raw_text)} characters\n")
                    f.write("="*80 + "\n\n")
                    f.write(raw_text)
                LOGGER.info("Full response saved to: %s", response_file)
            
            # Parse JSON
            data = json.loads(raw_text.strip('```json').strip('```').strip())
            
            mappings = {}
            for item in data.get("compound_mappings", []):
                identifiers = item.get("identifiers", [])
                if not identifiers and item.get("identifier"):
                    identifiers = [item.get("identifier")]
                
                mapping = CompoundMapping(
                    identifiers=identifiers,
                    iupac_name=item.get("iupac_name", ""),
                    common_names=item.get("common_names", []),
                    compound_type=item.get("compound_type", "unknown"),
                    source_location=item.get("source_location")
                )
                
                for identifier in mapping.identifiers + mapping.common_names:
                    if identifier:
                        mappings[identifier.lower().strip()] = mapping
            
            return mappings
            
        except Exception as exc:
            LOGGER.error("Failed to extract compound mappings with figures: %s", exc)
            return {}

    def _extract_compound_mappings_adaptive(
        self,
        compound_ids: List[str],
        initial_sections: List[str] = None,
        campaign_filter: Optional[str] = None,
        iupac_location_hint: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, CompoundMapping]:
        """Extract compound ID to IUPAC name mappings using simplified 2-tier strategy.
        
        1. First attempts extraction from specific SI sections + 10 manuscript pages
        2. If compounds missing, uses full manuscript + SI with multimodal figure analysis
        """
        if not compound_ids:
            return {}
            
        # Check cache first - return cached results for compounds we've already processed
        cached_mappings = {}
        uncached_compound_ids = []
        
        for cid in compound_ids:
            # Include campaign filter in cache key to prevent cross-campaign contamination
            cache_key = f"{campaign_filter}_{cid.lower().strip()}" if campaign_filter else cid.lower().strip()
            cached_mapping = self._compound_mapping_cache.get(cache_key)
            if cached_mapping is not None:
                cached_mappings[cid.lower().strip()] = cached_mapping
                LOGGER.info("Using cached compound mapping for: %s (campaign: %s)", cid, campaign_filter)
            else:
                uncached_compound_ids.append(cid)
        
        # If all compounds are cached, return immediately
        if not uncached_compound_ids:
            LOGGER.info("All %d compounds found in cache, skipping API calls", len(compound_ids))
            return cached_mappings
            
        LOGGER.info("Starting adaptive compound mapping for %d uncached compounds: %s", 
                   len(uncached_compound_ids), sorted(uncached_compound_ids))
        
        # Tier 1: Use IUPAC location hint if provided, otherwise standard sections
        if iupac_location_hint and iupac_location_hint.get('location'):
            LOGGER.info("Tier 1: Using IUPAC location hint: %s", iupac_location_hint.get('location'))
            if iupac_location_hint.get('compound_section_hint'):
                LOGGER.info("Tier 1: Compound section hint: %s", iupac_location_hint.get('compound_section_hint'))
            
            # Extract text from the specific IUPAC location
            iupac_text = self._get_extended_text_around_location(
                iupac_location_hint['location'], 
                before=2000, 
                after=10000
            )
            
            # Also check for compound-specific hints
            compound_hint = iupac_location_hint.get('compound_section_hint', '')
            if compound_hint and iupac_text:
                # Search for the specific compound section
                hint_pattern = re.escape(compound_hint)
                match = re.search(hint_pattern, iupac_text, re.IGNORECASE)
                if match:
                    # Extract more focused text around the compound hint
                    start = max(0, match.start() - 500)
                    end = min(len(iupac_text), match.end() + 2000)
                    iupac_text = iupac_text[start:end]
                    LOGGER.info("Found compound hint '%s' in IUPAC section", compound_hint)
            
            extraction_text = iupac_text or ""
            if extraction_text:
                LOGGER.info("Tier 1: Extracted %d chars from IUPAC location hint", len(extraction_text))
            else:
                LOGGER.warning("Tier 1: No text found at IUPAC location hint")
            # Add some manuscript context
            manuscript_text = "\n\n".join(self.ms_pages[:5])
        else:
            # Fallback to standard sections
            initial_sections = initial_sections or [
                "General procedure", "Compound characterization", 
                "Synthesis", "Experimental", "Materials and methods"
            ]
            
            # Extract from initial sections - search in all pages (manuscript + SI)
            extraction_text = self._extract_sections_by_title(initial_sections)
            
            # If no sections found by title, include first few SI pages which often have compound data
            if not extraction_text and self.si_pages:
                # SI often starts with compound characterization after TOC
                si_compound_pages = "\n\n".join(self.si_pages[2:10])  # Skip first 2 pages (usually TOC)
                extraction_text = si_compound_pages
            
            # Include manuscript pages (first 10) for model reaction context
            manuscript_text = "\n\n".join(self.ms_pages[:10])
        
        # Add campaign context if provided
        campaign_context = ""
        if campaign_filter:
            campaigns_warning = ""
            if self.all_campaigns:
                campaigns_warning = f"""
ALL CAMPAIGNS IN THIS PAPER:
{chr(10).join([f"- {campaign}" for campaign in self.all_campaigns])}

CRITICAL WARNING: Do NOT confuse campaigns! Each campaign uses completely different substrates.
"""
            
            campaign_context = f"""

IMPORTANT CAMPAIGN CONTEXT:
You are extracting compound information specifically for the {campaign_filter} campaign.
{campaigns_warning}
Focus ONLY on compound information relevant to the {campaign_filter} campaign/reaction system.
Do NOT include compound information from other campaigns.

"""
        
        # Combine manuscript text, campaign context, and extraction text
        if extraction_text:
            extraction_text = manuscript_text + campaign_context + "\n\n" + extraction_text
        else:
            extraction_text = manuscript_text + campaign_context
        
        # First extraction attempt - only for uncached compounds
        mappings = self._extract_compound_mappings_from_text(
            extraction_text[:50000], uncached_compound_ids, tag_suffix="initial", campaign_filter=campaign_filter
        )
        LOGGER.info("Tier 1: Found %d compound mappings from standard sections", len(mappings))
        
        # Check for missing compounds
        missing_compounds = []
        for cid in uncached_compound_ids:
            mapping = mappings.get(cid.lower().strip())
            if not mapping or not mapping.iupac_name:
                missing_compounds.append(cid)
        
        # Tier 2 (skip directly to full search): Full manuscript + SI search with all available figures
        if missing_compounds:
            LOGGER.info("Tier 2: %d compounds still missing IUPAC names, going directly to full search: %s", 
                       len(missing_compounds), sorted(missing_compounds))
            
            # Get all available figures for compound structure analysis
            figure_images = {}
            
            # Extract main manuscript figures
            figure_refs = ["Figure 1", "Figure 2", "Figure 3", "Figure 4", "Scheme 1", "Scheme 2", "Scheme 3"]
            for ref in figure_refs:
                img_b64 = self._extract_page_png(ref, extract_figure_only=True)
                if img_b64:
                    figure_images[ref] = img_b64
                    LOGGER.info("Retrieved %s for compound mapping", ref)
                
            # Get SI figures
            si_figure_refs = []
            for page in self.si_pages[:10]:  # Check first 10 SI pages
                matches = re.findall(r"Figure S\d+|Scheme S\d+", page)
                si_figure_refs.extend(matches[:10])  # Limit to 10 figures
            
            # Extract SI figures
            for ref in set(si_figure_refs):
                if ref not in figure_images:
                    img_b64 = self._extract_page_png(ref, extract_figure_only=True)
                    if img_b64:
                        figure_images[ref] = img_b64
                        LOGGER.info("Extracted %s for compound mapping", ref)
            
            # Full text search including ALL pages (manuscript + SI)
            full_text = "\n\n".join(self.all_pages)  # Send everything
            
            final_mappings = self._extract_compound_mappings_with_figures(
                full_text, missing_compounds, figure_images, tag_suffix="tier2", campaign_filter=campaign_filter
            )
            
            # Merge final mappings with better compound ID matching
            final_found = 0
            for key, mapping in final_mappings.items():
                if key not in mappings or not mappings[key].iupac_name:
                    if mapping.iupac_name:
                        mappings[key] = mapping
                        final_found += 1
                        iupac_display = mapping.iupac_name[:50] + "..." if mapping.iupac_name and len(mapping.iupac_name) > 50 else (mapping.iupac_name or "None")
                        LOGGER.info("Found IUPAC name for '%s' in full search: %s", key, iupac_display)
            
            LOGGER.info("Tier 2: Found %d additional compound mappings", final_found)
        
        # Cache all newly found mappings using campaign-aware cache key
        for key, mapping in mappings.items():
            cache_key = f"{campaign_filter}_{key}" if campaign_filter else key
            if self._compound_mapping_cache.get(cache_key) is None:
                self._compound_mapping_cache.put(cache_key, mapping)
                iupac_display = mapping.iupac_name[:50] + "..." if mapping.iupac_name and len(mapping.iupac_name) > 50 else (mapping.iupac_name or "None")
                LOGGER.info("Cached compound mapping for: %s -> %s (campaign: %s)", key, iupac_display, campaign_filter)
                
                # Also cache without campaign prefix for backward compatibility during integration
                if campaign_filter:
                    self._compound_mapping_cache.put(key, mapping)
        
        # Combine cached and new mappings
        final_mappings = cached_mappings.copy()
        final_mappings.update(mappings)
        
        LOGGER.info("Adaptive compound mapping complete: %d total mappings (%d cached, %d new)", 
                   len(final_mappings), len(cached_mappings), len(mappings))
        return final_mappings

    def gather_model_reaction_info(self, enzyme_variants: Optional[List[str]] = None, lineage_compound_ids: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
        """Extract model reaction information using identified locations and 3-tier compound mapping."""
        # First find the best locations
        locations = self.find_model_reaction_locations(enzyme_variants)
        if not locations:
            LOGGER.warning("Could not find model reaction locations, using fallback approach")
            # Fallback to old approach but include more manuscript text
            pattern = re.compile(r"(model reaction|general procedure|typical .*run|standard conditions|scheme 1|figure 1)", re.I)
            snippets: List[str] = []
            # Search both manuscript and SI
            for page in self.all_pages:
                if pattern.search(page):
                    para_match = re.search(r"(.{0,3000}?\n\n)", page)
                    if para_match:
                        snippets.append(para_match.group(0))
                if len(snippets) >= 5:
                    break
            text_context = "\n---\n".join(snippets)[:10000]
        else:
            # Gather text from identified locations
            text_snippets = []
            
            # Always include manuscript abstract and introduction for context
            if self.ms_pages:
                # First 3 pages typically contain abstract, introduction, and model reaction info
                manuscript_intro = "\n\n".join(self.ms_pages[:3])
                text_snippets.append(f"=== MANUSCRIPT INTRODUCTION ===\n{manuscript_intro}")
            
            # Get model reaction context
            if locations.get("model_reaction_location", {}).get("location"):
                model_loc = locations["model_reaction_location"]["location"]
                LOGGER.info("Looking for model reaction at: %s", model_loc)
                model_text = self._get_text_around_location(model_loc)
                if model_text:
                    text_snippets.append(f"=== {model_loc} ===\n{model_text}")
            
            # Get conditions context  
            if locations.get("conditions_location", {}).get("location"):
                cond_loc = locations["conditions_location"]["location"]
                LOGGER.info("Looking for reaction conditions at: %s", cond_loc)
                cond_text = self._get_text_around_location(cond_loc)
                if cond_text:
                    text_snippets.append(f"=== {cond_loc} ===\n{cond_text}")
            
            # Get IUPAC names context from the specific location identified
            if locations.get("iupac_location", {}).get("location"):
                iupac_loc = locations["iupac_location"]["location"]
                LOGGER.info("Looking for IUPAC names at: %s", iupac_loc)
                
                # If we have compound IDs from the model reaction location, search for them specifically
                compound_ids = locations.get("model_reaction_location", {}).get("compound_ids", [])
                if compound_ids:
                    LOGGER.info("Looking for specific compound IDs: %s", compound_ids)
                    # Search for each compound ID in the SI
                    for compound_id in compound_ids:
                        # Search patterns for compound characterization
                        patterns = [
                            rf"(?:compound\s+)?{re.escape(compound_id)}[:\s]*\([^)]+\)",  # 6a: (IUPAC name)
                            rf"(?:compound\s+)?{re.escape(compound_id)}[.\s]+[A-Z][^.]+",  # 6a. IUPAC name
                            rf"{re.escape(compound_id)}[^:]*:\s*[^.]+",  # Any format with colon
                        ]
                        
                        for page in self.si_pages:
                            for pattern in patterns:
                                match = re.search(pattern, page, re.I)
                                if match:
                                    # Get extended context around the match
                                    start = max(0, match.start() - 200)
                                    end = min(len(page), match.end() + 500)
                                    text_snippets.append(f"=== Compound {compound_id} characterization ===\n{page[start:end]}")
                                    break
                
                # Also search for substrate names mentioned in the reaction to find their IUPAC equivalents
                # Look for common substrate patterns in compound listings
                substrate_patterns = [
                    r"(?:substrate|reactant|reagent)s?\s*:?\s*([^.]+)",
                    r"(?:starting\s+material)s?\s*:?\s*([^.]+)",
                    r"\d+\.\s*([A-Za-z\s\-]+)(?:\s*\([^)]+\))?",  # numbered compound lists
                ]
                
                for pattern in substrate_patterns:
                    for page in self.si_pages[:5]:  # Check first few SI pages
                        matches = re.finditer(pattern, page, re.I)
                        for match in matches:
                            text = match.group(0)
                            if len(text) < 200:  # Reasonable length check
                                start = max(0, match.start() - 100)
                                end = min(len(page), match.end() + 300)
                                snippet = page[start:end]
                                if "prop-2-enoate" in snippet or "diazirin" in snippet:
                                    text_snippets.append(f"=== Substrate characterization ===\n{snippet}")
                                    break
                
                # Also get general IUPAC context
                iupac_text = self._get_text_around_location(iupac_loc)
                if iupac_text:
                    # Get more context around the identified location
                    extended_iupac_text = self._get_extended_text_around_location(iupac_loc, before=2000, after=10000)
                    if extended_iupac_text:
                        text_snippets.append(f"=== {iupac_loc} ===\n{extended_iupac_text}")
                    else:
                        text_snippets.append(f"=== {iupac_loc} ===\n{iupac_text}")
            
            text_context = "\n\n".join(text_snippets)[:35000]  # Increase limit for more context
        
        # Extract figure images for model reaction if identified
        figure_images = {}
        if locations:
            # Extract images from model reaction and conditions locations
            for loc_key in ["model_reaction_location", "conditions_location"]:
                loc_info = locations.get(loc_key, {})
                location = loc_info.get("location", "")
                if location and ("figure" in location.lower() or "fig" in location.lower()):
                    # Extract just the figure reference (e.g., "Figure 2" from "Figure 2. Caption...")
                    fig_match = re.search(r"(Figure\s+\d+|Fig\s+\d+|Scheme\s+\d+)", location, re.I)
                    if fig_match:
                        fig_ref = fig_match.group(1)
                        LOGGER.info("Extracting image for %s from %s", fig_ref, loc_key)
                        img_b64 = self._extract_page_png(fig_ref, extract_figure_only=True)
                        if img_b64:
                            figure_images[fig_ref] = img_b64
                            LOGGER.info("Successfully extracted %s image for model reaction analysis", fig_ref)
        
        # Extract compound IDs from locations or use lineage-specific ones
        compound_ids = []
        if lineage_compound_ids:
            # Use lineage-specific compound IDs if provided
            substrate_ids = lineage_compound_ids.get("substrate_ids", [])
            product_ids = lineage_compound_ids.get("product_ids", [])
            compound_ids = substrate_ids + product_ids
            LOGGER.info("Using lineage-specific compound IDs: %s", compound_ids)
        elif locations and locations.get("model_reaction_location", {}).get("compound_ids"):
            compound_ids = locations["model_reaction_location"]["compound_ids"]
            LOGGER.info("Found compound IDs in model reaction: %s", compound_ids)
        
        # Use the 3-tier compound mapping approach if we have compound IDs
        compound_mappings = {}
        if compound_ids:
            LOGGER.info("Using 3-tier compound mapping approach for compounds: %s", compound_ids)
            # Pass the IUPAC location hint if we have it
            iupac_hint = locations.get("iupac_location") if locations else None
            compound_mappings = self._extract_compound_mappings_adaptive(
                compound_ids, 
                campaign_filter=self.campaign_filter,
                iupac_location_hint=iupac_hint
            )
            
            # Add the mapped IUPAC names to the context for better extraction
            if compound_mappings:
                mapping_text = "\n\n=== COMPOUND MAPPINGS ===\n"
                for cid in compound_ids:
                    mapping = compound_mappings.get(cid.lower().strip())
                    if mapping and mapping.iupac_name:
                        mapping_text += f"Compound {cid}: {mapping.iupac_name}\n"
                text_context += mapping_text
        
        # Add campaign context if available
        campaign_context = ""
        if enzyme_variants and self.campaign_filter:
            campaigns_context = ""
            if self.all_campaigns:
                campaigns_context = f"""
ALL CAMPAIGNS IN THIS PAPER:
{chr(10).join([f"- {campaign}" for campaign in self.all_campaigns])}

CRITICAL WARNING: Do NOT confuse campaigns! Each campaign uses completely different substrates:
- Different campaigns may use similar enzyme names but different substrates
- Be extremely careful to only extract data for the {self.campaign_filter} campaign
- Ignore data from other campaigns even if they seem similar
"""
            
            campaign_context = f"""
IMPORTANT CONTEXT:
You are extracting the model reaction used specifically for these enzyme variants:
{', '.join(enzyme_variants[:10])}{'...' if len(enzyme_variants) > 10 else ''}

These variants belong to campaign: {self.campaign_filter}
{campaigns_context}
Focus on extracting the model reaction that was used to evaluate THESE specific variants.
Different campaigns may use different model reactions and substrates.

"""
        
        # Include both manuscript and SI text for better coverage
        prompt = campaign_context + PROMPT_MODEL_REACTION + "\n\n=== CONTEXT ===\n" + text_context
        
        try:
            # Use multimodal extraction if we have figure images
            if figure_images:
                LOGGER.info("Using multimodal extraction with %d figure images", len(figure_images))
                # Prepare multimodal content
                content_parts = [prompt]
                
                # Add figure images
                for fig_ref, fig_base64 in figure_images.items():
                    try:
                        img_bytes = b64decode(fig_base64)
                        # Format image for Gemini API
                        image_part = {"mime_type": "image/png", "data": img_bytes}
                        content_parts.append(f"\n[Figure: {fig_ref}]")
                        content_parts.append(image_part)
                    except Exception as e:
                        LOGGER.warning("Failed to process figure %s: %s", fig_ref, e)
                
                # Use multimodal model if we have valid images
                if len(content_parts) > 1:
                    # Create multimodal request
                    model = genai.GenerativeModel(
                        model_name=self.cfg.model_name,
                        generation_config={
                            "temperature": self.cfg.model_reaction_temperature,
                            "top_p": self.cfg.top_p,
                            "top_k": 1,
                            "max_output_tokens": self.cfg.max_tokens,
                        }
                    )
                    
                    try:
                        response = model.generate_content(content_parts)
                        
                        # Track token usage if available
                        try:
                            if hasattr(response, 'usage_metadata'):
                                input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0)
                                output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0)
                                if input_tokens or output_tokens:
                                    try:
                                        from .wrapper import add_token_usage
                                        add_token_usage('reaction_info_extractor', input_tokens, output_tokens)
                                    except ImportError:
                                        pass  # wrapper not available
                        except Exception:
                            pass  # token tracking is best-effort
                        
                        # Parse JSON from response
                        if response and response.text:
                            # Save debug output
                            if self.debug_dir:
                                timestamp = int(time.time())
                                _dump(prompt, self.debug_dir / f"model_reaction_multimodal_prompt_{timestamp}.txt")
                                _dump(response.text, self.debug_dir / f"model_reaction_multimodal_response_{timestamp}.txt")
                            
                            # Extract JSON from response
                            text = response.text.strip()
                            if text.startswith("```json"):
                                text = text[7:]
                            if text.endswith("```"):
                                text = text[:-3]
                            data = json.loads(text.strip())
                        else:
                            raise ValueError("Empty response from multimodal model")
                    except Exception as vision_error:
                        LOGGER.error("Vision API call failed: %s", vision_error)
                        LOGGER.info("Falling back to text-only extraction")
                        # Fall back to text-only extraction
                        data = generate_json_with_retry(
                            self.model,
                            prompt,
                            temperature=self.cfg.model_reaction_temperature,
                            debug_dir=self.debug_dir,
                            tag="model_reaction_fallback"
                        )
                else:
                    # Fall back to text-only extraction
                    data = generate_json_with_retry(
                        self.model,
                        prompt,
                        temperature=self.cfg.model_reaction_temperature,
                        debug_dir=self.debug_dir,
                        tag="model_reaction"
                    )
            else:
                # Standard text-only extraction
                data = generate_json_with_retry(
                    self.model,
                    prompt,
                    temperature=self.cfg.model_reaction_temperature,
                    debug_dir=self.debug_dir,
                    tag="model_reaction"
                )
            
            # Handle the new array format for substrates/products
            if isinstance(data, dict):
                # If we have compound mappings, enhance the IUPAC names
                if compound_ids and compound_mappings:
                    LOGGER.info("Enhancing IUPAC names using compound mappings. Available mappings: %s", 
                               list(compound_mappings.keys()))
                    
                    # First, populate IUPAC lists directly from compound mappings based on compound_type
                    substrate_iupacs_from_mappings = []
                    product_iupacs_from_mappings = []
                    
                    for mapping in compound_mappings.values():
                        if mapping.iupac_name and mapping.compound_type:
                            if mapping.compound_type.lower() == "substrate":
                                substrate_iupacs_from_mappings.append(mapping.iupac_name)
                                LOGGER.info("Added substrate IUPAC from mapping: '%s'", mapping.iupac_name)
                            elif mapping.compound_type.lower() == "product":
                                product_iupacs_from_mappings.append(mapping.iupac_name)
                                LOGGER.info("Added product IUPAC from mapping: '%s'", mapping.iupac_name)
                    
                    # Initialize or update the IUPAC lists with mapped compounds
                    if substrate_iupacs_from_mappings:
                        existing_substrates = data.get("substrate_iupac_list", []) or []
                        if isinstance(existing_substrates, list):
                            data["substrate_iupac_list"] = existing_substrates + substrate_iupacs_from_mappings
                        else:
                            data["substrate_iupac_list"] = substrate_iupacs_from_mappings
                    
                    if product_iupacs_from_mappings:
                        existing_products = data.get("product_iupac_list", []) or []
                        if isinstance(existing_products, list):
                            data["product_iupac_list"] = existing_products + product_iupacs_from_mappings
                        else:
                            data["product_iupac_list"] = product_iupacs_from_mappings
                    
                    # Try to map substrate/product lists through compound IDs
                    substrate_list = data.get("substrate_iupac_list", []) or data.get("substrate_list", [])
                    if isinstance(substrate_list, list):
                        enhanced_substrates = []
                        for item in substrate_list:
                            item_str = str(item).lower().strip()
                            # Check if it's a compound ID that we can map
                            mapping = compound_mappings.get(item_str)
                            if mapping and mapping.iupac_name:
                                enhanced_substrates.append(mapping.iupac_name)
                                LOGGER.info("Mapped substrate '%s' -> '%s'", item, mapping.iupac_name)
                            elif item and not re.match(r'^[0-9]+[a-z]?$|^S\d+$', str(item)):
                                # Keep valid IUPAC names that aren't compound IDs
                                enhanced_substrates.append(str(item))
                                LOGGER.info("Kept substrate IUPAC name: '%s'", item)
                            else:
                                LOGGER.warning("Could not map substrate compound ID '%s'", item)
                        data["substrate_iupac_list"] = enhanced_substrates
                    
                    product_list = data.get("product_iupac_list", []) or data.get("product_list", [])
                    if isinstance(product_list, list):
                        enhanced_products = []
                        for item in product_list:
                            item_str = str(item).lower().strip()
                            # Check if it's a compound ID that we can map
                            mapping = compound_mappings.get(item_str)
                            if mapping and mapping.iupac_name:
                                enhanced_products.append(mapping.iupac_name)
                                LOGGER.info("Mapped product '%s' -> '%s'", item, mapping.iupac_name)
                            elif item and not re.match(r'^[0-9]+[a-z]?$|^S\d+$', str(item)):
                                # Keep valid IUPAC names that aren't compound IDs
                                enhanced_products.append(str(item))
                                LOGGER.info("Kept product IUPAC name: '%s'", item)
                            else:
                                LOGGER.warning("Could not map product compound ID '%s'", item)
                        data["product_iupac_list"] = enhanced_products
                    
                    # Also try to enhance using both substrate_list and product_list if they contain compound IDs
                    for list_key, target_key in [("substrate_list", "substrate_iupac_list"), ("product_list", "product_iupac_list")]:
                        if list_key in data and isinstance(data[list_key], list):
                            if target_key not in data or not data[target_key]:
                                enhanced_list = []
                                for item in data[list_key]:
                                    item_str = str(item).lower().strip()
                                    mapping = compound_mappings.get(item_str)
                                    if mapping and mapping.iupac_name:
                                        enhanced_list.append(mapping.iupac_name)
                                        LOGGER.info("Enhanced %s: mapped '%s' -> '%s'", target_key, item, mapping.iupac_name)
                                if enhanced_list:
                                    data[target_key] = enhanced_list
                
                # Validate and convert arrays to semicolon-separated strings for CSV compatibility
                if "substrate_iupac_list" in data and isinstance(data["substrate_iupac_list"], list):
                    # Filter out non-IUPAC names (abbreviations like "1a", "S1", etc.)
                    valid_substrates = [s for s in data["substrate_iupac_list"] 
                                      if s and not re.match(r'^[0-9]+[a-z]?$|^S\d+$', s)]
                    # Join with semicolons instead of JSON encoding
                    data["substrate_iupac_list"] = "; ".join(valid_substrates) if valid_substrates else ""
                else:
                    data["substrate_iupac_list"] = ""
                    
                if "product_iupac_list" in data and isinstance(data["product_iupac_list"], list):
                    # Filter out non-IUPAC names
                    valid_products = [p for p in data["product_iupac_list"] 
                                    if p and not re.match(r'^[0-9]+[a-z]?$|^S\d+$', p)]
                    # Join with semicolons instead of JSON encoding
                    data["product_iupac_list"] = "; ".join(valid_products) if valid_products else ""
                else:
                    data["product_iupac_list"] = ""
                    
        except Exception as exc:
            LOGGER.error("Failed to extract model reaction: %s", exc)
            data = {
                "substrate_iupac_list": None,
                "product_iupac_list": None,
                "reaction_substrate_concentration": None,
                "cofactor": None,
                "reaction_temperature": None,
                "reaction_ph": None,
                "reaction_buffer": None,
                "reaction_other_conditions": None,
                "error": str(exc)
            }
        
        # Ensure all expected keys are present
        expected_keys = [
            "substrate_list", "substrate_iupac_list", "product_list", "product_iupac_list", 
            "reaction_substrate_concentration", "cofactor", "reaction_temperature", 
            "reaction_ph", "reaction_buffer", "reaction_other_conditions"
        ]
        for key in expected_keys:
            data.setdefault(key, None)
            
        return data

    def _process_single_lineage(self, location: Dict[str, Any], enzyme_df: pd.DataFrame) -> pd.DataFrame:
        """Process a single lineage case - use confidence-based processing."""
        # Create lineage analysis for single location
        lineage_analysis = {
            'has_multiple_lineages': False,
            'lineage_groups': [{
                'group_id': self._get_base_location(location['location']),
                'data_location': location['location'],
                'lineage_hint': location.get('lineage_hint', ''),
                'caption': location.get('caption', ''),
                'confidence': location.get('confidence', 0)
            }]
        }
        
        return self._process_multiple_lineages_by_confidence([location], enzyme_df, lineage_analysis)
    
    def _process_multiple_lineages_by_confidence(self, locations: List[Dict[str, Any]], 
                                                 enzyme_df: pd.DataFrame,
                                                 lineage_analysis: Dict[str, Any]) -> pd.DataFrame:
        """Process multiple lineages by confidence, detecting which enzymes belong to which campaign."""
        # Get all enzyme IDs
        all_enzyme_ids = enzyme_df['enzyme_id'].tolist() if 'enzyme_id' in enzyme_df.columns else enzyme_df['enzyme'].tolist()
        all_variants = set(all_enzyme_ids)
        variants_with_data = set()
        all_results = []
        
        # If enzyme_df has campaign_id column, we can use it to filter
        has_campaign_info = 'campaign_id' in enzyme_df.columns
        
        # Select the most confident source only
        best_location = None
        if locations:
            # Sort by confidence only
            locations_sorted = sorted(locations, key=lambda x: -x.get('confidence', 0))
            best_location = locations_sorted[0]
            
            LOGGER.info("Selected primary location: %s (type: %s, confidence: %d%%)", 
                       best_location['location'], 
                       best_location.get('type', 'unknown'), 
                       best_location.get('confidence', 0))
            
            # Extract metrics from the most confident source only
            metrics_rows = self.extract_metrics_batch(all_enzyme_ids, best_location['location'])
            
            # Filter to valid metrics
            valid_metrics = [m for m in metrics_rows if self._has_valid_metrics(m)]
            
            if not valid_metrics:
                LOGGER.warning("No valid metrics found in primary location %s", best_location['location'])
                return pd.DataFrame()
                
            LOGGER.info("Found %d enzymes with data in %s", len(valid_metrics), best_location['location'])
            
            # Create DataFrame for the single best location
            df_location = pd.DataFrame(valid_metrics)
            
            # Add metadata about the location
            df_location['data_location'] = best_location['location']
            df_location['confidence'] = best_location.get('confidence', 0)
            
            LOGGER.info("Successfully extracted data for %d enzymes from primary location", len(df_location))
            
            # Extract model reaction info once for this location
            location_context = f"Location: {best_location['location']}"
            if best_location.get('caption'):
                location_context += f"\nCaption: {best_location['caption']}"
            
            # Get enzyme list for model reaction  
            location_enzymes = df_location['enzyme'].unique().tolist()
            # Get model reaction locations for this campaign
            model_reaction_locations = self.find_model_reaction_locations(location_enzymes)
            
            # Extract model reaction for this location - use unified approach
            LOGGER.info("Extracting model reaction for location: %s", best_location['location'])
            
            # Try lineage-specific extraction first
            location_model_reaction = self.find_lineage_model_reaction(
                best_location['location'], 
                location_context,
                model_reaction_locations
            )
            
            # Check if lineage extraction was successful
            if location_model_reaction.get('substrate_ids') or location_model_reaction.get('product_ids'):
                LOGGER.info("Using lineage-specific model reaction data")
                model_info = self._extract_lineage_model_info(location_model_reaction, location_enzymes)
            else:
                LOGGER.info("Lineage extraction failed, using comprehensive multimodal extraction")
                # Use the comprehensive multimodal approach as fallback
                model_info = self.gather_model_reaction_info(location_enzymes)
                
            LOGGER.info("Model reaction extraction complete for location: %s", best_location['location'])
            
            # Add model reaction info to all enzymes from this location
            for key, value in model_info.items():
                if isinstance(value, list):
                    value = "; ".join(str(v) for v in value) if value else None
                df_location[key] = value
            
            # Add additional location metadata (data_location already set above)
            df_location['location_type'] = best_location.get('type', 'unknown')
            df_location['location_confidence'] = best_location.get('confidence', 0)
            
            LOGGER.info("Extraction complete: %d variants from primary location %s", 
                       len(df_location), best_location['location'])
            
            return df_location
        
        # No locations found
        LOGGER.warning("No valid locations found for extraction")
        return pd.DataFrame()
    
    def _has_valid_metrics(self, metrics_row: Dict[str, Any]) -> bool:
        """Check if a metrics row contains any valid performance data."""
        metric_fields = ['yield', 'ttn', 'ton', 'selectivity', 'conversion', 'tof', 'activity']
        
        for field in metric_fields:
            if metrics_row.get(field) is not None:
                return True
                
        # Also check other_metrics
        if metrics_row.get('other_metrics') and isinstance(metrics_row['other_metrics'], dict):
            if metrics_row['other_metrics']:  # Non-empty dict
                return True
                
        return False
    
    def _filter_locations_by_campaign(self, locations: List[Dict[str, Any]], 
                                     enzyme_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Filter locations to only those relevant to the current campaign."""
        if not self.campaign_filter or 'campaign_id' not in enzyme_df.columns:
            return locations
        
        # Get enzyme names for this campaign
        campaign_enzymes = enzyme_df[enzyme_df['campaign_id'] == self.campaign_filter]['enzyme_id' if 'enzyme_id' in enzyme_df.columns else 'enzyme'].tolist()
        
        # Extract any common patterns from enzyme names
        enzyme_patterns = set()
        for enzyme in campaign_enzymes:
            # Extract any uppercase abbreviations (e.g., 'PYS', 'INS')
            matches = re.findall(r'[A-Z]{2,}', enzyme)
            enzyme_patterns.update(matches)
        
        LOGGER.info("Campaign %s has enzyme patterns: %s", self.campaign_filter, enzyme_patterns)
        
        # Get campaign description keywords from the campaign data if available
        campaign_keywords = set()
        # Extract keywords from campaign_id (e.g., 'pyrrolidine_synthase_evolution' -> ['pyrrolidine', 'synthase'])
        words = self.campaign_filter.lower().replace('_', ' ').split()
        # Filter out generic words
        generic_words = {'evolution', 'campaign', 'synthase', 'enzyme', 'variant'}
        campaign_keywords.update(word for word in words if word not in generic_words and len(word) > 3)
        
        LOGGER.info("Campaign keywords: %s", campaign_keywords)
        
        # Filter locations based on campaign clues
        filtered = []
        for loc in locations:
            # Check caption and clues for campaign indicators
            caption = (loc.get('caption') or '').lower()
            campaign_clues = (loc.get('campaign_clues') or '').lower()
            lineage_hint = (loc.get('lineage_hint') or '').lower()
            combined_text = caption + ' ' + campaign_clues + ' ' + lineage_hint
            
            # Check if location is relevant to this campaign
            is_relevant = False
            
            # Check for enzyme patterns
            for pattern in enzyme_patterns:
                if pattern.lower() in combined_text:
                    is_relevant = True
                    break
            
            # Check for campaign keywords
            if not is_relevant:
                for keyword in campaign_keywords:
                    if keyword in combined_text:
                        is_relevant = True
                        break
            
            # Check if any campaign enzymes are explicitly mentioned
            if not is_relevant:
                for enzyme in campaign_enzymes[:5]:  # Check first few enzymes
                    if enzyme.lower() in combined_text:
                        is_relevant = True
                        break
            
            if is_relevant:
                filtered.append(loc)
                LOGGER.info("Location %s is relevant to campaign %s", 
                           loc.get('location'), self.campaign_filter)
            else:
                LOGGER.debug("Location %s filtered out for campaign %s", 
                            loc.get('location'), self.campaign_filter)
        
        return filtered
    
    def _extract_lineage_model_info(self, lineage_reaction: Dict[str, Any], enzyme_variants: Optional[List[str]] = None) -> Dict[str, Any]:
        """Extract full model reaction info including IUPAC names for a lineage."""
        # Get substrate/product IDs from lineage-specific extraction
        substrate_ids = lineage_reaction.get('substrate_ids', [])
        product_ids = lineage_reaction.get('product_ids', [])
        
        # Get general model reaction info for conditions, using lineage-specific compound IDs
        lineage_ids = {
            "substrate_ids": substrate_ids,
            "product_ids": product_ids
        }
        general_info = self.gather_model_reaction_info(enzyme_variants, lineage_compound_ids=lineage_ids)
        
        # Override substrate/product lists with lineage-specific ones only if they contain actual compound IDs
        model_info = general_info.copy()
        
        # Check if substrate_ids contain actual compound IDs (not generic terms like "alkyl azide")
        if substrate_ids and any(re.match(r'^[0-9]+[a-z]?$|^[A-Z][0-9]+$', sid) for sid in substrate_ids):
            model_info['substrate_list'] = substrate_ids
        elif not substrate_ids and general_info.get('substrate_list'):
            # Keep the general info if lineage extraction found nothing
            pass
        else:
            model_info['substrate_list'] = substrate_ids
            
        # Check if product_ids contain actual compound IDs (not generic terms like "pyrrolidine")
        if product_ids and any(re.match(r'^[0-9]+[a-z]?$|^[A-Z][0-9]+$', pid) for pid in product_ids):
            model_info['product_list'] = product_ids
        elif not product_ids and general_info.get('product_list'):
            # Keep the general info if lineage extraction found nothing
            pass
        else:
            # If we only have generic terms, try to keep general info if available
            if general_info.get('product_list') and all(len(pid) > 5 for pid in product_ids):
                # Likely generic terms like "pyrrolidine", keep general info
                pass
            else:
                model_info['product_list'] = product_ids
        
        # Extract IUPAC names for the compounds we're actually using
        # Use the IDs from model_info (which may have been preserved from general extraction)
        final_substrate_ids = model_info.get('substrate_list', [])
        final_product_ids = model_info.get('product_list', [])
        all_compound_ids = final_substrate_ids + final_product_ids
        
        if all_compound_ids:
            compound_mappings = self._extract_compound_mappings_adaptive(all_compound_ids)
            
            # Map substrate IUPAC names
            substrate_iupacs = []
            for sid in final_substrate_ids:
                mapping = compound_mappings.get(str(sid).lower().strip())
                if mapping and mapping.iupac_name:
                    substrate_iupacs.append(mapping.iupac_name)
            # Only update if we found IUPAC names
            if substrate_iupacs:
                model_info['substrate_iupac_list'] = substrate_iupacs
            
            # Map product IUPAC names
            product_iupacs = []
            for pid in final_product_ids:
                mapping = compound_mappings.get(str(pid).lower().strip())
                if mapping and mapping.iupac_name:
                    product_iupacs.append(mapping.iupac_name)
            # Only update if we found IUPAC names
            if product_iupacs:
                model_info['product_iupac_list'] = product_iupacs
        
        return model_info
    
    def _process_single_lineage_by_confidence(self, locations: List[Dict[str, Any]], 
                                             enzyme_df: pd.DataFrame) -> pd.DataFrame:
        """Process single lineage by confidence, stopping when all variants have data."""
        # Get list of all variants we need data for
        all_variants = set(enzyme_df['enzyme'].tolist() if 'enzyme' in enzyme_df.columns else 
                          enzyme_df['enzyme_id'].tolist())
        variants_with_data = set()
        all_results = []
        
        # Process locations in order of confidence
        for location in locations:
            if len(variants_with_data) >= len(all_variants):
                LOGGER.info("All variants have data, stopping extraction")
                break
                
            LOGGER.info("\nProcessing location %s (confidence: %d%%)", 
                       location['location'], location.get('confidence', 0))
            
            # Extract metrics from this location
            metrics_rows = self.extract_metrics_batch(list(all_variants), location['location'])
            
            # Filter to valid metrics
            valid_metrics = [m for m in metrics_rows if self._has_valid_metrics(m)]
            
            if not valid_metrics:
                LOGGER.warning("No valid metrics found in %s", location['location'])
                continue
            
            # Create DataFrame for this location
            df_location = pd.DataFrame(valid_metrics)
            
            # Track which variants we got data for
            new_variants = set(df_location['enzyme'].tolist()) - variants_with_data
            LOGGER.info("Found data for %d new variants in %s", len(new_variants), location['location'])
            variants_with_data.update(new_variants)
            
            # Add location info
            df_location['data_location'] = location['location']
            df_location['location_type'] = location.get('type', 'unknown')
            df_location['location_confidence'] = location.get('confidence', 0)
            
            all_results.append(df_location)
            
            # Log progress
            LOGGER.info("Progress: %d/%d variants have data", 
                       len(variants_with_data), len(all_variants))
        
        if all_results:
            # Combine all results
            df_combined = pd.concat(all_results, ignore_index=True)
            
            # If we have duplicates (same variant in multiple locations), keep the one with highest confidence
            if df_combined.duplicated(subset=['enzyme']).any():
                LOGGER.info("Removing duplicates, keeping highest confidence data")
                df_combined = df_combined.sort_values(
                    ['enzyme', 'location_confidence'], 
                    ascending=[True, False]
                ).drop_duplicates(subset=['enzyme'], keep='first')
            
            # Extract model reaction info once
            # Pass the enzyme variants we're processing
            enzyme_list = df_combined['enzyme'].unique().tolist()
            model_info = self.gather_model_reaction_info(enzyme_list)
            
            # Add model reaction info to all rows
            for key, value in model_info.items():
                if isinstance(value, list):
                    value = "; ".join(str(v) for v in value) if value else None
                df_combined[key] = value
            
            LOGGER.info("Extraction complete: %d unique variants with data", len(df_combined))
            
            return df_combined
        else:
            LOGGER.warning("No metrics extracted from any location")
            return pd.DataFrame()

    # ------------------------------------------------------------------
    # 6.5 Public orchestrator
    # ------------------------------------------------------------------

    def run(self, enzyme_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        # This module should always have enzyme CSV provided
        if enzyme_df is None:
            LOGGER.error("No enzyme DataFrame provided - this module requires enzyme CSV input")
            return pd.DataFrame()
        
        # Store enzyme_df for use in extract_metrics_batch
        self.enzyme_df = enzyme_df
        
        # Check if we have campaign_id column - if so, process each campaign separately
        if 'campaign_id' in enzyme_df.columns and not self.campaign_filter:
            campaigns = enzyme_df['campaign_id'].unique()
            if len(campaigns) > 1:
                LOGGER.info("Detected %d campaigns in enzyme data - processing each separately", len(campaigns))
                all_campaign_results = []
                
                for campaign_id in campaigns:
                    LOGGER.info("\n" + "="*60)
                    LOGGER.info("Processing campaign: %s", campaign_id)
                    LOGGER.info("="*60)
                    
                    # Create a new extractor instance for this campaign
                    campaign_extractor = ReactionExtractor(
                        manuscript=self.manuscript,
                        si=self.si,
                        cfg=self.cfg,
                        debug_dir=self.debug_dir / campaign_id if self.debug_dir else None,
                        campaign_filter=campaign_id,
                        all_campaigns=campaigns.tolist()
                    )
                    
                    # Run extraction for this campaign
                    campaign_df = campaign_extractor.run(enzyme_df)
                    
                    if not campaign_df.empty:
                        # Add a temporary campaign identifier for merging
                        campaign_df['_extraction_campaign'] = campaign_id
                        all_campaign_results.append(campaign_df)
                        LOGGER.info("Extracted %d reactions for campaign %s", len(campaign_df), campaign_id)
                
                # Combine results from all campaigns
                if all_campaign_results:
                    combined_df = pd.concat(all_campaign_results, ignore_index=True)
                    LOGGER.info("\nCombined extraction complete: %d total reactions across %d campaigns", 
                               len(combined_df), len(campaigns))
                    return combined_df
                else:
                    LOGGER.warning("No reactions extracted from any campaign")
                    return pd.DataFrame()
        
        # Filter by campaign if specified
        if self.campaign_filter and 'campaign_id' in enzyme_df.columns:
            LOGGER.info("Filtering enzymes for campaign: %s", self.campaign_filter)
            enzyme_df = enzyme_df[enzyme_df['campaign_id'] == self.campaign_filter].copy()
            LOGGER.info("Found %d enzymes for campaign %s", len(enzyme_df), self.campaign_filter)
            if len(enzyme_df) == 0:
                LOGGER.warning("No enzymes found for campaign %s", self.campaign_filter)
                return pd.DataFrame()
        
        # Find all locations with performance data
        locations = self.find_reaction_locations()
        if not locations:
            LOGGER.error("Failed to find reaction data locations")
            return pd.DataFrame()
        
        # Filter locations by campaign if specified
        if self.campaign_filter:
            filtered_locations = self._filter_locations_by_campaign(locations, enzyme_df)
            if filtered_locations:
                LOGGER.info("Filtered to %d locations for campaign %s", 
                           len(filtered_locations), self.campaign_filter)
                locations = filtered_locations
            else:
                LOGGER.warning("No locations found specifically for campaign %s, using all locations", 
                             self.campaign_filter)
        
        # Sort locations by confidence (highest first) and prefer tables over figures
        locations_sorted = sorted(locations, key=lambda x: (
            x.get('confidence', 0),
            1 if x.get('type') == 'table' else 0  # Prefer tables when confidence is equal
        ), reverse=True)
        
        LOGGER.info("Found %d reaction data location(s), sorted by confidence:", len(locations_sorted))
        for loc in locations_sorted:
            LOGGER.info("  - %s (%s, confidence: %d%%)", 
                       loc.get('location'), 
                       loc.get('type'),
                       loc.get('confidence', 0))
            
        # Analyze if we have multiple lineages
        lineage_analysis = self.analyze_lineage_groups(locations_sorted, enzyme_df)
        has_multiple_lineages = lineage_analysis.get('has_multiple_lineages', False)
        
        if has_multiple_lineages:
            LOGGER.info("Multiple lineage groups detected")
            return self._process_multiple_lineages_by_confidence(locations_sorted, enzyme_df, lineage_analysis)
        else:
            LOGGER.info("Single lineage detected, using confidence-based processing")
            return self._process_single_lineage_by_confidence(locations_sorted, enzyme_df)

###############################################################################
# 7 - MERGE WITH LINEAGE CSV + SAVE
###############################################################################

def merge_with_lineage_data(
    df_lineage: pd.DataFrame, df_metrics: pd.DataFrame
) -> pd.DataFrame:
    """Merge lineage and metrics data ensuring one-to-one mapping per campaign."""
    
    # Handle both 'enzyme' and 'enzyme_id' column names
    if "enzyme_id" in df_lineage.columns and "enzyme" not in df_lineage.columns:
        df_lineage = df_lineage.rename(columns={"enzyme_id": "enzyme"})
    
    if "enzyme" not in df_lineage.columns:
        raise ValueError("Lineage CSV must have an 'enzyme' or 'enzyme_id' column.")
    
    # Check if we have campaign information to match on
    if "campaign_id" in df_lineage.columns and "_extraction_campaign" in df_metrics.columns:
        # Match on both enzyme and campaign to ensure correct pairing
        df_metrics_temp = df_metrics.copy()
        df_metrics_temp['campaign_id'] = df_metrics_temp['_extraction_campaign']
        df_metrics_temp = df_metrics_temp.drop('_extraction_campaign', axis=1)
        merged = df_lineage.merge(df_metrics_temp, on=["enzyme", "campaign_id"], how="left")
    else:
        # Simple merge on enzyme only
        if "_extraction_campaign" in df_metrics.columns:
            df_metrics = df_metrics.drop('_extraction_campaign', axis=1)
        merged = df_lineage.merge(df_metrics, on="enzyme", how="left")
    
    return merged

###############################################################################
# 8 - CLI ENTRY-POINT
###############################################################################

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Extract enzyme reaction metrics from chemistry PDFs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--manuscript", required=True, type=Path)
    p.add_argument("--si", type=Path, help="Supporting-information PDF")
    p.add_argument("--lineage-csv", type=Path)
    p.add_argument("--output", type=Path, default=Path("reaction_metrics.csv"))
    p.add_argument("--verbose", action="store_true")
    p.add_argument(
        "--debug-dir",
        metavar="DIR",
        help="Write ALL intermediate artefacts (prompts, raw Gemini replies) to DIR",
    )
    return p

def main() -> None:
    args = build_parser().parse_args()
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    cfg = Config()
    
    # Load enzyme data from CSV if provided to detect campaign information
    enzyme_df = None
    campaign_filter = None
    all_campaigns = None
    
    if args.lineage_csv and args.lineage_csv.exists():
        LOGGER.info("Loading enzyme data from CSV…")
        enzyme_df = pd.read_csv(args.lineage_csv)
        
        # Detect campaign information from the enzyme CSV
        if 'campaign_id' in enzyme_df.columns:
            all_campaigns = enzyme_df['campaign_id'].dropna().unique().tolist()
            if len(all_campaigns) == 1:
                campaign_filter = all_campaigns[0]
                LOGGER.info("Detected single campaign: %s", campaign_filter)
                
                # Create campaign-specific debug directory even for single campaign
                campaign_debug_dir = None
                if args.debug_dir:
                    campaign_debug_dir = Path(args.debug_dir) / f"campaign_{campaign_filter}"
                    campaign_debug_dir.mkdir(parents=True, exist_ok=True)
                    LOGGER.info("Campaign debug directory: %s", campaign_debug_dir)
                
                extractor = ReactionExtractor(args.manuscript, args.si, cfg, debug_dir=campaign_debug_dir, 
                                            campaign_filter=campaign_filter, all_campaigns=all_campaigns)
                df_metrics = extractor.run(enzyme_df)
                
            elif len(all_campaigns) > 1:
                LOGGER.info("Detected multiple campaigns: %s", all_campaigns)
                all_results = []
                
                # Process each campaign separately
                for campaign in all_campaigns:
                    LOGGER.info("Processing campaign: %s", campaign)
                    
                    # Filter enzyme_df to this campaign
                    campaign_df = enzyme_df[enzyme_df['campaign_id'] == campaign].copy()
                    LOGGER.info("Found %d enzymes for campaign %s", len(campaign_df), campaign)
                    
                    if len(campaign_df) == 0:
                        LOGGER.warning("No enzymes found for campaign %s, skipping", campaign)
                        continue
                    
                    # Create extractor for this campaign with campaign-specific debug directory
                    campaign_debug_dir = None
                    if args.debug_dir:
                        campaign_debug_dir = Path(args.debug_dir) / f"campaign_{campaign}"
                        campaign_debug_dir.mkdir(parents=True, exist_ok=True)
                        LOGGER.info("Campaign debug directory: %s", campaign_debug_dir)
                    
                    extractor = ReactionExtractor(args.manuscript, args.si, cfg, debug_dir=campaign_debug_dir, 
                                                campaign_filter=campaign, all_campaigns=all_campaigns)
                    
                    # Run extraction for this campaign
                    campaign_metrics = extractor.run(campaign_df)
                    
                    if not campaign_metrics.empty:
                        # Merge with lineage data for this campaign
                        campaign_lineage = enzyme_df[enzyme_df['campaign_id'] == campaign].copy()
                        if "enzyme_id" in campaign_lineage.columns and "enzyme" not in campaign_lineage.columns:
                            campaign_lineage = campaign_lineage.rename(columns={"enzyme_id": "enzyme"})
                        
                        # Merge campaign metrics with lineage data
                        campaign_final = campaign_metrics.merge(campaign_lineage, on='enzyme', how='left', suffixes=('', '_lineage'))
                        
                        # Save campaign-specific file immediately
                        output_dir = args.output.parent
                        base_name = args.output.stem
                        campaign_file = output_dir / f"{base_name}_{campaign}.csv"
                        campaign_final.to_csv(campaign_file, index=False)
                        LOGGER.info("Saved %d rows for campaign %s -> %s", len(campaign_final), campaign, campaign_file)
                        
                        # Add the merged data (not just metrics) to final results
                        all_results.append(campaign_final)
                        LOGGER.info("Added %d merged results for campaign %s", len(campaign_final), campaign)
                    else:
                        LOGGER.warning("No results extracted for campaign %s", campaign)
                        
                        # Still save an empty campaign file with lineage data
                        campaign_lineage = enzyme_df[enzyme_df['campaign_id'] == campaign].copy()
                        if not campaign_lineage.empty:
                            output_dir = args.output.parent
                            base_name = args.output.stem
                            campaign_file = output_dir / f"{base_name}_{campaign}.csv"
                            campaign_lineage.to_csv(campaign_file, index=False)
                            LOGGER.info("Saved %d rows (lineage only) for campaign %s -> %s", len(campaign_lineage), campaign, campaign_file)
                
                # Combine all campaign results
                if all_results:
                    df_metrics = pd.concat(all_results, ignore_index=True)
                    LOGGER.info("Combined results from %d campaigns: %d total rows", len(all_results), len(df_metrics))
                else:
                    LOGGER.warning("No results from any campaign")
                    df_metrics = pd.DataFrame()
        else:
            # No campaign information, process all enzymes together
            campaign_debug_dir = None
            if args.debug_dir:
                campaign_debug_dir = Path(args.debug_dir) / "no_campaign"
                campaign_debug_dir.mkdir(parents=True, exist_ok=True)
                LOGGER.info("Debug directory (no campaign): %s", campaign_debug_dir)
            
            extractor = ReactionExtractor(args.manuscript, args.si, cfg, debug_dir=campaign_debug_dir, 
                                        campaign_filter=campaign_filter, all_campaigns=all_campaigns)
            df_metrics = extractor.run(enzyme_df)

    # Skip final merge since campaign-specific merges already happened during processing
    # This avoids duplicate entries when same enzyme appears in multiple campaigns
    df_final = df_metrics
    LOGGER.info("Using pre-merged campaign data - final dataset has %d rows", len(df_final) if df_final is not None else 0)

    df_final.to_csv(args.output, index=False)
    LOGGER.info("Saved %d rows -> %s", len(df_final), args.output)
    
    # Campaign-specific files are already saved during processing above

if __name__ == "__main__":
    main()

