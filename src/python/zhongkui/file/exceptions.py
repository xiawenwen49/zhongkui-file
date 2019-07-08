"""zhongkui zhongkui exceptions"""


class ZhongkuiCriticalError(Exception):
    """zhongkui critical error"""


class ZhongkuiScanError(ZhongkuiCriticalError):
    """zhongkui scan error"""


class ZhongkuiHTTPError(ZhongkuiCriticalError):
    """zhongkui http error"""


class ZhongkuiUnpackError(ZhongkuiCriticalError):
    """zhongkui unpack error"""


class ZhongkuiDatabaseError(ZhongkuiCriticalError):
    """Zhongkui database error."""


class ZhongkuiOperationalError(Exception):
    """Zhongkui operation error."""


class ZhongkuiApiError(ZhongkuiOperationalError):
    """Error during API usage."""