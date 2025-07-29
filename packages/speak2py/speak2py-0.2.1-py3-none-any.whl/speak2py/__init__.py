import os
import re
import time
import logging
import pandas as pd
from .file_reader import load_data

# Force non-interactive backend for plotting
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Union

# —— Google GenAI SDK ——
import google.genai as genai

# Set up logging
def get_logger():
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(h)
    logger.setLevel(logging.INFO)
    return logger
logger = get_logger()

# In-memory metrics
_METRICS = {
    "llm_calls": 0,
    "llm_errors": 0,
    "exec_errors": 0,
    "llm_latency": [],
    "exec_latency": [],
}

# Initialize the GenAI Client for Vertex AI
CLIENT = genai.Client(
    vertexai=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
)
MODEL = "gemini-2.5-flash"  # or another supported Gemini model


def _regex_speak2py(command: str) -> Union[pd.DataFrame, plt.Axes]:
    """
    Fallback: simple regex loader + head/describe
    """
    m = re.search(
        r"^(?:read|load)\s+(?:data\s+from\s+)?(?:file\s+)?['\"](?P<path>[^'\"]+)['\"]",
        command, re.IGNORECASE
    )
    if not m:
        raise ValueError(f"Could not parse command: {command!r}")
    df = load_data(m.group("path"))
    # head
    hh = re.search(r"\band\s+head\s+(\d+)", command, re.IGNORECASE)
    if hh:
        df = df.head(int(hh.group(1)))
    # describe
    if re.search(r"\band\s+describe\b", command, re.IGNORECASE):
        return df.describe()
    return df


def speak2py(command: str) -> Union[pd.DataFrame, plt.Axes]:
    """
    Main entry: try LLM → exec; fallback to regex if load commands or errors.
    """
    system = (
        "You are a Python interpreter assistant.\n"
        "Generate Python code using load_data(path) to load data, "
        "pandas (as pd) for DataFrame ops, and matplotlib.pyplot (as plt) for plotting.\n"
        "Assign the final DataFrame or Axes to `result`.\n"
        "Return ONLY the Python code, no commentary or fences."
    )
    prompt = f"{system}\nUser: {command}"

    # 1) Call LLM
    _METRICS["llm_calls"] += 1
    t0 = time.time()
    try:
        resp = CLIENT.models.generate_content(model=MODEL, contents=prompt)
        ll = time.time() - t0
        _METRICS["llm_latency"].append(ll)
        code_raw = getattr(resp, "text", str(resp))
    except Exception as e:
        _METRICS["llm_errors"] += 1
        logger.error("LLM failed: %s", e, exc_info=True)
        if command.strip().lower().startswith(("read", "load")):
            logger.warning("Falling back to regex on LLM error for: %s", command)
            return _regex_speak2py(command)
        raise

    # 2) Strip fences
    m = re.search(r"```(?:python)?\n([\s\S]+?)```", code_raw)
    code = m.group(1) if m else code_raw

    # 3) Execute
    t1 = time.time()
    try:
        g = {"load_data": load_data, "pd": pd, "plt": plt}
        l = {}
        exec(code, g, l)
        ex = time.time() - t1
        _METRICS["exec_latency"].append(ex)
    except Exception as e:
        _METRICS["exec_errors"] += 1
        logger.error("Exec failed: %s", e, exc_info=True)
        if command.strip().lower().startswith(("read", "load")):
            logger.warning("Falling back to regex on exec error for: %s", command)
            return _regex_speak2py(command)
        raise

    # 4) Return result if given
    if "result" in l:
        logger.info(
            "Success: %s | LLM: %.3fs | Exec: %.3fs",
            command, _METRICS["llm_latency"][-1], _METRICS["exec_latency"][-1]
        )
        return l["result"]

    # 5) Missing result fallback: count as exec_error
    if command.strip().lower().startswith(("read", "load")):
        _METRICS["exec_errors"] += 1
        logger.warning("No `result`; falling back to regex for: %s", command)
        return _regex_speak2py(command)

    # 6) Hard failure
    raise RuntimeError("Generated code did not set `result`.")
