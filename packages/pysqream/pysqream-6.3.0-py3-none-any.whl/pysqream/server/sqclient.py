import json
import hashlib
from threading import Lock
from struct import pack, unpack
from pysqream.globals import PROTOCOL_VERSION, SUPPORTED_PROTOCOLS, clean_sqream_errors, CAN_SUPPORT_PARAMETERS, CAN_SUPPORT_CLUSTER_FILES, DEFAULT_CHUNKSIZE
from pysqream.ping import _start_ping_loop, _end_ping_loop, PingLoop
from pysqream.server.sqsocket import SQSocket
from typing import Union


class SQClient:
    def __init__(self, socket: SQSocket):
        self.socket: SQSocket = socket
        self.logger = socket.logger
        self.ping_loop: PingLoop = _start_ping_loop(self, self.socket)
        self.connection_id: Union[int, None] = None
        self.statement_id: Union[int, None] = None

    # Non socket aux. functionality
    @staticmethod
    def generate_message_header(data_length: int, is_text_msg: bool = True, protocol_version: int = PROTOCOL_VERSION):
        """
        Generate SQream's 10 byte header prepended to any message
        """

        return pack('bb', protocol_version, 1 if is_text_msg else 2) + pack(
            'q', data_length)

    @staticmethod
    def format_binary_for_log(binary_data, max_bytes=20):
        """
        Format binary data for logging with a summary that includes:
        - First few bytes (up to max_bytes)
        - Total size in bytes
        - Hash based on first 8 bytes, last 8 bytes, and length (only for large data which we truncate in log)
        """

        if not binary_data:
            return "<empty binary data>"

        if len(binary_data) <= max_bytes:
            return f"{binary_data} (size: {len(binary_data)} bytes)"

        hash_input = binary_data[:8] + binary_data[-8:] + str(len(binary_data)).encode()
        hash_digest = hashlib.md5(hash_input).hexdigest()[:8]

        return f"{binary_data[:max_bytes]}... (truncated, size: {len(binary_data)} bytes, md5: {hash_digest})"

    def receive(self, byte_num, timeout=None):
        """
        Read a specific amount of bytes from a given socket
        """

        data = bytearray(byte_num)
        view = memoryview(data)
        total = 0

        if timeout:
            self.socket.s.settimeout(timeout)

        while view:
            # Get whatever the socket gives and put it inside the bytearray
            received = self.socket.s.recv_into(view)
            if received == 0:
                self.logger.log_and_raise(ConnectionRefusedError, f'SQreamd connection interrupted - 0 returned by socket',
                                          connection_id=self.connection_id, statement_id=self.statement_id)
            view = view[received:]
            total += received

        if timeout:
            self.socket.s.settimeout(None)

        return data

    def get_response(self, is_text_msg: bool = True):
        """
        Get answer JSON string from SQream after sending a relevant message
        """

        lock = Lock()

        # Getting 10-byte response header back
        with lock:
            header = self.receive(10)
        server_protocol = header[0]

        if server_protocol not in SUPPORTED_PROTOCOLS:
            self.logger.log_and_raise(Exception, f"Protocol mismatch, client version - {PROTOCOL_VERSION}, server version - {server_protocol}",
                                      connection_id=self.connection_id, statement_id=self.statement_id)

        # bytes_or_text =  header[1]
        message_len = unpack('q', header[2:10])[0]

        with lock:
            receive = self.receive(message_len).decode(
                'utf8') if is_text_msg else self.receive(message_len)

        return receive

    def validate_response(self, response, expected):

        if expected not in response:
            # Color first line of SQream error (before the haskell thingy starts) in Red
            response = '\033[31m' + (response.split('\\n')[0] if clean_sqream_errors else response) + '\033[0m'
            self.logger.log_and_raise(Exception, f'\nexpected response {expected} but got:\n\n {response}',
                                      connection_id=self.connection_id, statement_id=self.statement_id)

    def send_string(self, json_cmd: str, get_response: bool = True, is_text_msg: bool = True, sock=None):
        """
        Encode a JSON string and send to SQream. Optionally get response
        """

        # Generating the message header, and sending both over the socket
        self.logger.debug(f"string sent: {json_cmd}", connection_id=self.connection_id, statement_id=self.statement_id)
        self.socket.send(self.generate_message_header(len(json_cmd)) + json_cmd.encode('utf8'))

        if get_response:
            return self.get_response(is_text_msg)

    def get_statement_id(self):
        self.statement_id = json.loads(self.send_string('{"getStatementId" : "getStatementId"}'))["statementId"]
        return self.statement_id

    def prepare_statement(self, statement: str):
        stmt_json = json.dumps({"prepareStatement": statement,
                                "chunkSize": DEFAULT_CHUNKSIZE,
                                "canSupportParams": CAN_SUPPORT_PARAMETERS,
                                "canSupportClusterFiles": CAN_SUPPORT_CLUSTER_FILES})
        res = self.send_string(stmt_json)
        self.validate_response(res, "statementPrepared")

        return json.loads(res)

    def execute_statement(self):
        self.validate_response(self.send_string('{"execute" : "execute"}'), 'executed')

    def reconnect(self, statement_id: int, database: str, service: str, username: str, password: str, listener_id: int, ip: str, port: int):
        self.socket.reconnect(ip=ip, port=port)
        # Send reconnect and reconstruct messages
        reconnect_str = (f'{{"service": "{service}", '
                         f'"reconnectDatabase":"{database}", '
                         f'"connectionId":{self.connection_id}, '
                         f'"listenerId":{listener_id}, '
                         f'"username":"{username}", '
                         f'"password":"{password}"}}')
        self.send_string(reconnect_str)
        # Since summer 2024 sqreamd worker could be configured with non-gpu (cpu) instance
        # it raises exception here like `The query requires a GPU-Worker. Ensure the SQream Service has GPU . . .`
        # This exception should be validated here. Otherwise, it will be validated at the next call which provides
        # Unexpected behavior
        self.validate_response(self.send_string(f'{{"reconstructStatement": {statement_id}}}'), "statementReconstructed")

    def get_query_type_in(self):
        """
        Sends queryType in message
        """

        return json.loads(self.send_string('{"queryTypeIn": "queryTypeIn"}')).get('queryType', [])

    def get_query_type_out(self):
        """
        Sends queryType out message
        """

        return json.loads(self.send_string('{"queryTypeOut" : "queryTypeOut"}'))

    def put(self, capacity: int):
        self.send_string(f'{{"put":{capacity}}}', False)

    def send_data(self, capacity: int, packed_cols: [], byte_count: int):
        """
        Perform parameterized query - "put" json, header and binary packed columns.
        Note: Stop and start ping is must between sending message to the server, this is part of the protocol.
        """

        # Sending put message
        _end_ping_loop(self.ping_loop)
        self.send_string(f'{{"put":{capacity}}}', False)
        self.ping_loop = _start_ping_loop(self, self.socket)

        # Sending binary header message
        _end_ping_loop(self.ping_loop)
        self.socket.send((self.generate_message_header(byte_count, False)))
        self.ping_loop = _start_ping_loop(self, self.socket)

        # Sending packed data (binary buffer)
        _end_ping_loop(self.ping_loop)

        for packed_col in packed_cols:
            self.logger.debug(lambda: f"Packed data sent: {self.format_binary_for_log(packed_col)}",
                              connection_id=self.connection_id, statement_id=self.statement_id)
            self.socket.send(packed_col)

        self.validate_response(self.get_response(), '{"putted":"putted"}')
        self.ping_loop = _start_ping_loop(self, self.socket)

    def fetch(self):
        res = self.send_string('{"fetch" : "fetch"}')
        self.validate_response(res, "colSzs")
        return json.loads(res)

    def connect_to_socket(self, username: str, password: str, database: str, service: str):
        res = self.send_string(f'{{"username":"{username}", "password":"{password}", "connectDatabase":"{database}", "service":"{service}"}}')
        res = json.loads(res)

        try:
            self.connection_id = res['connectionId']
            version = None

            if 'version' in res:
                version = res['version']

            return self.connection_id, version
        except KeyError:
            raise KeyError(f"Error connecting to database: {res['error']}")

    def close_statement(self):
        self.validate_response(self.send_string('{"closeStatement": "closeStatement"}'), '{"statementClosed":"statementClosed"}')
        self.statement_id = None

    def close_connection(self):
        self.validate_response(self.send_string('{"closeConnection": "closeConnection"}'), '{"connectionClosed":"connectionClosed"}')
        self.disconnect_socket()
        self.connection_id = None

    def disconnect_socket(self):
        self.socket.close()
        _end_ping_loop(self.ping_loop)
