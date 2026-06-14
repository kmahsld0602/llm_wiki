---
title: Retrieval-Augmented Generation
slug: rag
tags: [retrieval, generation, knowledge-update]
updated: 2026-06-14
---

# Retrieval-Augmented Generation

RAG는 모델이 답변을 생성하기 전에 외부 문서나 Wiki page를 검색하고, 검색된 근거를 prompt context로 사용해 답변하는 방식입니다.

## 왜 필요한가

모델 파라미터에 저장된 지식은 갱신 비용이 높습니다. 반면 Wiki나 문서 저장소는 page를 수정하는 방식으로 빠르게 갱신할 수 있습니다. RAG는 이 두 방식을 연결합니다.

## LLM Wiki와의 차이

RAG는 검색된 문서를 답변에 활용하는 실행 패턴입니다. LLM Wiki는 문서 자체를 장기적으로 유지보수하는 지식 운영 패턴입니다. 따라서 Wiki는 RAG의 원천 지식이 될 수 있지만, Wiki의 핵심은 page 병합, 출처, 변경 로그, 검토 기록입니다.

## 관련

- [[evaluation-drift]]
- [[transformer]]
