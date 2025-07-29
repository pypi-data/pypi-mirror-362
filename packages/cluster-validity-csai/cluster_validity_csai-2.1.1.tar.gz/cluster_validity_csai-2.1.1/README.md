# CSAIEvaluator: Clustering Stability Assessment Index (CSAI)

CSAIEvaluator is a Python library for evaluating the stability and validity of clustering algorithms across multiple data partitions. It is based on the Clustering Stability Assessment Index (CSAI), which leverages feature-based information to measure the consistency and robustness clustering solutions.

## Installation

```bash
pip install cluster-validity-csai
```

### or the development version from GitHub:
```bash
pip install git+https://github.com/AdaneNT/cluster-validity-csai.git
```

## Example Usage

### Dataset
Let's use the **20 Newsgroups (20NG)** dataset — a collection of approximately 20,000 newsgroup posts organized into various categories.  
It is widely used for benchmarking text clustering and classification algorithms. 

### Load libraries
```python
import torch
from sentence_transformers import SentenceTransformer
from sklearn.datasets import fetch_20newsgroups
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import re
import umap

from csai import CSAIEvaluator
```

## Step 1: Text embedding (e.g. SentenceTransformer)
```python
def get_sbert_embeddings(texts):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts, convert_to_tensor=False)
```

## Step 2: Dimensionality reduction (e.g. UMAP)
```python
def reduce_with_umap(df, emb_col="Embedding", output_col="key_umap", n_components=10):
    reducer = umap.UMAP(n_components=n_components, random_state=42)
    emb_array = np.array(df[emb_col].tolist())
    reduced = reducer.fit_transform(emb_array)
    df[output_col] = reduced.tolist()
    return df
```

## Step 3: Load and preprocess data (20 Newsgroups dataset)
```python
def run_pipeline():
    newsgroups = fetch_20newsgroups(subset='all')
    data = newsgroups.data
    df = pd.DataFrame(data, columns=["text"])
    df = df.sample(n=5000, random_state=42).reset_index(drop=True)

    texts = df["text"].fillna("").apply(lambda x: re.sub(r"\d+|[^\w\s]|\s+@", " ", x.lower()).strip()).tolist()
    embeddings = get_sbert_embeddings(texts)
    df["Embeddings"] = embeddings.tolist()

    df = reduce_with_umap(df, emb_col="Embeddings", output_col="key_umap", n_components=10)
    return df

df_result = run_pipeline()
```

## Step 4: Train/test split
```python
X_train, X_test = train_test_split(df_result, test_size=0.30, random_state=42)
```

## Step 5: Define clustering function (e.g. K-means)
```python
def kmeans_label_func(embeddings, n_clusters=7):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(embeddings)
    return labels, model
```

## Step 6: Apply CSAI Evaluation
```python
csai = CSAIEvaluator()
score = csai.run_csai_evaluation(
    X_train, 
    X_test,
    key_col="key_umap", 
    label_func=kmeans_label_func, 
    n_splits=5)

print("CSAIEvaluator Score:", score)
```

## 📄 Citation

If you use this package in your work, please cite:

Tarekegn, A. N., Tessem, B., & Rabbi, F. (2025).  
*A New Cluster Validation Index Based on Stability Analysis*.  
In Proceedings of the 14th International Conference on Pattern Recognition Applications and Methods (ICPRAM),  
SciTePress, pp. 377–384.  
DOI: [10.5220/0013309100003905](https://doi.org/10.5220/0013309100003905)

## License

This software is provided under a custom academic, non-commercial license.  
See [LICENSE.txt](https://github.com/AdaneNT/cluster-validity-csai/blob/main/LICENSE) for full terms.
