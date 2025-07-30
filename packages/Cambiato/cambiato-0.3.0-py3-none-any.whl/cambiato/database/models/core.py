r"""The core database tables."""

# Standard library
import os
from typing import ClassVar

# Third party
from sqlalchemy import ForeignKey, Index, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from streamlit_passwordless.database.models import Base, ModifiedAndCreatedColumnMixin

SCHEMA: str | None = os.getenv('CAMBIATO_DB_SCHEMA')
metadata_obj = MetaData(schema=SCHEMA)


class DType(ModifiedAndCreatedColumnMixin, Base):
    r"""The data types.

    Used for mapping from what column to fetch a value
    based on the expected data type.

    Parameters
    ----------
    dtype_id : int
        The unique ID of the data type. The primary key of the table.

    name : str
        The name of the data type. Must be unique. Is indexed.

    description : str or None, default None
        An optional description of the data type.

    updated_at : datetime or None
        The timestamp at which the dtype was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the dtype.

    created_at : datetime
        The timestamp at which the dtype was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the dtype.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'dtype_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'dtype'

    dtype_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]


Index(f'{DType.__tablename__}_dtype_id_ix', DType.dtype_id)


class Unit(ModifiedAndCreatedColumnMixin, Base):
    r"""The measurement units.

    Parameters
    ----------
    unit_id : int
        The unique ID of the unit. The primary key of the table.

    name : str
        The name of the unit. Must be unique. Is indexed.

    description : str or None, default None
        A description of the unit.

    updated_at : datetime or None
        The timestamp at which the unit was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the unit.

    created_at : datetime
        The timestamp at which the unit was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the unit.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'unit_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'unit'

    unit_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{Unit.__tablename__}_name_uix', Unit.name, unique=True)


class ValueColumnName(ModifiedAndCreatedColumnMixin, Base):
    r"""The column names for storing information dependent on data types.

    Parameters
    ----------
    value_column_name_id : int
        The unique ID of the value column. The primary key of the table.

    dtype_id : int
        Th ID of the data type of the column. Foreign key to :attr:`DType.dtype_id`. Is indexed.

    name : str
        The unique name of the value column. Is indexed.

    description : str or None
        An optional description of the value column name.

    updated_at : datetime or None
        The timestamp at which the value column was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the value column.

    created_at : datetime
        The timestamp at which the value column was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the value column.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'value_column_name_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'value_column_name'

    value_column_name_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dtype_id: Mapped[int] = mapped_column(ForeignKey(DType.dtype_id))
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{ValueColumnName.__tablename__}_dtype_id_ix', ValueColumnName.dtype_id)
Index(f'{ValueColumnName.__tablename__}_name_ix', ValueColumnName.name, unique=True)


class ObjectType(ModifiedAndCreatedColumnMixin, Base):
    r"""The available object types.

    Parameters
    ----------
    object_id : int
        The unique ID of the object type. The primary key of the table.

    name : str
        The name of the object type. Must be unique.

    table_name : str
        The name of the table that contains the object. Must be unique.

    description : str or None, default None
        An optional description of the object.

    updated_at : datetime or None
        The timestamp at which the object type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the object type.

    created_at : datetime
        The timestamp at which the object type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the object type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'object_type_id',
        'name',
        'table_name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'object_type'

    object_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    table_name: Mapped[str] = mapped_column(unique=True)
    source_pk_column: Mapped[str]
    source_pk_column_dtype_id: Mapped[int] = mapped_column(
        ForeignKey(DType.dtype_id), nullable=False
    )
    description: Mapped[str | None]


Index(f'{ObjectType.__tablename__}_name_uix', ObjectType.name, unique=True)


class Utility(ModifiedAndCreatedColumnMixin, Base):
    r"""The utilities of the application.

    Parameters
    ----------
    utility_id : int
       The unique ID of the utility. The primary key of the table.

    name : str
        The name of the utility. Must be unique. Is indexed.

    description : str or None, default None
        A description of the utility.

    updated_at : datetime or None
        The timestamp at which the utility was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the utility.

    created_at : datetime
        The timestamp at which the utility was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the utility.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'utility_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'utility'

    utility_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{Utility.__tablename__}_name_uix', Utility.name, unique=True)


class CoordinateSystem(ModifiedAndCreatedColumnMixin, Base):
    r"""The available coordinate systems.

    Parameters
    ----------
    coordinate_system_id : str
        The unique ID of the coordinate system. The primary key of the table.

    name : str
        The unique name of the coordinate system. Is indexed.

    description : str or None
        A description of the coordinate system.

    updated_at : datetime or None
        The timestamp at which the coordinate system was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the coordinate system.

    created_at : datetime
        The timestamp at which the coordinate system was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the coordinate system.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'coordinate_system_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'coordinate_system'

    coordinate_system_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{CoordinateSystem.__tablename__}_name_uix', CoordinateSystem.name, unique=True)


# =================================================================================================
# Manufacturer, Type Description and Batch
# =================================================================================================


class Manufacturer(ModifiedAndCreatedColumnMixin, Base):
    r"""Manufacturers of devices and keys.

    Parameters
    ----------
    manufacturer_id : int
        The unique ID of the manufacturer. The primary key of the table.

    name : str
        The name of the manufacturer. Must be unique. Is indexed.

    description : str or None
        A description of the manufacturer.

    updated_at : datetime or None
        The timestamp at which the manufacturer was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the manufacturer.

    created_at : datetime
        The timestamp at which the manufacturer was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the manufacturer.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'manufacturer_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'manufacturer'

    manufacturer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{Manufacturer.__tablename__}_name_uix', Manufacturer.name, unique=True)


class TypeDescription(ModifiedAndCreatedColumnMixin, Base):
    r"""Type descriptions with info about the configuration of the device.

    Parameters
    ----------
    type_description_id : int
        The unique ID of the type description. The primary key of the table.

    manufacturer_id : int
        The ID of the manufacturer the type description belongs to. Foreign key to
        :attr:`Manufacturer.manufacturer_id`. Is indexed.

    code : str
        The the type description code. Must be unique within each manufacturer. Is indexed.

    description : str or None
        A description of the type description.

    updated_at : datetime or None
        The timestamp at which the type description was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the type description.

    created_at : datetime
        The timestamp at which the type description was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the type description.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'type description_id',
        'manufacturer_id',
        'code',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device_type_description'

    type_description_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey(Manufacturer.manufacturer_id))
    code: Mapped[str]
    description: Mapped[str | None]


Index(
    f'{TypeDescription.__tablename__}_manufacturer_id_code_uix',
    TypeDescription.manufacturer_id,
    TypeDescription.code,
    unique=True,
)


class ManufactureBatch(ModifiedAndCreatedColumnMixin, Base):
    r"""Information about the batches in which devices are manufactured.

    Parameters
    ----------
    manufacture_batch_id : int
        The unique ID of the manufacture batch. The primary key of the table.

    manufacturer_id : int
        The ID of the manufacturer the batch belongs to. Is indexed.

    code : str
        The batch code. Must be unique within each manufacturer. Is indexed.

    description : str or None
        A description of the batch.

    updated_at : datetime or None
        The timestamp at which the batch was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the batch.

    created_at : datetime
        The timestamp at which the batch was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the batch.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'manufacture_batch_id',
        'manufacturer_id',
        'code',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'manufacture_batch'

    manufacture_batch_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey(Manufacturer.manufacturer_id))
    code: Mapped[str]
    description: Mapped[str | None]


Index(
    f'{ManufactureBatch.__tablename__}_manufacturer_id_code_uix',
    ManufactureBatch.manufacturer_id,
    ManufactureBatch.code,
    unique=True,
)


class KeyType(ModifiedAndCreatedColumnMixin, Base):
    r"""The different types of keys.

    Parameters
    ----------
    key_type_id : int
        The unique ID of the key type. The primary key of the table.

    name : str
        The name of the key type. Must be unique. Is indexed.

    description : str or None
        A description of the key type.

    updated_at : datetime or None
        The timestamp at which the key type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the key type.

    created_at : datetime
        The timestamp at which the key type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the key type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'key_type_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'key_type'

    key_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{KeyType.__tablename__}_name_uix', unique=True)


class Key(ModifiedAndCreatedColumnMixin, Base):
    r"""Keys for accessing facilities.

    Parameters
    ----------
    key_id : int
        The unique ID of the key. The primary key of the table.

    ext_id : str or None
        The unique ID of the key in an external system. Must be unique. Is indexed.

    manufacturer_id : int or None
        The ID of the manufacturer of the key. Foreign key to
        :attr:`Manufacturer.manufacturer_id`. Is indexed.

    type_description_id : int or None
        The ID of the type description of the key, which conveys information about the model
        the key. Foreign key to :attr:`TypeDescription.type_description_id`. Is indexed.

    manufacture_batch_id : int or None
        The ID of the batch that the key was manufactured in. Foreign key to
        :attr:`ManufactureBatch.manufacture_batch_id`. Is indexed.

    key_type_id : int
        The key type. Foreign key to :attr:`KeyType.key_type_id`. Is indexed.

    code : str or None
        A code that uniquely defines the key.

    description : str or None
        A description of the key.

    updated_at : datetime or None
        The timestamp at which the key was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the key.

    created_at : datetime
        The timestamp at which the key was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the key.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'key_id',
        'ext_id',
        'manufacturer_id',
        'type_description_id',
        'manufacture_batch_id',
        'key_type_id',
        'code',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'key'

    key_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ext_id: Mapped[str | None]
    manufacturer_id: Mapped[int | None] = mapped_column(ForeignKey(Manufacturer.manufacturer_id))
    type_description_id: Mapped[int | None] = mapped_column(
        ForeignKey(TypeDescription.type_description_id)
    )
    manufacture_batch_id: Mapped[int | None] = mapped_column(
        ForeignKey(ManufactureBatch.manufacture_batch_id)
    )
    key_type_id: Mapped[int] = mapped_column(ForeignKey(KeyType.key_type_id))
    code: Mapped[str | None] = mapped_column(unique=True)
    description: Mapped[str | None]


Index(f'{Key.__tablename__}_ext_id_ix', Key.ext_id, unique=True)
Index(f'{Key.__tablename__}_manufacturer_id_ix', Key.manufacturer_id)
Index(f'{Key.__tablename__}_type_description_id_ix', Key.type_description_id)
Index(f'{Key.__tablename__}_manufacture_batch_id_ix', Key.manufacture_batch_id)
Index(f'{Key.__tablename__}_key_type_id_ix', Key.key_type_id)
