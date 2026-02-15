import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import RandomOverSampler

def load_and_balance(url):
    df = pd.read_csv(url)
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    ros = RandomOverSampler(random_state=42)
    X_res, y_res = ros.fit_resample(X, y)
    return pd.concat([X_res, y_res], axis=1)

def get_sampling_strategies(balanced_df, n):
    samples = {}
    
    samples['Sampling1'] = balanced_df.sample(n=n, random_state=42)
    
    step = len(balanced_df) // n
    samples['Sampling2'] = balanced_df.iloc[::step][:n]
    
    samples['Sampling3'] = balanced_df.groupby('Class', group_keys=False).apply(
        lambda x: x.sample(n=n//2), include_groups=True
    )

    balanced_df['Cluster'] = pd.cut(range(len(balanced_df)), bins=10, labels=False)
    selected_clusters = np.random.choice(range(10), size=3, replace=False)
    cluster_data = balanced_df[balanced_df['Cluster'].isin(selected_clusters)]
    samples['Sampling4'] = cluster_data.sample(n=n, replace=True, random_state=42)
    
    samples['Sampling5'] = balanced_df.sample(n=n, replace=True, random_state=1)
    
    return samples

def train_and_evaluate(sample_dict):
    models = {
        "M1_Logistic": LogisticRegression(max_iter=2000),
        "M2_RandomForest": RandomForestClassifier(),
        "M3_KNN": KNeighborsClassifier(),
        "M4_SVC": SVC(),
        "M5_ExtraTrees": ExtraTreesClassifier()
    }
    
    results = {}
    for m_name, model in models.items():
        acc_scores = []
        for s_name in ['Sampling1', 'Sampling2', 'Sampling3', 'Sampling4', 'Sampling5']:
            s_data = sample_dict[s_name]
            X = s_data.drop(['Class', 'Cluster'], axis=1, errors='ignore')
            y = s_data['Class']
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc_scores.append(round(accuracy_score(y_test, y_pred) * 100, 2))
        
        results[m_name] = acc_scores
    return results

if __name__ == "__main__":
    RAW_URL = "https://raw.githubusercontent.com/AnjulaMehto/Sampling_Assignment/main/Creditcard_data.csv"
    
    data = load_and_balance(RAW_URL)
    n_size = 390 
    
    all_samples = get_sampling_strategies(data, n_size)
    final_results = train_and_evaluate(all_samples)
    
    df_results = pd.DataFrame(final_results, index=['Sampling1', 'Sampling2', 'Sampling3', 'Sampling4', 'Sampling5']).T
    print("\n--- Model vs Sampling Technique Accuracy ---")
    print(df_results)