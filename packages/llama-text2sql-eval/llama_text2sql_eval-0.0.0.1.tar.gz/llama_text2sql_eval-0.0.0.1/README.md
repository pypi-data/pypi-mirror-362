# A Quick Library for Llama Text2SQL Accuracy Evaluation

This library provides a simple interface for evaluating the accuracy of Llama models on the Text2SQL task. It uses the BIRD DEV dataset and provides a simple API for running the evaluation pipeline using the Llama API.

## Quick Start

### Downloading Data
```bash
# Navigate to data directory
cd src/llama_text2sql_eval/data

# Run the download script
bash download_dev_unzip.sh

# This should create:
# - data/dev_20240627/dev.json
# - data/dev_20240627/dev_databases/
```

*** Setting up API Key

```bash
export LLAMA_API_KEY="your_key_here"
```
### Running the Pipeline

```bash
python test.py

### API-based Testing

```python
# Simple test without running actual models
from llama_text2sql_eval import LlamaText2SQLEval

# Initialize the evaluator
evaluator = LlamaText2SQLEval()

# Run the complete pipeline
results = evaluator.run(
    model="Llama-3.3-70B-Instruct",
    api_key=os.getenv("LLAMA_API_KEY")
)

if results:
    print(f"Overall Accuracy: {results['overall_accuracy']:.2f}%")
    print(f"Simple: {results['simple_accuracy']:.2f}%")
    print(f"Moderate: {results['moderate_accuracy']:.2f}%")
    print(f"Challenging: {results['challenging_accuracy']:.2f}%")
```
