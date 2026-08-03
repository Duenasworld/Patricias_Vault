from enum import Enum

APPNAME = "PWD-App"
CONFIG_FILE = "config/SLWtesting.cfg"
CERTIFICATE_FILE = "config/certificate.cfg"


class FlashMsgTyp(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


ENVIRONMENT_INFO = {"L": "Local", "M": "Mobile", "D": "Desktop"}


DEVELOPMENT_ENVIRONMENT = "L"
TEST_ENVIRONMENT = "L"
LINUX_DOCKER = "L"

ENVIRONMENT_COLOR = {"L": "bg-CS_BarRZX", "M": "bg-CS_BarRZX", "D": "bg-CS_BarRZY"}

ENVIRONMENT_TEXT = {"L": "text-black", "M": "text-white", "D": "text-white"}


UNIT_TEST = False


class SubUrl(Enum):
    USER_ACCESS = "/rest/authorization/v4/Access.json"
    USER_ENTITLEMENT = "rest/v4/GetEntitledUsers.json"


class PAK(Enum):
    FULL_ACCESS = "FullAccess"
    READONLY_ACCESS = "ReadOnlyAccess"
