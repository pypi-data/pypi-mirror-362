import socket
import ssl
import sys
from pysqream.logger import ContextLogger


class SQSocket:
    """
    Extended socket class with some
    """

    def __init__(self, ip: str, port: int, logger: ContextLogger, use_ssl: bool = False):
        self.ip = ip
        self.port = port
        self.logger = logger
        self.use_ssl = use_ssl
        self._setup_socket(ip, port)

    def _setup_socket(self, ip: str, port: int):

        self.s = socket.socket()
        if self.use_ssl:
            # Python 3.10 SSL fix
            # 3.10 has increased the default TLS security settings,
            # need to downgrade to be compatible with current versions of sqream
            if sys.version_info.minor >= 10:
                self.ssl_context = ssl._create_unverified_context()
                self.ssl_context.set_ciphers('DEFAULT')  # 'AES256-SHA', 'RSA'
                # self.ssl_context.verify_mode = ssl.VerifyMode.CERT_NONE
                # self.ssl_context.options &= ~ssl.OP_NO_SSLv3
                self.s = self.ssl_context.wrap_socket(self.s, server_hostname=ip)
            else:
                self.s = ssl.wrap_socket(self.s)
        try:
            self.timeout(10)
            self.s.connect((ip, port))
        except ConnectionRefusedError as e:
            self.logger.log_and_raise(ConnectionRefusedError, "Connection refused, perhaps wrong IP?")
        except ConnectionResetError:
            self.logger.log_and_raise(Exception, 'Trying to connect to an SSL port with use_ssl = False')
        except Exception as e:
            if 'timeout' in repr(e).lower():
                self.logger.log_and_raise(Exception, "Timeout when connecting to SQream, perhaps wrong IP?")
            elif '[SSL: UNKNOWN_PROTOCOL] unknown protocol' in repr(e) or '[SSL: WRONG_VERSION_NUMBER]' in repr(e):
                self.logger.log_and_raise(Exception, 'Using use_ssl=True but connected to non ssl sqreamd port')
            elif 'EOF occurred in violation of protocol (_ssl.c:' in repr(e):
                self.logger.log_and_raise(Exception, 'Using use_ssl=True but connected to non ssl sqreamd port')
            else:
                self.logger.log_and_raise(Exception, e)
        else:
            self.timeout(None)

    def send(self, data):
        """Send data via open socket"""
        res = self.s.send(data)
        return res

    def close(self):
        return self.s.close()

    def timeout(self, timeout='not passed'):

        if timeout == 'not passed':
            return self.s.gettimeout()

        self.s.settimeout(timeout)

    # Extended functionality
    def reconnect(self, ip: str = None, port: int = None):
        self.s.close()
        self._setup_socket(ip or self.ip, port or self.port)
