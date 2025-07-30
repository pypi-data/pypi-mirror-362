import threading
import pytest
from unittest.mock import Mock, patch
from pysqream.ping import PingLoop, _start_ping_loop, _end_ping_loop
from tests.unit_tests.mocks import SocketMock


class TestPingLoop:
    @pytest.fixture
    def mock_socket(self):
        return SocketMock()

    @pytest.fixture
    def mock_client(self):
        client = Mock()
        client.generate_message_header.return_value = b'\x01\x01\x0c\x00\x00\x00\x00\x00\x00\x00'
        return client

    def test_ping_loop_initialization(self, mock_client, mock_socket):
        """
        Ensure PingLoop is initialized with the correct client and socket, is a thread, and is not marked as done
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        assert ping_loop.socket == mock_socket
        assert ping_loop.client == mock_client
        assert isinstance(ping_loop, threading.Thread)
        assert ping_loop.done is False

    def test_ping_loop_halt(self, mock_client, mock_socket):
        """
        Verify that calling halt() sets the 'done' flag to True, stopping the ping loop
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        assert ping_loop.done is False
        ping_loop.halt()
        assert ping_loop.done is True

    def test_sleep_returns_false_when_done(self, mock_client, mock_socket):
        """
        Check that the sleep() method returns False immediately when 'done' is True before sleeping
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        ping_loop.done = True
        assert ping_loop.sleep() is False

    @patch('time.sleep')
    def test_sleep_returns_true_after_timeout(self, mock_sleep, mock_client, mock_socket):
        """
        Ensure sleep() returns True after 100 short sleeps when 'done' is never set to True
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        mock_sleep.return_value = None
        assert ping_loop.sleep() is True
        assert mock_sleep.call_count == 100

    @patch('time.sleep')
    def test_sleep_returns_false_if_halted_during_sleep(self, mock_sleep, mock_client, mock_socket):
        """
        Test that sleep() exits early and returns False if the 'done' flag is set mid-sleep cycle
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        call_count = 0

        def side_effect(duration):
            nonlocal call_count
            call_count += 1
            if call_count == 5:
                ping_loop.done = True

        mock_sleep.side_effect = side_effect
        assert ping_loop.sleep() is False
        assert call_count == 5

    def test_run_sends_ping_messages(self, mock_client, mock_socket):
        """
        Verify that run() sends a properly formatted ping message when the loop runs once
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        ping_loop.sleep = Mock(side_effect=[True, False])
        json_cmd = '{"ping":"ping"}'
        expected_binary = mock_client.generate_message_header(len(json_cmd)) + json_cmd.encode('utf8')
        ping_loop.run()
        assert len(mock_socket.sent_data) == 1
        assert mock_socket.sent_data[0] == expected_binary

    def test_run_handles_socket_exception(self, mock_client, mock_socket):
        """
        Ensure that run() sets 'done' to True if an exception is raised during socket.send
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        ping_loop.sleep = Mock(side_effect=[True, False])
        mock_socket.send = Mock(side_effect=Exception("Socket error"))
        ping_loop.run()
        assert ping_loop.done is True

    def test_start_ping_loop(self, mock_client, mock_socket):
        """Check that _start_ping_loop creates and starts a PingLoop with the provided client and socket
        """

        with patch.object(PingLoop, 'start') as mock_start:
            ping_loop = _start_ping_loop(mock_client, mock_socket)
            assert isinstance(ping_loop, PingLoop)
            assert ping_loop.client == mock_client
            assert ping_loop.socket == mock_socket
            assert mock_start.called

    def test_end_ping_loop(self, mock_client, mock_socket):
        """
        Verify that _end_ping_loop halts the PingLoop and calls join on the thread
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        ping_loop.join = Mock()
        _end_ping_loop(ping_loop)
        assert ping_loop.done is True
        assert ping_loop.join.called

    def test_end_ping_loop_with_none(self):
        """
        Confirm that _end_ping_loop can safely handle a None input without raising an exception
        """

        _end_ping_loop(None)

    def test_end_ping_loop_without_start(self, mock_client, mock_socket):
        """
        Check that _end_ping_loop raises a RuntimeError if join is called on a PingLoop that wasn't started
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        with pytest.raises(RuntimeError) as exc_info:
            _end_ping_loop(ping_loop)
        assert "cannot join thread before it is started" in str(exc_info.value)

    def test_ping_loop_integration(self, mock_client, mock_socket):
        """
        Run an integration test to verify ping message is sent and PingLoop can be properly ended
        """

        ping_loop = PingLoop(mock_client, mock_socket)
        ping_loop.sleep = Mock(side_effect=[True, False])
        ping_loop.join = Mock()
        json_cmd = '{"ping":"ping"}'
        expected_binary = mock_client.generate_message_header(len(json_cmd)) + json_cmd.encode('utf8')
        ping_loop.run()
        assert len(mock_socket.sent_data) > 0
        assert mock_socket.sent_data[0] == expected_binary
        _end_ping_loop(ping_loop)
        assert ping_loop.done is True
