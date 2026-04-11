---
TITLE: Gemma 4 model card | Google AI for Developers
CONTENT: 
Gemma 4 is a family of open multimodal models by Google DeepMind.
Context Window: 128K (E2B/E4B) to 256K (26B/31B).
Languages: 140+ pre-trained, 35+ out-of-the-box.

Model Specs:
- E2B: 2.3B effective, 128K context, Text/Image/Audio
- E4B: 4.5B effective, 128K context, Text/Image/Audio
- 26B A4B (MoE): 25.2B total, 3.8B active, 256K context, Text/Image
- 31B Dense: 30.7B total, 256K context, Text/Image

Architecture:
- Hybrid attention: local sliding window (512-1024) interleaved with full global attention.
- Unified Keys/Values (MQA/GQA) and Proportional RoPE for long context efficiency.

Capabilities:
- Reasoning (Thinking mode <|think|>)
- Multi-turn chat with native system role.
- Interleaved multimodal input.
- Function calling & Agentic workflows.

Sampling: temperature=1.0, top_p=0.95, top_k=64.
---
