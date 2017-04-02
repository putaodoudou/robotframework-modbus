from rammbock import Rammbock
from .version import VERSION

MODBUS_PORT = 502
PROTOCOL_ID_VALUE = 1
PDU_OFFSET = 2
FC1_READ_COILS = 0x01
FC1_REQUEST_MSG = 'Read Coils (FC1)'

class Modbus(object):
    """Modbus TCP/IP is a protocol testing library for the Robot Framework
    (generic test automation framework) which uses the test library Rammbock
    (generic protocol library) to provide keywords for testing Modbus TCP/IP
    v1.1b (NOT: Modbus over TCP/IP).

    Have a look into https://en.wikipedia.org/wiki/Modbus#Frame_format for an
    overview or into
    http://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b.pdf
    for a deeper insight.

    Implemented as hybrid Robot Framework API.
    """

    ROBOT_LIBRARY_VERSION = VERSION

    def start_modbus_server(self, ip, name=None, timeout=None):
        """Starts a new Modbus TCP/IP server.

        Examples:
        | Start Modbus Server | 10.10.10.2 |
        | Start Modbus Server | 10.10.10.2 | name=Server1 | timeout=5 |
        """
        Rammbock.start_tcp_server(ip=ip, port=MODBUS_PORT, name=name,
                    timeout=timeout, protocol='modbus', family='ipv4')

    def switch_modbus_server(self, name):
        """Switches the current active Modbus server to the given server `name`.

        Example:
        | Switch modbus server | Server1 |
        """
        Rammbock.switch_server(name=name)

    def close_modbus_server(self, name=None):
        """Closes the Modbus server connection based on the server `name`.

        If no `name` is provided it will close the current active connection.
        You have to explicitly `Switch Modbus Server` after close when sending
        or receiving any message without explicitly passing the server name.

        Example:
        | Close modbus server |
        | Close modbus server | Server1 |
        """
        Rammbock.close_server(name=name)

    def start_modbus_client(self, ip, name=None, timeout=None):
        """Starts a new Modbus TCP/IP client.

        Examples:
        | Start Modbus Client | 10.10.10.2 |
        | Start Modbus Client | 10.10.10.2 | name=Client1 | timeout=5 |
        """
        Rammbock.start_tcp_client(ip, port=MODBUS_PORT, name=name,
                    timeout=timeout, protocol='modbus', family='ipv4')

    def connect_modbus_client(self, server, name=None):
        """Connects a Modbus client to a Modbus server. If client `name` is not
        given then the latest client is connected.

        Examples:
        | Connect modbus client | 10.10.10.2 |
        | Connect modbus client | 10.10.10.2 | name=Client1 |
        """
        Rammbock.connect(host=server, port=MODBUS_PORT, name=name)

    def switch_modbus_client(self, name):
        """Switches the current active Modbus client to the given client `name`.

        Example:
        | Switch modbus client | Client1 |
        """

    def close_modbus_client(self, name=None):
        """Closes the modbus client connection based on the client `name`.

        If no name is provided it will close the current active connection.
        You have to explicitly `Switch modbus client` after close when sending
        or receiving any message without explicitly passing the client name.

        Example:
        | Close modbus client |
        | Close modbus client | Client1 |
        """
        Rammbock.close_client(name=name)

    def reset_modbus(self):
        """Closes all Modbus connections, deletes all Modbus servers, clients
        and the protocol.
        TODO: restrict to single rammbock instance
        """
        Rammbock.reset_rammbock()

    def reset_modbus_message_streams(self):
        """Reset streams and sockets of incoming messages.
        """
        Rammbock.clear_message_streams()

    def _define_modbus_protocol(self):
        """Defines the Modbus TCP/IP protocol.
        """
        Rammbock.new_protocol('modbus')
        Rammbock.u16(name='transactionIdentifier', value=None, align=None)
        Rammbock.u16(name='protocolIdentifier', value=PROTOCOL_ID_VALUE, align=None)
        Rammbock.u16(name='lengthField', value=None, align=None)
        Rammbock.u8(name='unitIdentifier', value=None, align=None)
        Rammbock.u8(name='functionCode', value=None, align=None)
        Rammbock.pdu(length='lengthField-PDU_OFFSET')  # TODO syntax ok?
        Rammbock.end_protocol()

    def _define_valid_fc1_request(self):
        """Define the FC1 request message template.

        Dynamic header content:
        - transactionIdentifier
        - unitIdentifier

        Dynamic PDU content:
        - starting address (2 bytes)
        - quantity of coils (2 bytes)
        """
        Rammbock.new_message(message_name=FC1_REQUEST_MSG, protocol='modbus')  #, 'lengthField':'STARTING_ADDRESS_BYTES+QUANTITY_OF_COILS_BYTES', 'functionCode':'FC1_READ_COILS')
        Rammbock.save_template(name=FC1_REQUEST_MSG, unlocked=False)

#    def server_sends_read_coils_request(self, transaction_id, unit_id, starting_address, quantity_of_coils):
#        """Server sends a new FC1 request message to given client `unit_id`.
#
#        Example:
#        | Server sends fc1 request | 1 |  |
#        """
#        Rammbock.load_copy_of_template(name=FC1_REQUEST_MSG) #, 'transactionIdentifier':transaction_id, 'unitIdentifier':unit_id)
#        Rammbock.u16()
#        Rammbock.u16()

    def discrete_input(self, name):
        """Add a discrete input with given `name` to the template.

        Example:
        | Discrete input | DigitalInput |
        """

    def coil(self, name, value):
        """Add a single coil with given name `name` and value `value`
        to the template.

        Example:
        | Coil | DigitalInput |
        | Coil | DigitialOutput | 0xFF00 |
        """
        ON = 0xFF00
        OFF = 0x0000
        if value not in [ON, OFF]:
            raise Exception("Invalid single coil value given")
        Rammbock.u8(name=name, value=value, align=None)

    def coils(self, name, value):
        """Add multiple coils with given name `name` and values `values`
        to the template.

        Examples:
        | Coils |  |
        |  |  |  |
        """
        # TODO range check
        #COIL_BITS=[0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]
        #if value not combination of COIL_BITS:
        #   raise Exception("Invalid multiple coil value given")
        Rammbock.u8(name=name, value=value, align=None)

    def input_register(self, name):
        """Add a input register with given

        Example:
        | Input register |  |
        """

    def holding_register(self, name, value=None):
        """Add a register (input/holding) with given name `name` and value
        `value` to the template.
        TODO: range check when value given and writing 0x0000-0xFFFF

        Example:
        | Holding register | AnalogIn1 |
        | Holding register | AnalogOut1 | 65535 |
        """
        Rammbock.u16(name=name, value=value, align=None)
