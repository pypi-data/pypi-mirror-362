# [LiteFlow Python SDK](https://liteflow.cloud)

**Access the best AI models with one unified API key — no tokens to juggle, no billing chaos, no compromises.**

LiteFlow lets you talk to top-tier LLMs like Claude, GPT, Mistral, and more — all through a single, resilient, and cost-efficient endpoint. The Python SDK is the easiest way to tap into that power in just a few lines.

---

## Why LiteFlow?

- **One key, every model**  
  Stop juggling API keys across 5 different dashboards. LiteFlow unifies the top LLMs under a single, clean interface.

- **Optimized for cost**  
  We've done the heavy-lifting optimzations to provide you with the cheapest cost on the market.

- **Intelligent fallback & resilience**  
  If a model is down or slow, LiteFlow seamlessly reroutes the request — so you never miss a beat.

- **Privacy-first**  
  No prompt logging, no training, no vendor lock-in. Your data stays yours.

---

## Quickstart

```bash
pip install liteflow-python
```

Then, in your code:

```python
from liteflow_python import LiteFlow

client = LiteFlow("<YOUR-API-KEY>")

response = client.chat_completion(
	messages=[{"role": "user", "content": """
Imagine a runaway trolley is hurtling down a track towards five dead people. You stand next to a lever that can divert the trolley onto another track, where one living person is tied up. Do you pull the lever?
Reason step-by-step to find the correct answer.
"""}],
  model="Claude Opus 4",
  max_tokens=1000
)
print(response)
```

---

## Features
- Simple chat_completions() interface
- Unified token usage tracking
- Transparent, simple and the most competitive pricing
- Built-in retries, fallbacks, and latency optimization

**Power Meets Simplicity**

Why waste time comparing models, managing budgets, and rewriting adapters?
Let LiteFlow be the layer between your app and LLM chaos — fast, cheap, and always online.

→ Install now and ship your next AI project with confidence.

---

## Community & Support
Need help? 
- [Contact us](mailto:contact@liteflow.cloud)
- [Join our Discord](https://discord.gg/sfRdZ9EAfg)
- [Open an issue](https://github.com/53gf4u1t/liteflow-python/issues)