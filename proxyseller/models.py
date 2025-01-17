from dataclasses import dataclass   
from datetime import datetime


@dataclass
class ExpiredAt:
    date: datetime
    timezone_type: int
    timezone: str

    def __post_init__(self):
        # 2025-02-12 23:59:59.000000
        self.date = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S.%f')

@dataclass
class ResidentialProxy:
    # {'rotation': -1, 'traffic_limit': 2147483648, 'expired_at': {'date': '2025-02-12 23:59:59.000000', 'timezone_type': 3, 'timezone': 'UTC'}, 'is_link_date': False, 'is_active': True, 'package_key': '884b7eb2ecc624d0c0c8', 'traffic_usage': 0, 'traffic_left': 2147483648, 'traffic_usage_sub': None, 'traffic_limit_sub': None, 'traffic_left_sub': None}
    rotation: int
    traffic_limit: int
    expired_at: ExpiredAt
    is_link_date: bool
    is_active: bool
    package_key: str
    traffic_usage: int
    traffic_left: int
    traffic_usage_sub: int
    traffic_limit_sub: int
    traffic_left_sub: int

    def __post_init__(self):
        self.expired_at = ExpiredAt(**self.expired_at)