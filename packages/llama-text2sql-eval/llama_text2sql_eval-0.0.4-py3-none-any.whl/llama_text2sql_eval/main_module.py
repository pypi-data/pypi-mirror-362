import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .llama_text2sql import (
    collect_response_from_llama,
    decouple_question_schema,
    generate_sql_file,
)
from .text2sql_eval import (
    compute_acc_by_diff,
    package_sqls,
    print_data,
    run_sqls_parallel,
    sort_results,
)


class LlamaText2SQLEval:
    """
    A library that implements the functionality of llama_eval.sh for text-to-SQL evaluation.
    """

    def __init__(
        self,
        eval_path: str = "data/dev_20240627/dev.json",
        db_root_path: str = "data/dev_20240627/dev_databases/",
        ground_truth_path: str = "data/",
        output_base_path: str = "output/",
    ):
        """
        Initialize the LlamaText2SQLEval class.

        Args:
            eval_path: Path to the evaluation JSON file
            db_root_path: Path to the database root directory
            ground_truth_path: Path to the ground truth data
            output_base_path: Base path for output files
        """
        self.eval_path = eval_path
        self.db_root_path = db_root_path
        self.ground_truth_path = ground_truth_path
        self.output_base_path = output_base_path

    def _create_output_directory(self, model: str) -> str:
        """Create output directory for the model."""
        output_path = os.path.join(self.output_base_path, model)
        os.makedirs(output_path, exist_ok=True)
        return output_path

    def _run_text2sql_generation(
        self,
        api_key: str,
        model: str,
        output_path: str,
        use_knowledge: bool = True,
        mode: str = "dev",
    ) -> bool:
        """
        Run the text2sql generation process.

        Args:
            api_key: API key for the model
            model: Model name/identifier
            output_path: Path to save output files
            use_knowledge: Whether to use external knowledge
            mode: Evaluation mode (dev/test)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load evaluation data
            with open(self.eval_path, "r") as f:
                eval_data = json.load(f)

            # Decouple questions and schemas
            question_list, db_path_list, knowledge_list = decouple_question_schema(
                datasets=eval_data, db_root_path=self.db_root_path
            )

            # Collect responses from Llama
            if use_knowledge:
                responses = collect_response_from_llama(
                    db_path_list=db_path_list,
                    question_list=question_list,
                    api_key=api_key,
                    model=model,
                    knowledge_list=knowledge_list,
                )
            else:
                responses = collect_response_from_llama(
                    db_path_list=db_path_list,
                    question_list=question_list,
                    api_key=api_key,
                    model=model,
                    knowledge_list=None,
                )

            # Generate SQL file
            output_file = os.path.join(output_path, f"predict_{mode}.json")
            generate_sql_file(sql_lst=responses, output_path=output_file)

            print(f"Successfully collected results from {model}")
            return True

        except Exception as e:
            print(f"Error in text2sql generation: {e}")
            return False

    def _run_evaluation(
        self,
        output_path: str,
        mode: str = "dev",
        num_cpus: int = 1,
        meta_time_out: float = 30.0,
    ) -> Dict:
        """
        Run the evaluation process.

        Args:
            output_path: Path containing the prediction files
            mode: Evaluation mode (dev/test)
            num_cpus: Number of CPUs for parallel processing
            meta_time_out: Timeout for SQL execution

        Returns:
            Dict: Evaluation results
        """
        try:
            exec_result = []

            # Package predicted SQLs
            pred_queries, db_paths = package_sqls(
                output_path + "/",
                self.db_root_path,
                mode="gpt",
                data_mode=mode,
            )

            # Package ground truth SQLs
            gt_queries, db_paths_gt = package_sqls(
                self.ground_truth_path, self.db_root_path, mode="gt", data_mode=mode
            )

            # Create query pairs
            query_pairs = list(zip(pred_queries, gt_queries))

            # Run evaluation in parallel
            import multiprocessing as mp

            def result_callback(result):
                exec_result.append(result)

            from .text2sql_eval import execute_model

            pool = mp.Pool(processes=num_cpus)
            for i, sql_pair in enumerate(query_pairs):
                predicted_sql, ground_truth = sql_pair
                pool.apply_async(
                    execute_model,
                    args=(predicted_sql, ground_truth, db_paths[i], i, meta_time_out),
                    callback=result_callback,
                )
            pool.close()
            pool.join()

            # Sort results
            exec_result = sort_results(exec_result)

            # Compute accuracy by difficulty
            simple_acc, moderate_acc, challenging_acc, acc, count_lists = (
                compute_acc_by_diff(exec_result, self.eval_path)
            )

            score_lists = [simple_acc, moderate_acc, challenging_acc, acc]

            # Print results
            print("Evaluating statistics...")
            print_data(score_lists, count_lists)
            print("=" * 87)

            return {
                "simple_accuracy": simple_acc,
                "moderate_accuracy": moderate_acc,
                "challenging_accuracy": challenging_acc,
                "overall_accuracy": acc,
                "counts": {
                    "simple": count_lists[0],
                    "moderate": count_lists[1],
                    "challenging": count_lists[2],
                    "total": count_lists[3],
                },
                "detailed_results": exec_result,
            }

        except Exception as e:
            print(f"Error in evaluation: {e}")
            return {}

    def run(
        self,
        model: str,
        api_key: str,
        use_knowledge: bool = True,
        mode: str = "dev",
        num_cpus: int = 1,
        meta_time_out: float = 30.0,
        skip_generation: bool = False,
    ) -> Dict:
        """
        Run the complete text2sql evaluation pipeline.

        Args:
            model: Model name/identifier
            api_key: API key for the model
            use_knowledge: Whether to use external knowledge
            mode: Evaluation mode (dev/test)
            num_cpus: Number of CPUs for parallel processing
            meta_time_out: Timeout for SQL execution
            skip_generation: Skip generation and only run evaluation

        Returns:
            Dict: Evaluation results including accuracies and detailed results
        """
        print(f"Text2SQL using {model}")

        # Create output directory
        output_path = self._create_output_directory(model)

        if not skip_generation:
            # Run text2sql generation
            success = self._run_text2sql_generation(
                api_key=api_key,
                model=model,
                output_path=output_path,
                use_knowledge=use_knowledge,
                mode=mode,
            )

            if not success:
                print(f"Error: text2sql generation failed. Skipping evaluation.")
                return {}

        # Run evaluation
        print("Generation completed successfully. Proceeding with evaluation...")
        results = self._run_evaluation(
            output_path=output_path,
            mode=mode,
            num_cpus=num_cpus,
            meta_time_out=meta_time_out,
        )

        if results:
            print(f"Done evaluating {model}.")

        return results

    def run_with_config(self, config: Dict) -> Dict:
        """
        Run evaluation with a configuration dictionary.

        Args:
            config: Configuration dictionary containing all parameters

        Returns:
            Dict: Evaluation results
        """
        return self.run(
            model=config.get("model"),
            api_key=config.get("api_key"),
            use_knowledge=config.get("use_knowledge", True),
            mode=config.get("mode", "dev"),
            num_cpus=config.get("num_cpus", 1),
            meta_time_out=config.get("meta_time_out", 30.0),
            skip_generation=config.get("skip_generation", False),
        )

    def get_supported_models(self) -> Dict[str, List[str]]:
        """
        Get a dictionary of supported model categories and their models.

        Returns:
            Dict: Dictionary with model categories as keys and model lists as values
        """
        return {
            "llama_api": [
                "Llama-3.3-8B-Instruct",
                "Llama-3.3-70B-Instruct",
                "Llama-4-Maverick-17B-128E-Instruct-FP8",
                "Llama-4-Scout-17B-16E-Instruct-FP8",
            ],
        }


if __name__ == "__main__":
    # Example usage
    evaluator = LlamaText2SQLEval()

    # Example configuration for Llama 3.3 model
    config = {
        "model": "Llama-3.3-8B-Instruct",
        "api_key": os.getenv("LLAMA_API_KEY"),
        "use_knowledge": True,
        "mode": "dev",
        "num_cpus": 1,
        "meta_time_out": 30.0,
    }

    print("Running evaluation with Llama API Llama-3.3-8B-Instruct...")
    results = evaluator.run_with_config(config)

    if results:
        print(f"\nFinal Results:")
        print(f"Overall Accuracy: {results['overall_accuracy']:.2f}%")
        print(f"Simple: {results['simple_accuracy']:.2f}%")
        print(f"Moderate: {results['moderate_accuracy']:.2f}%")
        print(f"Challenging: {results['challenging_accuracy']:.2f}%")
    else:
        print("Evaluation failed.")
