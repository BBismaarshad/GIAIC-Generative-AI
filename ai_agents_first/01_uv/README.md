# Python UV – The Ultimate Fast Python Package Manager

**Python UV** ek superfast package manager hai jo Python projects ke liye dependency management aur virtual environments ko bohat hi asaan aur tez bana deta hai.  
Ye `pip`, `virtualenv`, `pip-tools`, aur `poetry` ka **modern replacement** hai — **Rust** mein likha gaya, blazing fast .

---

## Key Concepts

### Kya hai UV?

**UV** ek **Rust-based CLI tool** hai jo:

-  Dependencies manage karta hai (pip ki jagah)
-  Virtual environments create karta hai (venv ki jagah)
-  Ultra-fast dependency resolution karta hai
-  Command Line Interface se operate karta hai

---
### 📁 New Project Initialize Karna
# 1. New project start
```
uv init --package Foldename
cd Foldename
code .
```

# 2. Activate virtual environment:
```
source .venv/bin/activate

In Windows 
\explore-uv\.venv\Scripts\activate
```
# 3. Run app
```
uv run explore-uv
```
