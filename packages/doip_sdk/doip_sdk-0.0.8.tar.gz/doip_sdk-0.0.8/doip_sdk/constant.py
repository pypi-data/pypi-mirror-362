from enum import Enum


class Operation(Enum):
    HELLO = '0.DOIP/Op.Hello'
    CREATE = '0.DOIP/Op.Create'
    RETRIEVE = '0.DOIP/Op.Retrieve'
    UPDATE = '0.DOIP/Op.Update'
    DELETE = '0.DOIP/Op.Delete'
    SEARCH = '0.DOIP/Op.Search'
    LIST_OPERATION = '0.DOIP/Op.ListOperations'


class ResponseStatus(Enum):
    SUCCESS = '0.DOIP/Status.001'
    INVALID = '0.DOIP/Status.101'
    UNAUTHENTICATED = '0.DOIP/Status.102'
    UNAUTHORIZED = '0.DOIP/Status.103'
    UNKNOWN_DO = '0.DOIP/Status.104'
    DUPLICATED_PID = '0.DOIP/Status.105'
    UNKNOWN_OPERATION = '0.DOIP/Status.200'
    UNKNOWN_ERROR = '0.DOIP/Status.500'
