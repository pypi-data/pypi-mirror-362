# A Quick Library for Llama Text2SQL Accuracy Evaluation

This library provides a simple interface for evaluating the accuracy of Llama models on the Text2SQL task. It uses the BIRD DEV dataset and provides a simple API for running the evaluation pipeline using the Llama API.

## Quick Start

1. Run `pip install llama-text2sql-eval` to install the library.

2. Download the [BIRD](https://bird-bench.github.io/) DEV dataset by running the following commands:

```bash

mkdir -p llama-text2sql-eval/data
cd llama-text2sql-eval/data
wget https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip
unzip dev.zip
rm dev.zip
rm -rf __MACOSX
cd dev_20240627
unzip dev_databases.zip
rm dev_databases.zip
rm -rf __MACOSX
cd ../..
```

3. Get your Llama API key [here](https://llama.developer.meta.com/) and set up an environment variable:

```bash
export LLAMA_API_KEY="your_key_here"
```

4. Run the eval with one of the two options:

Option A:

```bash
llama-text2sql-eval --model Llama-3.3-8B-Instruct
```

Option B:

Save the following code to a file named `run.py`, then `python run.py`:

```python
import os
from llama_text2sql_eval import LlamaText2SQLEval

evaluator = LlamaText2SQLEval()

results = evaluator.run(
    model="Llama-3.3-70B-Instruct", # or any other Llama models supported by the Llama API
    api_key=os.getenv("LLAMA_API_KEY")
)

if results:
    print(f"Overall Accuracy: {results['overall_accuracy']:.2f}%")
    print(f"Simple: {results['simple_accuracy']:.2f}%")
    print(f"Moderate: {results['moderate_accuracy']:.2f}%")
    print(f"Challenging: {results['challenging_accuracy']:.2f}%")
```

Running the eval will take about 40 minutes to complete. You should see something like at the end of the run:

```
Overall Accuracy: 57.95%
Simple: 65.30%
Moderate: 47.63%
Challenging: 44.14%
```
