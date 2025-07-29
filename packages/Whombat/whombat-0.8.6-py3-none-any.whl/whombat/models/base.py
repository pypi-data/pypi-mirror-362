"""Base class for SqlAlchemy Models.

All whombat models should inherit from this class.
"""

import datetime
import uuid
from pathlib import Path

import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.types as types
from fastapi_users_db_sqlalchemy.generics import GUID
from soundevent import data
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs

__all__ = [
    "Base",
]


class PathType(types.TypeDecorator):
    """SqlAlchemy type for Path objects."""

    impl = types.String

    cache_ok = True

    def process_bind_param(self, value: Path | None, dialect) -> str | None:
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value: str | None, dialect) -> Path | None:
        if value is None:
            return value
        return Path(value)


class GeometryType(types.TypeDecorator):
    """SqlAlchemy type for soundevent.Geometry objects."""

    impl = types.String

    cache_ok = True

    def process_bind_param(self, value: data.Geometry, _) -> str:  # type: ignore
        return value.model_dump_json()

    def process_result_value(
        self,
        value: str | None,
        dialect,
    ) -> data.Geometry | None:
        if value is None:
            return value
        return data.geometry_validate(value, mode="json")


class Base(AsyncAttrs, orm.MappedAsDataclass, orm.DeclarativeBase):
    """Base class for SqlAlchemy Models."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    created_on: orm.Mapped[datetime.datetime] = orm.mapped_column(
        name="created_on",
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        kw_only=True,
        repr=False,
    )

    # Add a type annotation map to allow for custom types.
    type_annotation_map = {
        uuid.UUID: GUID,
        Path: PathType,
        data.Geometry: GeometryType,
        datetime.datetime: sa.DateTime().with_variant(
            sa.TIMESTAMP(timezone=True), "postgresql"
        ),
    }

    # This is needed to make the default values work with
    # async sqlalchemy.
    __mapper_args__ = {
        "eager_defaults": True,
    }
