# TOPSIS Analysis for Pre-Trained Conversational Models

## Project Description
This project implements the **TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) method to find the best pre-trained model for **Text Conversational** tasks. 

This assignment corresponds to Roll Numbers ending with **4 or 9**.

### Models Compared
We compared standard pre-trained models commonly used for conversational AI:
1.  **DialoGPT-medium**
2.  **BlenderBot-400M**
3.  **GODEL-base**
4.  **T5-base**
5.  **GPT-2-large**

### Evaluation Criteria
The models were evaluated based on the following metrics:
* **Perplexity:** (Lower is better) - Measures how well the model predicts sample text.
* **BLEU Score:** (Higher is better) - Measures the quality of the generated text compared to human reference.
* **Parameters (Millions):** (Lower is better) - Represents model size/complexity.
* **Inference Time:** (Lower is better) - Time taken to generate a response.

---

## Results
After applying the TOPSIS algorithm (normalizing data, applying weights, and calculating Euclidean distances), the final ranking is as follows:

| Model Name | Perplexity | BLEU Score | Params (M) | Inference Time | TOPSIS Score | Rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BlenderBot-400M** | 19.1 | 0.29 | 365 | 145 | **0.682** | **1** |
| **GODEL-base** | 23.5 | 0.21 | 220 | 105 | **0.564** | **2** |
| **GPT-2-large** | 25.1 | 0.19 | 774 | 135 | **0.491** | **3** |
| **DialoGPT-medium** | 26.4 | 0.16 | 345 | 115 | **0.412** | **4** |
| **T5-base** | 33.2 | 0.13 | 220 | 175 | **0.187** | **5** |

**Winner:** Based on this analysis, **BlenderBot-400M** is the best choice because it balances a high BLEU score with reasonable perplexity.

---

## Visual Analysis
The following bar chart visualizes the TOPSIS scores of the different models:

![TOPSIS Result Graph](result_graph.png)