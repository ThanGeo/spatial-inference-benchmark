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

# Running your own models

In order to evaluate a model on our datasets, you need to give it specific instructions on the task.
Feel free to use whatever instruction you like.
For our experiments, we provided the following explicit instructions for each question, tailored to the specific task, to guide the model’s response:

## (Yes/No questions) Binary Classification

_"Instruction: Respond with only 'yes' or 'no'. Do not include any other text or explanation."_

## (Radio questions) Multiclass Classification

_"Instruction: Respond with only the single letter (a-e) corresponding to the correct option. Do not include any explanation or additional text."_

## (Checkbox questions) Multilabel Classification

_"Instruction: Respond with only the letters (a-e) separated with comma, corresponding to the correct options. Do not include any explanation or additional text."_


