---
title: Dimensionality Reduction and PCA
slug: dimensionality-reduction-pca
tags: [unsupervised-learning, dimensionality-reduction, pca, representation-learning]
updated: 2026-06-14
---

# Dimensionality Reduction and PCA

Dimensionality reduction은 고차원 데이터에서 더 낮은 차원의 유용한 표현을 찾는 과정입니다. 문서 분류처럼 feature가 수천 개 이상이거나, brain imaging처럼 위치와 시간 축이 결합된 데이터에서는 모든 feature를 그대로 쓰는 것이 항상 도움이 되지 않습니다.

## PCA의 목적

Principal Component Analysis, PCA는 고차원 데이터에서 hidden lower-dimensional structure를 찾는 비지도학습 기법입니다. 데이터 시각화, 시간/메모리/통신 비용 절감, 일반화 성능 개선, 노이즈 제거에 사용할 수 있습니다.

PCA는 데이터를 더 낮은 차원 subspace로 projection합니다. 이때 projection 방향은 데이터 variance를 최대화하는 방향, 즉 principal component입니다.

## 주요 가정

- Linearity: 데이터 구조를 선형 변환과 basis change로 다룰 수 있다고 가정합니다.
- Large variance is important: 큰 variance는 의미 있는 signal이고 작은 variance는 noise일 가능성이 높다고 봅니다.
- Orthogonality: principal components는 서로 직교하며, 중복이 적은 minimal representation을 만듭니다.

## 문제 정의

데이터 행렬 `X`를 더 informative한 표현 `Y`로 바꾸는 orthonormal matrix `P`를 찾습니다.

```text
Y = P X
```

목표는 `Y`의 covariance matrix가 diagonal matrix가 되도록 하는 것입니다. 이는 변환된 feature들이 서로 covariance가 0인 독립적인 방향을 갖는다는 뜻입니다.

## Eigenvector Decomposition

PCA는 covariance matrix의 eigenvector를 principal component로 사용합니다. Eigenvalue는 해당 principal component 방향의 variance를 나타냅니다. 차원을 줄일 때는 eigenvalue가 큰 component부터 선택해 데이터를 projection합니다.

## 장단점

- 장점: 노이즈 제거, 차원 축소, 시각화 개선에 유용합니다.
- 단점: 변수 scaling에 민감하고, 선형성/variance 중심의 강한 가정에 의존하며, 큰 데이터에서는 계산 비용이 커질 수 있습니다.

## Sources

- `raw/inbox/11_Unsupervised Learning 2_260514_125426.pdf`
- `raw/inbox/11_Unsupervised Learning 2_260519_124332.pdf`
- `raw/extracted/11_Unsupervised Learning 2_260514_125426.txt`
- `raw/extracted/11_Unsupervised Learning 2_260519_124332.txt`

## 관련

- [[unsupervised-clustering]]
- [[model-compression]]
