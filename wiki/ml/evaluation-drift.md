---
title: Evaluation Drift
slug: evaluation-drift
tags: [evaluation, monitoring, dataset-shift]
updated: 2026-06-14
---

# Evaluation Drift

Evaluation drift는 모델을 평가하는 기준이나 데이터 분포가 시간이 지나며 실제 사용 상황과 어긋나는 현상입니다.

## 예시

- benchmark 점수는 좋아졌지만 실제 사용자 질문에서는 답변 품질이 낮아지는 경우
- 학습 당시 데이터와 배포 이후 데이터 분포가 달라지는 경우
- 새로운 모델 기능이 기존 평가 지표로는 충분히 측정되지 않는 경우

## Wiki 변경 관점

머신러닝 Wiki는 모델 설명뿐 아니라 평가 기준의 변화도 기록해야 합니다. 새 page가 추가될 때 "어떤 평가 방식으로 검증했는가"를 함께 기록해야 합니다.

## 관련

- [[rag]]
- [[model-compression]]
