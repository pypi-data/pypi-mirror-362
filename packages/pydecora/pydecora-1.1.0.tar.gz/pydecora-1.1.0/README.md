# pydecora 🧩

A lightweight and modular Python decorator library that helps you write cleaner and more expressive code.

## 🚀 Features

- 🧠 `@cache`: Simple in-memory caching with optional TTL and size limit
- 🔁 `@retry`: Automatically retry failed operations with exponential backoff
- 🛑 `@suppress`: Suppress exceptions and optionally log them
- ⏱️ `@timeit`: Time execution of functions
- 🧪 `@validate_args`: Enforce argument types using runtime validation

## 📦 Installation

```
pip install pydecora
```
## 🧑‍💻 Usage
```
from pydecora import cache, retry

@cache(ttl=60)
def slow_func(x):
    return x * x

@retry(times=3, delay=1)
def flaky_api_call():
    ...
```

## 📁 Project Structure
```
pydecora/
├── pydecora/
│ ├── init.py
│ └── decorators/
│ ├── cache.py
│ ├── retry.py
│ ├── suppress.py
│ ├── timeit.py
│ └── validate_args.py
├── tests/
│ ├── test_cache.py
│ ├── test_retry.py
│ ├── test_suppress.py
│ ├── test_timeit.py
│ └── test_validate_args.py
├── README.md
├── LICENSE
├── setup.py
└── pyproject.toml
```

## 🧪 Running Tests

```
pytest pydecora/tests
```

## 🤝 Contributing
Pull requests and ideas welcome! Please open an issue or fork and PR.

## 📄 License
MIT — see [LICENSE](LICENSE)