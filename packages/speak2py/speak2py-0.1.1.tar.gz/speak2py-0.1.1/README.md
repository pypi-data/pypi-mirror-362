# Speak2Py

**Version:** MVP v0.1

---

## 🎯 Objective

Let users run **any** Python logic—data loading, analysis, plotting, even algorithm, data structures generation—by writing plain-English commands. The MVP proves out:

- **English→Python translation** via a hosted AI (Gemini on Vertex AI)
- **Safe execution** of the generated code and return of results
- **Zero-config UX**: no local AI models, no credentials, just install and run

---

## 📝 Overview

Speak2Py accepts natural-language prompts such as:

- “read file ‘data.csv’ and head 5”
- “plot x vs y from ‘data.csv’”
- “generate prime numbers up to 100 and assign to result”

Behind the scenes it:

1. Sends your prompt to a hosted FastAPI service on Cloud Run
2. Calls Gemini to produce a Python snippet assigning its output to `result`
3. Executes that snippet in a sandboxed namespace
4. Serializes and returns `result` as a DataFrame, list, or plot

End users simply:

```bash
pip install speak2py

```

---

## MVP Features (v0.1)

1. **Natural-Language Commands**

   - **CLI**:
     ```bash
     speak2py "read file 'data.csv' and head 5" --show
     ```
   - **Python API**:
     ```python
     from speak2py import speak2py
     df = speak2py("load 'data.csv' and describe")
     ```

2. **AI-Driven Code Generation**

   - Sends your English prompt to a hosted Gemini/Vertex AI service
   - Automatically generates and executes a Python snippet assigning the final object to `result`

3. **Zero-Config Deployment**

   - No GCP credentials or environment variables needed for end-users
   - All AI calls go through our Cloud Run service under our own service account

4. **Local Fallback**

   - If the AI service is unreachable, basic `read|load … + head|describe` still works via regex parsing

5. **File Loading**

   - Detects `.csv`, `.xls`, `.xlsx`, and `.json` by extension
   - Returns a `pandas.DataFrame`

6. **Plotting Support**

   - Generates histograms, scatter plots, line plots, etc.
   - Returns a `matplotlib.axes.Axes` for further customization

7. **CLI & Packaging Structure**

   - `cli.py` exposes the `speak2py` shell command
   - `src/speak2py/__init__.py` provides the `speak2py()` function

8. **Testing & Observability**
   - **Unit tests** for file loading and regex fallback
   - **Integration tests** for both CLI and Python API
   - Server logs LLM latency, execution time, and errors

---

## 📦 Installation

```bash
pip install speak2py
```

## MVP v0.3 Description

- **Purpose:**  
  Empower anyone to write and execute Python data‐analysis or algorithmic code using plain-English prompts—without installing AI libraries or managing credentials.

- **What’s Included:**

  - `speak2py(command: str) → DataFrame | Axes`  
    Sends your English command to a hosted AI service, executes the returned snippet, and returns the result.
  - **Local Regex Fallback**  
    For simple `read|load … + head|describe` commands when offline.
  - **File Formats**  
    `.csv`, `.xls`/`.xlsx`, `.json` automatically detected and loaded into pandas.
  - **Plotting**  
    Histogram, scatter, line‐plot support via matplotlib, returned as `Axes`.
  - **CLI Tool**  
    `speak2py "..." --show [--out file]` for shell usage.
  - **Zero-Config Deployment**  
    All AI inference happens on our Cloud Run endpoint—no GCP setup on the client side.
  - **Testing & Observability**  
    Unit tests (file loading, fallback) and integration tests (AI client + execution).  
    Server‐side logs of LLM latency, execution time, and errors.

- **Why It Matters:**  
  This MVP lays the groundwork for making Python coding accessible—non-developers can load data, visualize it, or even run algorithms (e.g. prime number generation) by simply typing what they want in English.

---

## Next Steps & Roadmap

1. **Extended Plot Types**  
   Boxplots, pivot‐tables, pairwise scatter‐matrix.

2. **More Data Sources**  
   Parquet, SQL databases, REST APIs, GCS buckets.

3. **Advanced Prompting**  
   Few‐shot examples, customizable templates, context retention.

4. **IDE/Notebook Integration**  
   JupyterMagics (e.g. `%%speak2py`), VS Code extension.

5. **User‐Defined Macros**  
   Let users define their own English→Python shortcuts.

6. **Security & Sandboxing**  
   Harden execution sandbox, validate generated code before running.

7. **Analytics & Usage Dashboard**  
   Track popular commands, lagging bottlenecks, error trends.

---

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## License

MIT © 2025 Speak2Py Contributors
