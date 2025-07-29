from enum import Enum


class WarnCode(Enum):
    DCCVersionNotMatchWarn = ("000000", "dcc version not match. your version: {}, file version: {}")

    def code(self):
        return self.value[0]

    def msg(self, *args):
        return self.value[1].format(*args)


class ErrorCode(Enum):
    DCCFileNotExistsError = ("000000", "{} is not exist!")
    DCCExeNotFoundError = ("000001", "Houdini {} not found locally!")
    AnalyzeFailError = ("000002", "{}")

    def code(self):
        return self.value[0]

    def msg(self, *args):
        return self.value[1].format(*args)


class RenderGException(Exception):

    def __init__(self, error: 'ErrorCode', *args):
        self.err_code = error.code()
        self.err_msg = error.msg(*args)

    def __str__(self):
        return "Error code:{}, Error message:{}".format(self.err_code, self.err_msg)


class DCCFileNotExistsError(RenderGException):
    '''DCCExeNotFoundError'''


class DCCExeNotFoundError(RenderGException):
    '''DCCExeNotFoundError'''


class AnalyzeFailError(RenderGException):
    '''DCCExeNotFoundError'''
