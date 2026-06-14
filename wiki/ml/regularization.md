---
title: Regularization
slug: regularization
tags: [regularization, ridge, lasso, bias-variance, generalization]
updated: 2026-06-14
---

# Regularization

Regularization은 훈련 오차만 줄이는 모델이 아니라, 보지 못한 데이터에서 잘 예측하는 모델을 만들기 위해 파라미터 크기나 모델 복잡도에 제약을 주는 방법입니다. 핵심 아이디어는 약간의 bias 증가를 허용하고 variance를 줄여 expected error를 낮추는 것입니다.

## 좋은 모델

설명 모델은 주어진 훈련 데이터를 잘 설명하고 training error를 줄이는 데 초점을 둡니다. 예측 모델은 test data 또는 unknown input에 대한 expected error를 줄이는 데 초점을 둡니다. 훈련을 계속하면 bias는 줄어들 수 있지만 variance 문제를 무시하면 overfitting이 발생합니다.

## 기본 형태

정규화된 목적함수는 일반적으로 기존 loss에 penalty를 더합니다.

```text
min_w Loss(w) + lambda * Penalty(w)
```

`lambda`는 훈련 정확도와 일반화 성능 사이의 trade-off를 조절합니다.

## Ridge Regression

Ridge regression은 linear regression에 L2-norm penalty를 더한 방식입니다.

```text
min_w MSE(w) + lambda * sum_j w_j^2
```

L2 제약은 weight를 전반적으로 작게 만들며, closed form solution을 가질 수 있습니다. `lambda`가 커질수록 estimator의 variance는 줄고 bias는 커지는 방향으로 움직입니다.

## Lasso Regression

Lasso, Least Absolute Shrinkage and Selection Operator는 L1-norm penalty를 사용합니다.

```text
min_w MSE(w) + lambda * sum_j |w_j|
```

L1 제약은 일부 파라미터를 정확히 0으로 만들 수 있어 feature selection 효과가 있습니다. 단, L1-norm은 0에서 미분 가능하지 않아 Ridge처럼 단순한 closed form solution을 기대하기 어렵고, 보통 최적화 기법으로 풉니다.

## Sources

- `raw/inbox/9_Regularization_260507_121409.pdf`
- `raw/extracted/9_Regularization_260507_121409.txt`

## 관련

- [[supervised-knn]]
- [[model-compression]]
- [[mlp]]
