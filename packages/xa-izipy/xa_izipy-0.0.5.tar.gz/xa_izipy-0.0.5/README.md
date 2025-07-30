# xa_izipy Lib

**🎯 Target:** Make Python easier (izi) 😎🔥

This library provides a few simple functions to simplify Python scripting — from detecting paths to importing built-in modules faster.

---

**❓ Changes:**

- `typing_text()` - Changed the logic of the command
- `check_available()` - New function

---

## 🛠️ Function List (default module)

- `help(choice="en")` – Shows info about the library in selected language  
  - `"en"` by default  
  - `"ru"` for Russian  
  - Example: `help("ru")` or `help(choice="ru")`

- `getdirectory()` – Returns the full path to the script location 📂

- `fast_import(show_loading=True)` – Automatically imports common Python libraries (`os`, `time`, `random`, `logging`, `json`)  
  - Set `show_loading=False` to disable import messages

- `get_platform_info()` – Returns detailed system information as a dictionary:  
  - `os` — Operating system name (e.g., Windows, Linux, macOS)  
  - `release` — OS version or release number (e.g., 10, 11, kernel version)  
  - `arch` — CPU architecture (e.g., x86_64, AMD64, ARM)  
  - `hostname` — Network name of the computer (PC name)  
  - `ram_total_GB` — Total RAM in gigabytes (rounded to 2 decimals)  
  - `ram_available_GB` — Available/free RAM in gigabytes (rounded to 2 decimals)  

- `typing_text("text", 0.1)` — Outputs text with typing animation  
  - `"text"` – Output text  
  - `"0.1"` – Delay in seconds  
  - Example: `typing_text("text", 0.1)` or `typing_text("text", delay=0.1)`

---

## 🧰 Function List (`xa_izipy.tools`)

- `create_logger(name="xa_izipy", level=logging.INFO)` – Creates a logger instance  
  - `name` – Logger name (default: `"xa_izipy"`)  
  - `level` – Logging level (default: `logging.INFO`)  
  - Example: `create_logger()` or `create_logger("mylog", logging.DEBUG)`

- `check_available(site, port=80, timeout=5)` – Checks if a site/server is reachable on a given port within the timeout.  
  - `site` – Hostname or IP address to check  
  - `port` – Port number to connect to (default: 80)  
  - `timeout` – Connection timeout in seconds (default: 5)  
  - Returns `True` if the connection is successful, otherwise `False`  

---

## 💻 Example usage

```python
from xa_izipy import getdirectory, help, fast_import, get_platform_info, typing_text

print(f"This directory: {getdirectory()}")  # Output full path of script

help()         # Show info in English
help("ru")     # Show info in Russian

fast_import()  # Import default modules with logs

info = get_platform_info()
print("System info:")
for key, value in info.items():
    print(f" - {key}: {value}")

typing_text("Hello World!", 0.15)
```

## 💻 Example usage (`xa_izipy.tools`)

```python
from xa_izipy.tools import create_logger, check_available

logger = create_logger()

logger.info("I like cookie ;>")
logger.warning("I not love cookie :<")
logger.error("I hate cookie :/")

if check_available("google.com", port=80, timeout=5) == True:
    print("Working!")
else:
    print("Not working!")
```
