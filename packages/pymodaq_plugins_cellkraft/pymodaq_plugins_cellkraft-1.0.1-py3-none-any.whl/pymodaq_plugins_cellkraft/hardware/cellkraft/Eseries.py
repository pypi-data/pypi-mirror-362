from pymodaq.utils.logger import set_logger, get_module_name
from pymodaq_plugins_cellkraft.hardware.tcpmodbus import SyncModBusInstrument
from enum import IntEnum
logger = set_logger(get_module_name(__file__))
# WRITE
#
# pump control : register 9107 value [0 auto 1 manual 2 prime] default 1
# SP temp var °C : register 9300 value [] default 10
# RH% : register 9240 default 10
# SP flow(g/min) register 9310 default 10
# SP TEMP tube °C register 9355
# Pump % 9109
#
# READ
#
# steam temp 4148
# Air humidity 4628
# flow (g/min) 6518
# pressure(bar) 5268
# Tube temp 4468
# pump % 6158
#
# turn down => write 0 to register 9310
# read status 6518


class Pump(IntEnum):
    read_address = 6158
    write_address = 9109
    default_write_value = 100
    scaling = 100
    read_scaling = scaling
    write_scaling = scaling


class PumpMode(IntEnum):
    write_address = 9107
    mode_auto = 0
    mode_manual = 1
    mode_prime = 2
    default_mode = mode_auto
    default_write_value = default_mode


class Steam(IntEnum):
    read_address = 4148
    write_address = 9300
    default_write_value = 0
    read_scaling = 10
    write_scaling = 1


class Air(IntEnum):
    read_address = 4628
    write_address = 9240
    default_write_value = 105.0
    scaling = 10
    read_scaling = scaling
    write_scaling = scaling


class Flow(IntEnum):
    read_address = 6518
    write_address = 9310
    default_write_value = 105.0
    scaling = 10
    read_scaling = scaling
    write_scaling = scaling


class Tube(IntEnum):
    read_address = 4468
    write_address = 9355
    default_write_value = 105.0
    read_scaling = 10
    write_scaling = 10


class Pressure(IntEnum):
    read_address = 5268
    read_scaling = 100


Eseries_Config = {
        1500: {
            "general": {
                "scaling_default": 1,
                },
            PumpMode.__name__: {
                "reference": PumpMode,
                "authorized_write_value": [0, 1, 2],
                },
            Pump.__name__: {
                "reference": Pump,
                "unit": "%",
                "type": float,
                "authorized_write_value": range(0, 105, 1),
                },
            Steam.__name__: {
                "reference": Steam,
                "type": float,
                "unit": "C",
                "authorized_write_value": range(0, 200, 1),
                },
            Air.__name__: {
                "reference": Air,
                "unit": "%",
                "type": float,
                "authorized_write_value": range(0, 105, 1),
                },
            Flow.__name__: {
                "reference": Flow,
                "unit": "g/min",
                "type": float,
                "authorized_write_value": [value for value in range(0, 250, 1)],
                },
            Tube.__name__: {
                "reference": Tube,
                "unit": "C",
                "type": float,
                "authorized_write_value": range(0, 200, 1),
                },
            Pressure.__name__: {
                "reference": Pressure,
                "unit": "Bar",
                "type": float,
                # "write_address": 9355,
                # "authorized_write_value": range(0, 200, 1),
                # "default_write_value": 105
                },
            }
        }


class CellKraftE1500Drivers:
    """TCP ModBus driver for the Steam Generator CellKraft E-series

    Relies on a custom tcpmodules based on pymodbus (source : https://github.com/pymodbus-dev/pymodbus
    documentation : https://pymodbus.readthedocs.io/en/latest/)
    """
    def __init__(self, host, config=None):
        """Initialize the Steam Generator driver

        :param host: hostname or ip address
        """
        self.instr = SyncModBusInstrument(host)
        self.host = host
        self.registers = {}
        self.init = False

        if config is None:
            self.config = Eseries_Config
        else:
            self.config = config

        self.ini_register(self.config)

    def ini_register(self, config_dict=None):
        """
        Initialise the register to expose the method/hardware parameters
        :param config_dict: Manual Configuration dictionary feeding should be self.config
        """

        if config_dict is None:
            if self.config is None:
                config_dict = Eseries_Config
            else:
                config_dict = self.config

        self.registers["PumpSetMode"] = {
            "method": self.PumpSetMode,
            "reference": config_dict[1500]["PumpMode"]["reference"],
            "register": config_dict[1500]["PumpMode"]["reference"].write_address.value,
            "mode": "write"
        }
        self.registers["Pump"] = {
            "method": self.Write_Pump,
            "reference": config_dict[1500]["Pump"]["reference"],
            "write_register": config_dict[1500]["Pump"]["reference"].write_address.value,
            "read_register": config_dict[1500]["Pump"]["reference"].read_address.value,
            "mode": "write",
            "scaling": config_dict[1500]["Pump"]["reference"].scaling.value
        }
        self.registers["SP_SteamT"] = {
            "method": self.SP_SteamT,
            "reference": config_dict[1500]["Steam"]["reference"],
            "register": config_dict[1500]["Steam"]["reference"].write_address.value,
            "mode": "write",
            "scaling": config_dict[1500]["Steam"]["reference"].write_scaling.value
        }
        self.registers["RH"] = {
            "method": self.RH,
            "reference": config_dict[1500]["Air"]["reference"],
            "register": config_dict[1500]["Air"]["reference"].write_address.value,
            "mode": "write",
            "scaling": config_dict[1500]["Air"]["reference"].scaling.value
        }
        self.registers["SP_Flow"] = {
            "method": self.SP_Flow,
            "reference": config_dict[1500]["Flow"]["reference"],
            "register": config_dict[1500]["Flow"]["reference"].write_address.value,
            "mode": "write",
            "scaling": config_dict[1500]["Flow"]["reference"].scaling.value
        }
        self.registers["SP_Tube_Temp"] = {
            "method": self.SP_Tube_Temp,
            "reference": config_dict[1500]["Tube"]["reference"],
            "register": config_dict[1500]["Tube"]["reference"].write_address.value,
            "mode": "write",
            "scaling": config_dict[1500]["Tube"]["reference"].write_scaling.value
        }
        self.registers["Get_Steam_T"] = {
            "method": self.Get_Steam_T,
            "reference": config_dict[1500]["Steam"]["reference"],
            "register": config_dict[1500]["Steam"]["reference"].read_address.value,
            "mode": "read",
            "scaling": config_dict[1500]["Steam"]["reference"].read_scaling.value
        }
        self.registers["Get_Air_H"] = {
            "method": self.Get_Air_H,
            "reference": config_dict[1500]["Air"]["reference"],
            "register": config_dict[1500]["Air"]["reference"].read_address.value,
            "mode": "read",
            "scaling": config_dict[1500]["Air"]["reference"].read_scaling.value
        }
        self.registers["Get_Flow"] = {
            "method": self.Get_Flow,
            "reference": config_dict[1500]["Flow"]["reference"],
            "register": config_dict[1500]["Flow"]["reference"].read_address.value,
            "mode": "read",
            "scaling": config_dict[1500]["Flow"]["reference"].read_scaling.value
        }
        self.registers["Get_Pressure"] = {
            "method": self.Get_Pressure,
            "reference": config_dict[1500]["Pressure"]["reference"],
            "register": config_dict[1500]["Pressure"]["reference"].read_address.value,
            "mode": "read",
            "scaling": config_dict[1500]["Pressure"]["reference"].read_scaling.value
        }
        self.registers["Get_Tube_T"] = {
            "method": self.Get_Tube_T,
            "reference": config_dict[1500]["Tube"]["reference"],
            "register": config_dict[1500]["Tube"]["reference"].read_address.value,
            "mode": "read",
            "scaling": config_dict[1500]["Tube"]["reference"].read_scaling.value
        }

    def init_hardware(self):
        """Connect and initialize the Steam Generator

        """
        self.init = self.instr.ini_hw()
        return self.init

    def stop(self):
        """Stop procedure

        :return:
        """
        self.SP_Flow(0)

    def close(self):
        """Close connection

        :return:
        """
        self.instr.close()

# ------------------------------------------------------ #

    def PumpSetMode(self, value: str = "auto"):
        """Writing the pump mode

        Auto : La pompe fonctionne automatiquement,
        sûrement en fonction des besoins du système.

        Manual : La pompe fonctionne en mode manuel,
        l'utilisateur doit contrôler son fonctionnement manuellement.

        Prime : Ce mode est généralement utilisé pour amorcer la pompe,
        pour remplir le système avec du liquide avant de commencer le fonctionnement normal.

        :param value: human-readable equivalent of the 3 allowed values (0 auto, 1 manual, 2 prime) defaulting to auto
        """

        order: int
        match value:
            case "auto":
                order = PumpMode.mode_auto.value
            case "manual":
                order = PumpMode.mode_manual.value
            case "prime":
                order = PumpMode.mode_prime.value
            case _:
                order = PumpMode.default_mode.value
        try:
            self.instr.write(self.registers["PumpSetMode"]["register"],
                             order)
        except Exception as e:
            raise (Exception, f"error in {self.__qualname__}, {e}")

    def Write_Pump(self, pump_power: int = 100):
        """Set the pump power in %

        :param pump_power: int% pump power
        """
        pump_power = int(pump_power*self.registers["Pump"]["scaling"])
        try:
            self.instr.write(self.registers["Pump"]["write_register"], pump_power)
        except Exception as e:
            raise (Exception, f"error {e}")
        return pump_power

    def Read_Pump(self):
        """Get the pump power in %

        :return pump_power: int% pump power
        """
        pump_power = self.instr.read(self.registers["Pump"]["read_register"])
        if isinstance(pump_power, Exception):
            raise pump_power
        else:
            return pump_power.registers[0] / self.registers["Pump"]["scaling"]

# ------------------------------------------------------ #

    def SP_SteamT(self, temperature: int | float = 10):
        """Set the SP Steam temperature in °C

        :param temperature: int in °C
        :return:
        """
        temperature = int(temperature * self.registers["SP_SteamT"]["scaling"])  # Scaling => 1
        try:
            self.instr.write(self.registers["SP_SteamT"]["register"], temperature)
        except Exception as e:
            raise (Exception, f"error {e}")
        return temperature

    def RH(self, relativehumidity: int | float = 105):
        """Set the relative humidity in %

        :param relativehumidity: int% relative humidity
        """
        relativehumidity = int(relativehumidity * self.registers["RH"]["scaling"])  # Scaling => 10
        try:
            self.instr.write(self.registers["RH"]["register"], relativehumidity)
        except Exception as e:
            raise (Exception, f"error {e}")
        return relativehumidity

    def SP_Flow(self, flow: int | float):
        """Set the flow in g/min

        :param flow:
        """
        flow = int(flow*self.registers["SP_Flow"]["scaling"])  # Scaling => 10
        try:
            self.instr.write(self.registers["SP_Flow"]["register"], flow)
        except Exception as e:
            raise (Exception, f"error {e}")
        return flow

    def SP_Tube_Temp(self, temperature: int | float):
        """Set the tube temperature

        :param temperature: tube temperature set point
        :return:
        """
        temperature = int(temperature * self.registers["SP_Tube_Temp"]["scaling"])  # Scaling => 10
        try:
            self.instr.write(self.registers["SP_Tube_Temp"]["register"], temperature)
        except Exception as e:
            raise (Exception, f"error {e}")
        return temperature

# ------------------------------------------------------ #

    def Get_Steam_T(self):
        """Get the steam temperature

        :return: temperature int °C
        """

        readresult = self.instr.read(self.registers["Get_Steam_T"]["register"])
        if isinstance(readresult, Exception):
            raise readresult
        else:
            return readresult.registers[0]/self.registers["Get_Steam_T"]["scaling"]

    def Get_Air_H(self):
        """Get the air humidity

        :return: int %
        """

        readresult = self.instr.read(self.registers["Get_Air_H"]["register"])
        if isinstance(readresult, Exception):
            raise readresult
        else:
            return readresult.registers[0]/self.registers["Get_Air_H"]["scaling"]

    def Get_Flow(self):
        """Get the air humidity

        :return: int %
        """

        readresult = self.instr.read(self.registers["Get_Flow"]["register"])
        if isinstance(readresult, Exception):
            raise readresult
        else:
            return readresult.registers[0]/self.registers["Get_Flow"]["scaling"]

    def Get_Pressure(self):
        """Get the pressure

        :return: int Bar
        """

        readresult = self.instr.read(self.registers["Get_Pressure"]["register"])
        if isinstance(readresult, Exception):
            raise readresult
        else:
            return readresult.registers[0]/self.registers["Get_Pressure"]["scaling"]

    def Get_Tube_T(self):
        """Get the tube temperature

        :return: int °C
        """

        readresult = self.instr.read(self.registers["Get_Tube_T"]["register"])
        if isinstance(readresult, Exception):
            raise readresult
        else:
            return readresult.registers[0]/self.registers["Get_Tube_T"]["scaling"]