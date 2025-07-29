<p align="center">
  <img src="assets/encourage_logo.png" alt="Encourage Logo" width="120" /><br />
  <span style="font-size: 2em; font-weight: bold;">EncouRAGe</span>
</p>

<p align="center">
  <b>the all-in one solution for evaluate RAG methods</b>. <br /> <br />
  <img src="https://img.shields.io/github/license/uhh-hcds/encourage" />
  <img src="https://img.shields.io/github/last-commit/uhh-hcds/encourage" />
  <img src="https://img.shields.io/github/issues/uhh-hcds/encourage" />
  <img src="https://img.shields.io/github/issues-pr/uhh-hcds/encourage" />
  <br />
  <img src="https://img.shields.io/badge/python-3.12-blue" />
  <img src="https://img.shields.io/badge/python-3.13-blue" />
</p>




This repository provides a flexible library for running local inference with or without context, leveraging a variety of popular LLM libraries for enhanced functionality:


- ⚙️ **[jinja2](https://github.com/pallets/jinja)**
  - Offers a template engine for dynamic prompt generation.
- 📝 **[mlflow](https://github.com/mlflow/mlflow)**
  - Designed to ensure observability of the model performance and tracing.
- 🔄 **[chroma](https://github.com/chroma-core/chroma)**
  - Strong in-memory vector database for efficient data retrieval.
- 🧭 **[qdrant](https://github.com/qdrant/qdrant)**
  - Supports robust vector search for efficient data retrieval.

---

### 🚀 Getting Started

```python
pip install encourage
```

To initialize the environment using `uv`, run the following command:

```bash
uv sync
```

### ⚡ Usage Inference Runners

For understanding how to use the inference runners, refer to the following tutorials:

- [ChatInferenceRunner](./docs/conversation.md)
- [BatchInferenceRunner](./docs/batch_inference.md)

### 🔍 RAG Methods

Encourage provides several RAG (Retrieval-Augmented Generation) methods to enhance your LLM responses with relevant context:

- [Overview of RAG Methods](./docs/rag_methods.md)

### 📊 Evaluation Metrics

Encourage offers a comprehensive set of metrics for evaluating LLM and RAG performance:

- [Metrics Overview](./docs/metrics_overview.md) - Table of all available metrics
- [Metrics Explanation](./docs/metrics_explanation.md) - Detailed explanations and formulas
- [Metrics Tutorial](./docs/metrics_tutorial.md) - Step-by-step guide to using metrics

### ⚙️ Custom Templates

To use a custom template for the inference, follow the steps below:

- [Create a custom template](./docs/templates.md)

### 📈 Model Tracking

For tracking the model performance, use the following commands:

- [Track the model](./docs/mlflow.md)
