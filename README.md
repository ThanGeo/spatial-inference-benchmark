# The Spatial Inference Benchmark

This repository contains code to evaluate a model’s responses to spatial reasoning queries — including **binary**, **multiclass**, and **multilabel** classification — against ground truth labels.

## 📂 Datasets

Datasets are located in the `datasets/` directory and were created using the **TIGER 2015** collection from [SpatialHadoop](https://spatialhadoop.cs.umn.edu/datasets.html).

We used the [SpaTex](https://github.com/ThanGeo/SpaTex---Spatial-To-Text-data-toolkit) toolkit to compute topological relations from spatial data and generate RDF triplets, which were then converted into natural language questions. We have included the RDF source file (`CSZt.nt`) that we generated and used for the question generation in the `datasets/` directory.

🗃️ You can also find our dataset on Hugging Face:  
👉 [huggingface.co/datasets/Rammen/SpatialReasoning](https://huggingface.co/datasets/Rammen/SpatialReasoning)

---

## 📊 Model Scores

To reproduce the results shown in **Figure 6**, run:

```bash
./scores.sh
```

To evaluate a specific model:

```bash
python3 src/evaluate.py \
  -response_path "<response_file_path>" \
  -label_type [MULTILABEL | BINARY | MULTICLASS]
```

- The response file must be a CSV with three columns: `query`, `truth`, `response`.
- The `label_type` must match one of the allowed types.

---

## 🧪 Running Your Own Models

To evaluate your own models, you must provide clear task-specific instructions. You may use your own phrasing, but for our experiments, we used the following formats:

### ✅ Binary Classification (Yes/No)

```
Instruction: Respond with only 'yes' or 'no'. Do not include any other text or explanation.
```

### 🔘 Multiclass Classification (Radio)

```
Instruction: Respond with only the single letter (a-e) corresponding to the correct option. Do not include any explanation or additional text.
```

### ☑️ Multilabel Classification (Checkbox)

```
Instruction: Respond with only the letters (a-e) separated with commas, corresponding to the correct options. Do not include any explanation or additional text.
```

---

## 📥 Getting Model Responses (spatial_reasoning.csv)

The file `datasets/spatial_reasoning.csv` merges 3,000 binary, multiclass, and multilabel questions into a single randomized dataset. It includes an extra column specifying the question type.

To collect model responses, use the provided `getResponses.py` script:

### Required Arguments:

- `-query_dataset_path`: Path to the `spatial_reasoning.csv` file
- `-query_result_path`: Path to the output responses file

### Optional:

- `-model`: Model ID (defaults to `meta-llama/Meta-Llama-3.1-8B-Instruct`)

### Example:

```bash
python3 src/getResponses.py \
  -query_dataset_path datasets/spatial_reasoning.csv \
  -query_result_path responses.csv \
  -model mistralai/Mistral-7B-Instruct
```

---

## ❓ Generating Questions

We offer a way to generate spatial reasoning questions from RDF triplets regarding spatial entities and their topological relations. The code in ```generateQuestionsFromRDF.py``` takes the following inputs:

### Required Arguments:
- `-input` : a .nt file containing spatial RDF triplets.
- `-num` : the number of questions to generate.

### Optional:
- `-output` : the file to write the generated questions to (default `output.csv`).
- `-yesno` : percentage of yes/no questions in the generated set (default 0.33).
- `-radio` : percentage of radio questions in the generated set (default 0.33).
- `-checkbox` : percentage of checkbox questions in the generated set (default 0.34).

In order to disable a specific question type from being used, set its value to 0. Note that the values of `-yesno`, `-radio` and `-checkbox` must add up to 1. 

### Supported Relations
The supported relations that may exist in the input RDF file are the following:

- (adjacent to and) north/south/west/east/
- (adjacent to and) northeast/northwest/southeast/southwest
- inside
- contains
- intersects

### Example:
We provide the RDF that we generated using SpaTex, that was used to generate our benchmark questions.

```bash
python3 src/generateQuestionsFromRDF.py \
  -input datasets/CSZt.nt \
  -num 1000 \
  -output questions_1000.csv
```

## 📝 License

**Full rights included.**