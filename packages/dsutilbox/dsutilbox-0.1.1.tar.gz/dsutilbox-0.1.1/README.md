# dsutilbox

**dsutilbox** is a lightweight, modular Python package that provides reusable utilities for data science workflows.

It helps you speed up experimentation and maintain consistency across projects by organizing commonly used preprocessing, modeling, and evaluation functions.

## Features

- 🧹 Preprocessing: missing value handling.

## Installation

To install in editable (development) mode:

```bash
pip install -e .
```

Make sure you run this command from the root folder that contains the `pyproject.toml` file.

## Example Usage

```python
from dsutilbox.preprocessing import fill_missing_num_cols

# Example
df = fill_missing_num_cols(df, strategy="mean")
model = train_logistic(X_train, y_train)
```

## 📄 License

MIT License © 2025 Yuki Li
