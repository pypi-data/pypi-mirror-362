from __future__ import annotations  # allow forward references
from contextlib import suppress
from importlib import import_module
from inspect import FrameInfo, stack
from enum import Enum, StrEnum
from logging import Logger
from pypomes_core import (
    APP_PREFIX,
    env_get_str, dict_get_key, dict_stringify
)
from pypomes_db import (
    db_exists, db_count, db_select,
    db_insert, db_update, db_delete
)
from types import ModuleType
from typing import Any, Final, Type, TypeVar

# base folder for all 'PySob' subclasses
SOB_BASE_FOLDER: Final[str] = env_get_str(key=f"{APP_PREFIX}_SOB_BASE_FOLDER")

# 'Sob' stands for all subclasses of 'PySob'
Sob = TypeVar("Sob",
              bound="PySob")

# must have entries for all subclasses of 'PySob':
#   key: the qualified name of the class type of the subclass of 'PySob'
#   value: a tuple with 4 elements:
#     - the name of the entity's DB table
#     - the name of its PK attribute (maps to 'self.id')
#     - the type of its PK attribute (currently, 'int' and 'str' are supported)
#     - whether the PK attribute is an identity (has values generated automatically by the DB)
_db_specs: dict[str, (StrEnum | str, StrEnum | str, type, bool)] = {}

# maps input parameters to DB columns
_attrs_map: dict[str, dict[StrEnum | str, StrEnum | str]] = {}

# holds 'PySob' subclasses referred to by the current class
_sob_references: dict[str, list[type[Sob]]] = {}


class PySob:
    """
    Root entity.
    """

    def __init__(self,
                 errors: list[str] = None,
                 load_references: bool = False,
                 where_data: dict[str, Any] = None,
                 db_conn: Any = None,
                 logger: Logger = None) -> None:

        self._logger: Logger = logger
        # maps to the entity's PK in its DB table (returned on INSERT operations)
        self.id: int | str = 0

        # determine whether the instance exists in the database
        self._is_new: bool = True

        if where_data:
            self.load(errors=errors,
                      omit_nulls=True,
                      where_data=where_data)
        if not errors and load_references:
            self.__load_references(errors=errors,
                                   db_conn=db_conn)

    def insert(self,
               errors: list[str] | None,
               db_conn: Any = None) -> bool:

        # prepara data for INSERT
        return_col: dict[str, type] | None = None
        insert_data: dict[str, Any] = self.to_columns(omit_nulls=True)
        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        if _db_specs[class_name][3]:
            # PK is an identity column
            insert_data.pop(_db_specs[class_name][1], None)
            return_col = {_db_specs[class_name][1]: _db_specs[class_name][2]}

        # execute the INSERT statement
        op_errors: list[str] = []
        rec: tuple[Any] = db_insert(errors=op_errors,
                                    insert_stmt=f"INSERT INTO {_db_specs[class_name][0]}",
                                    insert_data=insert_data,
                                    return_cols=return_col,
                                    connection=db_conn,
                                    logger=self._logger)
        if op_errors:
            msg = ("Error INSERTing into table "
                   f"{_db_specs[class_name][0]}: {'; '.join(op_errors)}")
            if isinstance(errors, list):
                errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            self._is_new = False
            if _db_specs[class_name][3]:
                # PK is an identity column
                self.id = rec[0]

        return not op_errors

    def update(self,
               errors: list[str] | None,
               db_conn: Any = None) -> bool:

        # prepare data for UPDATE
        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        update_data: dict[str, Any] = self.to_columns(omit_nulls=False)
        key: int = update_data.pop(_db_specs[class_name][1])

        # execute the UPDATE statement
        op_errors: list[str] = []
        db_update(errors=op_errors,
                  update_stmt=f"UPDATE {_db_specs[class_name][0]}",
                  update_data=update_data,
                  where_data={_db_specs[class_name][1]: key},
                  min_count=1,
                  max_count=1,
                  connection=db_conn,
                  logger=self._logger)
        if op_errors:
            msg: str = ("Error UPDATEing table "
                        f"{_db_specs[class_name][0]}: {'; '.join(op_errors)}")
            if isinstance(errors, list):
                errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)

        return not op_errors

    def persist(self,
                errors: list[str] | None,
                db_conn: Any = None) -> bool:

        # declare the return variable
        result: bool

        if self._is_new:
            result = self.insert(errors=errors,
                                 db_conn=db_conn)
        else:
            result = self.update(errors=errors,
                                 db_conn=db_conn)
        return result

    def delete(self,
               errors: list[str] | None,
               db_conn: Any = None) -> int | None:

        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        where_data: dict[str, Any]
        if self.id:
            where_data = {_db_specs[class_name][1]: self.id}
        else:
            where_data = self.to_columns(omit_nulls=True)
            where_data.pop(_db_specs[class_name][1], None)

        # execute the DELETE statement
        op_errors: list[str] = []
        result: int = db_delete(errors=op_errors,
                                delete_stmt=f"DELETE FROM {_db_specs[class_name][0]}",
                                where_data=where_data,
                                max_count=1,
                                connection=db_conn,
                                logger=self._logger)
        if op_errors:
            msg = ("Error DELETEing from table "
                   f"{_db_specs[class_name][0]}: {'; '.join(op_errors)}")
            if isinstance(errors, list):
                errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            self.clear()

        return result

    def clear(self) -> None:

        for key in self.__dict__:
            self.__dict__[key] = None

    def set(self,
            data: dict[str, Any]) -> None:

        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        for key, value in data.items():
            attr: str = (_attrs_map.get(class_name) or {}).get(key) or key

            # usa nomes de enums atribuídos como valores em 'data'
            if isinstance(value, Enum) and "use_names" in value.__class__:
                value = value.name  # noqa: PLW2901

            if attr in self.__dict__:
                self.__dict__[attr] = value
            elif self._logger:
                self._logger.warning(msg=f"'{attr}'is not an attribute of "
                                         f"{_db_specs[class_name][0]}")

    def in_db(self,
              errors: list[str] | None,
              where_data: dict[str, Any] = None,
              db_conn: Any = None) -> bool | None:

        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        if not where_data:
            if self.id:
                # use object's ID
                where_data = {_db_specs[class_name][1]: self.id}
            else:
                # use object's available data
                where_data = self.to_columns(omit_nulls=True)
                where_data.pop(_db_specs[class_name][1], None)

        return db_exists(errors=errors,
                         table=_db_specs[class_name][0],
                         where_data=where_data,
                         connection=db_conn,
                         logger=self._logger)

    def load(self,
             errors: list[str] | None,
             omit_nulls: bool,
             where_data: dict[str, Any] = None,
             db_conn: Any = None) -> bool:

        # initialize the return variable
        result: bool = False

        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        if not where_data:
            if self.id:
                where_data = {_db_specs[class_name][1]: self.id}
            else:
                where_data = self.to_columns(omit_nulls=omit_nulls)
                where_data.pop(_db_specs[class_name][1], None)

        # loading the object from the database might fail
        attrs: list[str] = self.get_columns()
        op_errors: list[str] = []
        recs: list[tuple] = db_select(errors=op_errors,
                                      sel_stmt=f"SELECT {', '.join(attrs)} "
                                               f"FROM {_db_specs[class_name][0]}",
                                      where_data=where_data,
                                      limit_count=2,
                                      connection=db_conn,
                                      logger=self._logger)
        msg: str | None = None
        if op_errors:
            msg = ("Error SELECTing from table "
                   f"{_db_specs[class_name][0]}: {'; '.join(op_errors)}")
        elif not recs:
            msg = (f"No record found on table "
                   f"{_db_specs[class_name][0]} for {dict_stringify(where_data)}")
        elif len(recs) > 1:
            msg = (f"More than on record found on table "
                   f"{_db_specs[class_name][0]} for {dict_stringify(where_data)}")

        if msg:
            if isinstance(errors, list):
                errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            rec: tuple = recs[0]
            for inx, attr in enumerate(attrs):
                # PK attribute in DB table might have a different name
                if attr == _db_specs[class_name][0]:
                    self.__dict__["id"] = rec[inx]
                else:
                    self.__dict__[attr] = rec[inx]
            self._is_new = False
            result = True

        return result

    def get_columns(self) -> list[str]:

        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        # PK attribute in DB table might have a different name
        result: list[str] = [_db_specs[class_name][1]]
        result.extend([k for k in self.__dict__
                      if k.islower() and not k.startswith("_") and not k == "id"])
        return result

    def to_columns(self,
                   omit_nulls: bool) -> dict[str, Any]:

        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        # PK attribute in DB table might have a different name
        result: dict[str, Any] = {_db_specs[class_name][1]: self.__dict__.get("id")}
        result.update({k: v for k, v in self.__dict__.items()
                      if k.islower() and not (k.startswith("_") or k == "id" or (omit_nulls and v is None))})
        return result

    def to_params(self,
                  omit_nulls: bool) -> dict[str, Any]:

        return self.data_to_params(data=self.__dict__,
                                   omit_nulls=omit_nulls)

    def data_to_params(self,
                       data: dict[str, Any],
                       omit_nulls: bool) -> dict[str, Any]:

        # initialize the return variable
        result: dict[str, Any] = {}
        
        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        for k, v in data.items():
            if not omit_nulls or v is not None:
                attr: str = dict_get_key(source=_attrs_map.get(class_name) or {},
                                         value=k) or k
                result[attr] = v

        return result

    # noinspection PyUnusedLocal
    def load_reference(self,
                       __cls: type[Sob],
                       /,
                       errors: list[str] | None,
                       db_conn: Any | None) -> Sob | list[Sob] | None:

        # must be implemented by subclasses containing references
        msg: str = f"Subclass {__cls.__module__}.{__cls.__qualname__} failed to implement 'load_reference()'"
        if isinstance(errors, list):
            errors.append(msg)
        if self._logger:
            self._logger.error(msg=msg)

        return None

    def __load_references(self,
                          errors: list[str] | None,
                          db_conn: Any) -> None:

        op_errors: list[str] = []
        class_name: str = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        for cls in (_sob_references.get(class_name) or []):
            self.load_reference(cls,
                                errors=op_errors,
                                db_conn=db_conn)
            if op_errors:
                msg = (f"Error SELECTing from table "
                       f"{_db_specs[cls][0]}: {'; '.join(op_errors)}")
                if isinstance(errors, list):
                    errors.append(msg)
                if self._logger:
                    self._logger.error(msg=msg)
                break

    @staticmethod
    # HAZARD:
    #   1. because 'typings.Type' has been deprecated, 'type' should be used here
    #   2. 'Sob' stands for all subclasses of 'PySob', and thus 'type[Sob]' should suffice
    #   3. PyCharm's code inspector, however, takes 'type[Sob]' to mean strict 'PySob' class
    #   4. thus, a fallback to 'Type[PySub]' was necessary
    def initialize(db_specs: tuple[StrEnum | str, StrEnum | str, int | str] |
                             tuple[StrEnum | str, StrEnum | str, int, bool],  # noqa
                   attrs_map: dict[StrEnum | str, StrEnum | str] = None,
                   sob_references: list[Type[PySob]] = None) -> None:

        # signal global variables
        global _db_specs, _attrs_map, _sob_references

        # obtain the invoking class
        cls: type[Sob] = PySob.__get_invoking_class()

        # initialize it
        if cls:
            name: str = f"{cls.__module__}.{cls.__qualname__}"
            if len(db_specs) == 3:
                # 'id' defaults to being an identity attribute in the DB for type 'int'
                db_specs += (db_specs[2] is int,)
            _db_specs.update({name: db_specs})
            if attrs_map:
                _attrs_map.update({name: attrs_map})
            if sob_references:
                _sob_references.update({name: sob_references})

    @staticmethod
    def count(errors: list[str] | None,
              where_data: dict[str, Any],
              db_conn: Any = None,
              logger: Logger = None) -> int | None:

        # inicialize the return variable
        result: int | None = None

        # obtain the invoking class
        op_errors: list[str] = []
        cls: type[Sob] = PySob.__get_invoking_class(errors=op_errors)

        if not op_errors:
            name: str = f"{cls.__module__}.{cls.__qualname__}"
            result = db_count(errors=errors,
                              table=_db_specs[name][0],
                              where_data=where_data,
                              connection=db_conn,
                              logger=logger)
        return result

    @staticmethod
    def exists(errors: list[str] | None,
               where_data: dict[str, Any],
               db_conn: Any = None,
               logger: Logger = None) -> int | None:

        # inicialize the return variable
        result: bool | None = None

        # obtain the invoking class
        op_errors: list[str] = []
        cls: type[Sob] = PySob.__get_invoking_class(errors=op_errors)

        if not op_errors:
            name: str = f"{cls.__module__}.{cls.__qualname__}"
            result = db_exists(errors=errors,
                               table=_db_specs[name][0],
                               where_data=where_data,
                               connection=db_conn,
                               logger=logger)
        if op_errors:
            msg = "; ".join(op_errors)
            if isinstance(errors, list):
                errors.append(msg)
            if logger:
                logger.error(msg=msg)

        return result

    @staticmethod
    def retrieve(errors: list[str] | None,
                 where_data: dict[str, Any] = None,
                 load_references: bool = False,
                 min_count: int = None,
                 max_count: int = None,
                 limit_count: int = None,
                 db_conn: Any = None,
                 logger: Logger = None) -> list[Sob] | None:

        # inicialize the return variable
        result: list[Sob] | None = None

        # obtain the invoking class
        op_errors: list[str] = []
        cls: type[Sob] = PySob.__get_invoking_class(errors=op_errors)

        if not op_errors:
            name: str = f"{cls.__module__}.{cls.__qualname__}"
            recs: list[tuple[int | str]] = db_select(errors=op_errors,
                                                     sel_stmt=f"SELECT {_db_specs[name][1]} "
                                                              f"FROM {_db_specs[name][0]}",
                                                     where_data=where_data,
                                                     min_count=min_count,
                                                     max_count=max_count,
                                                     limit_count=limit_count,
                                                     connection=db_conn,
                                                     logger=logger)
            if not op_errors:
                # build the objects list
                objs: list[Sob] = []
                for rec in recs:
                    # constructor of 'cls', a subclass of 'PySob', takes slightly different arguments
                    objs.append(cls(rec[0],
                                    errors=op_errors,
                                    load_references=load_references,
                                    db_conn=db_conn,
                                    logger=logger))
                    if op_errors:
                        break

                if not op_errors:
                    result = objs

        if op_errors:
            msg = "; ".join(op_errors)
            if isinstance(errors, list):
                errors.append(msg)
            if logger:
                logger.error(msg=msg)

        return result

    @staticmethod
    def erase(errors: list[str] | None,
              where_data: dict[str, Any],
              db_conn: Any = None,
              logger: Logger = None) -> int | None:

        # initialize the return variable
        result: int | None = None

        # obtain the invoking class
        op_errors: list[str] = []
        cls: type[Sob] = PySob.__get_invoking_class(errors=op_errors)

        # delete specified tuples
        if not op_errors:
            name: str = f"{cls.__module__}.{cls.__qualname__}"
            result: int = db_delete(errors=op_errors,
                                    delete_stmt=f"DELETE FROM {_db_specs[name][0]}",
                                    where_data=where_data,
                                    connection=db_conn,
                                    logger=logger)
        if op_errors:
            msg = "; ".join(op_errors)
            if isinstance(errors, list):
                errors.append(msg)
            if logger:
                logger.error(msg=msg)

        return result

    @staticmethod
    def __get_invoking_class(errors: list[str] = None) -> type[Sob] | None:

        # initialize the return variable
        result: type[Sob] | None = None

        # obtain the invoking function
        caller_frame: FrameInfo = stack()[1]
        invoking_function: str = caller_frame.function
        mark: str = f".{invoking_function}("

        # obtain the invoking class
        caller_frame = stack()[2]
        context: str = caller_frame.code_context[0]
        pos: int = context.find(mark)
        class_name: str = context[:pos]
        mark = "." + class_name

        for name in _db_specs:
            if name.endswith(mark):
                with suppress(Exception):
                    pos = name.rfind(".")
                    module_name: str = name[:pos]
                    module: ModuleType = import_module(name=module_name)
                    result = getattr(module,
                                     class_name)
                    break

        if not result and SOB_BASE_FOLDER:
            with suppress(Exception):
                pos = caller_frame.filename.find(SOB_BASE_FOLDER) + len(SOB_BASE_FOLDER) + 1
                module_name: str = caller_frame.filename[pos:-3].replace("\\", ".").replace("/", ".")
                module: ModuleType = import_module(name=module_name)
                result = getattr(module,
                                 class_name)

        if not result and isinstance(errors, list):
            errors.append(f"Unable to obtain class '{class_name}' "
                          f"of invoking function '{invoking_function}'")
        return result
