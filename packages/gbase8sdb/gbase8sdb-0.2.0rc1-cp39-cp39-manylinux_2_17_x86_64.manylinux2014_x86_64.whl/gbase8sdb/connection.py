# coding: utf-8

from . import __name__ as MODULE_NAME
from typing import Callable, Union
from . import errors
from . import driver
from .cursor import Cursor
from .lob import LOB
from .driver import DB_TYPE_BLOB, DB_TYPE_CLOB, DB_TYPE_NCLOB, DbType


class Connection:
    __module__ = MODULE_NAME

    def __init__(self, dsn: str, user: str, password: str) -> None:
        self._cyobj = None
        self._version = None
        cy_conn = driver.CyConnection(dsn, user, password)
        cy_conn.connect()
        self._cyobj = cy_conn
        
    def __repr__(self):
        cls_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        if self._cyobj is None:
            return f"<{cls_name} disconnected>"
        return f"<{cls_name} to {self.username}@{self.dsn}>"

    def __del__(self):
        if self._cyobj is not None:
            self._cyobj.close(in_del=True)
            self._cyobj = None

    def __enter__(self):
        self._verify_connected()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self._cyobj is not None:
            self._cyobj.close(in_del=True)
            self._cyobj = None

    def _verify_connected(self) -> None:
        if self._cyobj is None:
            errors.raise_error(errors.ERR_NOT_CONNECTED)   
    
    def close(self) -> None:
        self._verify_connected()
        self._cyobj.close()
        self._cyobj = None

    def commit(self) -> None:
        self._verify_connected()
        self._cyobj.commit()

    def createlob(
        self, lob_type: DbType, data: Union[str, bytes] = None
    ) -> LOB:
        self._verify_connected()
        if lob_type not in (DB_TYPE_CLOB, DB_TYPE_NCLOB, DB_TYPE_BLOB):
            message = (
                "lob type should be one of gbase8sdb.DB_TYPE_BLOB, "
                "gbase8sdb.DB_TYPE_CLOB or gbase8sdb.DB_TYPE_NCLOB"
            )
            raise TypeError(message)
        impl = self._cyobj.create_temp_lob_impl(lob_type)
        lob = LOB._create_with_cyobj(impl)
        if data:
            lob.write(data)
        return lob

    def cursor(self) -> Cursor:
        self._verify_connected()
        return Cursor(self)
   
    def ping(self) -> None:
        self._verify_connected()
        self._cyobj.ping()

    def rollback(self) -> None:
        self._verify_connected()
        self._cyobj.rollback()
        
    def cancel(self) -> None:
        self._verify_connected()
        self._cyobj.cancel()
        
    @property
    def autocommit(self) -> bool:
        self._verify_connected()
        return self._cyobj.autocommit

    @autocommit.setter
    def autocommit(self, value: bool) -> None:
        self._verify_connected()
        self._cyobj.autocommit = value

    @property
    def dsn(self) -> str:
        self._verify_connected()
        return self._cyobj.dsn

    @property
    def inputtypehandler(self) -> Callable:
        self._verify_connected()
        return self._cyobj.inputtypehandler

    @inputtypehandler.setter
    def inputtypehandler(self, value: Callable) -> None:
        self._verify_connected()
        self._cyobj.inputtypehandler = value


    @property
    def outputtypehandler(self) -> Callable:
        self._verify_connected()
        return self._cyobj.outputtypehandler

    @outputtypehandler.setter
    def outputtypehandler(self, value: Callable) -> None:
        self._verify_connected()
        self._cyobj.outputtypehandler = value

    @property
    def transaction_in_progress(self) -> bool:
        self._verify_connected()
        return self._cyobj.get_transaction_in_progress()

    @property
    def username(self) -> str:
        self._verify_connected()
        return self._cyobj.username

    @property
    def version(self) -> str:
        if self._version is None:
            self._verify_connected()
            self._version = ".".join(str(c) for c in self._cyobj.server_version)
        return self._version

    @property
    def warning(self) -> errors.ErrorWrapper:
        self._verify_connected()
        return self._cyobj.warning


def connect(dsn: str, user: str, password: str) -> Connection:
    """
    创建数据库连接，并返回连接对象
    """
    if len(dsn) == 0 or len(user) == 0 or len(password) == 0:
        raise errors.raise_error(errors.ERR_INVALID_CONNECT_PARAMS)
    return Connection(dsn=dsn, user=user, password=password)
