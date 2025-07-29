---

## 📄 Final `README.md` for `nanourls`

````markdown
# nanourls

**nanourls** is a minimal, fast, and dependency-free Python URL shortener package with support for a custom domain — by default, it uses `https://nano.ly/` as your branded short link prefix.

---

## 🚀 Features

- 🔗 Shortens any long URL
- 🌍 Uses your custom domain (`https://nano.ly/`)
- 💾 Stores URL mappings locally in a SQLite database
- 🔁 Expand short links back to original URLs
- 📦 Easy to install and import in any Python project

---

## 📦 Installation

```bash
pip install nanourls
````

Or, if you're using the source:

```bash
git clone https://github.com/yourusername/nanourls.git
cd nanourls
pip install .
```

---

## 🧠 Usage

```python
from nanourls import shorten_url, expand_url

# Shorten a long URL
short_url = shorten_url("https://google.com")
print(short_url)
# Output: https://nano.ly/aB3xT9

# Expand back to original URL
original = expand_url(short_url)
print(original)
# Output: https://google.com
```

---

## ⚙️ Configuration

By default, short URLs are prefixed with:

```
https://nano.ly/
```

To change this domain, edit `config.py`:

```python
# config.py
BASE_DOMAIN = "https://yourcustom.domain/"
```

---

## 📁 Project Structure

```
nanourls/
├── nanourls/
│   ├── __init__.py
│   ├── shortener.py      # Core logic for shorten & expand
│   ├── db.py             # SQLite database logic
│   └── config.py         # Custom domain config
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 📜 License

MIT License.
Feel free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

---

## ✨ Author

Made with ❤️ by **[Yug Bhuva](https://github.com/Yugbhuva)**

---