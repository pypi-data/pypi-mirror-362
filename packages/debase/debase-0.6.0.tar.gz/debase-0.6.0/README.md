# DEBase

DEBase is a Python package for extracting and analyzing enzyme lineage data from scientific papers using AI-powered parsing.

## Features

- Extract enzyme variant lineages from PDF documents
- Parse protein and DNA sequences with mutation annotations
- Extract reaction performance metrics (yield, TTN, ee)
- Extract and organize substrate scope data
- Match enzyme variants across different data sources using AI
- Generate structured CSV outputs for downstream analysis

## Installation

```bash
pip install debase
```

## Quick Start

```bash
# Run the complete pipeline
debase --manuscript paper.pdf --si supplementary.pdf --output results.csv

# Enable debug mode to save Gemini prompts and responses
debase --manuscript paper.pdf --si supplementary.pdf --output results.csv --debug-dir ./debug_output

# Individual components with debugging
python -m debase.enzyme_lineage_extractor --manuscript paper.pdf --output lineage.csv --debug-dir ./debug_output
python -m debase.reaction_info_extractor --manuscript paper.pdf --lineage-csv lineage.csv --output reactions.csv --debug-dir ./debug_output
python -m debase.substrate_scope_extractor --manuscript paper.pdf --lineage-csv lineage.csv --output substrate_scope.csv --debug-dir ./debug_output
python -m debase.lineage_format -r reactions.csv -s substrate_scope.csv -o final.csv -v
```

## Debugging

Use the `--debug-dir` flag to save all Gemini API prompts and responses for debugging:
- Location extraction prompts
- Sequence extraction prompts (can be very large, up to 150K characters)
- Enzyme matching prompts
- All API responses with timestamps
- Note: lineage_format.py uses `-v` for verbose output instead of `--debug-dir`

## Requirements

- Python 3.8+
- Google Gemini API key (set as GEMINI_API_KEY environment variable)

## Version

0.4.4

## License

MIT License

## Authors

DEBase Team - Caltech

## Contact

ylong@caltech.edu