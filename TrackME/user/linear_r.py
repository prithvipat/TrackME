import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from django.db.models import Sum

def recommend_budget(profile, transactions):

    categories = ['Food', 'Transportation', 'Clothing', 'Utilities', 'Groceries', 'Others']
    
    category_totals = {cat: 0 for cat in categories}
    for t in transactions:
        if t.category in category_totals:
            category_totals[t.category] += t.amount

    data = pd.DataFrame([category_totals])
    
    # Temp Sample
    sample_data = pd.DataFrame({
        'Food': [200, 300, 150, 400],
        'Transportation': [100, 200, 50, 300],
        'Clothing': [50, 150, 30, 100],
        'Utilities': [150, 250, 100, 200],
        'Groceries': [300, 400, 200, 500],
        'Others': [100, 50, 70, 80]
    })
    
    combined_data = pd.concat([sample_data, data], ignore_index=True)
    normalized_data = combined_data / combined_data.max()

    # K-Means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(normalized_data)
    user_cluster = kmeans.predict(normalized_data.iloc[[-1]])

    cluster_data = combined_data.iloc[kmeans.labels_ == user_cluster[0]]
    recommended_budget = cluster_data.mean().to_dict()

    return {cat: round(recommended_budget[cat]) for cat in categories}
