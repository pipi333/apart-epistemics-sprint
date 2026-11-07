import json
import time
import urllib.request

MODELS = [
    ("antigravity/gemini-3.8-flash", "low"),
    ("antigravity/claude-sonnet-5-5", "medium"),
    ("codex/gpt-6.1-sol", "medium"),
    ("grok/grok-4.7-build-fast", "medium"),
    ("workbuddy/deepseek-v4.1-flash", "high"),
]

for m, eff in MODELS:
    t0 = time.time()
    body = {
        "model": m,
        "stream": False,
        "max_output_tokens": 512,
        "instructions": 'Reply ONLY with a valid JSON object: {"choice": "A", "confidence": 85}',
        "input": [{"role": "user", "content": [{"type": "input_text", "text": "Is 2+2=4 (A) or 5 (B)?"}]}],
        "reasoning": {"effort": eff},
    }
    req = urllib.request.Request(
        "http://127.0.0.1:3425/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(req, timeout=45) as r:
            d = json.loads(r.read().decode("utf-8"))
            txt = "".join(
                c.get("text", "")
                for o in d.get("output", [])
                if o.get("type") == "message"
                for c in o.get("content", [])
                if c.get("type") == "output_text"
            )
            print(f"OK | {m} ({eff}) | {time.time() - t0:.2f}s | served={d.get('model')} | out={txt.strip()[:80]}")
    except Exception as e:
        print(f"ERR | {m} ({eff}) | {e}")
