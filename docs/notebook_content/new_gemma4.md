---
TITLE: gemma4
CONTENT: 
Gemma 4 models are designed to deliver frontier-level performance at each size. They are well-suited for reasoning, agentic workflows, coding, and multimodal understanding.
Vision   tools   thinking   audio   cloud   e2b   e4b   26b   31b

Applications:
- Claude Code: ollama launch claude --model gemma4
- Codex: ollama launch codex --model gemma4
- OpenClaw: ollama launch openclaw --model gemma4

Benchmark Results (31B Dense):
- MMLU Pro: 85.2%
- LiveCodeBench v6: 80.0%
- AIME 2026: 89.2%

Technical Advances:
- Native Thinking Mode (<|think|> token)
- Native System Prompt Support
- Variable Image Resolution
- 128K - 256K Context Windows

Configurations:
- temperature=1.0
- top_p=0.95
- top_k=64
---
