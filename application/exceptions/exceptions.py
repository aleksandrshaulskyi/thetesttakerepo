







class ApplicationException(Exception):
    'The base class of the application level exception to inherit from.'


class OpenPyXlException(ApplicationException):
    'The exception to be risen should any error happen during reading/writing with openpyxl.'


class HTTPManagerException(ApplicationException):
    'The exception to be risen should there be an exception during http manager methods execution.'
