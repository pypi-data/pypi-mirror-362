from enum import Enum

class LogMessageSeverity(Enum):
    Debug = 100
    Verbose = 200
    Init = 300
    Info = 500
    Warning = 600
    Error = 700
    Critical = 800
    Exception = 900
class StartEndEnum(Enum):
    Start = 400
    End = 402