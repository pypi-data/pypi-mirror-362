import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
from dotenv import load_dotenv
from eg4_inverter_api import EG4InverterAPI, EG4AuthError, EG4APIError

# Load environment variables for testing
load_dotenv(".env")

USERNAME = os.getenv("EG4_USERNAME")
PASSWORD = os.getenv("EG4_PASSWORD")
SERIAL_NUMBER = os.getenv("EG4_SERIAL_NUMBER")
PLANT_ID = os.getenv("EG4_PLANT_ID")
BASE_URL = os.getenv("EG4_BASE_URL", "https://monitor.eg4electronics.com")
IGNORE_SSL = os.getenv("EG4_DISABLE_VERIFY_SSL", "1") == "1"

@pytest.mark.asyncio
async def test_login():
    """Test successful login and exercise the functions"""
    api = EG4InverterAPI(USERNAME, PASSWORD, BASE_URL)
    print(api._password)
    await api.login(ignore_ssl=IGNORE_SSL)
    api.set_selected_inverter(inverterIndex=0)
    assert api.jsessionid is not None
    print("Logged in")
    data = await api.get_inverter_runtime_async()
    assert data.success
    assert data.statusText is not None
    print("get_inverter_runtime_async success")
    data = await api.get_inverter_energy_async()
    assert data.success
    print("get_inverter_energy_async success")
    data = await api.get_inverter_battery_async()
    assert data.remainCapacity is not None
    print("get_inverter_battery_async success")
    inverter_params = await api.read_settings_async()
    assert inverter_params.success is True
    assert hasattr(inverter_params, 'inverterRuntimeDeviceTime')
    print("read_settings_async success")
    attr = "OFF_GRID_HOLD_GEN_CHG_START_SOC" if hasattr(inverter_params, "OFF_GRID_HOLD_GEN_CHG_START_SOC") else "HOLD_BATTERY_WARNING_SOC"
    orig_value = getattr(inverter_params,attr)
    assert orig_value is not None
    new_value = int(orig_value) - 1
    data = await api.write_setting_async(hold_param=attr, value_text=new_value)
    assert data is True
    data = await api.write_setting_async(hold_param=attr, value_text=orig_value)
    print("write_setting_async success")
    
@pytest.mark.asyncio
async def test_invalid_login():
    """Test handling of invalid credentials."""
    api2 = EG4InverterAPI(USERNAME, "xxx", BASE_URL)
    with pytest.raises(EG4AuthError):
        await api2.login(ignore_ssl=IGNORE_SSL)
