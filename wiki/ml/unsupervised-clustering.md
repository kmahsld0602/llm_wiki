---
title: Unsupervised Learning and Clustering
slug: unsupervised-clustering
tags: [unsupervised-learning, clustering, k-means, dbscan, hierarchical-clustering]
updated: 2026-06-14
---

# Unsupervised Learning and Clustering

Unsupervised learning은 label 없이 데이터의 숨은 구조, 패턴, 군집, 표현을 찾는 학습 방식입니다. 이미지 segmentation, anomaly detection, recommender systems처럼 label이 부족하거나 raw data가 많은 상황에서 중요합니다.

## Clustering

Clustering은 주어진 샘플을 서로 다른 부분집합으로 묶는 작업입니다. 같은 cluster 안의 샘플은 유사해야 하고, 서로 다른 cluster의 샘플은 달라야 합니다. 이를 위해 Euclidean, Manhattan, cosine similarity, correlation, Mahalanobis distance 등 다양한 거리 척도를 사용합니다.

## 평가

- Sum of Squared Error, SSE: 각 샘플과 소속 centroid 사이의 거리 제곱합입니다.
- Silhouette score: 같은 cluster 안의 평균 거리와 가장 가까운 다른 cluster까지의 평균 거리를 비교합니다.
- Elbow point: cluster 수를 바꿔가며 loss 감소가 둔화되는 지점을 찾습니다.

## K-Means

K-Means는 대표적인 centroid-based clustering 알고리즘입니다. cluster 수 `k`를 먼저 정하고, 각 샘플을 가장 가까운 centroid에 할당한 뒤, 각 cluster의 평균으로 centroid를 갱신합니다. membership이 더 이상 바뀌지 않을 때까지 이 과정을 반복합니다.

장점은 구현이 쉽고 직관적이며 scalability가 좋고 수렴이 보장된다는 점입니다. 단점은 좋은 `k`를 찾기 어렵고, 초기 centroid에 결과가 영향을 받으며, outlier와 다양한 밀도/형상의 cluster에 약하다는 점입니다.

## DBSCAN

DBSCAN은 density-based clustering 방법입니다. 주요 하이퍼파라미터는 이웃으로 볼 최대 거리 `eps`와 core point가 되기 위한 최소 이웃 수 `min_samples`입니다.

- Core point: `eps` 안의 이웃 수가 `min_samples` 이상인 점입니다.
- Border point: core point는 아니지만 cluster에 연결될 수 있는 점입니다.
- Noise point: 충분한 이웃이 없어 어떤 cluster에도 속하지 않는 점입니다.

DBSCAN은 cluster 수를 미리 정하지 않아도 되고 outlier를 식별할 수 있습니다. 하지만 cluster 밀도가 크게 다르거나 neck-type cluster가 있거나 고차원 데이터인 경우 실패할 수 있습니다.

## Hierarchical Clustering

Hierarchical clustering은 cluster가 서로 중첩되는 계층 구조를 찾습니다. Bottom-up 방식은 agglomerative clustering, top-down 방식은 divisive clustering입니다. Agglomerative clustering에서는 cluster 사이 거리를 single link, complete link, average link 같은 linkage 기준으로 계산합니다.

## Sources

- `raw/inbox/10_Unsupervised Learning 1_260512_130055.pdf`
- `raw/inbox/10_Unsupervised Learning 1_260514_122058.pdf`
- `raw/extracted/10_Unsupervised Learning 1_260512_130055.txt`
- `raw/extracted/10_Unsupervised Learning 1_260514_122058.txt`

## 관련

- [[dimensionality-reduction-pca]]
- [[supervised-knn]]
