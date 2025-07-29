#!/usr/bin/env python3
"""
Command-line interface for llama-text2sql-eval
"""

import argparse
import os
import sys
from typing import Optional

from .main_module import LlamaText2SQLEval


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Llama Text2SQL Evaluation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  llama-text2sql-eval --model Llama-3.3-70B-Instruct
  llama-text2sql-eval --model Llama-3.3-8B-Instruct --no-knowledge
  llama-text2sql-eval --model Llama-3.3-70B-Instruct --num-cpus 4 --timeout 60
  llama-text2sql-eval --model Llama-3.3-70B-Instruct --skip-generation
        """,
    )

    # Required arguments
    parser.add_argument(
        "--model",
        required=True,
        help="Llama model to use for evaluation (e.g., Llama-3.3-70B-Instruct)",
    )

    # Optional arguments
    parser.add_argument(
        "--api-key",
        help="Llama API key (if not provided, will use LLAMA_API_KEY environment variable)",
    )

    parser.add_argument(
        "--eval-path",
        default="data/dev_20240627/dev.json",
        help="Path to the evaluation JSON file (default: data/dev_20240627/dev.json)",
    )

    parser.add_argument(
        "--db-root-path",
        default="data/dev_20240627/dev_databases/",
        help="Path to the database root directory (default: data/dev_20240627/dev_databases/)",
    )

    parser.add_argument(
        "--ground-truth-path",
        default="data/",
        help="Path to the ground truth data (default: data/)",
    )

    parser.add_argument(
        "--output-base-path",
        default="output/",
        help="Base path for output files (default: output/)",
    )

    parser.add_argument(
        "--no-knowledge", action="store_true", help="Disable use of external knowledge"
    )

    parser.add_argument(
        "--mode",
        default="dev",
        choices=["dev", "test"],
        help="Evaluation mode (default: dev)",
    )

    parser.add_argument(
        "--num-cpus",
        type=int,
        default=1,
        help="Number of CPUs for parallel processing (default: 1)",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Timeout for SQL execution in seconds (default: 30.0)",
    )

    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Skip generation and only run evaluation (useful if predictions already exist)",
    )

    parser.add_argument(
        "--list-models", action="store_true", help="List supported models and exit"
    )

    args = parser.parse_args()

    # Handle list models
    if args.list_models:
        evaluator = LlamaText2SQLEval()
        models = evaluator.get_supported_models()
        print("Supported models:")
        for category, model_list in models.items():
            print(f"\n{category.upper()}:")
            for model in model_list:
                print(f"  - {model}")
        return 0

    # Get API key
    api_key = args.api_key or os.getenv("LLAMA_API_KEY")
    if not api_key:
        print(
            "Error: API key not provided. Use --api-key or set LLAMA_API_KEY environment variable."
        )
        return 1

    # Validate data paths
    if not args.skip_generation:
        if not os.path.exists(args.eval_path):
            print(f"Error: Evaluation file not found: {args.eval_path}")
            print(
                "Please download the BIRD dataset first. See README.md for instructions."
            )
            return 1

        if not os.path.exists(args.db_root_path):
            print(f"Error: Database root path not found: {args.db_root_path}")
            print(
                "Please download the BIRD dataset first. See README.md for instructions."
            )
            return 1

    # Initialize evaluator
    try:
        evaluator = LlamaText2SQLEval(
            eval_path=args.eval_path,
            db_root_path=args.db_root_path,
            ground_truth_path=args.ground_truth_path,
            output_base_path=args.output_base_path,
        )
    except Exception as e:
        print(f"Error initializing evaluator: {e}")
        return 1

    # Run evaluation
    print(f"Starting evaluation with model: {args.model}")
    print(f"Using knowledge: {not args.no_knowledge}")
    print(f"Mode: {args.mode}")
    print(f"CPUs: {args.num_cpus}")
    print(f"Timeout: {args.timeout}s")
    print(f"Skip generation: {args.skip_generation}")
    print("-" * 50)

    try:
        results = evaluator.run(
            model=args.model,
            api_key=api_key,
            use_knowledge=not args.no_knowledge,
            mode=args.mode,
            num_cpus=args.num_cpus,
            meta_time_out=args.timeout,
            skip_generation=args.skip_generation,
        )

        if results:
            print("\n" + "=" * 50)
            print("FINAL RESULTS")
            print("=" * 50)
            print(f"Overall Accuracy: {results['overall_accuracy']:.2f}%")
            print(f"Simple: {results['simple_accuracy']:.2f}%")
            print(f"Moderate: {results['moderate_accuracy']:.2f}%")
            print(f"Challenging: {results['challenging_accuracy']:.2f}%")
            print("\nCounts:")
            counts = results.get("counts", {})
            print(f"Simple: {counts.get('simple', 'N/A')}")
            print(f"Moderate: {counts.get('moderate', 'N/A')}")
            print(f"Challenging: {counts.get('challenging', 'N/A')}")
            print(f"Total: {counts.get('total', 'N/A')}")
            return 0
        else:
            print("Error: Evaluation failed.")
            return 1

    except KeyboardInterrupt:
        print("\nEvaluation interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error during evaluation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
