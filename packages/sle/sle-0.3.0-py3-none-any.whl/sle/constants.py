class SleState:
    UNBOUND = "UNBOUND"
    BINDING = "BINDING"
    READY = "READY"
    STARTING = "STARTING"
    ACTIVE = "ACTIVE"
    STOPPING = " STOPPING"
    UNBINDING = "UNBINDING"


class AuthLevel:
    NONE = "none"
    BIND = "bind"
    ALL = "all"


class UnbindReason:
    END = "end"
    SUSPEND = "suspend"
    VERSION_NO_SUPPORTED = "version not supported"
    OTHER = "other"
