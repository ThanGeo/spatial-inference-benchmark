import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
import argparse

class bcolors:
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'

def evaluate_multilabel(df):
    """Evaluate multilabel checkbox responses (truth/response columns)"""
    # Clean and prepare
    y_true = df['truth'].str.replace(' ', '').str.split(',')
    y_pred = df['response'].str.replace(' ', '').str.split(',')

    # Convert to binary matrix representation (for sample-average)
    mlb = MultiLabelBinarizer(classes=['a', 'b', 'c', 'd', 'e'])
    y_true_bin = mlb.fit_transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    # Calculate sample-average metrics
    precision = precision_score(y_true_bin, y_pred_bin, average='samples', zero_division=0)
    recall = recall_score(y_true_bin, y_pred_bin, average='samples', zero_division=0)
    f1 = f1_score(y_true_bin, y_pred_bin, average='samples', zero_division=0)

    # Print results
    print(f"{bcolors.BLUE}sample-average Precision: {bcolors.ENDC}{precision:.2f}")
    print(f"{bcolors.BLUE}sample-average Recall: {bcolors.ENDC}{recall:.2f}")
    print(f"{bcolors.BLUE}sample-average F1-score: {bcolors.ENDC}{f1:.2f}")

def evaluate_binary(df):
    """Evaluate binary responses (truth/prediction columns)"""
    # Filter only 'yes'/'no' responses
    df = df[df['truth'].isin(['yes', 'no']) & df['response'].isin(['yes', 'no'])]
    # Clean and prepare
    y_true = df['truth']
    y_pred = df['response']

    # Calculate metrics
    precision = precision_score(y_true, y_pred, pos_label='yes', zero_division=0)
    recall = recall_score(y_true, y_pred, pos_label='yes', zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label='yes', zero_division=0)

    # Print results
    print(f"{bcolors.BLUE}Precision: {bcolors.ENDC}{precision:.2f}")
    print(f"{bcolors.BLUE}Recall: {bcolors.ENDC}{recall:.2f}")
    print(f"{bcolors.BLUE}F1-score: {bcolors.ENDC}{f1:.2f}")

def evaluate_multiclass(df):
    """Evaluate multiple-choice responses (truth/response columns)"""
    # Clean and prepare
    y_true = df['truth'].str.strip()
    y_pred = df['response'].str.strip()

    # Validate possible classes (a-e)
    valid_classes = {'a', 'b', 'c', 'd', 'e'}
    invalid_true = ~y_true.isin(valid_classes)
    invalid_pred = ~y_pred.isin(valid_classes)

    if invalid_true.any() or invalid_pred.any():
        print(f"{bcolors.RED}Warning: Invalid responses detected{bcolors.ENDC}")
        if invalid_true.any():
            print(f"Invalid truth values: {y_true[invalid_true].unique()}")
        if invalid_pred.any():
            print(f"Invalid predicted values: {y_pred[invalid_pred].unique()}")
        
        # Filter out invalid responses
        valid_mask = y_true.isin(valid_classes) & y_pred.isin(valid_classes)
        y_true = y_true[valid_mask]
        y_pred = y_pred[valid_mask]

    # Calculate macro-averaged metrics
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)

    # Print results
    print(f"\n{bcolors.BLUE}macro-Precision: {bcolors.ENDC}{precision:.2f}")
    print(f"{bcolors.BLUE}macro-Recall: {bcolors.ENDC}{recall:.2f}")
    print(f"{bcolors.BLUE}macro-F1-score: {bcolors.ENDC}{f1:.2f}")

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Evaluate responses based on type.")
    parser.add_argument("-response_path", type=str, required=True, help="Path to CSV with response data")
    parser.add_argument("-label_type", type=str, required=True, 
                        choices=['BINARY', 'MULTICLASS', 'MULTILABEL'], 
                        help="Type of evaluation to perform")
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.response_path)

    # Call appropriate evaluation function
    if args.label_type == 'MULTILABEL':
        evaluate_multilabel(df)
    elif args.label_type == 'BINARY':
        evaluate_binary(df)
    elif args.label_type == 'MULTICLASS':
        evaluate_multiclass(df)
    else:
        raise ValueError(f"Unknown label type: {args.label_type}")

if __name__ == "__main__":
    main()