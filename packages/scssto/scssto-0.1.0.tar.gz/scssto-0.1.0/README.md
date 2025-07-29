# scssto

**scssto** is a simple yet powerful Python tool that compiles all `.scss` files in a directory into `.css` using the official [Sass CLI](https://sass-lang.com/install). Ideal for static site generators, web projects, or automation workflows.

---

## 🚀 Features

- 🔍 Scans a directory and compiles all `.scss` files
- 📁 Outputs `.css` files with matching names in your target folder
- 🛠 Automatically creates the output directory if it doesn’t exist
- ⚙️ Uses `sass` CLI — no unreliable hacks
- 🧼 Clean and minimal codebase

---

## 📦 Installation

```bash
pip install scssto
```
## 🧪 Usage
📂 From the command line:

```python -m scssto -scss scss/ -css css/```

or


```python3 -m scssto -scss scss/ -css css/```

---
## 🐍 From Python:
```
from scssto import compile_scss_to_css

compile_scss_to_css("scss/", "css/")
```