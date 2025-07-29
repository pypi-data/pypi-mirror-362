

HEADERS = {
    'Content-Type': 'application/json'
}


class ControlType:
    STOP = 'stop'
    START = 'start'
    DELETE = 'delete'
    SUSPEND = 'suspend'
    SPEEDUP = 'speedup'
    REQUEUE = 'requeue'


class TransferLines:
    LINE_RENDERG = 0  # 内网专线
    LINE_UNICOM = 1  # 中国联通
    LINE_TELECOM = 2  # 中国电信


class JobStatus:
    STATUS_ANALYZE_FAILED = '10030'
    STATUS_ANALYZED = '10031'
    STATUS_UPLOAD = '10032'
    STATUS_ANALYZE_DOING = '10039'
    STATUS_COMPLETED = 'Completed'

