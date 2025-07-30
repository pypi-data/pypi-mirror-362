
# EG4 Inverter Python Client

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

**`eg4_python`** is a Python library that provides both **async** and **sync** methods to interact with the **EG4 Inverter** cloud API. It handles login, data retrieval, and session management efficiently — ideal for integration with **Home Assistant**, MCP, automation platforms, or custom monitoring solutions.

## Caveats

---

## Features
✅ Asynchronous and synchronous support (via `asyncio` and sync wrappers)  
✅ Automatic re-authentication on session expiry (401 errors)  
✅ Modular structure for future expandability  
✅ Supports DISCOVERING multiple inverters from a single account

---

## Installation

### Using PyPI (Recommended)
```bash
pip install eg4_python
```

### Development Version (Editable Mode)
```bash
git clone https://github.com/yourusername/eg4_python.git
cd eg4_python
pip install -e .[dev]  # For development and testing
```

---

## Usage

### Example Code
You can look at the "test" function in client.py

```python
import asyncio
from eg4_python import EG4InverterAPI

async def main():
    api = EG4InverterAPI(username="username", password="password", base_url="https://monitor.eg4electronics.com")
    await api.login(ignore_ssl=True)

    # Display Inverters
    for index, inverter in enumerate(api.get_inverters()):
        print(f"Inverter {index}: {inverter}")

    print("Selecting Inverter 0")
    api.set_selected_inverter(inverterIndex=0)

    # Fetch Runtime Data
    runtime_data = await api.get_inverter_runtime_async()
    print("Runtime Data:", runtime_data)

    # Fetch Energy Data
    energy_data = await api.get_inverter_energy_async()
    print("Energy Data:", energy_data)

    # Fetch Battery Data
    battery_data = await api.get_inverter_battery_async()
    print("Battery Data:", battery_data)
    await api.close()

asyncio.run(main())
```

---

## Configuration

### Environment Variables (Recommended for Secrets)
Create a `.env` file:
```
USERNAME=your_username
PASSWORD=your_password
SERIAL_NUMBER=
PLANT_ID=
BASE_URL=https://monitor.eg4electronics.com
```

### Example `.env` Loading in Code
```python
import os
from dotenv import load_dotenv

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
```

---

## API Methods

### **Authentication & Session Management**
- `async def login()` – Handles login and saves the JSESSIONID cookie.  Accepts ignore_ssl=[true|false]
- `async def close()` – Gracefully closes the HTTP session.

### **Setup**
- `get_inverters()` - list the inverters associated with the account, after login
- `set_selected_inverter(inverterIndex=index)` - Selects an inverter from the list of inverters
- `set_selected_inverter(plantId=plantId, serialNum=serialNum)`  - Explicitly sets the selected inverter

### **Data Retrieval**
- `async def get_inverter_runtime_async()` – Retrieves inverter runtime data.
- `async def get_inverter_energy_async()` – Retrieves inverter energy data.
- `async def get_inverter_battery_async()` – Retrieves battery data, including individual battery units.

### **Parameters read/write**
- `async def read_settings_async()` – reads parameters.
- `async def write_settings_async()` – writes a parameter value.

### **Sync Methods (Wrappers)**
- `get_inverter_runtime()`
- `get_inverter_energy()`
- `get_inverter_battery()`
- `read_settings()`
- `write_settings()`

---

## Running Tests
Ensure you have development dependencies installed:
```bash
pip install -e .[dev]
```

Then run the test suite:
```bash
pytest tests/
```

---

## Roadmap
- ✅ Initial EG4 API implementation
- ✅ Async/Sync support
- ✅ Setting inverter values
- 🔜 ...Full Home Assistant Integration
- 🔜 ...You tell me

---

## License
This project is licensed under the **APACHE License**.
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)


---

## Contributing
Contributions are welcome! Please open issues, suggest improvements, or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add an awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

---

## Author
**Garreth Jeremiah**  
[GitHub Profile](https://github.com/twistedroutes)

---

## Acknowledgments
Special thanks to DAB Ultimate beer!

