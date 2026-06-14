---
title: Machine Learning Wiki Index
slug: ml-index
tags: [index, machine-learning]
updated: 2026-06-14
---

# Machine Learning Wiki

이 Wiki는 빠르게 변하는 머신러닝 지식을 page 단위로 관리합니다. 목적은 개념 설명을 저장하는 것에 그치지 않고, 새 source가 들어왔을 때 기존 설명과 어떻게 연결되고 갱신되는지 추적하는 것입니다.

## 주요 Page

- [[supervised-knn]]: K-Nearest Neighbors, 거리 기반 lazy learning
- [[regularization]]: bias-variance trade-off, Ridge, Lasso 기반 일반화 전략
- [[unsupervised-clustering]]: K-Means, DBSCAN, hierarchical clustering
- [[dimensionality-reduction-pca]]: 고차원 데이터 표현 학습과 PCA
- [[mlp]]: perceptron, MLP, backpropagation, deep learning 기초
- [[ensemble-learning]]: bagging, boosting, stacking, model merging
- [[transformer]]: attention 기반 모델 구조의 기초
- [[rag]]: 검색 결과와 생성을 결합하는 지식 주입 패턴
- [[evaluation-drift]]: 평가 기준이 시간에 따라 낡아지는 현상
- [[model-compression]]: 모델을 작게 만들거나 빠르게 실행하는 방법

## 운영 원칙

새 자료가 들어오면 Agent가 기존 page를 검색하고 중복 개념과 갱신 후보를 먼저 제안합니다. 사람은 제안을 검토한 뒤 page를 병합합니다. 각 raw source 기반 page는 `Sources` 섹션에 원본 PDF와 추출 텍스트 경로를 남겨 추적 가능하게 유지합니다.
