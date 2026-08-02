import os
import requests
import eel
import ast
import datetime
import re

# Hugging Face token (optional)
# Read tokens at import time as defaults; prefer checking env at call time below.
HF_TOKEN = os.environ.get('HF_API_TOKEN')
# Default model used for instruction-style responses via Hugging Face Inference API
HF_MODEL = os.environ.get('HF_MODEL', 'google/flan-t5-large')

# Gemini / Google Generative Models API key (can be set at runtime via UI)
# module-level fallback key; prefer checking env at call time so changes take effect
GEMINI_KEY = os.environ.get('GOOGLE_API_KEY')
# Default Gemini model endpoint (chat-bison family). Update if needed.
GEMINI_MODEL = os.environ.get('GOOGLE_GEMINI_MODEL', 'chat-bison-001')


def get_chat_response(prompt: str, max_tokens: int = 150) -> str:
    """Return a chat-style response for `prompt`.

    Uses the Hugging Face Inference API when `HF_API_TOKEN` is present. Otherwise returns
    a helpful fallback message explaining how to enable the feature.
    """
    prompt = prompt.strip()
    if not prompt:
        return "I'm here — ask me anything!"

    # Prefer Gemini if API key supplied (check current env or module-level key)
    current_gemini = os.environ.get('GOOGLE_API_KEY') or GEMINI_KEY
    current_hf = os.environ.get('HF_API_TOKEN') or HF_TOKEN

    if current_gemini:
        resp = gemini_generate(prompt, max_tokens, api_key=current_gemini)
        if _is_error_response(resp):
            return _local_fallback(prompt)
        return resp

    if not current_hf:
        return _local_fallback(prompt)

    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Accept": "application/json"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # The inference API can return several formats. Try common ones.
        if isinstance(data, dict) and 'error' in data:
            return "Model error: " + str(data.get('error'))
        if isinstance(data, list) and len(data) > 0:
            first = data[0]
            if isinstance(first, dict) and 'generated_text' in first:
                return first['generated_text']
            if isinstance(first, str):
                return first
        if isinstance(data, dict) and 'generated_text' in data:
            return data['generated_text']
        # Fallback to string representation
        result = str(data)
        if _is_error_response(result):
            return _local_fallback(prompt)
        return result
    except Exception as e:
        # If HF is unreachable, return a local fallback reply instead
        return _local_fallback(prompt)


def gemini_generate(prompt: str, max_tokens: int = 150, api_key: str | None = None) -> str:
    """Call Google generative models REST endpoint using an API key.

    This uses the simple API-key-based endpoint. It keeps the key in memory
    (module-level `GEMINI_KEY`) and does not persist it to disk.
    """
    global GEMINI_MODEL
    key = api_key or os.environ.get('GOOGLE_API_KEY') or GEMINI_KEY
    if not key:
        return "Gemini API key not set."

    # Construct a lightweight request for the chat model. The exact schema
    # may differ by model/version; this is a commonly supported pattern.
    # Try the chat-style generateMessage endpoint first, then fall back to a
    # generic :generate endpoint if the model/version expects that.
    # Try several endpoint hostnames and payload shapes that have been observed
    endpoints = [
        # Newer generativelanguage endpoints
        (f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generate?key={key}",
         {"prompt": {"text": prompt}, "temperature": 0.2, "maxOutputTokens": max_tokens}),
        (f"https://generativelanguage.googleapis.com/v1beta2/models/{GEMINI_MODEL}:generate?key={key}",
         {"prompt": {"text": prompt}, "temperature": 0.2, "maxOutputTokens": max_tokens}),
        # Older generativemodels style endpoints
        (f"https://generativemodels.googleapis.com/v1/models/{GEMINI_MODEL}:generateMessage?key={key}",
         {"prompt": {"messages": [{"author": "user", "content": prompt}]}, "temperature": 0.2, "maxOutputTokens": max_tokens}),
        (f"https://generativemodels.googleapis.com/v1/models/{GEMINI_MODEL}:generate?key={key}",
         {"prompt": {"text": prompt}, "temperature": 0.2, "maxOutputTokens": max_tokens}),
        (f"https://generativemodels.googleapis.com/v1/models/{GEMINI_MODEL}:generate?key={key}",
         {"input": prompt, "temperature": 0.2, "maxOutputTokens": max_tokens}),
    ]
    headers = {"Content-Type": "application/json"}
    try:
        data = None
        resp = None
        for url, payload in endpoints:
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=30)
                if resp.status_code == 404:
                    # endpoint not found for this model; try next
                    continue
                resp.raise_for_status()
                data = resp.json()
                break
            except requests.HTTPError as he:
                # if 404 try next endpoint, otherwise propagate to outer handler
                if resp is not None and resp.status_code == 404:
                    continue
                return f"Failed to contact Gemini API: {he}"
            except Exception as e:
                return f"Failed to contact Gemini API: {e}"
        # If we never received any JSON data from the endpoints, return a helpful message
        if data is None:
            if resp is not None:
                # include a short snippet of the last response for debugging
                body = getattr(resp, 'text', '') or ''
                return f"Gemini returned no JSON (status {getattr(resp,'status_code',None)}). Response snippet: {body[:200]}"
            return "Gemini returned no response from any tried endpoint."

        # Try to extract a text candidate from the response
        if isinstance(data, dict):
            # common field: candidates -> list of {content}
            cands = data.get('candidates') or data.get('response', {}).get('candidates') or data.get('outputs')
            if isinstance(cands, list) and len(cands) > 0:
                first = cands[0]
                # candidate may be dict with 'content' or 'message' or 'text'
                if isinstance(first, dict):
                    # direct text
                    if 'text' in first:
                        return first['text']
                    if 'content' in first:
                        content = first['content']
                        if isinstance(content, str):
                            return content
                        if isinstance(content, dict):
                            return content.get('text') or str(content)
                    if 'message' in first and isinstance(first['message'], dict):
                        msg = first['message']
                        txt = None
                        # common place
                        if isinstance(msg.get('content'), dict):
                            txt = msg.get('content', {}).get('text')
                        if txt:
                            return txt
                elif isinstance(first, str):
                    return first
            # Some responses include `candidates` under `message` or `content` deeper
            # Try direct message content
            if 'message' in data and isinstance(data['message'], dict):
                m = data['message']
                if isinstance(m.get('content'), dict):
                    return m.get('content', {}).get('text') or str(m.get('content'))
            # Try `output` style
            if 'output' in data:
                out = data['output']
                if isinstance(out, str):
                    return out
        # Fallback: return JSON string
        return str(data)
    except Exception as e:
        return f"Failed to contact Gemini API: {e}"


def _is_error_response(resp: object) -> bool:
    """Return True if the response looks like an error or diagnostic string."""
    if resp is None:
        return True
    if not isinstance(resp, str):
        return False
    s = resp.strip().lower()
    if not s:
        return True
    errs = ["failed", "error", "no json", "not found", "unable to", "returned no"]
    return any(e in s for e in errs)


def _local_fallback(prompt: str) -> str:
    """Best-effort local responder when external APIs are unavailable.

    Capabilities:
    - simple arithmetic expressions (safe eval)
    - current time/date
    - small canned replies
    - otherwise a helpful offline notice
    """
    q = prompt.strip()
    # math: detect simple arithmetic questions like '2+2' or 'what is 2+2?'
    expr = q.lower()
    expr = re.sub(r"\b(what is|calculate|evaluate|equals|=|please|answer)\b", "", expr)
    expr = expr.strip(' ?.!')
    if expr and re.fullmatch(r"[0-9\s+\-*/%().]+", expr):
        try:
            val = _safe_eval(expr)
            return str(val)
        except Exception:
            pass

    # time/date
    if re.search(r"\btime\b", q, re.I):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if re.search(r"\bdate\b", q, re.I):
        return datetime.datetime.now().strftime("%Y-%m-%d")

    # identity
    if re.search(r"\bwho (are|r) you\b", q, re.I) or re.search(r"\bwhat are you\b", q, re.I):
        return "I'm your local Sophia assistant. I can open apps, run shortcuts, and answer simple local questions when offline."

    # common conversational/general-knowledge fallbacks
    if re.search(r"\bjoke\b", q, re.I):
        return "Why did the computer go to the doctor? Because it had a virus. A classic, slightly dusty, but it still boots."

    if re.search(r"\bmachine learning\b", q, re.I):
        return (
            "Machine learning is a branch of artificial intelligence where computers learn patterns from data "
            "and use those patterns to make predictions or decisions without being explicitly programmed for every case."
        )

    if re.search(r"\bphotosynthesis\b", q, re.I):
        return (
            "Photosynthesis is the process plants use to make food. They take in sunlight, water, and carbon dioxide, "
            "then produce glucose for energy and release oxygen."
        )

    if re.search(r"\bsky\b", q, re.I) and re.search(r"\bblue\b", q, re.I):
        return (
            "The sky looks blue because air molecules scatter shorter blue wavelengths of sunlight more than longer red wavelengths. "
            "That scattered blue light reaches your eyes from all directions."
        )

    # help with commands
    if re.search(r"\b(open|launch|start)\b", q, re.I):
        return (
            "I can open: notepad, youtube (in browser), github, whatsapp, instagram, calculator, "
            "facebook, telegram, canva, chrome, vscode, filemanager, commandprompt. Say 'open <name>'."
        )

    # Fallback message
    return (
        "I'm currently offline and can't reach cloud models. I can still answer simple math and time queries, "
        "or perform local actions (open apps). For full conversational replies, ensure internet access and valid API keys."
    )


def _safe_eval(expr: str):
    """Safely evaluate a simple arithmetic expression using ast."""
    node = ast.parse(expr, mode='eval')

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
                     ast.USub, ast.UAdd, ast.Load, ast.BitXor)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError("Unsafe expression")

    return eval(compile(node, '<string>', 'eval'), {'__builtins__': {}})


@eel.expose
def set_gemini_key(key: str, remember: bool = False):
    """Set the Gemini API key in memory. If `remember` is True, the UI may
    also persist it to localStorage (optional). The key is NOT written to disk.
    """
    global GEMINI_KEY
    GEMINI_KEY = key
    return True
