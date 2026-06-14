---
title: Multi-Layer Perceptron
slug: mlp
tags: [neural-network, perceptron, mlp, backpropagation, deep-learning]
updated: 2026-06-14
---

# Multi-Layer Perceptron

Multi-Layer Perceptron, MLP는 여러 perceptron layer를 쌓은 feedforward neural network입니다. 단일 perceptron은 선형 분리 가능한 문제에 강하지만 XOR처럼 비선형 decision boundary가 필요한 문제에는 한계가 있습니다. MLP는 여러 선형 변환과 activation function을 조합해 비선형 mapping을 학습합니다.

## Perceptron

Perceptron은 binary classification을 위한 단순한 알고리즘입니다. 입력 벡터와 weight의 선형 결합에 bias를 더하고, 그 결과를 activation 또는 threshold function에 통과시켜 출력을 냅니다.

```text
z = w^T x + b
y = f(z)
```

AND, OR, NAND 같은 선형 분리 가능한 논리 함수는 perceptron으로 표현할 수 있지만, XOR은 단일 perceptron으로 표현할 수 없습니다.

## Activation Function

- Sigmoid: 확률적 출력에 자주 사용됩니다.
- Tanh: 이진 분류 맥락에서 사용할 수 있습니다.
- ReLU: 현대 neural network에서 널리 쓰이며 계산이 단순합니다.

## MLP가 필요한 이유

MLP는 hidden layer를 통해 여러 선형 모델의 조합을 만들고, 결과적으로 비선형 decision boundary를 표현할 수 있습니다. Layer 수와 각 layer의 neuron 수는 문제에 따라 달라지며, 모델 용량을 키우면 표현력은 커지지만 overfitting과 계산 비용도 함께 고려해야 합니다.

## Backpropagation

Backpropagation은 loss에 대한 각 parameter의 gradient를 network의 뒤쪽 layer에서 앞쪽 layer 방향으로 계산하는 알고리즘입니다. Forward propagation으로 activation을 계산하고, output layer에서 시작한 error signal을 chain rule로 hidden layer까지 전달합니다.

Gradient descent 학습은 다음 흐름을 반복합니다.

1. 모든 layer를 통과하며 activation을 계산합니다.
2. Loss를 기준으로 parameter gradient를 계산합니다.
3. Gradient를 사용해 parameter를 업데이트합니다.

## Deep Learning과의 연결

ANN은 보통 더 크고 깊은 MLP 계열 network를 가리키며, CNN, RNN, Transformer 같은 다양한 구조로 발전했습니다. Deep network는 hierarchical feature learning, 효율적인 parameter 활용, automatic feature extraction을 가능하게 합니다.

## Sources

- `raw/inbox/12_MLP_260528_120840.pdf`
- `raw/extracted/12_MLP_260528_120840.txt`

## 관련

- [[regularization]]
- [[transformer]]
- [[model-compression]]
