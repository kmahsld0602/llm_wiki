---
title: K-Nearest Neighbors
slug: supervised-knn
tags: [supervised-learning, knn, lazy-learning, distance-metric]
updated: 2026-06-14
---

# K-Nearest Neighbors

K-Nearest Neighbors, KNN은 별도의 명시적 모델을 학습하기보다, 새 데이터가 들어왔을 때 훈련 데이터 중 가장 가까운 `k`개 이웃을 찾아 예측하는 지도학습 알고리즘입니다. 회귀에서는 가까운 이웃들의 평균값을, 분류에서는 다수 클래스를 반환합니다.

## 핵심 절차

1. 훈련 데이터 포인트를 저장합니다.
2. 새 데이터 포인트와 각 훈련 샘플 사이의 거리를 계산합니다.
3. 가장 가까운 `k`개 샘플을 고릅니다.
4. 회귀는 평균, 분류는 다수결로 출력을 정합니다.

## 특징

- Instance-based learning: 관측치 자체를 기반으로 예측합니다.
- Memory-based learning: 전체 훈련 데이터를 메모리에 보관해야 합니다.
- Lazy learning: 훈련 시점에 일반화 함수를 만들지 않고, 질의가 들어온 뒤 이웃 탐색을 수행합니다.

## 하이퍼파라미터

- `k`: 너무 작으면 개별 샘플과 노이즈에 민감하고, 너무 크면 국소 구조를 잃을 수 있습니다.
- 거리 척도: Euclidean, Manhattan, Hamming, cosine distance 등 문제와 데이터 표현에 맞는 척도를 골라야 합니다.
- 정규화: 거리 기반 알고리즘이므로 큰 스케일의 feature가 다른 feature를 압도하지 않게 feature scaling이 중요합니다.

## Weighted KNN

Weighted KNN은 가까운 이웃에 더 큰 가중치를 부여합니다. 예를 들어 거리의 역수를 weight로 쓰면 멀리 있는 이웃보다 가까운 이웃의 예측 영향이 커지고, 노이즈가 섞인 데이터에서 더 견고한 결과를 낼 수 있습니다.

## Eager Learning과의 비교

Eager learning은 SVM처럼 훈련 중 일반화 함수를 만들고 추론을 빠르게 수행합니다. Lazy learning은 KNN처럼 훈련 비용은 작지만 추론 때 전체 데이터 탐색과 거리 계산이 필요합니다.

## 장단점

- 장점: 구현이 단순하고 직관적이며, 큰 데이터셋에서는 노이즈에 비교적 강하게 동작할 수 있습니다.
- 단점: `k`와 거리 척도 선택에 민감하고, 추론 비용이 커질 수 있으며, 데이터 스케일링을 하지 않으면 일부 feature가 거리 계산을 지배합니다.

## Sources

- `raw/inbox/8_Supervised Learning 4_260430_122228.pdf`
- `raw/extracted/8_Supervised Learning 4_260430_122228.txt`

## 관련

- [[regularization]]
- [[unsupervised-clustering]]
