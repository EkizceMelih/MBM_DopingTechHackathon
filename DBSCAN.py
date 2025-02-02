import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors

# Örnek veri oluşturma
np.random.seed(42)
num_samples = 500
data = pd.DataFrame({
    'Total_Net': np.random.normal(50, 15, num_samples),
    'Study_Hours': np.random.normal(5, 1.5, num_samples),
    'Target_Rank': np.random.normal(100000, 30000, num_samples)
})

# Verileri 0-1 arasına normalleştirme
scaler = MinMaxScaler()
data[['Total_Net', 'Study_Hours', 'Target_Rank']] = scaler.fit_transform(data[['Total_Net', 'Study_Hours', 'Target_Rank']])

# Hedeflenen sıralamayı ters çevirerek başarıya göre ölçekleme
data['Inverse_Target_Rank'] = 1 - data['Target_Rank']  # 0 en kötü, 1 en iyi sıralama

# DBSCAN Kümeleme Modeli (eps = yoğunluk eşiği, min_samples = en az kaç komşu olmalı)
dbscan = DBSCAN(eps=0.2, min_samples=5)
data['DBSCAN_Cluster'] = dbscan.fit_predict(data[['Total_Net', 'Study_Hours', 'Inverse_Target_Rank']])

# Gürültü olarak belirlenen öğrencileri (-1 kümesine düşenler) filtreleme
filtered_data = data[data['DBSCAN_Cluster'] != -1]

# K-En Yakın Komşu (KNN) ile en benzer 5 öğrenciyi bulma
knn = NearestNeighbors(n_neighbors=6, metric='euclidean')  # K=6 çünkü kendisi dahil olacak
knn.fit(filtered_data[['Total_Net', 'Study_Hours', 'Inverse_Target_Rank']])

# Her öğrenci için en benzer 5 kişinin indekslerini çıkarma
_, indices = knn.kneighbors(filtered_data[['Total_Net', 'Study_Hours', 'Inverse_Target_Rank']])

# Benzer öğrencileri kaydetme
similar_students_dbscan = {filtered_data.index[i]: filtered_data.index[indices[i][1:]].tolist() for i in range(len(filtered_data))}

# Sonuçları tabloya ekleme
data['Most_Similar_Students_DBSCAN'] = data.index.map(similar_students_dbscan).fillna("Noise (Outlier)")

# CSV olarak kaydetme
data.to_csv("dbscan_clustering_results.csv", index=False)
print("Sonuçlar CSV olarak kaydedildi: dbscan_clustering_results.csv")

# 📌 **Görselleştirme & PNG olarak kaydetme**
plt.figure(figsize=(12, 8))

# Graf oluşturma
G = nx.Graph()

# Öğrencileri düğüm (node) olarak ekleme
for student in filtered_data.index:
    G.add_node(student, cluster=filtered_data.loc[student, 'DBSCAN_Cluster'])

# En benzer 5 öğrenciyi kenar (edge) olarak ekleme
for student, similar_students in similar_students_dbscan.items():
    for similar_student in similar_students:
        G.add_edge(student, similar_student)

# Küme renklerini belirleme (Hata düzeltildi!)
unique_clusters = list(filtered_data['DBSCAN_Cluster'].unique())
colormap = plt.colormaps.get_cmap("coolwarm")  # Tek argüman almalı

# Renk atamaları
cluster_colors = {cluster: colormap(i / len(unique_clusters)) for i, cluster in enumerate(unique_clusters)}

# Pozisyonları oluşturma
pos = nx.spring_layout(G, seed=42)

# Düğüm renkleri
node_colors = [cluster_colors[filtered_data.loc[node, 'DBSCAN_Cluster']] if filtered_data.loc[node, 'DBSCAN_Cluster'] != -1 else 'black' for node in G.nodes()]

# Grafiği çizme
nx.draw(G, pos, with_labels=False, node_size=50, edge_color="gray", node_color=node_colors, alpha=0.7)

plt.title("Student Similarity Graph (DBSCAN)")
plt.savefig("dbscan_similarity_graph.png")  # PNG olarak kaydetme
plt.show()

print("Görselleştirme PNG olarak kaydedildi: dbscan_similarity_graph.png")
