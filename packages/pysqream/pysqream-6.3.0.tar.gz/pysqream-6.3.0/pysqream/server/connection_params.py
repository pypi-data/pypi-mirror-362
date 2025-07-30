from dataclasses import dataclass


@dataclass
class ConnectionParams:
    """
    Holds the connection parameters to SQreamDB.
    Origin ip and Origin port are for cases when clustered is true, and we get the picker ip and port. later on we get the sqream ip and port
    """

    ip: str
    port: int
    database: str
    username: str
    password: str
    clustered: bool
    use_ssl: bool
    service: str

    def __post_init__(self):
        self.origin_ip: str = self.ip
        self.origin_port: int = self.port
