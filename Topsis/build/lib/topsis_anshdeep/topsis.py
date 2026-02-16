import sys
import pandas as pd
import numpy as np
import os

def main():
    if len(sys.argv) != 5:
        print("ERROR: Incorrect number of parameters.")
        print("Usage: topsis <InputFile> <Weights> <Impacts> <OutputFile>")
        return

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    if not os.path.isfile(input_file):
        print(f"ERROR: File '{input_file}' not found.")
        return

    try:
        df = pd.read_csv(input_file)
    except:
        print("ERROR: Could not read file. Ensure it is a valid CSV.")
        return

    if df.shape[1] < 3:
        print("ERROR: File must have 3 or more columns.")
        return

    try:
        temp_data = df.iloc[:, 1:].values.astype(float)
    except ValueError:
        print("ERROR: Columns from 2nd to last must contain only numeric values.")
        return

    try:
        weights = [float(w) for w in weights_str.split(',')]
        impacts = impacts_str.split(',')
    except ValueError:
        print("ERROR: Weights and impacts must be separated by commas.")
        return

    if len(weights) != temp_data.shape[1] or len(impacts) != temp_data.shape[1]:
        print("ERROR: Number of weights, impacts, and columns must be the same.")
        return

    if not all(i in ['+', '-'] for i in impacts):
        print("ERROR: Impacts must be either '+' or '-'.")
        return

    # 1. Normalize
    norm_data = temp_data / np.sqrt((temp_data**2).sum(axis=0))

    # 2. Assign Weights
    weighted_data = norm_data * weights

    # 3. Ideal Best & Worst
    ideal_best = []
    ideal_worst = []
    for i in range(len(weights)):
        if impacts[i] == '+':
            ideal_best.append(max(weighted_data[:, i]))
            ideal_worst.append(min(weighted_data[:, i]))
        else:
            ideal_best.append(min(weighted_data[:, i]))
            ideal_worst.append(max(weighted_data[:, i]))

    # 4. Euclidean Distance & Score
    S_plus = np.sqrt(((weighted_data - ideal_best)**2).sum(axis=1))
    S_minus = np.sqrt(((weighted_data - ideal_worst)**2).sum(axis=1))
    
    total_dist = S_plus + S_minus
    score = np.divide(S_minus, total_dist, out=np.zeros_like(S_minus), where=total_dist!=0)

    # 5. Rank and Save
    df['Topsis Score'] = score
    df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
    
    df.to_csv(output_file, index=False)
    print(f"SUCCESS: Result saved to {output_file}")

if __name__ == "__main__":
    main()