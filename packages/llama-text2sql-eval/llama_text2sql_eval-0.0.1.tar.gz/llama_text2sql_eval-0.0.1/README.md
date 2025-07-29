# A Quick Library for Llama Text2SQL Accuracy Evaluation

This library provides a simple interface for evaluating the accuracy of Llama models on the Text2SQL task. It uses the BIRD DEV dataset and provides a simple API for running the evaluation pipeline using the Llama API.

## Quick Start

1. Run `pip install llama-text2sql-eval` to install the library.

2. Download the [BIRD](https://bird-bench.github.io/) DEV dataset by running the following commands:

```bash
with-proxy wget https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip
unzip dev.zip
rm dev.zip
rm -rf __MACOSX
cd dev_20240627
unzip dev_databases.zip
rm dev_databases.zip
rm -rf __MACOSX
cd ..
```

3. Get your Llama API key [here](https://llama.developer.meta.com/) and set up an environment variable:

```bash
export LLAMA_API_KEY="your_key_here"
```

4. Create a Python script and run it:

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

You should see something like:
```
Overall Accuracy: 57.95%
Simple: 65.30%
Moderate: 47.63%
Challenging: 44.14%
```
