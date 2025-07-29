# autopylog

🔍 `autopylog` is a simple, lightweight Python package that automatically logs function calls, input arguments, return values, execution time, and exceptions using a single decorator.

---

## 🚀 Features

- ✅ Log function name and arguments
- ✅ Log return values
- ✅ Measure and log execution time
- ✅ Catch and log exceptions
- ✅ Clean decorator-based syntax
- ✅ Plug-and-play (no setup required)

---

## 📦 Installation

```bash
pip install autopylog
🧠 Usage


from autopylog import log_this

@log_this
def divide(x, y):
    return x / y

divide(10, 2)
divide(10, 0)  # Will log the exception
🧾 Output



[INFO] Calling: divide(x=10, y=2)
[INFO] Returned: 5.0 in 0.0001s

[INFO] Calling: divide(x=10, y=0)
[ERROR] Exception in divide: division by zero



🧩 Why autopylog?
Many developers forget or ignore logging — autopylog makes it automatic and painless. Ideal for debugging, tracing, and monitoring Python functions in any project.


