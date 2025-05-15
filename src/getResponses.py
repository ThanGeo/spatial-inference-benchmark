from collections import Counter
from tqdm import tqdm
from llm_class import PlainLLM
import torch
import argparse
import re
torch.cuda.empty_cache()


REPEAT_FACTOR = 3
# regex to remove non-chars in necessary
regex = re.compile('[^a-zA-Z]')
llm = None

class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

def getYesNoResponse(query):
    for i in range(REPEAT_FACTOR):
        responses = []
        try:
            response = llm.generate(query + " Instruction: Respond with only 'yes' or 'no'. Do not include any other text or explanation.")  # for yes/no queries, append an extra instruction
            response = response.replace("\n", " ").lower()
            response = regex.sub('', response)
            responses.append(response)
        except torch.cuda.OutOfMemoryError:
            print(bcolors.WARNING + f"CUDA out of memory error encountered, skipping query: '{query}'..." + bcolors.ENDC)
            response = "no response"
            responses.append(response)
    # Count occurrences of each option
    counts = Counter(responses)
    most_prominent_response = counts.most_common(1)[0][0]
    # conformity check
    if most_prominent_response not in ['yes', 'no']:
        print(bcolors.WARNING + f"Invalid response: {most_prominent_response}" + bcolors.ENDC)
        most_prominent_response = "no response"
    return most_prominent_response

def getRadioResponse(query):
    for i in range(REPEAT_FACTOR):
        responses = []
        try:
            response = llm.generate(query + " \"Instruction: Respond with only the single letter (a-e) corresponding to the correct option. Do not include any explanation or additional text.\"")
            response = response.replace("\n", " ").lower()
            response = response.replace(".", "")
            response = regex.sub('', response)
            if response not in ["a","b","c","d","e"]:
                response = "no response"
            responses.append(response)
        except torch.cuda.OutOfMemoryError:
            print(bcolors.WARNING + f"CUDA out of memory error encountered, skipping query: '{query}'..." + bcolors.ENDC)
            response = "no response"
            responses.append(response)
    # Count occurrences of each option
    counts = Counter(responses)
    most_prominent_response = counts.most_common(1)[0][0]
    # conformity check
    if most_prominent_response not in ['a', 'b', 'c', 'd', 'e']:
        print(bcolors.WARNING + f"Invalid response: {most_prominent_response}" + bcolors.ENDC)
        most_prominent_response = "no response"
    return most_prominent_response


def getCheckboxResponse(query):
    for i in range(REPEAT_FACTOR):
        responses = []
        try:
            response = llm.generate(query + " \"Instruction: Respond with only the letters (a-e) separated with comma, corresponding to the correct options. Do not include any explanation or additional text.\"")
            response = response.replace("\n", " ").lower()
            response = response.replace(".", "")
            response = response.replace(" ", "")
            responses.append(response)
        except torch.cuda.OutOfMemoryError:
            print(bcolors.WARNING + f"CUDA out of memory error encountered, skipping query: '{query}'..." + bcolors.ENDC)
            response = "no response"
            responses.append(response)

    # Count occurrences of each option
    counts = Counter(responses)
    most_prominent_response = counts.most_common(1)[0][0]
    
    # conformity check
    tokens = most_prominent_response.split(',')
    for token in tokens:
        if token not in ['a', 'b', 'c', 'd', 'e','']:
            print(bcolors.WARNING + f"Invalid response: {most_prominent_response}" + bcolors.ENDC)
            most_prominent_response = "no response"
            break
    return most_prominent_response

def main():
    global llm
    # Define argument parser
    parser = argparse.ArgumentParser(description="Run an LLM with optional RAG functionality.")

    # Add arguments
    parser.add_argument("-query_dataset_path", type=str, help="Path of the query dataset to use")
    parser.add_argument("-query_result_path", type=str, help="Path of the output result")
    parser.add_argument("-model", type=str, default="meta-llama/Meta-Llama-3.1-8B-Instruct", help="LLM model to load")

    # Parse arguments
    args = parser.parse_args()

    # default model is meta-llama/Meta-Llama-3.1-8B-Instruct
    llm_modelid = args.model

    # init llm
    llm = PlainLLM(llm_modelid)
    print(bcolors.GREEN + "Using default LLM" + bcolors.ENDC)

    # parse queries
    entries = None
    with open(args.query_dataset_path, "r") as f:
        document = f.read()
        entries = document.strip().split("\n")[1:]

    print(bcolors.GREEN + f"Running model {llm_modelid}" + bcolors.ENDC)

    output_path = args.query_result_path
    with open(output_path, "w") as f:
        f.write("type,query,truth,response\n")
        for index,entry in tqdm(enumerate(entries), desc="Evaluating queries..."):
            tokens = entry.split(',') 
            # get query type
            qtype = tokens[0]
            query = tokens[1]
            print(bcolors.BLUE + f"Query Type: {qtype}, Query: " + query + bcolors.ENDC)

            # get response based on type
            if qtype == "yes/no":
                response = getYesNoResponse(query)
            elif qtype == "radio":
                response = getRadioResponse(query)
            elif qtype == "checkbox":
                response = getCheckboxResponse(query)
            else:
                print(bcolors.WARNING + f"Unknown query type encountered '{qtype}', ignoring..." + bcolors.ENDC)
                response = "no response"

            print(bcolors.RED + "response: " + response + bcolors.ENDC)
            entry += "," + response
            f.write(entry + "\n")


if __name__=="__main__":
    main()
