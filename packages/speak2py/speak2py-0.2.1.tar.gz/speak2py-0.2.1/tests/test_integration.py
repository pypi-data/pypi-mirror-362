import os
import re
import pandas as pd
import pytest
from speak2py import speak2py, CLIENT
from speak2py import _METRICS

# A dummy response object to mimic the GenAI SDK
class DummyResponse:
    def __init__(self, text):
        self.text = text

@pytest.fixture(autouse=True)
def clear_metrics():
    # reset in-memory metrics before each test
    for k in _METRICS:
        if isinstance(_METRICS[k], list):
            _METRICS[k].clear()
        else:
            _METRICS[k] = 0
    yield

def test_golden_prompt_load_and_head(monkeypatch, tmp_path):
    # Write a small CSV
    csv = tmp_path / "data.csv"
    df_orig = pd.DataFrame({"x": [10,20,30]})
    csv.write_text(df_orig.to_csv(index=False))

    # Stub GenAI to return code that loads & heads
    code = f"```python\nresult = load_data(r'{csv}') .head(1)\n```"
    monkeypatch.setattr(
        CLIENT.models, "generate_content",
        lambda model, contents: DummyResponse(text=code)
    )

    result = speak2py(f"read the file '{csv}' and head 1")
    # Should match the first row of the original
    pd.testing.assert_frame_equal(result, df_orig.head(1))

    # Metrics should record one successful LLM call and exec
    assert _METRICS["llm_calls"] == 1
    assert _METRICS["llm_errors"] == 0
    assert _METRICS["exec_errors"] == 0
    assert len(_METRICS["llm_latency"]) == 1
    assert len(_METRICS["exec_latency"]) == 1

def test_golden_prompt_manual_dataframe(monkeypatch):
    # Stub GenAI to return code constructing its own DataFrame
    code = (
        "```python\n"
        "import pandas as pd\n"
        "result = pd.DataFrame({'a':[1,2,3],'b':['x','y','z']})\n"
        "```"
    )
    monkeypatch.setattr(
        CLIENT.models, "generate_content",
        lambda model, contents: DummyResponse(text=code)
    )

    df = speak2py("build a dataframe with columns a and b")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["a", "b"]
    assert list(df["a"]) == [1,2,3]

def test_failure_mode_missing_result(monkeypatch, tmp_path):
    # GenAI returns code without setting `result`
    monkeypatch.setattr(
        CLIENT.models, "generate_content",
        lambda model, contents: DummyResponse(text="```python\nx=1\n```")
    )
    # Fallback should kick in for read commands
    csv = tmp_path / "f.csv"
    csv.write_text("m,n\n5,6\n")
    df = speak2py(f"read file '{csv}'")
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["m","n"]

    # Should have recorded one exec error
    assert _METRICS["exec_errors"] == 1

def test_failure_mode_llm_exception(monkeypatch, tmp_path):
    # GenAI client raises an exception
    def boom(model, contents):
        raise RuntimeError("LLM is down")
    monkeypatch.setattr(CLIENT.models, "generate_content", boom)

    # Fallback to regex for load commands
    csv = tmp_path / "g.csv"
    csv.write_text("p,q\n7,8\n")
    df = speak2py(f"load '{csv}'")
    assert isinstance(df, pd.DataFrame)
    assert list(df["p"]) == [7]

    # Should have recorded one LLM error
    assert _METRICS["llm_errors"] == 1
