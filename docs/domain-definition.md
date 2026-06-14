# Wiki Domain Definition: Machine Learning

## 대상 지식 도메인

본 프로젝트의 Wiki 도메인은 **Machine Learning**입니다. 특정 수업명이나 기관명에 종속된 문서를 서빙하기보다, 독립적인 지식 관리 대상이 될 수 있는 머신러닝 개념을 Wiki로 구성했습니다.

머신러닝은 새로운 모델, 학습 방식, 평가 방식, 배포 전략이 빠르게 등장하는 분야입니다. 따라서 단순한 정적 요약 문서보다, source가 추가될 때 기존 page와의 관계를 추적하고 점진적으로 갱신할 수 있는 Wiki 구조가 적합합니다.

## 도메인 선택 이유

머신러닝 지식은 다음과 같은 이유로 Wiki 관리에 적합합니다.

- 개념 간 연결이 중요합니다. 예를 들어 MLP, regularization, ensemble learning, model compression은 서로 다른 주제지만 모델 일반화와 성능 개선이라는 공통 축으로 연결됩니다.
- 새로운 source가 들어올 때 기존 개념과 병합하거나 새 page를 만들지 판단해야 합니다.
- 알고리즘 설명뿐 아니라 평가, 데이터 분포 변화, 배포 비용, 모델 크기 같은 운영 관점도 함께 관리해야 합니다.
- 강의자료, 논문, 구현 노트처럼 다양한 source를 한 곳에서 추적할 수 있어야 합니다.

## Wiki가 관리할 지식 범위

이 Wiki는 다음 범위의 지식을 관리합니다.

- 지도학습: K-Nearest Neighbors, regression, classification
- 정규화와 일반화: bias-variance trade-off, Ridge, Lasso
- 비지도학습: clustering, K-Means, DBSCAN, hierarchical clustering
- 표현 학습: dimensionality reduction, PCA
- 신경망: perceptron, MLP, backpropagation, deep learning 기초
- 앙상블: bagging, boosting, stacking, model merging
- LLM 관련 확장 주제: Transformer, RAG, model compression, evaluation drift

## Wiki Page 구성 원칙

각 Wiki page는 Markdown 파일로 관리하며, front matter에 다음 정보를 포함합니다.

```yaml
---
title: Page Title
slug: page-slug
tags: [tag1, tag2]
updated: YYYY-MM-DD
---
```

본문은 다음 기준으로 작성합니다.

- 하나의 page는 하나의 핵심 개념을 다룹니다.
- source 기반으로 추가된 내용은 `Sources` 섹션에 원본 경로를 남깁니다.
- 관련 개념은 `[[slug]]` 형태의 내부 링크로 연결합니다.
- 단순 암기용 설명보다, 개념의 사용 이유와 trade-off를 함께 기록합니다.

## 시각화 방식

GUI는 세 영역으로 구성됩니다.

- 왼쪽 sidebar: 검색 입력과 page 목록
- 중앙 article view: 선택한 Wiki page의 Markdown 본문
- 오른쪽 chat panel: Wiki Agent에게 질문하고 source 기반 답변 확인

이 구조는 사용자가 page를 직접 탐색하는 방식과, 질문을 통해 관련 page를 찾는 방식을 모두 지원합니다.

## 평가 기준과의 연결

- 무엇을 만들 것인가: 머신러닝 지식을 관리하는 Wiki page와 이를 조회하는 MCP Tool을 만든다.
- 왜 만들 것인가: 머신러닝 지식은 source가 계속 추가되고 개념 간 연결이 중요하므로, 검색 가능하고 갱신 가능한 Wiki가 필요하다.
- 어떻게 만들 것인가: Markdown page, MCP Tool, GUI, Wiki Agent, raw source ingest workflow를 결합한다.
- 어떤 기능이 필요한가: page 목록, 검색, 본문 조회, 질문 응답, source 추적, merge request 생성 기능이 필요하다.

## Raw Source 반영 방식

새로운 PDF, Markdown, text source는 `raw/inbox`에 넣고 `scripts/ingest_raw.py`로 처리합니다. PDF는 텍스트로 추출되어 `raw/extracted`에 저장되고, `wiki/merge-queue`에 병합 검토 요청 문서가 생성됩니다.

최종 Wiki page 병합은 사람이 검토한 뒤 수행합니다. 이는 agent가 source를 잘못 해석해 기존 지식을 자동으로 덮어쓰는 위험을 줄이기 위한 결정입니다.
