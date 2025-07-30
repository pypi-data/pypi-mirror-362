import pytest
from unittest.mock import Mock
from struct import pack
from pysqream.globals import PROTOCOL_VERSION, SUPPORTED_PROTOCOLS
from tests.unit_tests.mocks import SocketMock, SQClients


class TestClient:
    def test_receive_full_data(self):
        """
        Test receiving complete data from socket
        """

        test_data = b'Hello World'
        socket_mock = SocketMock(test_data)
        client = SQClients(socket_mock)
        result = client.receive(len(test_data))

        assert result == test_data

    def test_receive_interrupted_connection(self):
        """
        Test handling of interrupted connection (receive returns 0)
        """

        socket_mock = SocketMock(b'')
        client = SQClients(socket_mock)

        with pytest.raises(ConnectionRefusedError) as exc_info:
            client.receive(10)

        assert 'SQreamd connection interrupted' in str(exc_info.value)

    def test_get_text_response(self):
        """
        Test getting text response with valid protocol
        """

        message = "test message"
        message_bytes = message.encode('utf8')
        header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(message_bytes))
        socket_mock = SocketMock(header + message_bytes)
        client = SQClients(socket_mock)
        response = client.get_response()

        assert response == message

    def test_protocol_mismatch(self):
        """
        Test handling of unsupported protocol version
        """

        invalid_protocol = max(SUPPORTED_PROTOCOLS) + 1
        header = pack('bb', invalid_protocol, 1) + pack('q', 10)
        socket_mock = SocketMock(header + b'0123456789')
        client = SQClients(socket_mock)

        with pytest.raises(Exception) as exc_info:
            client.get_response()

        assert 'Protocol mismatch' in str(exc_info.value)

    def test_send_string_basic(self):
        """
        Test basic string sending functionality
        """

        socket_mock = SocketMock(b'{"response": "ok"}')
        client = SQClients(socket_mock)
        test_json = '{"test": "value"}'
        client.send_string(test_json, get_response=False)
        sent_data = b''.join(socket_mock.sent_data)

        assert len(sent_data) == 10 + len(test_json)  # header + message
        assert test_json.encode('utf8') in sent_data

    def test_send_string_with_response(self):
        """
        Test sending string and getting response
        """

        response = '{"response": "ok"}'
        response_bytes = response.encode('utf8')
        header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(response_bytes))
        socket_mock = SocketMock(header + response_bytes)
        client = SQClients(socket_mock)
        result = client.send_string('{"test": "value"}')

        assert result == response

    def test_prepare_statement_success(self):
        """
        Test successful statement preparation
        """

        response = '{"statementPrepared": true, "chunkSize": 1048576, "canSupportParams": true}'
        response_bytes = response.encode('utf8')
        header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(response_bytes))
        socket_mock = SocketMock(header + response_bytes)
        client = SQClients(socket_mock)
        result = client.prepare_statement("SELECT * FROM table")

        assert result["statementPrepared"] is True
        assert result["canSupportParams"] is True
        assert result["chunkSize"] == 1048576

    def test_prepare_statement_error(self):
        """
        Test handling of preparation error
        """

        response = '{"error": "Invalid SQL"}'
        response_bytes = response.encode('utf8')
        header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(response_bytes))
        socket_mock = SocketMock(header + response_bytes)
        client = SQClients(socket_mock)

        with pytest.raises(Exception) as exc_info:
            client.prepare_statement("INVALID SQL")

        assert 'Invalid SQL' in str(exc_info.value)

    def test_execute_success(self):
        """
        Test successful statement execution
        """

        response = '{"executed": "executed"}'
        response_bytes = response.encode('utf8')
        header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(response_bytes))
        socket_mock = SocketMock(header + response_bytes)
        client = SQClients(socket_mock)
        client.execute_statement()
        sent_data = b''.join(socket_mock.sent_data)

        assert b'{"execute" : "execute"}' in sent_data

    def test_execute_error(self):
        """
        Test handling of execution error
        """

        response = '{"error": "Execution failed"}'
        response_bytes = response.encode('utf8')
        header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(response_bytes))
        socket_mock = SocketMock(header + response_bytes)
        client = SQClients(socket_mock)

        with pytest.raises(Exception) as exc_info:
            client.execute_statement()

        assert 'Execution failed' in str(exc_info.value)

    def test_reconnect_success(self):
        """
        Test successful reconnection
        """

        reconnect_response = '{"reconnected": true}'
        reconstruct_response = '{"statementReconstructed": true}'

        responses = []
        for resp in [reconnect_response, reconstruct_response]:
            resp_bytes = resp.encode('utf8')
            header = pack('bb', PROTOCOL_VERSION, 1) + pack('q', len(resp_bytes))
            responses.extend([header, resp_bytes])

        socket_mock = SocketMock(b''.join(responses))
        client = SQClients(socket_mock)

        client.reconnect(
            statement_id=1,
            database="test_db",
            service="test_service",
            username="test_user",
            password="test_pass",
            listener_id=3,
            ip="127.0.0.1",
            port=5000
        )

        sent_data = b''.join(socket_mock.sent_data)
        assert b'"reconnectDatabase"' in sent_data
        assert b'"reconstructStatement"' in sent_data

    def test_reconnect_gpu_error(self):
        """
        Test handling of GPU requirement error during reconnect
        """

        error_msg = 'The query requires a GPU-Worker. Ensure the SQream Service has GPU'

        socket_mock = SocketMock()
        client = SQClients(socket_mock)

        client.send_string = Mock(return_value=f'{{"error": "{error_msg}"}}')

        with pytest.raises(Exception) as exc_info:
            client.reconnect(1, "test_db", "test_service", "user", "pass", 3, "127.0.0.1", 5000)

        assert error_msg in str(exc_info.value)
