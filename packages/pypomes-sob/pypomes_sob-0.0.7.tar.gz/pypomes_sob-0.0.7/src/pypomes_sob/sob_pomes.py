from __future__ import annotations  # allow forward references
from inspect import FrameInfo, stack
from enum import Enum, StrEnum
from logging import Logger
from pypomes_core import dict_get_key, dict_stringify
from pypomes_db import (
    db_exists, db_count, db_select,
    db_insert, db_update, db_delete
)
# 'type' is not a viable replacement for 'typing.Type', because the former does not accept subclasses
from typing import Any, ClassVar, Final, Type  # noqa


# ruff: noqa: UP006  - checks for generics that can be replaced with standard library variants based on PEP 585
class PySob:
    """
    Root entity.
    """
    # must have entries for all subclasses of 'PySob':
    #   key: the class type of the subclass of 'PySob'
    #   value: a tuple with 4 elements:
    #     - the name of the entity's DB table
    #     - the name of its PK attribute (maps to 'self.id')
    #     - the type of its PK attribute (currently, 'int' and 'str' are supported)
    #     - whether the PK attribute is an identity (values generated automatically by the DB)
    _db_specs: ClassVar[dict[Type[PySob], (StrEnum | str, StrEnum | str, type, bool)]] = {}

    # maps input parameters to DB columns
    _attrs_map: ClassVar[dict[Type[PySob], dict[StrEnum | str, StrEnum | str]]] = {}

    _sob_references: ClassVar[dict[Type[PySob], list[Type[PySob]]]] = {}

    def __init__(self,
                 errors: list[str] = None,
                 load_references: bool = False,
                 where_data: dict[str, Any] = None,
                 db_conn: Any = None,
                 logger: Logger = None) -> None:

        self._logger: Logger = logger
        # maps to the entity's PK in its DB table (returned on INSERT operations)
        self.id: int | str = 0

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
        if PySob._db_specs[self.__class__][3]:
            # PK is as identity column
            insert_data.pop(PySob._db_specs[self.__class__][1], None)
            return_col = {PySob._db_specs[self.__class__][1]: PySob._db_specs[self.__class__][2]}

        # execute the INSERT statement
        errors = errors if isinstance(errors, list) else []
        rec: tuple[Any] = db_insert(errors=errors,
                                    insert_stmt=f"INSERT INTO {PySob._db_specs[self.__class__][0]}",
                                    insert_data=insert_data,
                                    return_cols=return_col,
                                    connection=db_conn,
                                    logger=self._logger)
        if errors:
            msg = ("Error INSERTing into table "
                   f"{PySob._db_specs[self.__class__][0]}: {'; '.join(errors)}")
            errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        elif PySob._db_specs[self.__class__][3]:
            # PK is as identity column
            self.id = rec[0]

        return not errors

    def update(self,
               errors: list[str] | None,
               load_references: bool = False,
               db_conn: Any = None) -> bool | None:

        # inicialize the return variable
        result: bool | None = None

        # prepare data for UPDATE
        update_data: dict[str, Any] = self.to_columns(omit_nulls=False)
        key: int = update_data.pop(PySob._db_specs[self.__class__][1])

        # execute the UPDATE statement
        errors = errors if isinstance(errors, list) else []
        db_update(errors=errors,
                  update_stmt=f"UPDATE {PySob._db_specs[self.__class__][0]}",
                  update_data=update_data,
                  where_data={PySob._db_specs[self.__class__][1]: key},
                  min_count=1,
                  max_count=1,
                  connection=db_conn,
                  logger=self._logger)

        if not errors and load_references:
            self.__load_references(errors=errors,
                                   db_conn=db_conn)
        if errors:
            msg = ("Error UPDATEing table "
                   f"{PySob._db_specs[self.__class__][0]}: {'; '.join(errors)}")
            errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            result = True

        return result

    def delete(self,
               errors: list[str] | None,
               db_conn: Any = None) -> int | None:

        where_data: dict[str, Any]
        if self.id:
            where_data = {PySob._db_specs[self.__class__][1]: self.id}
        else:
            where_data = self.to_columns(omit_nulls=True)
            where_data.pop(PySob._db_specs[self.__class__][1], None)

        # execute the DELETE statement
        result: int = db_delete(errors=errors,
                                delete_stmt=f"DELETE FROM {PySob._db_specs[self.__class__][0]}",
                                where_data=where_data,
                                max_count=1,
                                connection=db_conn,
                                logger=self._logger)
        if errors:
            msg = ("Error DELETEing from table "
                   f"{PySob._db_specs[self.__class__][0]}: {'; '.join(errors)}")
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

        for key, value in data.items():
            attr: str = (PySob._attrs_map.get(self.__class__) or {}).get(key) or key

            # usa nomes de enums atribuídos como valores em 'data'
            if isinstance(value, Enum) and "use_names" in value.__class__:
                value = value.name  # noqa: PLW2901

            if attr in self.__dict__:
                self.__dict__[attr] = value
            elif self._logger:
                self._logger.warning(msg=f"'{attr}'is not an attribute of "
                                         f"{PySob._db_specs[self.__class__][0]}")

    def exists(self,
               errors: list[str] | None,
               where_data: dict[str, Any] = None,
               db_conn: Any = None) -> bool | None:

        if not where_data:
            if self.id:
                # use object's ID
                where_data = {PySob._db_specs[self.__class__][1]: self.id}
            else:
                # use object's available data
                where_data = self.to_columns(omit_nulls=True)
                where_data.pop(PySob._db_specs[self.__class__][1], None)

        return db_exists(errors=errors,
                         table=PySob._db_specs[self.__class__][0],
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

        if not where_data:
            if self.id:
                where_data = {PySob._db_specs[self.__class__][1]: self.id}
            else:
                where_data = self.to_columns(omit_nulls=omit_nulls)
                where_data.pop(PySob._db_specs[self.__class__][1], None)

        # it is acceptable that loading the object from the database might fail
        attrs: list[str] = self.get_columns()
        errors = errors if isinstance(errors, list) else []
        recs: list[tuple] = db_select(errors=errors,
                                      sel_stmt=f"SELECT {', '.join(attrs)} "
                                               f"FROM {PySob._db_specs[self.__class__][0]}",
                                      where_data=where_data,
                                      limit_count=2,
                                      connection=db_conn,
                                      logger=self._logger)
        msg: str | None = None
        if errors:
            msg = ("Error SELECTing from table "
                   f"{PySob._db_specs[self.__class__][0]}: {'; '.join(errors)}")
        elif not recs:
            msg = (f"No record found on table "
                   f"{PySob._db_specs[self.__class__][0]} for {dict_stringify(where_data)}")
        elif len(recs) > 1:
            msg = (f"More than on record found on table "
                   f"{PySob._db_specs[self.__class__][0]} for {dict_stringify(where_data)}")
        if msg:
            errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            rec: tuple = recs[0]
            for inx, attr in enumerate(attrs):
                # PK attribute in DB table might have a different name
                if attr == PySob._db_specs[self.__class__][0]:
                    self.__dict__["id"] = rec[inx]
                else:
                    self.__dict__[attr] = rec[inx]
            result = True

        return result

    def get_columns(self) -> list[str]:

        # PK attribute in DB table might have a different name
        result: list[str] = [PySob._db_specs[self.__class__][1]]
        result.extend([k for k in self.__dict__
                      if k.islower() and not k.startswith("_") and not k == "id"])
        return result

    def to_columns(self,
                   omit_nulls: bool) -> dict[str, Any]:

        # PK attribute in DB table might have a different name
        result: dict[str, Any] = {PySob._db_specs[self.__class__][1]: self.__dict__.get("id")}
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

        result: dict[str, Any] = {}
        for k, v in data.items():
            if not omit_nulls or v is not None:
                attr: str = dict_get_key(source=PySob._attrs_map.get(self.__class__) or {},
                                         value=k) or k
                result[attr] = v

        return result

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def load_reference(self,
                       __cls: Type[PySob],
                       /,
                       errors: list[str] | None,  # noqa: ARG002
                       db_conn: Any | None) -> PySob | list[PySob] | None:  # noqa: ARG002

        # to be implemented by subclasses containing references
        return None

    def __load_references(self,
                          errors: list[str],
                          db_conn: Any) -> None:

        for cls in (PySob._sob_references.get(self.__class__) or []):
            self.load_reference(cls,
                                errors=errors,
                                db_conn=db_conn)
            if errors:
                msg = (f"Error SELECTing from table "
                       f"{PySob._db_specs[cls][0]}: {'; '.join(errors)}")
                errors.append(msg)
                if self._logger:
                    self._logger.error(msg=msg)
                break

    @staticmethod
    def initialize(__cls: Type[PySob],
                   /,
                   db_specs: tuple[StrEnum | str, StrEnum | str, int | str] |
                             tuple[StrEnum | str, StrEnum | str, int, bool],  # noqa
                   attrs_map: dict[StrEnum | str, StrEnum | str] = None,
                   sob_references: list[Type[PySob]] = None) -> None:

        # initialize the class
        specs: list = list(db_specs)
        if len(specs) == 3:
            # 'id' defaults to being an identity attribute in the DB for type 'int'
            specs.append(specs[2] is int)
        PySob._db_specs.update({__cls: tuple(db_specs)})
        if attrs_map:
            PySob._attrs_map.update({__cls: attrs_map})
        if sob_references:
            PySob._sob_references.update({__cls: sob_references})

    @staticmethod
    def count(errors: list[str] | None,
              where_data: dict[str, Any],
              db_conn: Any = None,
              logger: Logger = None) -> int | None:

        # obtain the invoking class
        cls: Type[PySob] = PySob.__get_invoking_class()

        return db_count(errors=errors,
                        table=PySob._db_specs[cls][0],
                        where_data=where_data,
                        connection=db_conn,
                        logger=logger)

    @staticmethod
    def retrieve(errors: list[str] | None,
                 where_data: dict[str, Any] = None,
                 load_references: bool = False,
                 required: bool = False,
                 db_conn: Any = None,
                 logger: Logger = None) -> list[PySob] | None:

        # inicialize the return variable
        result: list[PySob] | None = None

        # obtain rtheinvoking class
        cls: Type[PySob] = PySob.__get_invoking_class()

        errors = errors if isinstance(errors, list) else []
        recs: list[tuple[int]] = db_select(errors=errors,
                                           sel_stmt=f"SELECT {PySob._db_specs[cls][1]} "
                                                    f"FROM {PySob._db_specs[cls][0]}",
                                           where_data=where_data,
                                           min_count=1 if required else None,
                                           connection=db_conn,
                                           logger=logger)
        if not errors:
            # build the objects list
            objs: list[PySob] = []
            for rec in recs:
                objs.append(cls(errors=errors,
                                load_references=load_references,
                                db_conn=db_conn,
                                where_data={PySob._db_specs[cls][1]: rec[0]},
                                logger=logger))
                if errors:
                    break

            if not errors:
                result = objs

        return result

    @staticmethod
    def erase(errors: list[str] | None,
              where_data: dict[str, Any],
              db_conn: Any = None,
              logger: Logger = None) -> int | None:

        # obtain the invoking class
        cls: Type[PySob] = PySob.__get_invoking_class()

        # delete specified tuples
        return db_delete(errors=errors,
                         delete_stmt=f"DELETE FROM {PySob._db_specs[cls][0]}",
                         where_data=where_data,
                         connection=db_conn,
                         logger=logger)

    @staticmethod
    def __get_invoking_class() -> Type[PySob]:

        # obtain the invoking function
        caller_frame: FrameInfo = stack()[1]
        mark: str = f".{caller_frame.function}("

        # obtain the invoking class
        caller_frame = stack()[2]
        context: str = caller_frame.code_context[0]
        pos_to: int = context.find(mark)
        pos_from: int = context.rfind(" ", 0, pos_to)
        mark = "." + context[pos_from+1:pos_to]

        result: Type[PySob] | None = None
        for cls in PySob._db_specs:
            name = f"{cls.__module__}.{cls.__qualname__}"
            if name.endswith(mark):
                result = cls
                break

        return result
