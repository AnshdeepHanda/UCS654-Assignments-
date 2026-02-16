import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    'Model': ['DialoGPT-medium', 'BlenderBot-400M', 'GODEL-base', 'T5-base', 'GPT-2-large'],
    'Perplexity': [28.5, 18.2, 22.4, 35.1, 24.6],       # Lower is better
    'BLEU_Score': [0.15, 0.28, 0.22, 0.12, 0.18],       # Higher is better
    'Inference_Time_ms': [120, 150, 110, 180, 140],     # Lower is better (latency)
    'Model_Size_MB': [1400, 1600, 950, 890, 1550]       # Lower is better (storage)
}

df = pd.DataFrame(data)

print("--- Initial Data ---")
print(df)
print("\n")

cols = ['Perplexity', 'BLEU_Score', 'Inference_Time_ms', 'Model_Size_MB']

weights = [0.25, 0.35, 0.20, 0.20]

# Impacts: '+' means higher is better, '-' means lower is better
# Perplexity (-), BLEU (+), Time (-), Size (-)
impacts = ['-', '+', '-', '-']

normalized_df = df[cols].copy()

for col in cols:
    column_data = df[col]
    rss = np.sqrt(np.sum(column_data**2))
    normalized_df[col] = column_data / rss


weighted_df = normalized_df.copy()

for i, col in enumerate(cols):
    weighted_df[col] = normalized_df[col] * weights[i]


ideal_best = []
ideal_worst = []

for i, col in enumerate(cols):
    if impacts[i] == '+':
        ideal_best.append(weighted_df[col].max())
        ideal_worst.append(weighted_df[col].min())
    else:
        ideal_best.append(weighted_df[col].min())
        ideal_worst.append(weighted_df[col].max())


S_plus = []
S_minus = [] 

for index, row in weighted_df.iterrows():
    dist_best = np.sqrt(np.sum((row - ideal_best)**2))
    S_plus.append(dist_best)
    
    dist_worst = np.sqrt(np.sum((row - ideal_worst)**2))
    S_minus.append(dist_worst)


scores = []
for i in range(len(S_plus)):
    score = S_minus[i] / (S_plus[i] + S_minus[i])
    scores.append(score)

df['Topsis_Score'] = scores

df['Rank'] = df['Topsis_Score'].rank(ascending=False)

print("--- Final Results with TOPSIS Score ---")
print(df.sort_values(by='Rank'))

df.to_csv('topsis_results_conversational.csv', index=False)

plt.figure(figsize=(10, 6))
plt.bar(df['Model'], df['Topsis_Score'], color=['#4CAF50', '#2196F3', '#FF9800', '#F44336', '#9C27B0'])
plt.xlabel('Conversational Models')
plt.ylabel('TOPSIS Score')
plt.title('Comparison of Pre-trained Conversational Models using TOPSIS')
plt.ylim(0, 1) 
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, v in enumerate(df['Topsis_Score']):
    plt.text(i, v + 0.02, str(round(v, 3)), ha='center')

plt.savefig('topsis_graph.png')
plt.show()