import pytest
import pysqream
from tests.test_base import TestBaseWithoutBeforeAfter, Logger, connect_dbapi

logger = Logger()


class TestConnection(TestBaseWithoutBeforeAfter):

    def test_wrong_ip(self):
        """Test connection failure with incorrect IP address"""
        with pytest.raises(Exception, match="perhaps wrong IP?"):
            pysqream.connect('123.4.5.6', self.port, self.database, self.username, self.password, self.clustered, self.use_ssl)

    def test_wrong_port(self):
        """Test connection failure with incorrect port"""
        with pytest.raises(Exception, match="Connection refused"):
            pysqream.connect(self.ip, self.port + 1, self.database, self.username, self.password, self.clustered, self.use_ssl)

    def test_wrong_database(self):
        """Test connection failure with incorrect database name"""
        db_name = self.database + "bla"
        with pytest.raises(Exception, match=f"Database {db_name} no longer exists"):
            pysqream.connect(self.ip, self.port, db_name, self.username, self.password, self.clustered, self.use_ssl)

    def test_wrong_username(self):
        """Test connection failure with incorrect username"""
        user_name = self.username + "bla"
        with pytest.raises(Exception, match=f"role '{user_name}' doesn't exist"):
            pysqream.connect(self.ip, self.port, self.database, user_name, self.password, self.clustered, self.use_ssl)

    def test_wrong_password(self):
        """Test connection failure with incorrect password"""
        with pytest.raises(Exception, match="wrong password for role 'sqream'"):
            pysqream.connect(self.ip, self.port, self.database, self.username, self.password + "bla", self.clustered, self.use_ssl)

    def test_close_connection(self):
        """Test closing connection and cursor behavior"""
        con = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl,
                            port=self.port, picker_port=self.picker_port,
                            database=self.database, username=self.username,
                            password=self.password)
        cur = con.cursor()
        con.close()

        with pytest.raises(Exception, match="Connection has been closed"):
            cur.execute('select 1')

    def test_close_already_closed_connection(self):
        """Test closing a connection that is already closed"""
        con = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl,
                            port=self.port, picker_port=self.picker_port,
                            database=self.database, username=self.username,
                            password=self.password)
        con.close()

        with pytest.raises(Exception, match="Trying to close a connection that's already closed"):
            con.close()

    def test_negative_clustered(self):
        """Test connection with incorrect clustered setting"""
        with pytest.raises(Exception, match="Connected with clustered=True, but apparently not a server picker port"):
            pysqream.connect(self.ip, self.port, self.database, self.username,
                             self.password, True, self.use_ssl)

    def test_sq_12821(self):
        """Test that closing one connection doesn't affect other connections"""
        con1 = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl,
                             port=self.port, picker_port=self.picker_port,
                             database=self.database, username=self.username,
                             password=self.password)
        con2 = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl,
                             port=self.port, picker_port=self.picker_port,
                             database=self.database, username=self.username,
                             password=self.password)

        cur = con1.cursor()
        cur.execute('select 1')
        cur.fetchall()
        cur.close()

        con2.close()

        cur = con1.cursor()
        cur.execute('select 1')
        cur.fetchall()
        cur.close()

        con1.close()

    def test_positive_clustered(self):
        logger.info("Connection tests - positive test for clustered=True")
        con = pysqream.connect(self.ip, self.picker_port, self.database, self.username, self.password, True, self.use_ssl, log=True)
        cur = con.cursor()
        cur.execute('select 1')
        res = cur.fetchall()[0][0]

        assert res == 1
        con.close()

        logger.info("Connection tests - both clustered and use_ssl flags on True")
        con = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl, port=self.port,
                            picker_port=self.picker_port, database=self.database,
                            username=self.username, password=self.password)
        cur = con.cursor()
        res = cur.execute('select 1').fetchall()[0][0]

        assert res == 1
        con.close()

    def test_close_connection_when_not_connected(self):
        """Test closing a connection that hasn't been connected to database"""
        con = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl,
                            port=self.port, picker_port=self.picker_port,
                            database=self.database, username=self.username,
                            password=self.password)
        con._Connection__connect_to_socket = False
        con._Connection__connect_to_database = False

        con.close()
        con._Connection__close_connection()

        assert con._Connection__cursors == {}
        assert not con._Connection__is_connection_closed

    def test_close_base_connection_with_sub_connections(self):
        """Test closing a base connection with sub-connections"""
        base_conn = connect_dbapi(self.ip, clustered=self.clustered, use_ssl=self.use_ssl,
                                  port=self.port, picker_port=self.picker_port,
                                  database=self.database, username=self.username,
                                  password=self.password)

        cur1 = base_conn.cursor()
        cur2 = base_conn.cursor()

        assert base_conn._Connection__cursors == {}  # every cursor we open should be in the sub connection that is opened, not in main base connection
        assert len(base_conn._Connection__sub_connections) == 2
        assert len(base_conn._Connection__sub_connections[0]._Connection__sub_connections) == 0
        assert len(base_conn._Connection__sub_connections[1]._Connection__sub_connections) == 0

        for sub_conn in base_conn._Connection__sub_connections:
            assert len(sub_conn._Connection__cursors.keys()) == 1

        base_conn.close()
        assert len(base_conn._Connection__sub_connections) == 0
        assert base_conn._Connection__is_connection_closed
        assert base_conn._Connection__cursors == {}
        assert cur1.get_is_cursor_closed()
        assert cur2.get_is_cursor_closed()
