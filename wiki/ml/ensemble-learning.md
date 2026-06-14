---
title: Ensemble Learning
slug: ensemble-learning
tags: [ensemble, bagging, boosting, stacking, model-merging]
updated: 2026-06-14
---

# Ensemble Learning

Ensemble learning은 여러 모델, 또는 weak learner를 같은 문제에 대해 학습시키고 그 예측을 결합해 단일 모델보다 나은 결과를 얻으려는 machine learning paradigm입니다. 단순 voting, weighted average, input-dependent gating, stacking처럼 다양한 결합 방식이 있습니다.

## 왜 여러 모델을 쓰는가

서로 다른 모델이 서로 다른 실수를 한다면, 예측을 결합했을 때 전체 성능이 좋아질 수 있습니다. Ensemble의 핵심은 diversity입니다.

- 어려운 pattern 때문에 생기는 실수는 여러 모델을 결합해 줄일 수 있습니다.
- Overfitting은 서로 다른 training dataset을 사용해 완화할 수 있습니다.
- Noisy feature 문제는 서로 다른 input feature subset을 사용해 완화할 수 있습니다.

## Bagging

Bagging, Bootstrap Aggregation은 훈련 데이터에서 replacement sampling으로 여러 subset을 만들고, 각 subset에서 독립적인 모델을 학습한 뒤 voting이나 averaging으로 결과를 결합합니다.

장점은 구현이 단순하고 weak learner들이 독립적이라 병렬화가 쉽다는 점입니다. 단점은 여러 모델을 학습해야 해 계산 비용이 크고, 평균화된 모델의 내부 의사결정을 해석하기 어렵다는 점입니다.

## Boosting

Boosting은 weak learner들을 독립적으로 학습하지 않고 순차적으로 연결합니다. 이전 learner가 틀린 데이터에 더 집중하도록 다음 learner를 학습시키며, 단계별로 예측을 강화합니다.

장점은 각 learner가 이전 실패를 보완하므로 상대적으로 작은 모델로도 성능을 높일 수 있다는 점입니다. 단점은 순차 의존성 때문에 병렬화가 어렵고, 일부 경우 overfitting 논쟁이 있다는 점입니다.

## Stacking

Stacking은 여러 base model의 예측을 다시 입력으로 받아 meta model을 학습합니다. Bagging보다 일반화된 형태로 볼 수 있으며, meta model은 보통 regression task에서는 linear regression, classification task에서는 logistic regression처럼 단순한 모델을 쓰는 경우가 많습니다.

## 현대적 연결

Ensemble의 diversity 아이디어는 Mixture-of-Experts, multi-agent systems, model merging, model soup 같은 최신 연구와도 연결됩니다. Model merging은 독립적으로 학습된 neural network weight를 loss landscape에서 연결하거나 평균하는 방식으로 inference 비용을 늘리지 않고 성능을 얻으려는 접근입니다.

## Sources

- `raw/inbox/13_Ensemble Learning_260528_125950.pdf`
- `raw/extracted/13_Ensemble Learning_260528_125950.txt`

## 관련

- [[mlp]]
- [[model-compression]]
- [[transformer]]
