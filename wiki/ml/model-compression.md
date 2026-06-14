---
title: Model Compression
slug: model-compression
tags: [optimization, quantization, distillation]
updated: 2026-06-14
---

# Model Compression

Model compression은 모델 성능을 가능한 유지하면서 크기, 지연 시간, 메모리 사용량을 줄이는 기법입니다.

## 대표 기법

- Quantization: weight나 activation을 낮은 정밀도로 표현합니다.
- Pruning: 중요도가 낮은 weight나 구조를 제거합니다.
- Distillation: 큰 teacher model의 행동을 작은 student model에 학습시킵니다.

## Wiki 변경 관점

새로운 압축 기법이 등장하면 단순히 성능 수치만 기록하지 않고, 어떤 하드웨어와 배포 조건에서 유효한지 함께 기록해야 합니다.

## 관련

- [[transformer]]
- [[evaluation-drift]]
