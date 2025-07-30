"""Utilities for handling campaign information across extractors.

This module provides functions to load and use campaign information
to improve extraction accuracy by providing context about model substrates,
products, and data locations.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


def load_campaigns_from_file(campaign_file: Path) -> List[Dict[str, Any]]:
    """Load campaign information from a JSON file.
    
    Args:
        campaign_file: Path to campaigns.json file
        
    Returns:
        List of campaign dictionaries
    """
    if not campaign_file.exists():
        logger.warning(f"Campaign file not found: {campaign_file}")
        return []
        
    try:
        with open(campaign_file, 'r') as f:
            campaigns = json.load(f)
        logger.info(f"Loaded {len(campaigns)} campaigns from {campaign_file}")
        return campaigns
    except Exception as e:
        logger.error(f"Failed to load campaigns from {campaign_file}: {e}")
        return []


def find_campaign_by_id(campaigns: List[Dict[str, Any]], campaign_id: str) -> Optional[Dict[str, Any]]:
    """Find a specific campaign by ID.
    
    Args:
        campaigns: List of campaign dictionaries
        campaign_id: Campaign ID to search for
        
    Returns:
        Campaign dictionary if found, None otherwise
    """
    for campaign in campaigns:
        if campaign.get('campaign_id') == campaign_id:
            return campaign
    return None


def get_campaign_context(campaign: Dict[str, Any]) -> str:
    """Generate context string for prompts from campaign information.
    
    Args:
        campaign: Campaign dictionary
        
    Returns:
        Formatted context string for inclusion in prompts
    """
    context_parts = []
    
    # Basic campaign info
    context_parts.append(f"Campaign: {campaign.get('campaign_name', 'Unknown')}")
    context_parts.append(f"Description: {campaign.get('description', '')}")
    
    # Model reaction info
    if campaign.get('model_substrate'):
        context_parts.append(f"Model Substrate: {campaign['model_substrate']} (ID: {campaign.get('substrate_id', 'unknown')})")
    if campaign.get('model_product'):
        context_parts.append(f"Model Product: {campaign['model_product']} (ID: {campaign.get('product_id', 'unknown')})")
    
    # Data locations
    if campaign.get('data_locations'):
        locations = ', '.join(campaign['data_locations'])
        context_parts.append(f"Key Data Locations: {locations}")
    
    # Lineage hint if available
    if campaign.get('lineage_hint'):
        context_parts.append(f"Evolution Pathway: {campaign['lineage_hint']}")
    
    # Additional notes
    if campaign.get('notes'):
        context_parts.append(f"Notes: {campaign['notes']}")
    
    return '\n'.join(context_parts)


def get_location_hints_for_campaign(campaign: Dict[str, Any]) -> List[str]:
    """Extract specific location hints from campaign data.
    
    Args:
        campaign: Campaign dictionary
        
    Returns:
        List of location strings (e.g., ["Figure 2a", "Table S4"])
    """
    return campaign.get('data_locations', [])


def enhance_prompt_with_campaign(prompt: str, campaign: Optional[Dict[str, Any]], 
                                 section_name: str = "CAMPAIGN CONTEXT") -> str:
    """Enhance a prompt with campaign context information.
    
    Args:
        prompt: Original prompt
        campaign: Campaign dictionary (optional)
        section_name: Section header for the campaign context
        
    Returns:
        Enhanced prompt with campaign context
    """
    if not campaign:
        return prompt
    
    context = get_campaign_context(campaign)
    locations = get_location_hints_for_campaign(campaign)
    
    campaign_section = f"\n\n{section_name}:\n{'-' * 50}\n{context}"
    
    if locations:
        campaign_section += f"\n\nIMPORTANT: Focus particularly on these locations: {', '.join(locations)}"
    
    campaign_section += f"\n{'-' * 50}\n"
    
    # Insert campaign context early in the prompt
    # Look for a good insertion point after initial instructions
    lines = prompt.split('\n')
    insert_idx = 0
    
    # Find a good place to insert (after first paragraph or instruction block)
    for i, line in enumerate(lines):
        if i > 5 and (not line.strip() or line.startswith('Given') or line.startswith('You')):
            insert_idx = i
            break
    
    if insert_idx == 0:
        # Fallback: just prepend
        return campaign_section + prompt
    else:
        # Insert at found position
        lines.insert(insert_idx, campaign_section)
        return '\n'.join(lines)