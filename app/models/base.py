import re
from typing import TypeVar, NoReturn

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.sql import operators

from app.utils.datetime import utcnow
from app.utils.exceptions import DatabaseValidationError

snake_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')
BaseClass = declarative_base(metadata=sa.MetaData())
TBase = TypeVar("TBase", bound="Base")


class Base(BaseClass):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = sa.Column(sa.DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # noqa
        return snake_case_pattern.sub('_', cls.__name__).lower()

    def __str__(self):
        return f"<{type(self).__name__}({self.id=})>"

    @classmethod
    def _raise_validation_exception(cls, e: IntegrityError) -> NoReturn:
        info = e.orig.args[0] if e.orig.args else ""
        if (match := re.findall(r"Key \((.*)\)=\(.*\) already exists|$", info)) and match[0]:
            raise DatabaseValidationError(f"Unique constraint violated for {cls.__name__}", match[0]) from e
        if (match := re.findall(r"Key \((.*)\)=\(.*\) conflicts with existing key|$", info)) and match[0]:
            field_name = match[0].split(",", 1)[0]
            raise DatabaseValidationError(f"Range overlapped for {cls.__name__}", field_name) from e
        if (match := re.findall(r"Key \((.*)\)=\(.*\) is not present in table|$", info)) and match[0]:
            raise DatabaseValidationError(f"Foreign key constraint violated for {cls.__name__}", match[0]) from e
        raise e


operators_map = {
    "isnull": lambda c, v: (c is None) if v else (c is not None),
    "exact": operators.eq,
    "ne": operators.ne,  # not equal or is not (for None)
    "gt": operators.gt,  # greater than , >
    "ge": operators.ge,  # greater than or equal, >=
    "lt": operators.lt,  # lower than, <
    "le": operators.le,  # lower than or equal, <=
    "in": operators.in_op,
    "notin": operators.notin_op,
    "between": lambda c, v: c.between(v[0], v[1]),
    "like": operators.like_op,
    "ilike": operators.ilike_op,
    "startswith": operators.startswith_op,
    "istartswith": lambda c, v: c.ilike(v + "%"),
    "endswith": operators.endswith_op,
    "iendswith": lambda c, v: c.ilike("%" + v),
    "overlaps": lambda c, v: getattr(c, "overlaps")(v),
}
