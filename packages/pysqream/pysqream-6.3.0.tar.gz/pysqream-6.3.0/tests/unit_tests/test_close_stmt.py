"""Tests for catching errors on closeStatement

In the past, the closeStatement operation remained silent, causing interference
with SQ-13979. As a result, when inserting sequences (TEXT / ARRAY) that
exceeded the limited size, the process would silently close, giving the
impression of success.
"""

import pytest
from pysqream.cursor import Cursor
from tests.unit_tests.test_client import SQClients
from tests.unit_tests.mocks import SocketMock
from pysqream.server.connection_params import ConnectionParams
from pysqream.logger import ContextLogger


@pytest.mark.parametrize("bad_message", ['{"error": "mock SQREAM error"}',
                                         "I'm invalid json",
                                         '["valid array"]'])
def test_raise_on_error_from_sqream(monkeypatch, bad_message):
    """Test that JSON with error from SQREAM on closeStatement raises Exception"""

    socket_mock = SocketMock()
    client = SQClients(socket_mock)
    conn_params = ConnectionParams(
        ip="127.0.0.1",
        port=5000,
        database="test_db",
        username="test_user",
        password="test_pass",
        clustered=False,
        use_ssl=False,
        service="test_service"
    )
    client.send_string = lambda *_: bad_message

    cur = Cursor(
        conn_params=conn_params,
        client=client,
        connection_id=123,
        allow_array=False,
        logger=ContextLogger()
    )
    cur._Cursor__client = client
    cur._Cursor__open_statement = True

    with pytest.raises(Exception) as exc_info:
        cur._Cursor__close_stmt()

    assert ('expected response {"statementClosed":"statementClosed"} but got:' in str(exc_info.value)
            and bad_message in str(exc_info.value))
