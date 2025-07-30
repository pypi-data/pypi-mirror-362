"""Universal caption pattern for all DEBase extractors.

This module provides a consistent caption pattern that handles various
formats found in scientific papers, including:
- Standard formats: Figure 1, Fig. 1, Table 1
- Supplementary formats: Supplementary Figure 1, Supp. Table 1
- Extended data: Extended Data Figure 1, ED Fig. 1
- Other types: Scheme 1, Chart 1
- Page headers: S14 Table 5
- Various punctuation: Figure 1. Figure 1: Figure 1 |
"""

import re

# Universal caption pattern that handles all common formats
UNIVERSAL_CAPTION_PATTERN = re.compile(
    r"""
    ^                                      # Start of line
    [^\n]{0,20}?                          # Up to 20 chars of any content (page headers, etc.)
    (                                      # Start capture group
        (?:Extended\s+Data\s+)?           # Optional "Extended Data" prefix
        (?:ED\s+)?                        # Optional "ED" prefix
        (?:Supplementary|Supp\.?|Suppl\.?)?\s*  # Optional supplementary prefixes
        (?:Table|Fig(?:ure)?|Scheme|Chart)      # Main caption types
    )                                      # End capture group
    (?:                                    # Non-capturing group for what follows
        \s*                               # Optional whitespace
        (?:S?\d+[A-Za-z]?|[IVX]+)        # Number (with optional S prefix or roman)
        (?:[.:|]|\s+\|)?                  # Optional punctuation (. : or |)
    |                                      # OR
        \.                                # Just a period (for "Fig." without number)
    )
    """,
    re.I | re.X | re.M
)

def get_universal_caption_pattern():
    """Get the universal caption pattern for use in extractors."""
    return UNIVERSAL_CAPTION_PATTERN