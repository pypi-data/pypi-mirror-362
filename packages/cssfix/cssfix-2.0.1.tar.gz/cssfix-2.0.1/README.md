# cssfix

**cssfix** is a lightweight Python utility that cleans and optimizes your CSS code.  
It removes comments 🗑️, merges duplicate selectors 🧩, and outputs a compact result ⚡.  
Perfect for small projects, automation, or integrating into build tools.

---

## ✨ Features

- 🧽 **Removes all CSS comments**
- 🔁 **Merges repeated selectors** (e.g. `.class1 {}` multiple times)
- 🧠 **Consolidates CSS properties without duplicates**
- 📥 **Takes raw CSS string as input**
- 📤 **Returns optimized CSS string output immediately on instantiation**
- 🐍 **Pure Python - no dependencies**

---

## 📦 Installation

From PyPI:
```cmd
pip install cssfix
```
---

## 🚀 Usage
```python
from cssfix import css

css_text = """
/* This is a comment */
.box {
	color: red;
}
.box {
	background: blue;
}
"""

optimized_css = css(css_text)
print(optimized_css)
```
### ✅ Output:
```css
.box{color:red;background:blue;}
```
---

## 📚 API

```python
class css(css_text: str)
```

Creates a new instance of the CSS optimizer and immediately returns optimized CSS string.

#### Parameters:
> `css_text`: `str` — Raw CSS code to optimize

#### Returns:
> `str` — Optimized, minified CSS with merged selectors and no comments