 #!/usr/bin/env python3
"""
lineage_flattener.py
====================
A **complete rewrite** of the original `lineage_format.py`, structured in the
same sectioned style as `enzyme_lineage_extractor.py`, but **without any non-ASCII
characters**. All input and output column names are declared once as top-level
constants to prevent accidental drift.

The tool reads an annotated CSV containing enzyme variant information (lineage,
sequences, reaction data, fitness, etc.) and produces a flat reaction table
(one row per product) suitable for robotic plate builders or downstream ML.

-------------------------------------------------------------------------------
SECTION GUIDE (grep-able):
  # === 1. CONFIG & CONSTANTS ===
  # === 2. DOMAIN MODELS ===
  # === 3. LOGGING HELPERS ===
  # === 4. CACHE & DB HELPERS ===
  # === 5. SEQUENCE / MUTATION HELPERS ===
  # === 6. SMILES CONVERSION HELPERS ===
  # === 7. FLATTENING CORE ===
  # === 8. PIPELINE ORCHESTRATOR ===
  # === 9. CLI ENTRYPOINT ===
-------------------------------------------------------------------------------
"""

# === 1. CONFIG & CONSTANTS ===================================================
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import pickle
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd
from tqdm import tqdm

try:
    from rdkit import Chem  # type: ignore
    RDKIT_OK = True
except ImportError:  # pragma: no cover
    RDKIT_OK = False

try:
    import google.generativeai as genai  # type: ignore
    GEMINI_OK = True
except ImportError:  # pragma: no cover
    GEMINI_OK = False

# Input columns that MUST be present ------------------------------------------------
INPUT_REQUIRED: Tuple[str, ...] = (
    "enzyme_id",
    "substrate_iupac_list",    # preferred source for SMILES lookup
    "product_iupac_list",      # preferred source for SMILES lookup
)

# Alternative column names that can be used instead
COLUMN_ALIASES: Dict[str, str] = {
    "enzyme": "enzyme_id",     # Handle 'enzyme' as an alias for 'enzyme_id'
}

# Optional but recognized input fields ----------------------------------------------
OPTIONAL_INPUT: Tuple[str, ...] = (
    "parent_enzyme_id",
    "generation",
    "protein_sequence",
    "aa_sequence",
    "nucleotide_sequence",
    "nt_sequence",
    "ttn",
    "yield",
    "reaction_temperature",
    "reaction_ph",
    "reaction_other_conditions",
    "reaction_substrate_concentration",
    "cofactor_iupac_list",
    "cofactor_list",
    "ee",
    "data_type",               # either "lineage" or "substrate_scope"
    "substrate",               # fallback names
    "substrate_name",
    "compound",
    "product",
    "product_name",
)

# Output columns --------------------------------------------------------------------
OUTPUT_COLUMNS: Tuple[str, ...] = (
    "id",
    "barcode_plate",
    "plate",
    "well",
    "smiles_string",
    "smiles_reaction",
    "alignment_count",
    "alignment_probability",
    "nucleotide_mutation",
    "amino_acid_substitutions",
    "nt_sequence",
    "aa_sequence",
    "x_coordinate",
    "y_coordinate",
    "fitness_value",
    "fitness_type",
    "cofactor",
    "reaction_condition",
    "ee",
    "campaign_id",
    "generation",
    "parent_enzyme_id",
    "additional_information",
)

# Plate layout constants -------------------------------------------------------------
PLATE_SIZE: int = 96
BARCODE_START: int = 1

# Batch / parallelism ----------------------------------------------------------------
MAX_WORKERS: int = min(32, (os.cpu_count() or 4) * 2)
BATCH_SIZE: int = 50

# Cache files ------------------------------------------------------------------------
CACHE_DIR: Path = Path(os.environ.get("LINEAGE_CACHE_DIR", "./.cache"))
SMILES_CACHE_FILE: Path = CACHE_DIR / "smiles_cache.pkl"
SUBSTRATE_CACHE_FILE: Path = CACHE_DIR / "substrate_smiles_cache.pkl"
CANONICAL_CACHE_FILE: Path = CACHE_DIR / "canonical_smiles_cache.pkl"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# API endpoints for IUPAC to SMILES conversion --------------------------------------

# Gemini API configuration -----------------------------------------------------------
GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")

# Miscellaneous ----------------------------------------------------------------------
WELL_ROWS: str = "ABCDEFGH"  # 8 rows, 12 cols => 96 wells


# === 2. DOMAIN MODELS ===============================================================
@dataclass
class VariantRecord:
    """Minimal representation of an enzyme variant row from the input CSV."""

    row: Dict[str, str]

    def __post_init__(self) -> None:
        # Apply column aliases
        for alias, canonical in COLUMN_ALIASES.items():
            if alias in self.row and canonical not in self.row:
                self.row[canonical] = self.row[alias]
        
        missing = [c for c in INPUT_REQUIRED if c not in self.row]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

    # Convenience accessors ---------------------------------------------------------
    @property
    def eid(self) -> str:
        return str(self.row["enzyme_id"]).strip()

    @property
    def parent_id(self) -> str:
        return str(self.row.get("parent_enzyme_id", "")).strip()

    @property
    def generation(self) -> str:
        return str(self.row.get("generation", "")).strip()

    @property
    def aa_seq(self) -> str:
        return (
            str(self.row.get("protein_sequence", ""))
            or str(self.row.get("aa_sequence", ""))
        ).strip()

    @property
    def nt_seq(self) -> str:
        # First try to get actual NT sequence
        nt = (
            str(self.row.get("nucleotide_sequence", ""))
            or str(self.row.get("nt_sequence", ""))
        ).strip()
        
        # If no NT sequence but we have AA sequence, reverse translate
        if (not nt or nt == "nan") and self.aa_seq:
            nt = _rev_translate(self.aa_seq)
        
        return nt

    # Reaction-related -------------------------------------------------------------
    def substrate_iupac(self) -> List[str]:
        raw = str(self.row.get("substrate_iupac_list", "")).strip()
        result = _split_list(raw)
        if not result and raw and raw.lower() != 'nan':
            log.debug(f"substrate_iupac_list for {self.eid}: raw='{raw}', parsed={result}")
        return result

    def product_iupac(self) -> List[str]:
        raw = str(self.row.get("product_iupac_list", "")).strip()
        result = _split_list(raw)
        if not result and raw and raw.lower() != 'nan':
            log.debug(f"product_iupac_list for {self.eid}: raw='{raw}', parsed={result}")
        return result


    def ttn_or_yield(self) -> Optional[float]:
        for col in ("ttn", "yield"):
            val = self.row.get(col)
            if val is not None and pd.notna(val):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    continue
        return None


@dataclass
class FlatRow:
    """Row for the output CSV. Only validated on demand."""

    id: str
    barcode_plate: int
    plate: str
    well: str
    smiles_string: str
    smiles_reaction: str
    alignment_count: int = 1
    alignment_probability: float = 1.0
    nucleotide_mutation: str = ""
    amino_acid_substitutions: str = ""
    nt_sequence: str = ""
    aa_sequence: str = ""
    x_coordinate: str = ""
    y_coordinate: str = ""
    fitness_value: Optional[float] = None
    fitness_type: str = ""
    cofactor: str = ""
    reaction_condition: str = ""
    ee: str = ""
    campaign_id: str = ""
    generation: str = ""
    parent_enzyme_id: str = ""
    additional_information: str = ""

    def as_dict(self) -> Dict[str, str]:
        data = {
            "id": self.id,
            "barcode_plate": self.barcode_plate,
            "plate": self.plate,
            "well": self.well,
            "smiles_string": self.smiles_string,
            "smiles_reaction": self.smiles_reaction,
            "alignment_count": self.alignment_count,
            "alignment_probability": self.alignment_probability,
            "nucleotide_mutation": self.nucleotide_mutation,
            "amino_acid_substitutions": self.amino_acid_substitutions,
            "nt_sequence": self.nt_sequence,
            "aa_sequence": self.aa_sequence,
            "x_coordinate": self.x_coordinate,
            "y_coordinate": self.y_coordinate,
            "fitness_value": self.fitness_value,
            "fitness_type": self.fitness_type,
            "cofactor": self.cofactor,
            "reaction_condition": self.reaction_condition,
            "ee": self.ee,
            "campaign_id": self.campaign_id,
            "generation": self.generation,
            "parent_enzyme_id": self.parent_enzyme_id,
            "additional_information": self.additional_information,
        }
        # Convert None to empty string for CSV friendliness
        return {k: ("" if v is None else v) for k, v in data.items()}


# === 3. LOGGING HELPERS =============================================================

def get_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        handler.setFormatter(logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

log = get_logger(__name__)


# === 4. CACHE & DB HELPERS ==========================================================

def _load_pickle(path: Path) -> Dict[str, str]:
    if path.exists():
        try:
            with path.open("rb") as fh:
                return pickle.load(fh)
        except Exception as exc:  # pragma: no cover
            log.warning("Could not read cache %s: %s", path, exc)
    return {}


def _save_pickle(obj: Dict[str, str], path: Path) -> None:
    try:
        with path.open("wb") as fh:
            pickle.dump(obj, fh)
    except Exception as exc:  # pragma: no cover
        log.warning("Could not write cache %s: %s", path, exc)


SMILES_CACHE: Dict[str, str] = _load_pickle(SMILES_CACHE_FILE)
SUBSTRATE_CACHE: Dict[str, str] = _load_pickle(SUBSTRATE_CACHE_FILE)
CANONICAL_CACHE: Dict[str, str] = _load_pickle(CANONICAL_CACHE_FILE)


# --- Removed local database - using only online APIs -------------------------------


# === 5. SEQUENCE / MUTATION HELPERS ================================================

# Genetic code for naive reverse translation --------------------------------
CODON: Dict[str, str] = {
    # One representative codon per amino acid (simplified)
    "A": "GCT", "R": "CGT", "N": "AAT", "D": "GAT", "C": "TGT", "Q": "CAA",
    "E": "GAA", "G": "GGT", "H": "CAT", "I": "ATT", "L": "CTT", "K": "AAA",
    "M": "ATG", "F": "TTT", "P": "CCT", "S": "TCT", "T": "ACT", "W": "TGG",
    "Y": "TAT", "V": "GTT", "*": "TAA",
}


def _rev_translate(aa: str) -> str:
    """Rudimentary AA -> DNA translation (three-letter codon table above)."""
    return "".join(CODON.get(res, "NNN") for res in aa)


def _aa_mut(parent: str, child: str) -> str:
    """Return simple mutation descriptor P12V_P34L ... comparing AA sequences."""
    mutations = []
    for idx, (p, c) in enumerate(zip(parent, child), start=1):
        if p != c:
            mutations.append(f"{p}{idx}{c}")
    return "_".join(mutations)


def _nt_mut(parent_aa: str, child_aa: str, parent_nt: str = "", child_nt: str = "") -> str:
    """Return mutations at nucleotide level (uses reverse translation if needed)."""
    if parent_nt and child_nt and len(parent_nt) > 0 and len(child_nt) > 0:
        # Use actual nucleotide sequences if both are available
        muts = []
        for idx, (p, c) in enumerate(zip(parent_nt, child_nt), start=1):
            if p != c:
                muts.append(f"{p}{idx}{c}")
        return "_".join(muts)
    else:
        # Fall back to reverse translation from protein sequences
        p_seq = _rev_translate(parent_aa) if parent_aa else ""
        c_seq = _rev_translate(child_aa) if child_aa else ""
        muts = []
        for idx, (p, c) in enumerate(zip(p_seq, c_seq), start=1):
            if p != c:
                muts.append(f"{p}{idx}{c}")
        return "_".join(muts)


# === 6. SMILES CONVERSION HELPERS ==================================================

def search_smiles_with_gemini(compound_name: str, model=None) -> Optional[str]:
    """
    Use Gemini to search for SMILES strings of complex compounds.
    Returns SMILES string if found, None otherwise.
    """
    if not compound_name or compound_name.lower() in ['nan', 'none', '']:
        return None
        
    if not model:
        try:
            # Import get_model from enzyme_lineage_extractor
            import sys
            from pathlib import Path
            sys.path.append(str(Path(__file__).parent))
            from enzyme_lineage_extractor import get_model
            model = get_model()
        except Exception as e:
            log.warning(f"Could not load Gemini model: {e}")
            return None
    
    prompt = f"""Search for the SMILES string representation of this chemical compound:
"{compound_name}"

IMPORTANT: 
- Do NOT generate or create a SMILES string
- Only provide SMILES that you can find in chemical databases or literature
- For deuterated compounds, search for the specific isotope-labeled SMILES
- If you cannot find the exact SMILES, say "NOT FOUND"

Return ONLY the SMILES string if found, or "NOT FOUND" if not found.
No explanation or additional text."""
    
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        if result and result != "NOT FOUND" and not result.startswith("I"):
            # Basic validation that it looks like SMILES
            if any(c in result for c in ['C', 'c', 'N', 'O', 'S', 'P', '[', ']', '(', ')']):
                log.info(f"Gemini found SMILES for '{compound_name}': {result}")
                return result
        return None
    except Exception as e:
        log.debug(f"Gemini SMILES search failed for '{compound_name}': {e}")
        return None


def _split_list(raw: str) -> List[str]:
    if not raw or str(raw).lower() == 'nan':
        return []
    return [s.strip() for s in raw.split(";") if s.strip() and s.strip().lower() != 'nan']


def _canonical_smiles(smiles: str) -> str:
    if not smiles or not RDKIT_OK:
        return smiles
    if smiles in CANONICAL_CACHE:
        return CANONICAL_CACHE[smiles]
    try:
        mol = Chem.MolFromSmiles(smiles)  # type: ignore[attr-defined]
        if mol:
            canon = Chem.MolToSmiles(mol, canonical=True)  # type: ignore[attr-defined]
            CANONICAL_CACHE[smiles] = canon
            return canon
    except Exception:  # pragma: no cover
        pass
    return smiles


def _name_to_smiles(name: str, is_substrate: bool) -> str:
    """Convert IUPAC (preferred) or plain name to SMILES with multi-tier lookup."""
    # NO CACHING - Always try fresh conversion
    
    # Filter out invalid values that shouldn't be converted
    if not name or name.lower() in ['nan', 'none', 'null', 'n/a', 'na', '']:
        return ""
    
    # 1. OPSIN (if installed) - fast and reliable for IUPAC names
    try:
        import subprocess

        # Use stdin to avoid shell interpretation issues with special characters
        result = subprocess.run(
            ["opsin", "-osmi"], input=name, capture_output=True, text=True, check=False
        )
        if result.returncode == 0 and result.stdout.strip():
            # OPSIN output may include a header line, so get the last non-empty line
            lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
            if lines:
                opsin_smiles = lines[-1]
                return opsin_smiles
    except FileNotFoundError:
        pass  # OPSIN not installed

    # 2. PubChem PUG REST API (online) - comprehensive database
    try:
        import requests

        url = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{requests.utils.quote(name)}/property/IsomericSMILES/TXT"
        )
        resp = requests.get(url, timeout=10)
        if resp.ok:
            pug_smiles = resp.text.strip().split("\n")[0]
            return pug_smiles
    except Exception:  # pragma: no cover
        pass
    
    # 3. Gemini search (for complex compounds) - AI fallback
    gemini_smiles = search_smiles_with_gemini(name)
    if gemini_smiles:
        return gemini_smiles

    # Return empty string if all methods fail
    return ""


def _batch_convert(names: Sequence[str], is_substrate: bool) -> Dict[str, str]:
    """Convert a batch of names to SMILES in parallel."""
    out: Dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_name_to_smiles, n, is_substrate): n for n in names}
        for fut in tqdm(as_completed(futures), total=len(futures), desc="SMILES"):
            name = futures[fut]
            try:
                result = fut.result()
                # Only store successful conversions
                if result:
                    out[name] = result
                else:
                    log.debug("SMILES conversion failed for %s", name)
            except Exception as exc:  # pragma: no cover
                log.debug("SMILES conversion exception for %s: %s", name, exc)
    return out


# === 7. FLATTENING CORE ============================================================

def _fill_missing_sequences(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing sequences in substrate scope entries from reaction data entries.
    
    This function:
    1. First cleans up 3a data (lineage entries) to standardize enzyme_id column
    2. Then populates sequences in 3b data (substrate scope) based on campaign_id + enzyme_id matching
    3. Uses Gemini API for intelligent matching when exact matches fail
    """
    # Step 1: Clean up 3a data format
    log.info("Cleaning up reaction data (3a) format...")
    
    # Handle column aliasing for enzyme_id
    if 'enzyme' in df.columns and 'enzyme_id' not in df.columns:
        df['enzyme_id'] = df['enzyme']
        log.info("Renamed 'enzyme' column to 'enzyme_id' in reaction data")
    
    # Step 2: Create sequence lookup from cleaned 3a data
    seq_lookup = {}
    campaign_enzymes = {}  # Track enzymes by campaign for Gemini matching
    
    # Collect sequences from reaction data entries (3a) - these have data_type='lineage'
    reaction_entries = df[df.get("data_type") == "lineage"]
    log.info(f"Found {len(reaction_entries)} reaction data entries to extract sequences from")
    
    for _, row in reaction_entries.iterrows():
        eid = str(row["enzyme_id"])
        campaign_id = str(row.get("campaign_id", "default"))
        
        # Prioritize protein_sequence (from 3a) over aa_sequence (from lineage file)
        aa_seq = str(row.get("protein_sequence", "")) or str(row.get("aa_sequence", ""))
        nt_seq = str(row.get("nucleotide_sequence", "")) or str(row.get("nt_sequence", "")) or str(row.get("dna_seq", ""))
        
        if aa_seq and aa_seq != "nan" and aa_seq != "":
            # Use campaign_id + enzyme_id as composite key for exact matching
            composite_key = f"{campaign_id}_{eid}"
            seq_lookup[composite_key] = {
                "aa_sequence": aa_seq,
                "nt_sequence": nt_seq if nt_seq != "nan" else "",
                "campaign_id": campaign_id,
                "enzyme_id": eid,
                "generation": str(row.get("generation", "")),
                "parent_enzyme_id": str(row.get("parent_enzyme_id", ""))
            }
            
            # Also keep simple enzyme_id lookup as fallback
            seq_lookup[eid] = {
                "aa_sequence": aa_seq,
                "nt_sequence": nt_seq if nt_seq != "nan" else "",
                "campaign_id": campaign_id,
                "enzyme_id": eid,
                "generation": str(row.get("generation", "")),
                "parent_enzyme_id": str(row.get("parent_enzyme_id", ""))
            }
            
            # Track enzymes by campaign for Gemini matching
            if campaign_id not in campaign_enzymes:
                campaign_enzymes[campaign_id] = []
            campaign_enzymes[campaign_id].append({
                "enzyme_id": eid,
                "has_sequence": True,
                "generation": str(row.get("generation", "")),
                "parent_id": str(row.get("parent_enzyme_id", ""))
            })
    
    log.info(f"Created sequence lookup with {len(seq_lookup)} entries from reaction data")
    
    # Setup Gemini if available
    gemini_model = None
    if GEMINI_OK and GEMINI_API_KEY:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            log.info("Gemini API configured for intelligent enzyme matching")
        except Exception as e:
            log.warning(f"Failed to configure Gemini API: {e}")
    
    # Step 3: Fill missing sequences in substrate scope entries (3b)
    substrate_entries = df[df.get("data_type") == "substrate_scope"]
    log.info(f"Found {len(substrate_entries)} substrate scope entries to populate sequences for")
    
    filled_count = 0
    gemini_matched_count = 0
    unmatched_enzymes = []  # Track enzymes that need Gemini matching
    
    for idx, row in df.iterrows():
        if row.get("data_type") != "substrate_scope":
            continue
            
        eid = str(row["enzyme_id"])
        campaign_id = str(row.get("campaign_id", "default"))
        
        # Check if this row needs sequence filling
        aa_seq = str(row.get("protein_sequence", "")) or str(row.get("aa_sequence", ""))
        if not aa_seq or aa_seq == "nan" or aa_seq == "":
            # Try campaign-specific lookup first (most precise match)
            composite_key = f"{campaign_id}_{eid}"
            if composite_key in seq_lookup:
                df.at[idx, "protein_sequence"] = seq_lookup[composite_key]["aa_sequence"]
                df.at[idx, "aa_sequence"] = seq_lookup[composite_key]["aa_sequence"]
                if seq_lookup[composite_key]["nt_sequence"]:
                    df.at[idx, "nucleotide_sequence"] = seq_lookup[composite_key]["nt_sequence"]
                    df.at[idx, "nt_sequence"] = seq_lookup[composite_key]["nt_sequence"]
                df.at[idx, "generation"] = seq_lookup[composite_key]["generation"]
                df.at[idx, "parent_enzyme_id"] = seq_lookup[composite_key]["parent_enzyme_id"]
                filled_count += 1
                log.debug(f"Filled sequence for {eid} in campaign {campaign_id} (exact match)")
            
            # Fallback to enzyme_id only lookup
            elif eid in seq_lookup:
                df.at[idx, "protein_sequence"] = seq_lookup[eid]["aa_sequence"]
                df.at[idx, "aa_sequence"] = seq_lookup[eid]["aa_sequence"]
                if seq_lookup[eid]["nt_sequence"]:
                    df.at[idx, "nucleotide_sequence"] = seq_lookup[eid]["nt_sequence"]
                    df.at[idx, "nt_sequence"] = seq_lookup[eid]["nt_sequence"]
                df.at[idx, "generation"] = seq_lookup[eid]["generation"]
                df.at[idx, "parent_enzyme_id"] = seq_lookup[eid]["parent_enzyme_id"]
                filled_count += 1
                log.debug(f"Filled sequence for {eid} (fallback lookup)")
            
            else:
                # Collect for Gemini matching
                unmatched_enzymes.append({
                    "idx": idx,
                    "enzyme_id": eid,
                    "campaign_id": campaign_id
                })
    
    # Step 4: Use Gemini for intelligent matching of unmatched enzymes
    if unmatched_enzymes and gemini_model:
        log.info(f"Using Gemini to intelligently match {len(unmatched_enzymes)} unmatched enzymes")
        
        # Group unmatched enzymes by campaign
        unmatched_by_campaign = {}
        for entry in unmatched_enzymes:
            cid = entry["campaign_id"]
            if cid not in unmatched_by_campaign:
                unmatched_by_campaign[cid] = []
            unmatched_by_campaign[cid].append(entry)
        
        # Process each campaign
        for campaign_id, entries in unmatched_by_campaign.items():
            if campaign_id not in campaign_enzymes or not campaign_enzymes[campaign_id]:
                log.warning(f"No enzymes with sequences found in campaign {campaign_id}")
                continue
            
            # Get enzyme IDs that need matching
            unmatched_ids = [e["enzyme_id"] for e in entries]
            
            # Get available enzymes in this campaign
            available_ids = [e["enzyme_id"] for e in campaign_enzymes[campaign_id] if e["has_sequence"]]
            
            if not available_ids:
                log.warning(f"No enzymes with sequences available in campaign {campaign_id}")
                continue
            
            # Create prompt for Gemini
            prompt = f"""Match enzyme variant IDs from substrate scope data to their corresponding sequences in reaction data.
These are from the same campaign ({campaign_id}) but may use slightly different naming conventions.

Enzymes needing sequences (from substrate scope):
{json.dumps(unmatched_ids, indent=2)}

Enzymes with sequences available (from reaction data):
{json.dumps(available_ids, indent=2)}

Match each enzyme from the first list to its corresponding enzyme in the second list.
Consider variations like:
- Case differences (p411-hf vs P411-HF)
- Underscore vs hyphen (p411_hf vs p411-hf)
- Additional prefixes/suffixes
- Similar naming patterns within the campaign

Return ONLY a JSON object mapping substrate scope IDs to reaction data IDs:
{{"substrate_scope_id": "reaction_data_id", ...}}

Only include matches you are confident about. If no match exists, omit that enzyme.
"""
            
            try:
                response = gemini_model.generate_content(prompt)
                mapping_text = response.text.strip()
                
                # Extract JSON from response
                if '```json' in mapping_text:
                    mapping_text = mapping_text.split('```json')[1].split('```')[0].strip()
                elif '```' in mapping_text:
                    mapping_text = mapping_text.split('```')[1].split('```')[0].strip()
                
                mapping = json.loads(mapping_text)
                
                # Apply the matches
                for entry in entries:
                    substrate_id = entry["enzyme_id"]
                    if substrate_id in mapping:
                        matched_id = mapping[substrate_id]
                        composite_key = f"{campaign_id}_{matched_id}"
                        
                        if composite_key in seq_lookup:
                            idx = entry["idx"]
                            df.at[idx, "protein_sequence"] = seq_lookup[composite_key]["aa_sequence"]
                            df.at[idx, "aa_sequence"] = seq_lookup[composite_key]["aa_sequence"]
                            if seq_lookup[composite_key]["nt_sequence"]:
                                df.at[idx, "nucleotide_sequence"] = seq_lookup[composite_key]["nt_sequence"]
                                df.at[idx, "nt_sequence"] = seq_lookup[composite_key]["nt_sequence"]
                            
                            # Also copy generation and parent_enzyme_id
                            df.at[idx, "generation"] = seq_lookup[composite_key]["generation"]
                            df.at[idx, "parent_enzyme_id"] = seq_lookup[composite_key]["parent_enzyme_id"]
                            
                            # Store the match for later mutation copying
                            df.at[idx, "_matched_enzyme_id"] = matched_id
                            df.at[idx, "_matched_campaign_id"] = campaign_id
                            
                            gemini_matched_count += 1
                            log.info(f"Gemini matched '{substrate_id}' -> '{matched_id}' in campaign {campaign_id}")
                        else:
                            log.warning(f"Gemini suggested match '{matched_id}' not found in sequence lookup")
                
            except Exception as e:
                log.warning(f"Failed to get Gemini matches for campaign {campaign_id}: {e}")
    
    # Final logging
    total_filled = filled_count + gemini_matched_count
    if total_filled > 0:
        log.info(f"Successfully filled sequences for {total_filled} substrate scope entries "
                f"({filled_count} exact matches, {gemini_matched_count} Gemini matches)")
    
    # Log any remaining unmatched
    for entry in unmatched_enzymes:
        if not any(df.at[entry["idx"], col] for col in ["protein_sequence", "aa_sequence"] 
                  if col in df.columns and df.at[entry["idx"], col]):
            log.warning(f"No sequence found for enzyme_id={entry['enzyme_id']} in campaign {entry['campaign_id']}")
    
    return df


def _copy_mutations_from_matched_enzymes(out_df: pd.DataFrame, orig_df: pd.DataFrame) -> pd.DataFrame:
    """Copy nucleotide_mutation and amino_acid_substitutions from matched enzymes.
    
    This function looks for entries that were matched by Gemini and copies their
    mutation information from the corresponding matched enzyme.
    """
    # Look for entries with _matched_enzyme_id (these were matched by Gemini)
    if "_matched_enzyme_id" not in orig_df.columns:
        return out_df
    
    matched_entries = orig_df[orig_df["_matched_enzyme_id"].notna()]
    
    if len(matched_entries) == 0:
        return out_df
    
    log.info(f"Copying mutations for {len(matched_entries)} Gemini-matched entries")
    
    # Create a lookup of mutations from the output dataframe
    mutation_lookup = {}
    for idx, row in out_df.iterrows():
        key = f"{row['campaign_id']}_{row['id']}"  # 'id' is the enzyme_id in output
        mutation_lookup[key] = {
            "nucleotide_mutation": row.get("nucleotide_mutation", ""),
            "amino_acid_substitutions": row.get("amino_acid_substitutions", "")
        }
    
    # Copy mutations for matched entries
    mutations_copied = 0
    for idx, row in out_df.iterrows():
        # Check if this row needs mutation copying
        # Find the original row in orig_df with the same enzyme_id and campaign_id
        orig_mask = (orig_df["enzyme_id"] == row["id"]) & (orig_df["campaign_id"] == row["campaign_id"])
        orig_rows = orig_df[orig_mask]
        
        if len(orig_rows) > 0 and "_matched_enzyme_id" in orig_rows.columns:
            orig_row = orig_rows.iloc[0]
            if pd.notna(orig_row.get("_matched_enzyme_id")):
                # This was a Gemini-matched entry
                matched_id = orig_row["_matched_enzyme_id"]
                matched_campaign = orig_row["_matched_campaign_id"]
                lookup_key = f"{matched_campaign}_{matched_id}"
                
                if lookup_key in mutation_lookup:
                    out_df.at[idx, "nucleotide_mutation"] = mutation_lookup[lookup_key]["nucleotide_mutation"]
                    out_df.at[idx, "amino_acid_substitutions"] = mutation_lookup[lookup_key]["amino_acid_substitutions"]
                    mutations_copied += 1
                    log.debug(f"Copied mutations for {row['id']} from {matched_id}")
    
    if mutations_copied > 0:
        log.info(f"Successfully copied mutations for {mutations_copied} entries")
    
    return out_df


def _identify_parents_with_gemini(df: pd.DataFrame) -> pd.DataFrame:
    """Use Gemini API to identify parent enzymes for entries with missing parent information."""
    if not GEMINI_OK:
        log.warning("Gemini API not available (missing google.generativeai). Skipping parent identification.")
        return df
    
    if not GEMINI_API_KEY:
        log.warning("GEMINI_API_KEY not set. Skipping parent identification.")
        return df
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        log.warning(f"Failed to configure Gemini API: {e}. Skipping parent identification.")
        return df
    
    # Find entries with empty sequences but missing parent information
    entries_needing_parents = []
    for idx, row in df.iterrows():
        aa_seq = str(row.get("protein_sequence", "")) or str(row.get("aa_sequence", ""))
        nt_seq = str(row.get("nucleotide_sequence", "")) or str(row.get("nt_sequence", ""))
        parent_id = str(row.get("parent_enzyme_id", "")).strip()
        
        # Only process entries that have empty sequences AND no parent info
        if (not aa_seq or aa_seq == "nan" or aa_seq == "") and (not nt_seq or nt_seq == "nan" or nt_seq == "") and (not parent_id or parent_id == "nan"):
            enzyme_id = str(row.get("enzyme_id", ""))
            campaign_id = str(row.get("campaign_id", ""))
            generation = str(row.get("generation", ""))
            
            entries_needing_parents.append({
                "idx": idx,
                "enzyme_id": enzyme_id,
                "campaign_id": campaign_id,
                "generation": generation
            })
    
    if not entries_needing_parents:
        log.info("No entries need parent identification from Gemini")
        return df
    
    log.info(f"Found {len(entries_needing_parents)} entries needing parent identification. Querying Gemini...")
    
    # Create a lookup of all available enzyme IDs for context
    available_enzymes = {}
    for idx, row in df.iterrows():
        enzyme_id = str(row.get("enzyme_id", ""))
        campaign_id = str(row.get("campaign_id", ""))
        aa_seq = str(row.get("protein_sequence", "")) or str(row.get("aa_sequence", ""))
        generation = str(row.get("generation", ""))
        
        if enzyme_id and enzyme_id != "nan":
            available_enzymes[enzyme_id] = {
                "campaign_id": campaign_id,
                "has_sequence": bool(aa_seq and aa_seq != "nan" and aa_seq != ""),
                "generation": generation
            }
    
    identified_count = 0
    for entry in entries_needing_parents:
        enzyme_id = entry["enzyme_id"]
        campaign_id = entry["campaign_id"]
        generation = entry["generation"]
        
        # Create context for Gemini
        context_info = []
        context_info.append(f"Enzyme ID: {enzyme_id}")
        context_info.append(f"Campaign ID: {campaign_id}")
        if generation:
            context_info.append(f"Generation: {generation}")
        
        # Add available enzymes from the same campaign for context
        campaign_enzymes = []
        for enz_id, enz_data in available_enzymes.items():
            if enz_data["campaign_id"] == campaign_id:
                status = "with sequence" if enz_data["has_sequence"] else "without sequence"
                gen_info = f"(gen {enz_data['generation']})" if enz_data["generation"] else ""
                campaign_enzymes.append(f"  - {enz_id} {status} {gen_info}")
        
        if campaign_enzymes:
            context_info.append("Available enzymes in same campaign:")
            context_info.extend(campaign_enzymes[:10])  # Limit to first 10 for context
        
        context_text = "\n".join(context_info)
        
        prompt = f"""
Based on the enzyme information provided, can you identify the parent enzyme for this enzyme?

{context_text}

This enzyme currently has no sequence data and no parent information. Based on the enzyme ID and the available enzymes in the same campaign, can you identify which enzyme is likely the parent?

Please provide your response in this format:
Parent: [parent_enzyme_id or "Unknown"]

If you cannot identify a parent enzyme, just respond with "Parent: Unknown".
"""
        
        try:
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse the response
            parent_match = re.search(r'Parent:\s*([^\n]+)', response_text)
            
            if parent_match:
                parent = parent_match.group(1).strip()
                if parent and parent != "Unknown" and parent != "No parent identified":
                    # Verify the parent exists in our available enzymes
                    if parent in available_enzymes:
                        df.at[entry["idx"], "parent_enzyme_id"] = parent
                        identified_count += 1
                        log.info(f"Identified parent for {enzyme_id}: {parent}")
                    else:
                        log.warning(f"Gemini suggested parent {parent} for {enzyme_id}, but it's not in available enzymes")
            
        except Exception as e:
            log.warning(f"Failed to identify parent for {enzyme_id} from Gemini: {e}")
            continue
    
    if identified_count > 0:
        log.info(f"Successfully identified {identified_count} parent enzymes using Gemini API")
    else:
        log.info("No parent enzymes were identified using Gemini API")
    
    return df

def _plate_and_well(index: int) -> Tuple[int, str, str]:
    """Return (barcode_plate, plate_name, well) for the given running index."""
    plate_number = index // PLATE_SIZE + BARCODE_START
    idx_in_plate = index % PLATE_SIZE
    row = WELL_ROWS[idx_in_plate // 12]
    col = idx_in_plate % 12 + 1
    well = f"{row}{col:02d}"
    plate_name = f"Plate_{plate_number}"
    return plate_number, plate_name, well


def _root_enzyme_id(eid: str, idmap: Dict[str, Dict[str, str]], lineage_roots: Dict[str, str], campaign_id: str = "default") -> str:
    """Get root enzyme id, falling back to generation 0 ancestor or self."""
    if eid in lineage_roots:
        return lineage_roots[eid]
    cur = eid
    seen: set[str] = set()
    while cur and cur not in seen:
        seen.add(cur)
        # Try campaign-specific lookup first, then fall back to composite key
        row = idmap.get(cur, {})
        if not row:
            composite_key = f"{campaign_id}_{cur}"
            row = idmap.get(composite_key, {})
        
        # Look for generation 0 as the root
        if str(row.get("generation", "")).strip() == "0":
            return cur
        parent = row.get("parent_enzyme_id", "")
        if not parent:
            # If no parent, this is the root
            return cur
        cur = parent
    return eid


def _generate_lineage_roots(df: pd.DataFrame) -> Dict[str, str]:
    """Infer lineage roots using generation numbers and simple sequence similarity."""
    # Create idmap, handling missing enzyme_id gracefully
    idmap: Dict[str, Dict[str, str]] = {}
    for _, r in df.iterrows():
        eid = r.get("enzyme_id")
        if pd.isna(eid) or str(eid).strip() == "":
            continue
        idmap[str(eid)] = r
    roots: Dict[str, str] = {}
    # Look for generation 0 as the root
    gen0 = {r["enzyme_id"] for _, r in df.iterrows() 
            if str(r.get("generation", "")).strip() == "0" 
            and not pd.isna(r.get("enzyme_id"))}
    # If no gen0 found, fall back to gen1
    if not gen0:
        gen0 = {r["enzyme_id"] for _, r in df.iterrows() 
                if str(r.get("generation", "")).strip() == "1" 
                and not pd.isna(r.get("enzyme_id"))}

    def _seq_sim(a: str, b: str) -> float:
        if not a or not b:
            return 0.0
        matches = sum(1 for x, y in zip(a, b) if x == y)
        return matches / max(len(a), len(b))

    for _, row in df.iterrows():
        eid = row.get("enzyme_id")
        if pd.isna(eid) or str(eid).strip() == "":
            continue
        if eid in gen0:
            roots[eid] = eid
            continue
        cur = eid
        lineage_path: List[str] = []
        while cur and cur not in lineage_path:
            lineage_path.append(cur)
            cur_row = idmap.get(cur, {})
            parent = cur_row.get("parent_enzyme_id", "")
            if not parent:
                break
            cur = parent
        # If we found a gen0 ancestor in the path, use it
        for anc in reversed(lineage_path):
            if anc in gen0:
                roots[eid] = anc
                break
        else:
            # Fall back to closest by sequence similarity among gen0
            aa_seq = (
                str(row.get("protein_sequence", "")) or str(row.get("aa_sequence", ""))
            )
            best_match = None
            best_sim = 0.0
            for g0 in gen0:
                g0_row = idmap[g0]
                g0_seq = (
                    str(g0_row.get("protein_sequence", ""))
                    or str(g0_row.get("aa_sequence", ""))
                )
                sim = _seq_sim(aa_seq, g0_seq)
                if sim > best_sim:
                    best_sim, best_match = sim, g0
            roots[eid] = best_match if best_match else eid
    return roots


def flatten_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Main public API: returns a DataFrame in the flat output format."""
    log.info(f"Starting flatten_dataframe with {len(df)} input rows")
    log.info(f"Input columns: {list(df.columns)}")
    
    # Apply column aliases to the dataframe
    for alias, canonical in COLUMN_ALIASES.items():
        if alias in df.columns and canonical not in df.columns:
            df = df.rename(columns={alias: canonical})
    
    # Fill missing sequences in substrate scope entries from lineage data
    df = _fill_missing_sequences(df)
    
    # Note: Removed parent identification - we only want exact variant matching
    
    # 1. Generate lineage roots once -----------------------------------------
    lineage_roots = _generate_lineage_roots(df)

    # 2. Precompute SMILES in bulk -------------------------------------------
    all_products: List[str] = []
    all_subs: List[str] = []
    for _, r in df.iterrows():
        rec = VariantRecord(r.to_dict())
        all_products.extend(rec.product_iupac())
        all_subs.extend(rec.substrate_iupac())
    prod_cache = _batch_convert(list(set(all_products)), is_substrate=False)
    sub_cache = _batch_convert(list(set(all_subs)), is_substrate=True)

    # NO CACHING - Comment out cache updates
    # SMILES_CACHE.update(prod_cache)
    # SUBSTRATE_CACHE.update(sub_cache)
    # _save_pickle(SMILES_CACHE, SMILES_CACHE_FILE)
    # _save_pickle(SUBSTRATE_CACHE, SUBSTRATE_CACHE_FILE)

    # 3. Flatten rows ---------------------------------------------------------
    # Create idmap for parent lookups, using campaign_id + enzyme_id as composite key
    idmap = {}
    campaign_idmap = {}  # For within-campaign lookups
    
    for _, r in df.iterrows():
        eid = str(r["enzyme_id"])
        campaign_id = str(r.get("campaign_id", "default"))
        
        # Use composite key for global idmap
        composite_key = f"{campaign_id}_{eid}"
        idmap[composite_key] = r.to_dict()
        
        # Also maintain campaign-specific idmap for parent lookups
        if campaign_id not in campaign_idmap:
            campaign_idmap[campaign_id] = {}
        campaign_idmap[campaign_id][eid] = r.to_dict()
    
    # Check for duplicate enzyme_ids within campaigns
    from collections import defaultdict, Counter
    campaign_enzyme_counts = defaultdict(list)
    for _, r in df.iterrows():
        eid = str(r["enzyme_id"])
        campaign_id = str(r.get("campaign_id", "default"))
        campaign_enzyme_counts[campaign_id].append(eid)
    
    total_duplicates = 0
    for campaign_id, enzyme_ids in campaign_enzyme_counts.items():
        id_counts = Counter(enzyme_ids)
        duplicates = {k: v for k, v in id_counts.items() if v > 1}
        if duplicates:
            total_duplicates += sum(duplicates.values()) - len(duplicates)
            log.warning(f"Campaign {campaign_id} has duplicate enzyme_ids: {duplicates}")
    
    if total_duplicates > 0:
        log.warning(f"Found {total_duplicates} duplicate enzyme_ids across campaigns")
        log.info("All entries within each campaign will be preserved")
    
    output_rows: List[Dict[str, str]] = []
    skipped_count = 0
    processed_count = 0
    
    for idx, (_, row) in enumerate(df.iterrows()):
        rec = VariantRecord(row.to_dict())
        eid = rec.eid

        # Reaction data -------------------------------------------------------
        subs = rec.substrate_iupac()
        prods = rec.product_iupac()
        data_type = rec.row.get("data_type", "")
        
        if not prods:
            # Skip entries without product info unless it's marked as lineage only
            if data_type == "lineage":
                subs, prods = [""], [""]  # placeholders
            else:
                log.info(f"Skipping enzyme_id={eid} (row {idx}) due to missing product data. prods={prods}, data_type={data_type}")
                skipped_count += 1
                continue
        
        # If no substrates but we have products, use empty substrate list
        if not subs:
            log.debug(f"Empty substrate list for enzyme_id={eid}, using empty placeholder")
            subs = [""]

        sub_smiles = [sub_cache.get(s, "") for s in subs]
        prod_smiles = [prod_cache.get(p, "") for p in prods]

        smiles_string = ".".join(prod_smiles)
        smiles_reaction = ".".join(sub_smiles) + " >> " + ".".join(prod_smiles)
        smiles_string = _canonical_smiles(smiles_string)

        # Mutations - calculate based on generation 0 enzyme in same campaign --------
        campaign_id = str(rec.row.get("campaign_id", "default"))
        generation = str(rec.row.get("generation", "")).strip()
        parent_id = rec.parent_id
        
        # Find generation 0 enzyme in same campaign as reference (only for non-gen-0 enzymes)
        reference_row = {}
        if generation != "0":
            for cid, cmap in campaign_idmap.items():
                if cid == campaign_id:
                    # First try to find generation 0
                    for enzyme_id, enzyme_row in cmap.items():
                        enzyme_gen = str(enzyme_row.get("generation", "")).strip()
                        if enzyme_gen == "0" or enzyme_gen == "0.0":
                            reference_row = enzyme_row
                            log.debug(f"Found generation 0 enzyme {enzyme_id} as reference for {eid}")
                            break
                    
                    # If no generation 0 found, find the earliest generation
                    if not reference_row:
                        earliest_gen = float('inf')
                        earliest_enzyme = None
                        for enzyme_id, enzyme_row in cmap.items():
                            try:
                                enzyme_gen = float(str(enzyme_row.get("generation", "")).strip())
                                if enzyme_gen < earliest_gen and enzyme_gen < float(generation):
                                    earliest_gen = enzyme_gen
                                    earliest_enzyme = enzyme_id
                                    reference_row = enzyme_row
                            except (ValueError, AttributeError):
                                continue
                        
                        if reference_row:
                            log.info(f"No generation 0 found in campaign {campaign_id}, using generation {earliest_gen} enzyme {earliest_enzyme} as reference for {eid}")
                        else:
                            log.warning(f"No suitable reference enzyme found in campaign {campaign_id} for {eid}")
                    break
        
        reference_aa = ""
        reference_nt = ""
        if reference_row:
            reference_aa = (
                str(reference_row.get("protein_sequence", ""))
                or str(reference_row.get("aa_sequence", ""))
            )
            reference_nt = (
                str(reference_row.get("nucleotide_sequence", ""))
                or str(reference_row.get("nt_sequence", ""))
            )
            # If reference doesn't have NT sequence but has AA sequence, reverse translate
            if (not reference_nt or reference_nt == "nan") and reference_aa and reference_aa != "nan":
                reference_nt = _rev_translate(reference_aa)
        
        # For generation 0 enzymes, don't calculate mutations (they are the reference)
        if generation == "0":
            aa_muts = ""
            nt_muts = ""
            log.info(f"Generation 0 enzyme {eid} - no mutations calculated (is reference)")
        else:
            # Debug sequence availability
            log.info(f"Mutation calc for {eid}: gen={generation}, has_ref_aa={bool(reference_aa and reference_aa != 'nan')}, has_rec_aa={bool(rec.aa_seq and rec.aa_seq != 'nan')}")
            
            # Calculate mutations relative to generation 0 reference
            aa_muts = _aa_mut(reference_aa, rec.aa_seq) if rec.aa_seq and rec.aa_seq != "nan" and reference_aa and reference_aa != "nan" else ""
            nt_muts = _nt_mut(reference_aa, rec.aa_seq, reference_nt, rec.nt_seq) if (reference_aa and reference_aa != "nan") or (reference_nt and reference_nt != "nan") else ""
            
            if aa_muts or nt_muts:
                log.info(f"Calculated mutations for {eid} relative to generation 0: AA={aa_muts}, NT={nt_muts}")
            else:
                log.warning(f"No mutations calculated for {eid} - ref_aa_len={len(reference_aa) if reference_aa else 0}, rec_aa_len={len(rec.aa_seq) if rec.aa_seq else 0}")

        # Plate / well --------------------------------------------------------
        barcode_plate, plate_name, well = _plate_and_well(idx)

        # Reaction conditions -------------------------------------------------
        cond_parts = []
        for fld in (
            "reaction_temperature",
            "reaction_ph",
            "reaction_other_conditions",
            "reaction_substrate_concentration",
        ):
            if row.get(fld):
                cond_parts.append(f"{fld}:{row[fld]}")
        reaction_condition = ";".join(cond_parts)

        # Cofactor (IUPAC list preferred, fallback plain list) ---------------
        cof_iupac = str(row.get("cofactor_iupac_list", "")).strip()
        cof_list = str(row.get("cofactor_list", "")).strip()
        cofactor = cof_iupac or cof_list

        # Fitness type -------------------------------------------------------
        fitness_type = ""
        if rec.ttn_or_yield() is not None:
            ttn_val = row.get("ttn")
            fitness_type = "ttn" if (ttn_val is not None and pd.notna(ttn_val)) else "yield"
        
        # Additional info -----------------------------------------------------
        extra: Dict[str, str] = {
            k: str(v) for k, v in row.items() if k not in INPUT_REQUIRED + OPTIONAL_INPUT
        }
        # Don't include fitness_type in additional_information since it's now a separate column
        extra.pop("fitness_type", None)
        additional_information = json.dumps(extra, separators=(",", ":")) if extra else ""

        flat = FlatRow(
            id=eid,
            barcode_plate=barcode_plate,
            plate=plate_name,
            well=well,
            smiles_string=smiles_string,
            smiles_reaction=smiles_reaction,
            nucleotide_mutation=nt_muts,
            amino_acid_substitutions=aa_muts,
            nt_sequence=rec.nt_seq,
            aa_sequence=rec.aa_seq,
            fitness_value=rec.ttn_or_yield(),
            fitness_type=fitness_type,
            cofactor=cofactor,
            reaction_condition=reaction_condition,
            ee=str(row.get("ee", "")),
            campaign_id=campaign_id,
            generation=generation,
            parent_enzyme_id=parent_id,
            additional_information=additional_information,
        )
        output_rows.append(flat.as_dict())
        processed_count += 1

    log.info(f"Flattening complete: {processed_count} rows processed, {skipped_count} rows skipped")
    out_df = pd.DataFrame(output_rows, columns=OUTPUT_COLUMNS)
    
    # Post-process: Copy mutations from matched enzymes for Gemini-matched substrate scope entries
    out_df = _copy_mutations_from_matched_enzymes(out_df, df)
    
    return out_df


# === 8. PIPELINE ORCHESTRATOR ======================================================

def run_pipeline(reaction_csv: str | Path | None = None, 
                substrate_scope_csv: str | Path | None = None,
                output_csv: str | Path | None = None) -> pd.DataFrame:
    """Run the pipeline on reaction and/or substrate scope CSV files.
    
    Args:
        reaction_csv: Path to reaction/lineage data CSV (optional)
        substrate_scope_csv: Path to substrate scope data CSV (optional)
        output_csv: Path to write the formatted output CSV
        
    Returns:
        DataFrame with flattened lineage data
    """
    t0 = time.perf_counter()
    
    dfs = []
    
    # Load reaction data if provided
    if reaction_csv:
        df_reaction = pd.read_csv(reaction_csv)
        df_reaction['data_type'] = 'lineage'
        # Handle column aliasing for reaction data
        if 'enzyme' in df_reaction.columns and 'enzyme_id' not in df_reaction.columns:
            df_reaction['enzyme_id'] = df_reaction['enzyme']
        log.info("Loaded %d reaction entries from %s", len(df_reaction), reaction_csv)
        dfs.append(df_reaction)
    
    # Load substrate scope data if provided
    if substrate_scope_csv:
        df_substrate = pd.read_csv(substrate_scope_csv)
        df_substrate['data_type'] = 'substrate_scope'
        log.info("Loaded %d substrate scope entries from %s", len(df_substrate), substrate_scope_csv)
        dfs.append(df_substrate)
    
    if not dfs:
        raise ValueError("At least one input CSV must be provided")
    
    # Combine dataframes without deduplication
    if len(dfs) > 1:
        df_in = pd.concat(dfs, ignore_index=True)
        log.info("Combined data: %d total entries", len(df_in))
    else:
        df_in = dfs[0]

    df_out = flatten_dataframe(df_in)
    log.info("Flattened to %d rows", len(df_out))

    if output_csv:
        df_out.to_csv(output_csv, index=False)
        log.info("Wrote output CSV to %s (%.1f kB)", output_csv, Path(output_csv).stat().st_size / 1024)

    log.info("Pipeline finished in %.2f s", time.perf_counter() - t0)
    return df_out


# === 9. CLI ENTRYPOINT =============================================================

def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="lineage_flattener",
        description="Flatten enzyme lineage CSV into reaction table for automation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("-r", "--reaction", help="Reaction/lineage data CSV file")
    p.add_argument("-s", "--substrate-scope", help="Substrate scope data CSV file")
    p.add_argument("-o", "--output", help="Path to write flattened CSV")
    p.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity (-v, -vv)")
    return p


def main(argv: Optional[List[str]] = None) -> None:
    args = _build_arg_parser().parse_args(argv)
    level = logging.DEBUG if args.verbose and args.verbose > 1 else logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
    
    if not args.reaction and not args.substrate_scope:
        log.error("At least one input file must be provided (--reaction or --substrate-scope)")
        sys.exit(1)
    
    run_pipeline(args.reaction, args.substrate_scope, args.output)


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------- END ---

