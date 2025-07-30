from typing import List, Optional
from datetime import datetime

class DailyChartDataPoint:
    """Represents a single data point in the daily chart time series."""
    
    def __init__(self, captureExtra=True, **kwargs):
        self.time = kwargs.get("time")
        self.year = kwargs.get("year")
        self.month = kwargs.get("month") 
        self.day = kwargs.get("day")
        self.hour = kwargs.get("hour")
        self.minute = kwargs.get("minute")
        self.second = kwargs.get("second")
        
        # Power measurements (in watts)
        self.solar_pv = kwargs.get("solarPv", 0)  # Solar PV generation
        self.grid_power = kwargs.get("gridPower", 0)  # Grid power (negative = importing from grid)
        self.battery_discharging = kwargs.get("batteryDischarging", 0)  # Battery power (negative = charging, positive = discharging)
        self.consumption = kwargs.get("consumption", 0)  # Total consumption
        self.ac_couple_power = kwargs.get("acCouplePower", 0)  # AC coupled power
        
        # Battery state
        self.soc = kwargs.get("soc", 0)  # State of charge (percentage)
        
        # Store raw data if requested
        if captureExtra:
            self.raw_data = kwargs

    @property
    def datetime(self) -> Optional[datetime]:
        """Convert time string to datetime object."""
        if self.time:
            try:
                return datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None
        return None

    @property
    def is_battery_charging(self) -> bool:
        """Check if battery is charging (negative discharge = charging)."""
        return self.battery_discharging < 0

    @property
    def is_battery_discharging(self) -> bool:
        """Check if battery is discharging (positive discharge)."""
        return self.battery_discharging > 0

    @property
    def is_importing_from_grid(self) -> bool:
        """Check if importing power from grid (negative grid power)."""
        return self.grid_power < 0

    @property
    def is_exporting_to_grid(self) -> bool:
        """Check if exporting power to grid (positive grid power)."""
        return self.grid_power > 0

    @property
    def net_solar_generation(self) -> int:
        """Net solar generation after battery charging."""
        return max(0, self.solar_pv + min(0, self.battery_discharging))

    def __str__(self):
        return (f"DailyChartDataPoint(time={self.time}, "
                f"solar={self.solar_pv}W, grid={self.grid_power}W, "
                f"battery={self.battery_discharging}W, consumption={self.consumption}W, "
                f"soc={self.soc}%)")

    def __repr__(self):
        return self.__str__()


class DailyChartData:
    """Container for daily chart data with time series analysis capabilities."""
    
    def __init__(self, captureExtra=True, **kwargs):
        self.success = kwargs.get("success", False)
        self.x_axis = kwargs.get("xAxis", "time")
        
        # Parse data points
        self.data_points: List[DailyChartDataPoint] = []
        raw_data = kwargs.get("data", [])
        
        for point_data in raw_data:
            data_point = DailyChartDataPoint(captureExtra=captureExtra, **point_data)
            self.data_points.append(data_point)
        
        # Store raw data if requested
        if captureExtra:
            self.raw_data = kwargs

    @property
    def total_data_points(self) -> int:
        """Total number of data points."""
        return len(self.data_points)

    @property
    def date_range(self) -> tuple:
        """Get start and end dates of the data."""
        if not self.data_points:
            return None, None
        
        start_time = self.data_points[0].datetime
        end_time = self.data_points[-1].datetime
        return start_time, end_time

    @property 
    def total_solar_generation_kwh(self) -> float:
        """Total solar generation for the day in kWh (assuming 10-minute intervals)."""
        total_wh = sum(point.solar_pv for point in self.data_points) * (10/60)  # 10 minutes
        return total_wh / 1000  # Convert to kWh

    @property
    def total_consumption_kwh(self) -> float:
        """Total consumption for the day in kWh."""
        total_wh = sum(point.consumption for point in self.data_points) * (10/60)
        return total_wh / 1000

    @property
    def total_grid_import_kwh(self) -> float:
        """Total grid import for the day in kWh."""
        total_wh = sum(abs(point.grid_power) for point in self.data_points 
                      if point.is_importing_from_grid) * (10/60)
        return total_wh / 1000

    @property
    def total_grid_export_kwh(self) -> float:
        """Total grid export for the day in kWh."""
        total_wh = sum(point.grid_power for point in self.data_points 
                      if point.is_exporting_to_grid) * (10/60)
        return total_wh / 1000

    @property
    def peak_solar_generation(self) -> int:
        """Peak solar generation in watts."""
        return max((point.solar_pv for point in self.data_points), default=0)

    @property
    def peak_consumption(self) -> int:
        """Peak consumption in watts."""
        return max((point.consumption for point in self.data_points), default=0)

    @property
    def average_soc(self) -> float:
        """Average state of charge for the day."""
        if not self.data_points:
            return 0.0
        return sum(point.soc for point in self.data_points) / len(self.data_points)

    @property
    def min_soc(self) -> int:
        """Minimum state of charge for the day."""
        return min((point.soc for point in self.data_points), default=0)

    @property
    def max_soc(self) -> int:
        """Maximum state of charge for the day."""
        return max((point.soc for point in self.data_points), default=0)

    def get_solar_generation_by_hour(self) -> dict:
        """Get hourly solar generation totals."""
        hourly_data = {}
        for point in self.data_points:
            hour = point.hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(point.solar_pv)
        
        return {hour: sum(values) * (10/60) / 1000 for hour, values in hourly_data.items()}  # kWh

    def get_consumption_by_hour(self) -> dict:
        """Get hourly consumption totals."""
        hourly_data = {}
        for point in self.data_points:
            hour = point.hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(point.consumption)
        
        return {hour: sum(values) * (10/60) / 1000 for hour, values in hourly_data.items()}  # kWh

    def filter_by_time_range(self, start_hour: int = None, end_hour: int = None) -> List[DailyChartDataPoint]:
        """Filter data points by hour range."""
        filtered_points = []
        for point in self.data_points:
            if start_hour is not None and point.hour < start_hour:
                continue
            if end_hour is not None and point.hour > end_hour:
                continue
            filtered_points.append(point)
        return filtered_points

    def __str__(self):
        if not self.data_points:
            return "DailyChartData(no data)"
        
        start, end = self.date_range
        return (f"DailyChartData(points={self.total_data_points}, "
                f"range={start.date() if start else 'N/A'} to {end.date() if end else 'N/A'}, "
                f"solar={self.total_solar_generation_kwh:.2f}kWh, "
                f"consumption={self.total_consumption_kwh:.2f}kWh)")

    def __repr__(self):
        return self.__str__()


class Inverter:
    """Represents an EG4 Inverter."""

    def __init__(self, plantId, plantName, captureExtra=True, **kwargs) -> None:
        self.plantId = plantId
        self.plantName = plantName
        self.serialNum = None
        self._main_args = [
            "serialNum",
            "phase",
            "dtc",
            "deviceType",
            "subDeviceType",
            "allowExport2Grid",
            "batteryType",
            "standard",
            "slaveVersion",
            "fwVersion",
            "allowGenExercise",
            "withbatteryData",
            "hardwareVersion",
            "voltClass",
            "machineType",
            "protocolVersion",
        ]
        for key in self._main_args:
            setattr(self, key, kwargs.get(key))

        if captureExtra:
            self.from_dict(
                {x: y for x, y in kwargs.items() if x not in self._main_args}
            )

    def from_dict(self, d):
        """Set values based on dictionary."""
        for key, value in d.items():
            setattr(self, key, value)

    def __repr__(self):
        return (
            "Inverter("
            f"serialNum={self.serialNum}, plantName={self.plantName} "
            f"plantName={self.plantId}, batteryType={self.batteryType}, "
            f"fwVersion={self.fwVersion}, phase={self.phase}"
            ")"
        )


class BatteryUnit:
    """Represents an individual battery unit."""

    def __init__(self, captureExtra=True, **kwargs):
        """Initialize BatteryUnit."""
        self._main_args = [
            "batteryKey",
            "batIndex",
            "batterySn",
            "totalVoltage",
            "current",
            "soc",
            "soh",
            "cycleCnt",
        ]
        for key in self._main_args:
            setattr(self, key, kwargs.get(key))

        # Capture any unknown or new API fields dynamically
        if captureExtra:
            self.from_dict(
                {x: y for x, y in kwargs.items() if x not in self._main_args}
            )

    def from_dict(self, d) -> None:
        """Set values based on dictionary."""
        for key, value in d.items():
            setattr(self, key, value)

    def to_dict(self):
        """Return the battery unit as a dictionary."""
        return self.__dict__

    def __repr__(self):
        return f"BatteryUnit({self.batIndex}: sn {self.batterySn}, soc% {self.soc}, soh% {self.soh}, cycles {self.cycleCnt}, v {self.totalVoltage / 100}, )"


class BatteryData:
    """Represents overall battery data including individual battery units."""

    def __init__(
        self,
        remainCapacity,
        fullCapacity,
        totalNumber,
        totalVoltageText,
        currentText,
        battery_units=[],
    ):
        self.remainCapacity = remainCapacity
        self.fullCapacity = fullCapacity
        self.totalNumber = totalNumber
        self.totalVoltageText = totalVoltageText
        self.currentText = currentText

        # Battery units as a list
        self.battery_units = battery_units if battery_units else []

    def to_dict(self):
        """Return the battery data including individual units as a dictionary."""
        data = self.__dict__.copy()
        data["battery_units"] = [unit.to_dict() for unit in self.battery_units]
        return data

    def __repr__(self):
        d = self.to_dict()
        data = {x: y for x, y in d.items() if x != "battery_units"}
        return f"BatteryData({data.items()} )"


class EnergyData:
    """Represents inverter energy data from the API."""

    def __init__(self, captureExtra=True, **kwargs):
        self._main_args = [
            "todayYielding",
            "totalYielding",
            "todayDischarging",
            "totalDischarging",
            "todayCharging",
            "totalCharging",
            "todayImport",
            "totalImport",
            "todayExport",
            "totalExport",
            "todayUsage",
            "totalUsage",
        ]
        for key in self._main_args:
            setattr(self, key, kwargs.get(key))

        # Capture any unknown or new API fields dynamically
        if captureExtra:
            self.from_dict(
                {x: y for x, y in kwargs.items() if x not in self._main_args}
            )

    def from_dict(self, d) -> None:
        """Set values based on dictionary."""
        for key, value in d.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"EnergyData({self.to_dict()})"

    def to_dict(self):
        return self.__dict__


class RuntimeData:
    """Represents inverter runtime data from the API."""

    def __init__(
        self,
        captureExtra=True,
        **kwargs,
    ):
        self._main_args = [
            "statusText",
            "batteryType",
            "batParallelNum",
            "batCapacity",
            "consumptionPower",
            "vpv1",
            "vpv2",
            "vpv3",
            "vpv4",
            "ppvpCharge",
            "pDisCharge",
            "peps",
            "pToGrid",
            "pToUser",
        ]
        for key in self._main_args:
            setattr(self, key, kwargs.get(key))

        # Capture any unknown or new API fields dynamically
        if captureExtra:
            d = {x: y for x, y in kwargs.items() if x not in self._main_args}
            self.from_dict(d)

    def from_dict(self, d) -> None:
        """Set values based on dictionary."""
        for key, value in d.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"RuntimeData({self.to_dict()})"

    def to_dict(self):
        return self.__dict__

class InverterParameters:
    """Represents inverter parameters."""

    def __init__(
        self
    ):
        self._skip_args = ["valueFrame","inverterSn","startRegister","pointNumber"]
        self._main_args = ["success"]
        self.success=True

    def from_dict(self, d) -> None:
        """Set values based on dictionary."""
        for key, value in d.items():
            if key not in self._main_args and key not in self._skip_args:
                setattr(self, key, value)

    def __repr__(self):
        return f"RuntimeData({self.to_dict()})"

    def to_dict(self):
        return self.__dict__


class APIResponse:
    """A general-purpose response model for handling success/failure states."""

    def __init__(self, success, data=None, error_message=None):
        self.success = success
        self.data = data
        self.error_message = error_message

    def __repr__(self):
        return f"APIResponse(success={self.success}, data={self.data}, error={self.error_message})"
