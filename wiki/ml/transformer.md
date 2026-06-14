---
title: Transformer
slug: transformer
tags: [architecture, attention, foundation-model]
updated: 2026-06-14
---

# Transformer

Transformer는 self-attention을 중심으로 sequence 정보를 처리하는 모델 구조입니다. recurrent 구조에 의존하지 않고 token 간 관계를 병렬적으로 계산할 수 있어 대규모 언어 모델과 멀티모달 모델의 기반이 되었습니다.

## 핵심 아이디어

- Self-attention은 각 token이 다른 token을 얼마나 참고해야 하는지 계산합니다.
- Positional encoding은 순서 정보를 보완합니다.
- Encoder-decoder 구조는 번역 같은 sequence-to-sequence 작업에 쓰이며, decoder-only 구조는 언어 생성 모델에서 널리 사용됩니다.

## Wiki 변경 관점

Transformer page는 새로운 attention 변형, 효율화 기법, long context 구조가 등장할 때 갱신되어야 합니다.

## 관련

- [[rag]]
- [[model-compression]]
