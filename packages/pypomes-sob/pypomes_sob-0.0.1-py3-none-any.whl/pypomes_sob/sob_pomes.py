from __future__ import annotations  # allow forward references
from inspect import FrameInfo, stack
from enum import Enum, StrEnum, auto
from logging import Logger
from pypomes_core import dict_get_key, dict_stringify, validate_format_error
from pypomes_db import (
    db_exists, db_count, db_select,
    db_insert, db_update, db_delete
)
# 'type' is not a viable replacement for 'typing.Type', because it does not accept subclasses
from typing import Any, ClassVar, Final, Type  # noqa

DB_ID: Final[str] = "id"
DB_TABLE: Final[str] = "table"


# noinspection Annotator
# ruff: noqa: UP006
class PySob:
    """
    Root entity.
    """
    class _Db(StrEnum):
        TABLE = auto()
        ID = auto()

    db_specs: ClassVar[dict[Type[PySob], list[StrEnum]]] = {}

    attrs_map: ClassVar[dict[Type[PySob], dict[StrEnum, StrEnum]]] = []

    def __init__(self,
                 __references: list[Type[PySob]],
                 /,
                 errors: list[str] = None,
                 load_references: bool = False,
                 where_data: dict[str, Any] = None,
                 db_conn: Any = None,
                 logger: Logger = None) -> None:

        self._references: list[Type[PySob]] = __references
        self._logger: Logger = logger
        self.id: int = 0

        if where_data:
            attrs: list[str] = self.get_columns()
            recs: list[tuple] = db_select(errors=errors,
                                          sel_stmt=f"SELECT {', '.join(attrs)} "
                                                   f"FROM {PySob.db_specs[self.__class__][DB_TABLE]}",
                                          where_data=where_data,
                                          limit_count=2,
                                          connection=db_conn,
                                          logger=self._logger)
            msg: str | None = None
            if errors:
                # 201: Erro na interação com o BD em {}: {}
                msg = validate_format_error(201,
                                            f"{PySob.db_specs[self.__class__][DB_TABLE]}",
                                            f"{'; '.join(errors)}")
            elif not recs:
                # 202: Nenhum registro encontrado no BD, em {} para {}
                msg = validate_format_error(202,
                                            f"{PySob.db_specs[self.__class__][DB_TABLE]}",
                                            f"{dict_stringify(where_data)}")
            elif len(recs) > 1:
                # 207 Mais de um registro existente no BD, em {} para {}
                msg = validate_format_error(207,
                                            f"{PySob.db_specs[self.__class__][DB_TABLE]}",
                                            f"{dict_stringify(where_data)}")
            if msg:
                errors.append(msg)
                if self._logger:
                    self._logger.error(msg=msg)
            else:
                rec: tuple = recs[0]
                for inx, attr in enumerate(attrs):
                    self.__dict__[attr] = rec[inx]
                if load_references:
                    self.__load_references(errors=errors,
                                           db_conn=db_conn)

    def insert(self,
               errors: list[str] | None,
               db_conn: Any = None) -> bool:

        # prepara os dados para INSERT
        insert_data: dict[str, Any] = self.to_columns(omit_nulls=False)
        insert_data.pop(PySob.db_specs[self.__class__][DB_ID])

        # executa o INSERT
        errors = errors if isinstance(errors, list) else []
        rec: tuple[int] = db_insert(errors=errors,
                                    insert_stmt=f"INSERT INTO {PySob.db_specs[self.__class__][DB_TABLE]}",
                                    insert_data=insert_data,
                                    return_cols={PySob.db_specs[self.__class__][DB_ID]: int},
                                    connection=db_conn,
                                    logger=self._logger)
        if errors:
            # 201: Erro na interação com o BD em {}: {}
            msg = validate_format_error(201,
                                        f"{PySob.db_specs[self.__class__][DB_TABLE]}",
                                        f"{'; '.join(errors)}")
            errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            self.id = rec[0]

        return not errors

    def update(self,
               errors: list[str] | None,
               load_references: bool = False,
               db_conn: Any = None) -> bool | None:

        # inicializa a variável de retorno
        result: bool | None = None

        # prepara os dados para UPDATE
        update_data: dict[str, Any] = self.to_columns(omit_nulls=False)
        key: int = update_data.pop(PySob.db_specs[self.__class__][DB_ID])

        # execute the UPDATE operation
        errors = errors if isinstance(errors, list) else []
        db_update(errors=errors,
                  update_stmt=f"UPDATE {PySob.db_specs[self.__class__][DB_TABLE]}",
                  update_data=update_data,
                  where_data={PySob.db_specs[self.__class__][DB_ID]: key},
                  min_count=1,
                  max_count=1,
                  connection=db_conn,
                  logger=self._logger)

        if not errors and load_references:
            self.__load_references(errors=errors,
                                   db_conn=db_conn)
        if errors:
            # 201: Erro na interação com o BD em {}: {}
            msg = validate_format_error(201,
                                        f"{PySob.db_specs[self.__class__][DB_TABLE]}",
                                        f"{'; '.join(errors)}")
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
            where_data = {PySob.db_specs[self.__class__][DB_ID]: self.id}
        else:
            where_data = self.to_columns(omit_nulls=True)
            where_data.pop(PySob.db_specs[self.__class__][DB_ID])

        # execute the DELETE operation
        result: int = db_delete(errors=errors,
                                delete_stmt=f"DELETE FROM {PySob.db_specs[self.__class__][DB_TABLE]}",
                                where_data=where_data,
                                max_count=1,
                                connection=db_conn,
                                logger=self._logger)
        if errors:
            # 201: Erro na interação com o BD em {}: {}
            msg = validate_format_error(201,
                                        f"{PySob.db_specs[self.__class__][DB_TABLE]}",
                                        f"{'; '.join(errors)}")
            errors.append(msg)
            if self._logger:
                self._logger.error(msg=msg)
        else:
            self.clear()

        return result

    def clear(self) -> None:

        for key in self.__dict__.keys():
            self.__dict__[key] = None

    def set(self,
            data: dict[str, Any]) -> None:

        for key, value in data.items():
            attr: str = PySob.attrs_map[self.__class__].get(key) or key

            # usa nomes de enums atribuídos como valores em 'data'
            if isinstance(value, Enum) and "use_names" in value.__class__:
                value = value.name

            if attr in self.__dict__:
                self.__dict__[attr] = value
            elif self._logger:
                self._logger.warning(msg=f"'{attr}' não é atributo de "
                                         f"'{PySob.db_specs[self.__class__][DB_TABLE]}'")

    def exists(self,
               errors: list[str] | None,
               where_data: dict[str, Any] = None,
               db_conn: Any = None) -> bool | None:

        if not where_data:
            if self.id:
                # use object's ID
                where_data = {PySob.db_specs[self.__class__][DB_ID]: self.id}
            else:
                # use object's available data
                where_data = self.to_columns(omit_nulls=True)
                where_data.pop(PySob.db_specs[self.__class__][DB_ID])

        return db_exists(errors=errors,
                         table=PySob.db_specs[self.__class__][DB_TABLE],
                         where_data=where_data,
                         connection=db_conn,
                         logger=self._logger)

    def load(self,
             errors: list[str] | None,
             omit_nulls: bool,
             where_data: dict[str, Any] = None,
             db_conn: Any = None) -> bool:

        if not where_data:
            if self.id:
                where_data = {PySob.db_specs[self.__class__][DB_ID]: self.id}
            else:
                where_data = self.to_columns(omit_nulls=omit_nulls)
                where_data.pop(PySob.db_specs[self.__class__][DB_ID])

        # it is acceptable that loading the object from the database might fail
        attrs: list[str] = self.get_columns()
        errors = errors if isinstance(errors, list) else []
        recs: list[tuple] = db_select(errors=errors,
                                      sel_stmt=f"SELECT {', '.join(attrs)} "
                                               f"FROM {PySob.db_specs[self.__class__][DB_TABLE]}",
                                      where_data=where_data,
                                      limit_count=2,
                                      connection=db_conn,
                                      logger=self._logger)
        if recs and len(recs) == 1:
            rec: tuple = recs[0]
            for inx, attr in enumerate(attrs):
                self.__dict__[attr] = rec[inx]
        elif self._logger:
            self._logger.warning(msg=f"Unable to load from "
                                     f"'{PySob.db_specs[self.__class__][DB_TABLE]}' "
                                     f"with data {where_data}")

        return recs and len(recs) == 1

    def get_columns(self) -> list[str]:

        return [k for k in self.__dict__
                if k.islower() and not k.startswith("_")]

    def to_columns(self,
                   omit_nulls: bool) -> dict[str, Any]:

        result: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.islower() and not key.startswith("_") and \
                    (not omit_nulls or value is not None):
                result[key] = value

        return result

    def to_params(self,
                  omit_nulls: bool) -> dict[str, Any]:

        result: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if key.islower() and not key.startswith("_") and \
                    (not omit_nulls or value is not None):
                attr: str = dict_get_key(source=PySob.attrs_map[self.__class__],
                                         value=key) or key
                result[attr] = value

        return result

    def data_to_params(self,
                       data: dict[str, Any],
                       omit_nulls: bool) -> dict[str, Any]:

        result: dict[str, Any] = {}
        for key, value in data.items():
            if not omit_nulls or value is not None:
                attr: str = dict_get_key(source=PySob.attrs_map[self.__class__],
                                         value=key) or key
                result[attr] = value

        return result

    # noinspection PyMethodMayBeStatic, PyUnusedLocal
    def load_reference(self,
                       errors: list[str] | None,  # noqa: ARG002
                       db_conn: Any | None) -> PySob | list[PySob] | None:  # noqa: ARG002

        # to be implemented by subclasses containing references
        return None

    def __load_references(self,
                          errors: list[str],
                          db_conn: Any) -> None:

        for cls in self._references or []:
            self.load_reference(errors=errors,
                                db_conn=db_conn)
            if errors:
                # 201: Erro na interação com o BD em {}: {}
                msg = validate_format_error(201,
                                            f"{cls._Db.TABLE}",
                                            f"{'; '.join(errors)}")
                errors.append(msg)
                if self._logger:
                    self._logger.error(msg=msg)
                break

    @staticmethod
    def count(errors: list[str] | None,
              where_data: dict[str, Any],
              db_conn: Any = None,
              logger: Logger = None) -> int | None:

        # obtem a classe invocante
        # noinspection PyTypeChecker
        cls: Type[PySob] = PySob.__get_invoking_class()

        return db_count(errors=errors,
                        table=cls._Db.TABLE,
                        where_data=where_data,
                        connection=db_conn,
                        logger=logger)

    @staticmethod
    def retrieve(errors: list[str] | None,
                 where_data: dict[str, Any] = None,
                 references: list[Type[PySob]] = None,
                 required: bool = False,
                 db_conn: Any = None,
                 logger: Logger = None) -> list[Type[PySob]] | None:

        # inicializa a variável de retorno
        result: list[PySob] | None = None

        # obtem a classe invocante
        # noinspection PyTypeChecker
        cls: Type[PySob] = PySob.__get_invoking_class()

        errors = errors if isinstance(errors, list) else []
        recs: list[tuple[int]] = db_select(errors=errors,
                                           sel_stmt=f"SELECT {cls._Db.ID} FROM {cls._Db.TABLE}",
                                           where_data=where_data,
                                           min_count=1 if required else None,
                                           connection=db_conn,
                                           logger=logger)
        if not errors:
            # constrói a lista de objetos
            # noinspection PyTypeChecker
            objs: list[PySob] = []
            for rec in recs:
                # noinspection PyTypeChecker
                objs.append(cls(references,
                                errors=errors,
                                load_references=isinstance(references, list) and len(references) > 0,
                                db_conn=db_conn,
                                where_data={cls._Db.ID: rec[0]},
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

        # obtem a classe invocante
        # noinspection PyTypeChecker
        cls: Type[PySob] = PySob.__get_invoking_class()

        # delete specified tuples
        return db_delete(errors=errors,
                         delete_stmt=f"DELETE FROM {cls._Db.TABLE}",
                         where_data=where_data,
                         connection=db_conn,
                         logger=logger)

    @staticmethod
    def __get_invoking_class() -> Type[PySob]:

        # obtem a função invocante
        caller_frame: FrameInfo = stack()[1]
        mark: str = f".{caller_frame.function}("

        # obtem a classe invocante
        caller_frame = stack()[2]
        context: str = caller_frame.code_context[0]
        pos_to: int = context.find(mark)
        pos_from: int = context.rfind(" ", 0, pos_to)
        mark = "." + context[pos_from+1:pos_to]

        result: Type[PySob] | None = None
        for typ in PySob.db_specs:
            name = f"{typ.__module__}.{typ.__qualname__}"
            if name.endswith(mark):
                result = typ
                break

        return result
