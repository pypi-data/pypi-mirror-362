#!/usr/bin/env python3
"""
Enzyme Analysis Pipeline Wrapper (Clean Version)

Pipeline flow:
1. enzyme_lineage_extractor.py - Extract enzyme data from PDFs
2. cleanup_sequence.py - Clean and validate protein sequences
3. reaction_info_extractor.py - Extract reaction performance metrics
4. substrate_scope_extractor.py - Extract substrate scope data (runs independently)
5. lineage_format.py - Format and merge all data into final CSV

The reaction_info and substrate_scope extractors run in parallel,
then their outputs are combined in lineage_format.
"""
import os
import sys
import argparse
import logging
import time
from datetime import datetime
from pathlib import Path
import threading

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EnzymePipeline")

# Global token tracking
_token_lock = threading.Lock()
_token_usage = {
    'total_input_tokens': 0,
    'total_output_tokens': 0,
    'calls_by_module': {
        'enzyme_lineage_extractor': {'input': 0, 'output': 0, 'calls': 0},
        'reaction_info_extractor': {'input': 0, 'output': 0, 'calls': 0},
        'substrate_scope_extractor': {'input': 0, 'output': 0, 'calls': 0}
    }
}

def add_token_usage(module_name: str, input_tokens: int, output_tokens: int):
    """Add token usage from a module to the global tracking."""
    with _token_lock:
        _token_usage['total_input_tokens'] += input_tokens
        _token_usage['total_output_tokens'] += output_tokens
        if module_name in _token_usage['calls_by_module']:
            _token_usage['calls_by_module'][module_name]['input'] += input_tokens
            _token_usage['calls_by_module'][module_name]['output'] += output_tokens
            _token_usage['calls_by_module'][module_name]['calls'] += 1

def calculate_token_usage_and_cost():
    """Calculate total token usage and estimated cost for Gemini 2.5 Flash."""
    with _token_lock:
        total_input = _token_usage['total_input_tokens']
        total_output = _token_usage['total_output_tokens']
        
        # Gemini 2.5 Flash pricing (as of 2025)
        # Input: $0.30 per 1M tokens
        # Output: $2.50 per 1M tokens  
        input_cost = (total_input / 1_000_000) * 0.30
        output_cost = (total_output / 1_000_000) * 2.50
        total_cost = input_cost + output_cost
        
        return total_input, total_output, total_cost

def reset_token_usage():
    """Reset token usage counters."""
    with _token_lock:
        _token_usage['total_input_tokens'] = 0
        _token_usage['total_output_tokens'] = 0
        for module_data in _token_usage['calls_by_module'].values():
            module_data['input'] = 0
            module_data['output'] = 0
            module_data['calls'] = 0

def save_token_usage_to_csv(manuscript_path: Path, input_tokens: int, output_tokens: int, cost: float, runtime: float, output_dir: Path):
    """Save token usage and cost to CSV with naming format: price_manuscriptname.csv"""
    import pandas as pd
    
    # Create filename: price_manuscriptname.csv
    manuscript_name = manuscript_path.stem.replace(' ', '_').replace('-', '_')
    csv_filename = f"price_{manuscript_name}.csv"
    csv_path = output_dir / csv_filename
    
    # Prepare the data
    data = {
        'manuscript_name': [manuscript_name],
        'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'input_tokens': [input_tokens],
        'output_tokens': [output_tokens],
        'total_tokens': [input_tokens + output_tokens],
        'estimated_cost_usd': [cost],
        'runtime_seconds': [runtime]
    }
    
    # Add module breakdown
    with _token_lock:
        for module_name, usage in _token_usage['calls_by_module'].items():
            if usage['calls'] > 0:
                data[f'{module_name}_calls'] = [usage['calls']]
                data[f'{module_name}_input_tokens'] = [usage['input']]
                data[f'{module_name}_output_tokens'] = [usage['output']]
                module_cost = (usage['input'] / 1_000_000) * 0.30 + (usage['output'] / 1_000_000) * 2.50
                data[f'{module_name}_cost_usd'] = [module_cost]
            else:
                data[f'{module_name}_calls'] = [0]
                data[f'{module_name}_input_tokens'] = [0]
                data[f'{module_name}_output_tokens'] = [0]
                data[f'{module_name}_cost_usd'] = [0.0]
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    
    logger.info(f"Token usage saved to: {csv_path}")
    return csv_path


def run_lineage_extraction(manuscript: Path, si: Path, output: Path, debug_dir: Path = None) -> Path:
    """
    Step 1: Extract enzyme lineage data from PDFs
    Calls: enzyme_lineage_extractor.py
    """
    logger.info(f"Extracting enzyme lineage from {manuscript.name}")
    
    from .enzyme_lineage_extractor import run_pipeline
    run_pipeline(manuscript=manuscript, si=si, output_csv=output, debug_dir=debug_dir)
    
    logger.info(f"Lineage extraction complete: {output}")
    return output


def run_sequence_cleanup(input_csv: Path, output_csv: Path) -> Path:
    """
    Step 2: Clean and validate protein sequences
    Calls: cleanup_sequence.py
    Returns output path even if cleanup fails (copies input file)
    """
    logger.info(f"Cleaning sequences from {input_csv.name}")
    
    try:
        from .cleanup_sequence import main as cleanup_sequences
        cleanup_sequences([str(input_csv), str(output_csv)])
        
        logger.info(f"Sequence cleanup complete: {output_csv}")
        return output_csv
        
    except Exception as e:
        logger.warning(f"Sequence cleanup failed: {e}")
        logger.info("Copying original file to continue pipeline...")
        
        # Copy the input file as-is to continue pipeline
        import shutil
        shutil.copy2(input_csv, output_csv)
        
        logger.info(f"Original file copied: {output_csv}")
        return output_csv


def run_reaction_extraction(manuscript: Path, si: Path, lineage_csv: Path, output: Path, debug_dir: Path = None) -> Path:
    """
    Step 3a: Extract reaction performance metrics
    Calls: reaction_info_extractor.py main function to get full functionality including campaign CSV saving
    Returns output path even if extraction fails (creates empty file)
    """
    logger.info(f"Extracting reaction info for enzymes in {lineage_csv.name}")
    
    try:
        import sys
        
        # Call reaction_info_extractor.main() directly in same process for token tracking
        old_argv = sys.argv
        sys.argv = [
            "reaction_info_extractor",
            "--manuscript", str(manuscript),
            "--lineage-csv", str(lineage_csv),
            "--output", str(output)
        ]
        
        # Add optional arguments
        if si:
            sys.argv.extend(["--si", str(si)])
        if debug_dir:
            sys.argv.extend(["--debug-dir", str(debug_dir)])
        
        # Import and call main() directly
        from .reaction_info_extractor import main
        main()
        
        # Restore original argv
        sys.argv = old_argv
        
        logger.info(f"Reaction extraction complete: {output}")
        return output
        
    except Exception as e:
        logger.warning(f"Reaction extraction failed: {e}")
        logger.info("Creating empty reaction info file to continue pipeline...")
        
        # Create empty reaction CSV with basic columns
        import pandas as pd
        empty_df = pd.DataFrame(columns=[
            'enzyme', 'substrate', 'product', 'yield_percent', 'ee_percent',
            'conversion_percent', 'reaction_type', 'reaction_conditions', 'notes'
        ])
        empty_df.to_csv(output, index=False)
        
        logger.info(f"Empty reaction file created: {output}")
        return output
        
    except Exception as e:
        logger.warning(f"Reaction extraction failed: {e}")
        logger.info("Creating empty reaction info file to continue pipeline...")
        
        # Create empty reaction CSV with basic columns
        import pandas as pd
        empty_df = pd.DataFrame(columns=[
            'enzyme', 'substrate', 'product', 'yield_percent', 'ee_percent',
            'conversion_percent', 'reaction_type', 'reaction_conditions', 'notes'
        ])
        empty_df.to_csv(output, index=False)
        
        logger.info(f"Empty reaction file created: {output}")
        return output


def run_substrate_scope_extraction(manuscript: Path, si: Path, lineage_csv: Path, output: Path, debug_dir: Path = None) -> Path:
    """
    Step 3b: Extract substrate scope data (runs in parallel with reaction extraction)
    Calls: substrate_scope_extractor.py
    Returns output path even if extraction fails (creates empty file)
    """
    logger.info(f"Extracting substrate scope for enzymes in {lineage_csv.name}")
    
    try:
        from .substrate_scope_extractor import run_pipeline
        
        # Run substrate scope extraction
        run_pipeline(
            manuscript=manuscript,
            si=si,
            lineage_csv=lineage_csv,
            output_csv=output,
            debug_dir=debug_dir
        )
        
        logger.info(f"Substrate scope extraction complete: {output}")
        return output
        
    except Exception as e:
        logger.warning(f"Substrate scope extraction failed: {e}")
        logger.info("Creating empty substrate scope file to continue pipeline...")
        
        # Create empty substrate scope CSV with proper headers
        import pandas as pd
        empty_df = pd.DataFrame(columns=[
            'enzyme', 'substrate', 'product', 'yield_percent', 'ee_percent', 
            'conversion_percent', 'selectivity', 'reaction_conditions', 'notes'
        ])
        empty_df.to_csv(output, index=False)
        
        logger.info(f"Empty substrate scope file created: {output}")
        return output


def match_enzyme_variants_with_gemini(lineage_enzymes: list, data_enzymes: list, model=None) -> dict:
    """
    Use Gemini to match enzyme variant IDs between different datasets.
    Returns a mapping of data_enzyme_id -> lineage_enzyme_id.
    """
    import json
    
    if not model:
        try:
            from .enzyme_lineage_extractor import get_model
            model = get_model()
        except:
            logger.warning("Could not load Gemini model for variant matching")
            return {}
    
    prompt = f"""Match enzyme variant IDs between two lists from the same scientific paper.

These lists come from different sections or analyses of the same study, but may use different naming conventions.

List 1 (from lineage/sequence data):
{json.dumps(lineage_enzymes)}

List 2 (from experimental data):
{json.dumps(data_enzymes)}

Analyze the patterns and match variants that refer to the same enzyme.
Return ONLY a JSON object mapping IDs from List 2 to their corresponding IDs in List 1.
Format: {{"list2_id": "list1_id", ...}}
Only include matches you are confident about based on the naming patterns.
"""
    
    try:
        response = model.generate_content(prompt)
        mapping_text = response.text.strip()
        
        # Extract JSON from response
        if '```json' in mapping_text:
            mapping_text = mapping_text.split('```json')[1].split('```')[0].strip()
        elif '```' in mapping_text:
            mapping_text = mapping_text.split('```')[1].split('```')[0].strip()
        
        mapping = json.loads(mapping_text)
        logger.info(f"Gemini matched {len(mapping)} enzyme variants")
        for k, v in mapping.items():
            logger.info(f"  Matched '{k}' -> '{v}'")
        return mapping
    except Exception as e:
        logger.warning(f"Failed to match variants with Gemini: {e}")
        return {}


def run_lineage_format(reaction_csv: Path, substrate_scope_csv: Path, cleaned_csv: Path, output_csv: Path) -> Path:
    """
    Step 4: Format and merge all data into final CSV
    Uses lineage_format module to normalize data, convert IUPAC to SMILES, fill missing sequences,
    and create the plate format output
    """
    logger.info(f"Formatting and merging data into final plate format output")
    
    try:
        from . import lineage_format
        import pandas as pd
        
        # Check which files have data
        has_reaction_data = False
        has_scope_data = False
        
        try:
            df_reaction = pd.read_csv(reaction_csv)
            has_reaction_data = len(df_reaction) > 0
            logger.info(f"Reaction data has {len(df_reaction)} entries")
        except Exception as e:
            logger.info(f"No reaction data available: {e}")
            
        try:
            df_scope = pd.read_csv(substrate_scope_csv)
            has_scope_data = len(df_scope) > 0
            logger.info(f"Substrate scope data has {len(df_scope)} entries")
        except Exception as e:
            logger.info(f"No substrate scope data available: {e}")
        
        # Use lineage_format's run_pipeline to process the data
        logger.info("Running lineage format pipeline to create plate format...")
        
        # The lineage_format expects string paths
        reaction_path = str(reaction_csv) if has_reaction_data else None
        scope_path = str(substrate_scope_csv) if has_scope_data else None
        
        # If neither file has data, just copy the cleaned file
        if not has_reaction_data and not has_scope_data:
            logger.warning("No data to process in either reaction or substrate scope files")
            import shutil
            shutil.copy2(cleaned_csv, output_csv)
            return output_csv
        
        # Call lineage_format's run_pipeline function
        # This will handle all the processing including:
        # - Merging reaction and substrate scope data
        # - Filling missing sequences
        # - Converting IUPAC names to SMILES
        # - Creating the flattened plate format
        logger.info("Calling lineage_format.run_pipeline...")
        
        # Run the pipeline and get the formatted dataframe
        df = lineage_format.run_pipeline(
            reaction_csv=reaction_path,
            substrate_scope_csv=scope_path,
            output_csv=str(output_csv)
        )
        
        logger.info(f"Lineage format pipeline completed successfully")
        logger.info(f"Final output saved to: {output_csv}")
        logger.info(f"Output contains {len(df)} rows in plate format (flattened)")
        
        # Log column summary
        key_columns = ['enzyme_id', 'substrate', 'product', 'yield', 'ee', 'ttn', 
                      'substrate_smiles', 'product_smiles', 'protein_sequence']
        available_columns = [col for col in key_columns if col in df.columns]
        logger.info(f"Key columns in output: {', '.join(available_columns)}")
        
        return output_csv
        
    except Exception as e:
        logger.warning(f"Lineage formatting failed: {e}")
        logger.info("Falling back to simple concatenation...")
        
        # Fallback to simple concatenation
        import pandas as pd
        dfs = []
        
        try:
            df_reaction = pd.read_csv(reaction_csv)
            if len(df_reaction) > 0:
                dfs.append(df_reaction)
        except:
            pass
            
        try:
            df_scope = pd.read_csv(substrate_scope_csv)
            if len(df_scope) > 0:
                dfs.append(df_scope)
        except:
            pass
        
        if dfs:
            df_final = pd.concat(dfs, ignore_index=True)
            df_final.to_csv(output_csv, index=False)
        else:
            import shutil
            shutil.copy2(cleaned_csv, output_csv)
        
        logger.info(f"Fallback output saved to: {output_csv}")
        return output_csv


def run_pipeline(
    manuscript_path: Path,
    si_path: Path = None,
    output_path: Path = None,
    keep_intermediates: bool = False,
    debug_dir: Path = None
) -> Path:
    """Run the complete enzyme analysis pipeline."""
    # Setup paths
    manuscript_path = Path(manuscript_path)
    si_path = Path(si_path) if si_path else None
    
    # Create output filename based on manuscript
    if not output_path:
        output_name = manuscript_path.stem.replace(' ', '_')
        output_path = Path(f"{output_name}_debase.csv")
    else:
        output_path = Path(output_path)
    
    # Use the output directory for all files
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define intermediate file paths (all in the same directory as output)
    lineage_csv = output_dir / "enzyme_lineage_data.csv"  # This is what enzyme_lineage_extractor actually outputs
    cleaned_csv = output_dir / "2_enzyme_sequences.csv"
    reaction_csv = output_dir / "3a_reaction_info.csv"
    substrate_csv = output_dir / "3b_substrate_scope.csv"
    
    # Setup file logging
    log_file = output_dir / f"debase_pipeline_{time.strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure logging to both file and console
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add file handler to root logger and all module loggers
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # Also add to module-specific loggers
    for module_name in ['debase.enzyme_lineage_extractor', 'debase.cleanup_sequence', 
                        'debase.reaction_info_extractor', 'debase.substrate_scope_extractor', 
                        'debase.lineage_format', 'debase.wrapper']:
        module_logger = logging.getLogger(module_name)
        module_logger.addHandler(file_handler)
    
    try:
        # Reset token usage tracking for this pipeline run
        reset_token_usage()
        
        logger.info("="*60)
        logger.info("Starting DEBase Enzyme Analysis Pipeline")
        logger.info(f"Manuscript: {manuscript_path}")
        logger.info(f"SI: {si_path if si_path else 'None'}")
        logger.info(f"Output: {output_path}")
        logger.info(f"Log file: {log_file}")
        logger.info("="*60)
        
        start_time = time.time()
        
        # Step 1: Extract enzyme lineage
        logger.info("\n[Step 1/5] Extracting enzyme lineage...")
        run_lineage_extraction(manuscript_path, si_path, lineage_csv, debug_dir=debug_dir)
        
        # Step 2: Clean sequences
        logger.info("\n[Step 2/5] Cleaning sequences...")
        run_sequence_cleanup(lineage_csv, cleaned_csv)
        
        # Step 3: Extract reaction and substrate scope in parallel
        logger.info("\n[Step 3/5] Extracting reaction info and substrate scope...")
        
        # Run reaction extraction
        logger.info("  - Extracting reaction metrics...")
        run_reaction_extraction(manuscript_path, si_path, cleaned_csv, reaction_csv, debug_dir=debug_dir)
        
        # Add small delay to avoid API rate limits
        time.sleep(2)
        
        # Run substrate scope extraction
        logger.info("  - Extracting substrate scope...")
        run_substrate_scope_extraction(manuscript_path, si_path, cleaned_csv, substrate_csv, debug_dir=debug_dir)
        
        # Step 4: Format and merge
        logger.info("\n[Step 4/5] Formatting and merging data...")
        final_output = run_lineage_format(reaction_csv, substrate_csv, cleaned_csv, output_path)
        
        # Step 5: Finalize
        logger.info("\n[Step 5/5] Finalizing...")
        elapsed = time.time() - start_time
        
        if keep_intermediates:
            logger.info(f"All intermediate files saved in: {output_dir}")
        else:
            logger.info("Note: Use --keep-intermediates to save intermediate files")
        
        # Calculate token usage and estimated costs
        total_input_tokens, total_output_tokens, estimated_cost = calculate_token_usage_and_cost()
        
        # Save token usage to CSV file
        save_token_usage_to_csv(manuscript_path, total_input_tokens, total_output_tokens, estimated_cost, elapsed, output_dir)
        
        logger.info("\n" + "="*60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info(f"Comprehensive output: {output_path}")
        if final_output != output_path:
            logger.info(f"Plate-based output: {final_output}")
        logger.info(f"Runtime: {elapsed:.1f} seconds")
        logger.info("")
        logger.info("TOKEN USAGE & COST ESTIMATE:")
        logger.info(f"  Input tokens:  {total_input_tokens:,}")
        logger.info(f"  Output tokens: {total_output_tokens:,}")
        logger.info(f"  Total tokens:  {total_input_tokens + total_output_tokens:,}")
        logger.info(f"  Estimated cost: ${estimated_cost:.4f} USD")
        logger.info("  (Based on Gemini 2.5 Flash pricing: $0.30/1M input, $2.50/1M output)")
        logger.info("")
        
        # Show breakdown by module
        with _token_lock:
            logger.info("BREAKDOWN BY MODULE:")
            for module_name, usage in _token_usage['calls_by_module'].items():
                if usage['calls'] > 0:
                    logger.info(f"  {module_name}:")
                    logger.info(f"    API calls: {usage['calls']}")
                    logger.info(f"    Input tokens: {usage['input']:,}")
                    logger.info(f"    Output tokens: {usage['output']:,}")
                    module_cost = (usage['input'] / 1_000_000) * 0.30 + (usage['output'] / 1_000_000) * 2.50
                    logger.info(f"    Module cost: ${module_cost:.4f} USD")
        
        logger.info("="*60)
        
        return final_output
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise
    finally:
        # Clean up file handler
        file_handler.close()
        root_logger.removeHandler(file_handler)
        for module_name in ['debase.enzyme_lineage_extractor', 'debase.cleanup_sequence', 
                            'debase.reaction_info_extractor', 'debase.substrate_scope_extractor', 
                            'debase.lineage_format', 'debase.wrapper']:
            module_logger = logging.getLogger(module_name)
            module_logger.removeHandler(file_handler)
    

def main():
    parser = argparse.ArgumentParser(
        description='DEBase Enzyme Analysis Pipeline - Extract enzyme data from chemistry papers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline steps:
  1. enzyme_lineage_extractor - Extract enzyme variants from PDFs
  2. cleanup_sequence - Validate and clean protein sequences  
  3. reaction_info_extractor - Extract reaction performance metrics
  4. substrate_scope_extractor - Extract substrate scope data
  5. lineage_format - Format and merge into final CSV

The pipeline automatically handles all steps sequentially.
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--manuscript',
        type=Path,
        help='Path to manuscript PDF'
    )
    
    # Optional arguments
    parser.add_argument(
        '--si',
        type=Path,
        help='Path to supplementary information PDF'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output CSV path (default: manuscript_name_debase.csv)'
    )
    parser.add_argument(
        '--keep-intermediates',
        action='store_true',
        help='Keep intermediate files for debugging'
    )
    parser.add_argument(
        '--debug-dir',
        type=Path,
        help='Directory for debug output (prompts, API responses)'
    )
    
    args = parser.parse_args()
    
    # Check inputs
    if not args.manuscript.exists():
        parser.error(f"Manuscript not found: {args.manuscript}")
    if args.si and not args.si.exists():
        parser.error(f"SI not found: {args.si}")
    
    # Run pipeline
    try:
        run_pipeline(
            manuscript_path=args.manuscript,
            si_path=args.si,
            output_path=args.output,
            keep_intermediates=args.keep_intermediates,
            debug_dir=args.debug_dir
        )
    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()