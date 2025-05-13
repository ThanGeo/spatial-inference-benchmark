# Spatial Inference Benchmark code

Simple code that evaluates a model's responses for a set of queries (binary, multiclass or multilabel classification) against their corresponding truths.


# Model Scores

To recreate all the results of Figure 6 (model scores), run ```scores.sh```.
Alternatively, you can get the scores of a specific model with the following command:
```
python3 evaluate.py -response_path "<response_file_path>" -label_type [MULTILABEL, BINARY, MULTICLASS]
```

The response file should be a csv file with 3 columns: query,truth,response
One of the three label types should be used as they appear in the exmaple.
