from unittest.mock import Mock
from pysqream.server.sqclient import SQClient
from pysqream.logger import ContextLogger


class SQClients(SQClient):
    """
    behaves just like SQClient, but making sure that we close ping loops so pytest will end and exit
    """

    all_clients = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_clients.append(self)

    @classmethod
    def close_all_connections(cls):
        for client in cls.all_clients:
            client.disconnect_socket()

        cls.all_clients.clear()


class SocketMock:
    def __init__(self, recv_data=None):
        self.s = Mock()
        self.s.recv_into = self.mock_recv_into
        self.sent_data = []
        self.recv_data = recv_data or b''
        self.position = 0
        self.logger = ContextLogger()

    def mock_recv_into(self, view):
        remaining = len(self.recv_data) - self.position
        if remaining == 0:
            return 0
        chunk_size = min(len(view), remaining)
        view[:chunk_size] = self.recv_data[self.position:self.position + chunk_size]
        self.position += chunk_size
        return chunk_size

    def send(self, data):
        self.sent_data.append(data)
        return len(data)

    def close(self):
        return

    def reconnect(self, ip=None, port=None):
        return
