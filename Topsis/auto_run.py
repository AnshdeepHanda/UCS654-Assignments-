import pandas as pd
import os
import sys

# 1. Create the Dummy Data (So you don't have to make a CSV manually)
data = {
    'Fund Name': ['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8'],
    'P1': [0.67, 0.6, 0.82, 0.6, 0.76, 0.69, 0.79, 0.84],
    'P2': [0.45, 0.36, 0.67, 0.36, 0.58, 0.48, 0.62, 0.71],
    'P3': [6.5, 3.6, 3.8, 3.5, 4.8, 6.6, 4.8, 6.5],
    'P4': [42.6, 53.3, 63.1, 69.2, 43, 48.7, 59.2, 34.5],
    'P5': [12.56, 14.47, 17.1, 18.42, 12.29, 14.12, 16.35, 10.64]
}

# Save this data to a file called data.csv
df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)
print("1. File 'data.csv' created successfully.")

# 2. Define the parameters automatically
# You can change these weights/impacts here if you want
file_name = "data.csv"
weights = "1,1,1,1,1"
impacts = "+,+,+,+,-"
result_file = "result.csv"

# 3. Construct the command
command = f"python topsis.py {file_name} \"{weights}\" \"{impacts}\" {result_file}"

print(f"2. Executing command: {command}")
print("-" * 30)

# 4. Run the command
os.system(command)