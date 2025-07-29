from pymodbus.client import ModbusTcpClient
from pymodaq.utils.logger import set_logger, get_module_name
logger = set_logger(get_module_name(__file__))


class SyncModBusInstrument:
    """

    """
    def __init__(self, host, port = 502):
        self.connected = False
        self.host = host
        self.port = port
        self.precision = 1
        self.modbus = ModbusTcpClient(self.host)
        self.registerdict = {}

    def close(self):
        """End the connection
        """
        self.modbus.close()
        self.connected = False

    def write(self, register, value):
        """

        :param register:
        :param value:
        :return:
        """

        self.modbus.write_register(register, value)

    def read(self, register):
        """

        :param register:
        :return:
        """
        return self.modbus.read_input_registers(register)

    def ini_hw(self):
        """

        """
        try:
            self.modbus.connect()
            self.connected = True
            return self.connected
        except:
            return False

    def addregister(self, name, address, values, readwrite):
        """

        :param adress:
        :param values:
        :param readwrite:
        :return:
        """
        if str(address) not in address.keys():
            self.registerdict[str(address)]= {'authorizedvalues' :values, 'rwstatus': readwrite}