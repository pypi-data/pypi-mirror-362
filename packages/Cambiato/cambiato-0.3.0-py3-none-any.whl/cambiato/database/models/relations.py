r"""Tables with relationships to one another."""

# Standard library
from datetime import date, datetime
from typing import ClassVar

# Third party
from sqlalchemy import TIMESTAMP, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from streamlit_passwordless.database.models import Base, ModifiedAndCreatedColumnMixin, User

# Local
from .core import (
    CoordinateSystem,
    DType,
    Key,
    ManufactureBatch,
    Manufacturer,
    TypeDescription,
    Unit,
    Utility,
    ValueColumnName,
)

# =================================================================================================
# Location
# =================================================================================================


class LocationType(ModifiedAndCreatedColumnMixin, Base):
    r"""The type of a location.

    Parameters
    ----------
    location_type_id : int
        The primary key of the table.

    name : str
        The name of the location type. Must be unique. Is indexed.

    description : str or None
        A description of the location type.

    updated_at : datetime or None
        The timestamp at which the location type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the location type.

    created_at : datetime
        The timestamp at which the location type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the location type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'location_type_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'location_type'

    location_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]

    locations: Mapped[list['Location']] = relationship(back_populates='location_type')


Index(f'{LocationType.__tablename__}_name_uix', LocationType.name, unique=True)


class Location(ModifiedAndCreatedColumnMixin, Base):
    r"""A location where facilities are located.

    Parameters
    ----------
    location_id : int
        The unique ID of the location. The primary key of the table.

    ext_id : str or None
        The unique ID of the location in an external system. Is indexed.

    name : str or None
        The name of the location.

    common_name : str or None
        A "common" name used for the location. E.g. "The old house by the sea".

    description : str or None
        A description of the location.

    location_type_id : int
        The type of location. Foreign key to :attr:`LocationType.location_type_id`. Is indexed.

    coordinate_system_id : int or None
        The coordinate system of location coordinates. Foreign key to
        :attr:`CoordinateSystem.coordinate_system_id`.

    x_coord : float or None
        The x-coordinate of the location (longitude).

    y_coord : float or None
        The y-coordinate of the location (latitude).

    z_coord : float or None
        The z-coordinate of the location (height).

    street_name : str or None
        The street name of the location.

    street_number : int or None
        The street number of the location.

    street_number_suffix : str or None
        The street number suffix of the location E.g. A or B.

    apartment_number : int or None
        The apartment number of the location.

    zip_code : int or None
        The zip code of the location.

    city : int or None
        The city or town of the location.

    region : int or None
        The region of the location.

    country : str or None
        The country of the location.

    updated_at : datetime or None
        The timestamp at which the location was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the location.

    created_at : datetime
        The timestamp at which the location was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the location.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'location_id',
        'ext_id',
        'name',
        'common_name',
        'description',
        'location_type_id',
        'coordinate_system_id',
        'x_coord',
        'y_coord',
        'z_coord',
        'street_name',
        'street_number',
        'street_number_suffix',
        'apartment_number',
        'zip_code',
        'city',
        'region',
        'country',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'location'

    location_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ext_id: Mapped[str | None]
    name: Mapped[str | None]
    common_name: Mapped[str | None]
    description: Mapped[str | None]
    location_type_id: Mapped[int] = mapped_column(
        ForeignKey(LocationType.location_type_id, ondelete='SET NULL')
    )
    coordinate_system_id: Mapped[int | None] = mapped_column(
        ForeignKey(CoordinateSystem.coordinate_system_id)
    )
    x_coord: Mapped[float | None]
    y_coord: Mapped[float | None]
    z_coord: Mapped[float | None]
    street_name: Mapped[str | None]
    street_number: Mapped[int | None]
    street_number_suffix: Mapped[str | None]
    apartment_number: Mapped[int | None]
    zip_code: Mapped[int | None]
    city: Mapped[int | None]
    region: Mapped[int | None]
    country: Mapped[str | None]

    location_type: Mapped[LocationType] = relationship(back_populates='locations')
    coordinate_system: Mapped[CoordinateSystem] = relationship()


Index(f'{Location.__tablename__}_ext_id_uix', Location.ext_id, unique=True)
Index(f'{Location.__tablename__}_location_type_id_ix', Location.location_type_id)


# =================================================================================================
# Customer
# =================================================================================================


class CustomerType(ModifiedAndCreatedColumnMixin, Base):
    r"""The type of customer.

    Parameters
    ----------
    customer_type_id : int
        The unique ID of the customer type. The primary key of the table.

    name : str
        The name of the customer type. Must be unique. Is indexed.

    description : str or None
        A description of the customer type.

    updated_at : datetime or None
        The timestamp at which the customer type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the customer type.

    created_at : datetime
        The timestamp at which the customer type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the customer type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'customer_type_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'customer_type'

    customer_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]

    customers: Mapped[list['Customer']] = relationship(back_populates='customer_type')


Index(f'{CustomerType.__tablename__}_name_uix', CustomerType.name, unique=True)


class ContactMethod(ModifiedAndCreatedColumnMixin, Base):
    r"""The contact methods of a customer.

    Parameters
    ----------
    contact_method_id : int
        The unique ID of the contact method. The primary key of the table.

    name : str
        The name of the contact method. Must be unique. Is indexed.

    description : str or None
        A description of the contact method.

    updated_at : datetime or None
        The timestamp at which the contact method was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the contact method.

    created_at : datetime
        The timestamp at which the contact method was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the contact method.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'contact_method_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'contact_method'

    contact_method_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]

    customers: Mapped[list['Customer']] = relationship(back_populates='preferred_contact_method')


Index(f'{ContactMethod.__tablename__}_name_uix', ContactMethod.name, unique=True)


class Customer(ModifiedAndCreatedColumnMixin, Base):
    r"""The customers that can be owners of facilities.

    Parameters
    ----------
    customer_id : int
        The unique ID of the customer. The primary key of the table.

    ext_id : str or None
        A unique ID of the customer defined in an external system. Is indexed.

    first_name : str or None
        The first name of the customer.

    last_name : str or None
        The last name of the customer.

    company_name : str or None
        The name of the company if the customer is a company.

    customer_type_id : int
        The type of customer. Foreign key to :attr:`CustomerType.customer_type_id`.
        Is indexed.

    preferred_contact_method_id : int or None
        The preferred contact method of the customer. Foreign key to
        :attr:`ContactMethod.contact_method_id`. Is indexed.

    deceased : bool, default False
        True if the customer is deceased and False otherwise.

    description : str or None
        A description of the customer.

    updated_at : datetime or None
        The timestamp at which the customer was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the customer.

    created_at : datetime
        The timestamp at which the customer was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the customer.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'customer_id',
        'ext_id',
        'first_name',
        'last_name',
        'company_name',
        'customer_type_id',
        'preferred_contact_method_id',
        'deceased',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'customer'

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ext_id: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    company_name: Mapped[str | None]
    customer_type_id: Mapped[int] = mapped_column(
        ForeignKey(CustomerType.customer_type_id, ondelete='SET NULL')
    )
    preferred_contact_method_id: Mapped[int] = mapped_column(
        ForeignKey(ContactMethod.contact_method_id, ondelete='SET NULL')
    )
    deceased: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str | None]

    customer_type: Mapped[CustomerType] = relationship(back_populates='customers')
    preferred_contact_method: Mapped[ContactMethod] = relationship(back_populates='customers')
    emails: Mapped[list['CustomerEmail']] = relationship(
        back_populates='customer', cascade='delete'
    )
    phone_numbers: Mapped[list['CustomerPhone']] = relationship(
        back_populates='customer', cascade='delete'
    )
    facilities: Mapped[list['Facility']] = relationship(back_populates='customer')


Index(f'{Customer.__tablename__}_ext_id_uix', Customer.ext_id, unique=True)
Index(f'{Customer.__tablename__}_customer_type_id_ix', Customer.customer_type_id)
Index(f'{Customer.__tablename__}_preferred_contact_method_ix', Customer.preferred_contact_method_id)


class CustomerEmail(ModifiedAndCreatedColumnMixin, Base):
    r"""Email addresses of customers.

    Parameters
    ----------
    customer_email_id : int
        A unique ID of the email. The primary key of the table.

    customer_id : int
        The ID of the customer that the email address belongs to.
        Foreign key to :attr:`Customer.customer_id`. Is indexed.

    email : str
        The email address. Must be unique. Is indexed.

    rank : int
        The rank of the email, where 1 defines the primary email, 2 the secondary
        and 3 the tertiary etc ... A customer can only have one email of each rank.

    verified : bool, default False
        True if the email address is verified by the customer and False otherwise.

    verified_at : datetime or None
        The timestamp at which the email address was verified.

    updated_at : datetime or None
        The timestamp at which the email address was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the email address.

    created_at : datetime
        The timestamp at which the email address was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the email address.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'customer_email_id',
        'customer_id',
        'email',
        'rank',
        'verified',
        'verified_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'customer_email'

    customer_email_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.customer_id, ondelete='CASCADE'))
    email: Mapped[str]
    rank: Mapped[int] = mapped_column(default=1)
    verified: Mapped[bool] = mapped_column(default=False)
    verified_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())

    customer: Mapped['Customer'] = relationship(back_populates='emails')


Index(f'{CustomerEmail.__tablename__}_email_uix', CustomerEmail.email, unique=True)
Index(
    f'{CustomerEmail.__tablename__}_customer_id_rank_uix',
    CustomerEmail.customer_id,
    CustomerEmail.rank,
    unique=True,
)


class PhoneType(ModifiedAndCreatedColumnMixin, Base):
    r"""The types of phone numbers.

    Parameters
    ----------
    phone_type_id : int
        A unique ID of the phone number type. The primary key of the table.

    name : str
        The name of the phone number type. Must be unique. Is indexed.

    description : str or None, default None
        A description of the phone number type.

    updated_at : datetime or None
        The timestamp at which the phone number type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the phone number type.

    created_at : datetime
        The timestamp at which the phone number type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the phone number type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'phone_type_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'phone_type'

    phone_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{PhoneType.__tablename__}_name_uix', PhoneType.name, unique=True)


class CustomerPhone(ModifiedAndCreatedColumnMixin, Base):
    r"""Phone numbers of customers.

    Parameters
    ----------
    customer_phone_id : int
        The unique ID of the customer phone number. The primary key of the table.

    customer_id : int
        The ID of the customer that the phone number belongs to.
        Foreign key to model :attr:`Customer.customer_id`. Is indexed.

    phone_type_id : int
        The type of phone number. Foreign key to :attr:`PhoneType.phone_type_id`. Is indexed.

    number : int
        The phone number. Must be unique across all customers. Is indexed.

    country_code : int or None
        The country code of the phone number e.g. 46 for Sweden.

    rank : int
        The rank of the phone number, where 1 defines the primary number, 2 the secondary
        and 3 the tertiary etc ... A customer can only have one phone number of each rank.

    verified : bool, default False
        True if the phone number is verified by the customer and False otherwise.

    verified_at : datetime or None
        The timestamp at which the phone number was verified.

    updated_at : datetime or None
        The timestamp at which the phone number was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the phone number.

    created_at : datetime
        The timestamp at which the phone number was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the phone number.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'customer_phone_id',
        'customer_id',
        'phone_type_id',
        'number',
        'country_code',
        'rank',
        'verified',
        'verified_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'customer_phone'

    customer_phone_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.customer_id))
    phone_type_id: Mapped[int] = mapped_column(ForeignKey(PhoneType.phone_type_id))
    number: Mapped[int]
    country_code: Mapped[int | None]
    rank: Mapped[int] = mapped_column(default=1)
    verified: Mapped[bool] = mapped_column(default=False)
    verified_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())

    customer: Mapped['Customer'] = relationship(back_populates='phone_numbers')


Index(f'{CustomerPhone.__tablename__}_number_uix', CustomerPhone.number, unique=True)
Index(
    f'{CustomerPhone.__tablename__}_customer_id_rank_uix',
    CustomerPhone.customer_id,
    CustomerPhone.rank,
    unique=True,
)


# =================================================================================================
# Device
# =================================================================================================


class DeviceType(ModifiedAndCreatedColumnMixin, Base):
    r"""The types of devices.

    Parameters
    ----------
    device_type_id : int
        The unique ID of the device. The primary key of the table.

    name : str
        The name of the device type. Must be unique. Is indexed.

    table_name : str
        The name of the table where device type specific information is stored. Must be unique.

    description : str or None
        An optional description of the device type.

    updated_at : datetime or None
        The timestamp at which the device type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device type.

    created_at : datetime
        The timestamp at which the device type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_state_id',
        'name',
        'table_name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device_type'

    device_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    table_name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]


Index(f'{DeviceType.name}_name_uix', unique=True)


class DeviceState(ModifiedAndCreatedColumnMixin, Base):
    r"""The state of a device e.g. enabled or disabled.

    Parameters
    ----------
    device_state_id : int
        The unique ID of the device state. The primary key of the table.

    name : str
        The name of the device state. Must be unique. Is indexed.

    description : str or None
        An optional description of the device state.

    updated_at : datetime or None
        The timestamp at which the device state was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device state.

    created_at : datetime
        The timestamp at which the device state was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device state.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_state_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device_state'

    device_state_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{DeviceState.name}_name_uix', unique=True)


class Device(ModifiedAndCreatedColumnMixin, Base):
    r"""A device that can be enabled on a facility e.g. a meter.

    Parameters
    ----------
    device_id : int
        The unique ID of the device. The primary key of the table.

    ext_id : str or None
        The unique ID of the device in an external system. Must be unique. Is indexed.

    device_type_id : int
        The type of device. Foreign key to :attr:`DeviceType.device_type_id`. Is indexed.

    device_state_id : int
        The current state of device. Foreign key to :attr:`DeviceState.device_state_id`.
        Is indexed.

    manufacture_date : date or None
        The date when the device was manufactured.

    manufacturer_id : int or None
        The ID of the company that manufactured the device. Foreign key to
        :attr:`Manufacturer.manufacturer_id`. Is indexed.

    type_description_id : int or None
        The ID of the type description of the device, which conveys information
        about the model and the configuration of the device. Foreign key to
        :attr:`TypeDescription.type_description_id`. Is indexed.

    manufacture_batch_id : int or None
        The ID of the batch that the device was manufactured in. Foreign key to
        :attr:`ManufactureBatch.manufacture_batch_id`. Is indexed.

    warranty_date : date or None
        The last date that the warranty of the device is valid.

    purchase_price : int or None
        The purchase price of the device. Specify as the lowest currency unit e.g. cent.

    updated_at : datetime or None
        The timestamp at which the device was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device.

    created_at : datetime
        The timestamp at which the device was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_id',
        'ext_id',
        'device_type_id',
        'device_state_id',
        'manufacture_date',
        'manufacturer_id',
        'type_description_id',
        'manufacture_batch_id',
        'warranty_date',
        'purchase_price',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device'

    device_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ext_id: Mapped[str | None]
    device_type_id: Mapped[int] = mapped_column(ForeignKey(DeviceType.device_type_id))
    device_state_id: Mapped[int] = mapped_column(ForeignKey(DeviceState.device_state_id))
    manufacture_date: Mapped[date | None]
    manufacturer_id: Mapped[int | None] = mapped_column(ForeignKey(Manufacturer.manufacturer_id))
    type_description_id: Mapped[int | None] = mapped_column(
        ForeignKey(TypeDescription.type_description_id)
    )
    manufacture_batch_id: Mapped[int | None] = mapped_column(
        ForeignKey(ManufactureBatch.manufacture_batch_id)
    )
    warranty_date: Mapped[date | None]
    purchase_price: Mapped[int | None]

    facility: Mapped['DeviceFacilityLink'] = relationship(back_populates='device')


Index(f'{Device.__tablename__}_ext_id_uix', Device.ext_id, unique=True)
Index(f'{Device.__tablename__}_device_type_id_ix', Device.device_type_id)
Index(f'{Device.__tablename__}_device_state_id_ix', Device.device_state_id)
Index(f'{Device.__tablename__}_manufacturer_id_ix', Device.manufacturer_id)
Index(f'{Device.__tablename__}_type_description_id_ix', Device.type_description_id)
Index(f'{Device.__tablename__}_manufacture_batch_id_ix', Device.manufacture_batch_id)


class ElectricityMeter(ModifiedAndCreatedColumnMixin, Base):
    r"""Properties of an electricity meter.

    Parameters
    ----------
    device_id : int
        The unique ID of the device. The primary key of the table.
        Foreign key to :attr:`Device.device_id`.

    fuse_size : int or None
        The fuse size [A] of the meter.

    nr_phases : int or None
        The number of phases of the meter.

    category : int or None
        The category of the meter.

    updated_at : datetime or None
        The timestamp at which the meter was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the meter.

    created_at : datetime
        The timestamp at which the meter was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the meter.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_id',
        'fuse_size',
        'nr_phases',
        'category',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'electricity_meter'

    device_id: Mapped[int] = mapped_column(
        ForeignKey(Device.device_id, ondelete='CASCADE'), primary_key=True
    )
    fuse_size: Mapped[int | None]
    nr_phases: Mapped[int | None]
    category: Mapped[int | None]


class DeviceLocationType(ModifiedAndCreatedColumnMixin, Base):
    r"""The type of location of the device(s) at the facility.

    Parameters
    ----------
    device_loc_type_id : int
        The unique ID of the device location type. The primary key of the table.

    name : str
        The name of the device location type. Must be unique. Is indexed.

    description : str or None
        A description of the device location type.

    updated_at : datetime or None
        The timestamp at which the device location type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device location type.

    created_at : datetime
        The timestamp at which the device location type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device location type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_loc_type_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device_location_type'

    device_loc_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{DeviceLocationType.name}_name_uix', unique=True)


# =================================================================================================
# Facility
# =================================================================================================


class FacilityAccessMethod(ModifiedAndCreatedColumnMixin, Base):
    r"""The method for how a technician can be granted access to the facility.

    Parameters
    ----------
    facility_access_method_id : int
        The unique ID of the facility access method. The primary key of the table.

    name : str
        The name of the facility access method. Must be unique. Is indexed.

    description : str or None
        A description of the facility access method.

    updated_at : datetime or None
        The timestamp at which the facility access method was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the facility access method.

    created_at : datetime
        The timestamp at which the facility access method was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the facility access method.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'facility_access_method_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'facility_access_method'

    facility_access_method_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{FacilityAccessMethod.name}_name_uix', unique=True)


class Facility(ModifiedAndCreatedColumnMixin, Base):
    r"""A facility is where a service e.g. electricity is being delivered.

    Parameters
    ----------
    facility_id : int
        The unique ID of the facility. The primary key of the table.

    customer_id : int or None
        The ID of the customer who owns the facility. Foreign key to
        :attr:`Customer.customer_id`. Is indexed.

    ext_id : str or None
        The unique ID of the facility in an external system. Must be unique. Is indexed.

    ean : int or None
        The EAN code or GS1-number of the facility (18 digits). Must be unique. Is indexed.

    name : str or None
        A name for the facility.

    common_name : str or None
        A common name used for the facility.

    description : str or None
        An optional description of the facility.

    facility_access_method_id : int or None
        The method for how a technician can be granted access to the facility.
        Foreign key to :attr:`FacilityAccessMethod.facility_access_method_id`. Is indexed.

    key_id : int or None
        The ID of the key that is needed to access the facility.
        Foreign key to :attr:`Key.key_id`. Is indexed.

    device_loc_type_id : int or None
        The type of location of the device(s) of the facility. Foreign key to
        :attr:`DeviceLocationType.device_loc_type_id`. Is indexed.

    device_loc_description : str or None
        A description of the device location.

    access_code : int or None
        An access code to the facility.

    has_alarm : bool or None
        True if the facility has an alarm activated.

    alarm_code : int or None
        A code to deactivate the alarm when entering the facility.

    has_electricity : bool or None
        True if the facility has a functional electricity outlet
        to which devices can be connected and False otherwise.

    min_nr_technicians_at_device_change : int or None
        The minimum required number of technicians to perform
        a device change on the facility.

    updated_at : datetime or None
        The timestamp at which the facility was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the facility.

    created_at : datetime
        The timestamp at which the facility was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the facility.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'facility_id',
        'customer_id',
        'ext_id',
        'ean',
        'name',
        'common_name',
        'description',
        'facility_access_method_id',
        'key_id',
        'device_loc_type_id',
        'device_loc_description',
        'access_code',
        'has_alarm',
        'alarm_code',
        'has_electricity',
        'min_nr_technicians_at_device_change',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'facility'

    facility_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey(Customer.customer_id))
    ext_id: Mapped[str | None]
    ean: Mapped[int | None]
    name: Mapped[str | None]
    common_name: Mapped[str | None]
    description: Mapped[str | None]
    key_id: Mapped[int | None] = mapped_column(ForeignKey(Key.key_id, ondelete='SET NULL'))
    facility_access_method_id: Mapped[int | None] = mapped_column(
        ForeignKey(FacilityAccessMethod.facility_access_method_id, ondelete='SET NULL')
    )
    device_loc_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(DeviceLocationType.device_loc_type_id, ondelete='SET NULL')
    )
    device_loc_description: Mapped[str | None]
    access_code: Mapped[int | None]
    has_alarm: Mapped[bool | None]
    alarm_code: Mapped[int | None]
    has_electricity: Mapped[bool | None]
    min_nr_technicians_at_device_change: Mapped[int | None]

    devices: Mapped[list['DeviceFacilityLink']] = relationship(back_populates='facility')
    customer: Mapped[Customer] = relationship(back_populates='facilities')
    images: Mapped[list['Image']] = relationship(back_populates='facility')


Index(f'{Facility.__tablename__}_customer_id_ix', Facility.customer_id)
Index(f'{Facility.__tablename__}_ext_id_uix', Facility.ext_id, unique=True)
Index(f'{Facility.__tablename__}_ean_uix', Facility.ean, unique=True)
Index(f'{Facility.__tablename__}_key_id_ix', Facility.key_id)
Index(f'{Facility.__tablename__}_facility_access_method_id_ix', Facility.facility_access_method_id)
Index(f'{Facility.__tablename__}_device_loc_type_id_ix', Facility.device_loc_type_id)


class DeviceFacilityLink(ModifiedAndCreatedColumnMixin, Base):
    r"""How devices are currently linked to facilities.

    Parameters
    ----------
    device_id : int
        The unique ID of the device. The primary key of the table.
        Foreign key to :attr:`Device.device_id`.

    facility_id : int
        The ID of the facility where the device is located.
        Foreign key to :attr:`Facility.facility_id`. Is indexed.

    updated_at : datetime or None
        The timestamp at which the device facility link was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device facility link.

    created_at : datetime
        The timestamp at which the device facility link was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device facility link.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_id',
        'facility_id',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device_facility_link'

    device_id: Mapped[int] = mapped_column(ForeignKey(Device.device_id), primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey(Facility.facility_id))

    device: Mapped[Device] = relationship(back_populates='facility')
    facility: Mapped[Facility] = relationship(back_populates='devices')


Index(f'{DeviceFacilityLink.__tablename__}_facility_id_ix', DeviceFacilityLink.facility_id)


class DeviceFacilityEnabledDisabledLog(ModifiedAndCreatedColumnMixin, Base):
    r"""The log of when a device has been enabled or disabled on a facility.

    Parameters
    ----------
    device_id : int
        The unique ID of the device. Part of primary key of the table.
        Foreign key to :attr:`DeviceState.device_state_id`.

    enabled_at : datetime
        The timestamp when the device was enabled at the facility.
        Part of primary key of the table.

    facility_id : int
        The ID of the facility where the device is or was located depending on if
        the device was enabled or disabled. Foreign key to :attr:`Facility.facility_id`.
        Is indexed.

    disabled_at : datetime or None
        The timestamp when the device was disabled at the facility.

    updated_at : datetime or None
        The timestamp at which the device change was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device change.

    created_at : datetime
        The timestamp at which the device change was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device change.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_id',
        'enabled_at',
        'facility_id',
        'disabled_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'device_facility_enabled_disabled_log'

    device_id: Mapped[int] = mapped_column(
        ForeignKey(Device.device_id, ondelete='CASCADE'), primary_key=True
    )
    enabled_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.current_timestamp(), primary_key=True
    )
    facility_id: Mapped[int] = mapped_column(ForeignKey(Facility.facility_id, ondelete='CASCADE'))
    disabled_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())


class MountType(ModifiedAndCreatedColumnMixin, Base):
    r"""The type mount point of a device place.

    Parameters
    ----------
    mount_type_id : int
        The unique ID of the mount type. The primary key of the table.

    name : str
        The name of the mount type. Must be unique. Is indexed.

    description : str or None
        A description of the mount type.

    updated_at : datetime or None
        The timestamp at which the mount type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the mount type.

    created_at : datetime
        The timestamp at which the mount type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the mount type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = ('mount_type_id', 'name', 'description')

    __tablename__ = 'mount_type'

    mount_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]


Index(f'{MountType.name}_name_uix', unique=True)


class DistrictHeatingCoolingFacility(ModifiedAndCreatedColumnMixin, Base):
    r"""Properties of a district heating or cooling facility.

    Parameters
    ----------
    facility_id : int
        The unique ID of the facility. The primary key of the table.
        Foreign key to :attr:`Facility.facility_id`.

    device_loc_build_length : int or None
        The build length [mm] where the volume pipe should be fitted to the device location.

    device_loc_mount_type_id : int or None
        The mount type of the volume pipe to the device location.
        Foreign key to :attr:`MountType.mount_type_id`. Is indexed.

    device_loc_mount_dim : int or None
        The dimension of the mount type.

    device_loc_mount_dim_unit_id : int or None
        The ID of the unit of the mount dimension.
        Foreign key to :attr:`Unit.unit_id`. Is indexed.

    updated_at : datetime or None
        The timestamp at which the facility was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the facility.

    created_at : datetime
        The timestamp at which the facility was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the facility.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'facility_id',
        'device_loc_build_length',
        'device_loc_mount_type_id',
        'device_loc_mount_dim',
        'device_loc_mount_dim_unit_id',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'district_heating_cooling_facility'

    facility_id: Mapped[int] = mapped_column(
        ForeignKey(Facility.facility_id, ondelete='CASCADE'), primary_key=True
    )
    device_loc_build_length: Mapped[int | None]
    device_loc_mount_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(MountType.mount_type_id, ondelete='SET NULL')
    )
    device_loc_mount_dim: Mapped[int | None]
    device_loc_mount_dim_unit_id: Mapped[int | None] = mapped_column(ForeignKey(Unit.unit_id))


Index(f'{DistrictHeatingCoolingFacility.__tablename__}_device_loc_mount_type_id_ix')
Index(f'{DistrictHeatingCoolingFacility.__tablename__}_device_loc_mount_dim_unit_id_ix')


class ElectricityFacility(ModifiedAndCreatedColumnMixin, Base):
    r"""Properties of an electricity facility.

    Parameters
    ----------
    facility_id : int
        The unique ID of the facility. The primary key of the table.
        Foreign key to :attr:`Facility.facility_id`.

    prod_facility_ean : int or None
        The unique ID of the related production facility if such exist.

    prod_facility_installed_power : float or None
        The installed power [kW] of the related production facility.

    device_loc_fuse_size : int or None
        The fuse size [A] of the device location.

    device_loc_plinth : int or None
        The plinth number of the device location where electricity meter is connected.

    updated_at : datetime or None
        The timestamp at which the facility was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the facility.

    created_at : datetime
        The timestamp at which the facility was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the facility.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'facility_id',
        'prod_facility_ean',
        'prod_facility_installed_power',
        'device_loc_fuse_size',
        'device_loc_plinth',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'electricity_facility'

    facility_id: Mapped[int] = mapped_column(
        ForeignKey(Facility.facility_id, ondelete='CASCADE'), primary_key=True
    )
    prod_facility_ean: Mapped[int | None]
    prod_facility_installed_power: Mapped[float | None]
    device_loc_fuse_size: Mapped[int | None]
    device_loc_plinth: Mapped[int | None]


Index(f'{ElectricityFacility.__tablename__}_prod_facility_ean_uix', unique=True)


class LatestDeviceMeterReading(ModifiedAndCreatedColumnMixin, Base):
    r"""The latest meter reading of a device.

    Parameters
    ----------
    device_id : int
        The unique ID of the device. Part of primary key of the table.
        Foreign key to :attr:`Device.device_id`.

    unit_id : int
        The unit of the meter reading. Part of primary key of the table.
        Foreign key to :attr:`Unit.unit_id`.

    facility_id : int or None
        The facility the device was connected to at the time of the latest reading.
        Foreign key to :attr:`Facility.facility_id`. Is indexed.

    timestamp_id : datetime
        The timestamp when the meter reading was recorded.

    meter_reading : float
        The meter reading

    comment : str or None
        An optional comment about the meter reading.

    updated_at : datetime or None
        The timestamp at which the device meter reading was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device meter reading.

    created_at : datetime
        The timestamp at which the device meter reading was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device meter reading.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'device_id',
        'unit_id',
        'facility_id',
        'timestamp_id',
        'meter_reading',
        'comment',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'latest_device_meter_reading'

    device_id: Mapped[int] = mapped_column(
        ForeignKey(Device.device_id, ondelete='CASCADE'), primary_key=True
    )
    unit_id: Mapped[int] = mapped_column(ForeignKey(Unit.unit_id), primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey(Facility.facility_id))
    timestamp_id: Mapped[datetime]
    meter_reading: Mapped[float]
    comment: Mapped[str | None]


Index(
    f'{LatestDeviceMeterReading.__tablename__}_facility_id_ix', LatestDeviceMeterReading.facility_id
)


# =================================================================================================
# Checklist
# =================================================================================================


class Checklist(ModifiedAndCreatedColumnMixin, Base):
    r"""A checklist of an order.

    A checklist holds the steps a technician needs to go through when
    processing a device order.

    Parameters
    ----------
    checklist_id : int
        The unique ID of the checklist. The primary key of the table.

    utility_id : int
        The ID of the utility the checklist belongs to. Foreign key to
        :attr:`Utility.utility_id`. Is indexed.

    name : str
        A name of the checklist.

    description : str or None
        A description of the checklist.

    updated_at : datetime or None
        The timestamp at which the checklist was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the checklist.

    created_at : datetime
        The timestamp at which the checklist was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the checklist.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'checklist_id',
        'utility_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'checklist'

    checklist_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    utility_id: Mapped[int] = mapped_column(ForeignKey(Utility.utility_id))
    name: Mapped[str]
    description: Mapped[str | None]

    checklist_items: Mapped[list['ChecklistItem']] = relationship(back_populates='checklist')
    orders: Mapped[list['Order']] = relationship(back_populates='checklist')


Index(f'{Checklist.__tablename__}_utility_id_ix', Checklist.utility_id)


class ChecklistItem(ModifiedAndCreatedColumnMixin, Base):
    r"""An item of a checklist that can hold information.

    Parameters
    ----------
    checklist_item_id : int
        The unique ID of the checklist item. The primary key of the table.

    checklist_id : int
        The checklist that the item belongs to. Foreign key to
        :attr:`Checklist.checklist_id`. Is indexed.

    dtype_id : int
        The data type of the value that the checklist item can hold.
        Foreign key to :attr:`Dtype.dtype_id`. Is indexed.

    value_column_name_id : int
        The column name where the checklist item value is stored, which depends of `dtype_id`.
        Foreign key to :attr:`ValueColumnName.value_column_name_id`. Is indexed.

    name : str
        The name of the checklist item.

    description : str or None
        An optional description of the checklist item.

    updated_at : datetime or None
        The timestamp at which the checklist item was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the checklist item.

    created_at : datetime
        The timestamp at which the checklist item was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the checklist item.

    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'checklist_item_id',
        'checklist_id',
        'dtype_id',
        'value_column_name_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'checklist_item'

    checklist_item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    checklist_id: Mapped[int] = mapped_column(
        ForeignKey(Checklist.checklist_id, ondelete='CASCADE')
    )
    dtype_id: Mapped[int] = mapped_column(ForeignKey(DType.dtype_id))
    value_column_name_id: Mapped[int] = mapped_column(
        ForeignKey(ValueColumnName.value_column_name_id)
    )
    name: Mapped[str]
    description: Mapped[str | None]

    checklist: Mapped[Checklist] = relationship(back_populates='checklist_items')
    order_checklist_items: Mapped[list['OrderChecklistItem']] = relationship(
        back_populates='checklist_item'
    )


Index(f'{ChecklistItem.__tablename__}_checklist_id_ix', ChecklistItem.checklist_id)
Index(f'{ChecklistItem.__tablename__}_dtype_id_ix', ChecklistItem.dtype_id)
Index(f'{ChecklistItem.__tablename__}_value_column_name_id_ix', ChecklistItem.value_column_name_id)


# =================================================================================================
# Orders
# =================================================================================================


class OrderType(ModifiedAndCreatedColumnMixin, Base):
    r"""The types of orders.

    Parameters
    ----------
    order_type_id : int
        The unique ID of the order type. The primary key of the table.

    utility_id : int
        The utility that the order type belongs to. Foreign key to
        :attr:`Utility.utility_id`. Is indexed.

    name : str
        The name of the order type. Is indexed.

    description : str or None
        A description of the order type.

    updated_at : datetime or None
        The timestamp at which the order type was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the order type.

    created_at : datetime
        The timestamp at which the order type was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the order type.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_type_id',
        'utility_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_type'

    order_type_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    utility_id: Mapped[int] = mapped_column(ForeignKey(Utility.utility_id))
    name: Mapped[str]
    description: Mapped[str | None]

    orders: Mapped[list['Order']] = relationship(back_populates='order_type')


Index(f'{OrderType.__tablename__}_utility_id_ix', OrderType.utility_id)
Index(f'{OrderType.__tablename__}_name_ix', OrderType.name)


class OrderStatus(ModifiedAndCreatedColumnMixin, Base):
    r"""The statuses of an order.

    Parameters
    ----------
    order_status_id : int
        The unique ID of the order status. The primary key of the table.

    name : str
        The name of the status. Must be unique. Is indexed.

    description : str or None
        A description of the status

    updated_at : datetime or None
        The timestamp at which the order status was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the order status.

    created_at : datetime
        The timestamp at which the order status was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the order status.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_status_id',
        'name',
        'description',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_status'

    order_status_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]

    orders: Mapped[list['Order']] = relationship(back_populates='order_status')


Index(f'{OrderStatus.__tablename__}_name_uix', OrderType.name, unique=True)


class Order(ModifiedAndCreatedColumnMixin, Base):
    r"""An order for a technician to carry out a task e.g. a device change.

    Parameters
    ----------
    order_id : int
        The unique ID of the order. The primary key of the table.

    order_type_id : int
        The type of order. Foreign key to :attr:`OrderType.order_type_id`. Is indexed.

    order_status_id : int
        The status of the order. Foreign key to :attr:`OrderStatus.order_status_id`. Is indexed.

    ext_id : str or None
        The unique reference ID to the order in an external system. Is indexed.

    facility_id : int
        The facility the order is targeting. Foreign key to :attr:`Facility.facility_id`.
        Is indexed.

    location_id : int
        The location where the order takes place. Foreign key to :attr:`Location.location_id`.
        Is indexed.

    customer_id : int
        The ID of the customer that owned the target facility of the order at the time when
        the order was carried out. Foreign key to :attr:`Customer.customer_id`. Is indexed.

    checklist_id : int or None
        The checklist assigned to the order with the tasks the technician needs to carry out.
        Foreign key to :attr:`Checklist.checklist_id`. Is indexed.

    assigned_to : str or None
        The technician that is assigned to the order. Foreign key to
        :attr:`streamlit_passwordless.User.user_id`. Is indexed.

    scheduled_start_at : datetime or None
        The scheduled start time of the order.

    scheduled_end_at : datetime or None
        The scheduled end time of the order.

    closing_comment : str or None
        An optional comment from the technician regarding the completion of the order.
        Usually entered if the order could not be carried out as expected.

    completed_by : str or None
        The user that marked the order as complete. Foreign key to
        :attr:`streamlit_passwordless.User.user_id`. Is indexed.

    completed_at : datetime or None
        The timestamp at which the order was completed.

    updated_at : datetime or None
        The timestamp at which the order was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the order.

    created_at : datetime
        The timestamp at which the order was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the order.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_id',
        'order_type_id',
        'order_status_id',
        'ext_id',
        'facility_id',
        'location_id',
        'customer_id',
        'checklist_id',
        'assigned_to',
        'scheduled_start_at',
        'scheduled_end_at',
        'closing_comment',
        'completed_by',
        'completed_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order'

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_type_id: Mapped[int] = mapped_column(ForeignKey(OrderType.order_type_id))
    order_status_id: Mapped[int] = mapped_column(ForeignKey(OrderStatus.order_status_id))
    ext_id: Mapped[str | None]
    facility_id: Mapped[int] = mapped_column(ForeignKey(Facility.facility_id))
    location_id: Mapped[int] = mapped_column(ForeignKey(Location.location_id))
    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey(Customer.customer_id, ondelete='SET NULL')
    )
    checklist_id: Mapped[int | None] = mapped_column(
        ForeignKey(Checklist.checklist_id, ondelete='SET NULL')
    )

    assigned_to_user_id: Mapped[str | None] = mapped_column(
        ForeignKey(User.user_id), onupdate='SET NULL'
    )
    scheduled_start_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())
    scheduled_end_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())
    closing_comment: Mapped[str | None]
    completed_by: Mapped[str | None] = mapped_column(ForeignKey(User.user_id, ondelete='SET NULL'))
    completed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())

    order_type: Mapped[OrderType] = relationship(back_populates='orders')
    order_status: Mapped[OrderStatus] = relationship(back_populates='orders')
    checklist: Mapped[Checklist] = relationship(back_populates='orders')
    checklist_items: Mapped[list['OrderChecklistItem']] = relationship(back_populates='order')
    enabled_disabled_devices_mr: Mapped[list['OrderEnabledDisabledDeviceMR']] = relationship(
        back_populates='order'
    )
    enabled_disabled_devices: Mapped[list['OrderEnabledDisabledDevice']] = relationship(
        back_populates='order'
    )
    images: Mapped[list['Image']] = relationship(back_populates='order')
    order_comments: Mapped[list['OrderComment']] = relationship(
        back_populates='order', foreign_keys='OrderComment.order_id'
    )
    order_schedules: Mapped[list['OrderScheduleLog']] = relationship(back_populates='order')


Index(f'{Order.__tablename__}_order_type_id_ix', Order.order_type_id)
Index(f'{Order.__tablename__}_order_status_id_ix', Order.order_status_id)
Index(f'{Order.__tablename__}_facility_id_ix', Order.facility_id)
Index(f'{Order.__tablename__}_location_id_ix', Order.location_id)
Index(f'{Order.__tablename__}_customer_id_ix', Order.customer_id)
Index(f'{Order.__tablename__}_checklist_id_ix', Order.checklist_id)
Index(f'{Order.__tablename__}_assigned_to_user_id_ix', Order.assigned_to_user_id)


class OrderEnabledDisabledDeviceMR(ModifiedAndCreatedColumnMixin, Base):
    r"""Enabled and disabled devices that collect meter readings related to an order.

    Parameters
    ----------
    order_id : int
        The ID of the order the device change belongs to. Part of primary key of the table.
        Foreign key to :attr:`Order.order_id`.

    unit_id : int
        The unit of meter readings. Part of primary key of the table.
        Foreign key to :attr:`Unit.unit_id`.

    enabled_device_id : int or None
        The ID of the enabled device. Foreign key to :attr:`Device.device_id`. Is indexed.

    enabled_meter_reading : float or None
        The meter reading of the enabled device when it was enabled. Usually 0.

    enabled_at : datetime or None
        The timestamp when the enabled device was enabled.

    disabled_device_id : int or None
        The ID of the disabled device. Foreign key to :attr:`Device.device_id`. Is indexed.

    disabled_meter_reading : float or None
        The meter reading of the disabled device when it was disabled.

    disabled_at : datetime or None
        The timestamp when the disabled device was disabled.

    comment : str or None
        An optional comment from the technician regarding the changed devices.

    updated_at : datetime or None
        The timestamp at which the device change was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device change.

    created_at : datetime
        The timestamp at which the device change was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device change.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_id',
        'unit_id',
        'enabled_device_id',
        'enabled_meter_reading',
        'enabled_at',
        'disabled_device_id',
        'disabled_meter_reading',
        'disabled_at',
        'comment',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_enabled_disabled_device_mr'

    order_id: Mapped[int] = mapped_column(
        ForeignKey(Order.order_id, ondelete='CASCADE'), primary_key=True
    )
    unit_id: Mapped[int] = mapped_column(ForeignKey(Unit.unit_id), primary_key=True)
    enabled_device_id: Mapped[int | None] = mapped_column(ForeignKey(Device.device_id))
    enabled_meter_reading: Mapped[float | None]
    enabled_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())
    disabled_device_id: Mapped[int | None] = mapped_column(ForeignKey(Device.device_id))
    disabled_meter_reading: Mapped[float | None]
    disabled_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())
    comment: Mapped[str | None]

    order: Mapped[Order] = relationship(back_populates='enabled_disabled_devices_mr')


class OrderEnabledDisabledDevice(ModifiedAndCreatedColumnMixin, Base):
    r"""Extra devices that have been enabled or disabled that do not collect meter readings.

    E.g. installing an antenna to an electricity meter.

    Parameters
    ----------
    order_id : int
        The ID of the order the device change belongs to. Part of primary key of the table.
        Foreign key to :attr:`Order.order_id`.

    enabled_device_id : int or None
        The ID of the enabled device. Part of primary key of the table.
        Foreign key to :attr:`Device.device_id`.

    disabled_device_id : int or None
        The ID of the disabled device. Part of primary key of the table.
        Foreign key to :attr:`Device.device_id`.

    related_device_id : int or None
        The ID of the device that the enabled or disabled device relate to.
        E.g. the ID of an electricity meter when an antenna has been enabled.
        Foreign key to :attr:`Device.device_id`. Is indexed.

    enabled_at : datetime or None
        The timestamp when the enabled device was enabled.

    disabled_at : datetime or None
        The timestamp when the disabled device was disabled.

    comment : str or None
        An optional comment from the technician regarding the changed devices.

    updated_at : datetime or None
        The timestamp at which the device change was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the device change.

    created_at : datetime
        The timestamp at which the device change was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the device change.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_id',
        'enabled_device_id',
        'disabled_device_id',
        'related_device_id',
        'enabled_at',
        'disabled_at',
        'comment',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_enabled_disabled_device'

    order_id: Mapped[int] = mapped_column(
        ForeignKey(Order.order_id, ondelete='CASCADE'), primary_key=True
    )
    enabled_device_id: Mapped[int | None] = mapped_column(
        ForeignKey(Device.device_id), primary_key=True
    )
    disabled_device_id: Mapped[int | None] = mapped_column(
        ForeignKey(Device.device_id), primary_key=True
    )
    related_device_id: Mapped[int | None] = mapped_column(ForeignKey(Device.device_id))
    enabled_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())
    disabled_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())
    comment: Mapped[str | None]

    order: Mapped[Order] = relationship(back_populates='enabled_disabled_devices')


Index(
    f'{OrderEnabledDisabledDevice.__tablename__}_related_device_id_ix',
    OrderEnabledDisabledDevice.related_device_id,
)


class OrderChecklistItem(ModifiedAndCreatedColumnMixin, Base):
    r"""A checklist item associated with an order with info from a technician.

    Parameters
    ----------
    order_id : int
        The ID of the order to which the checklist item belongs. Part of primary key
        of the table. Foreign key to :attr:`Order.order_id`.

    checklist_item_id : int
        The unique ID of the checklist item. Part of primary key of the table.
        Foreign key to :attr:`ChecklistItem.checklist_item_id`.

    text_value : str or None
        A text value of the checklist item entered by the technician.

    float_value : float or None
        A float value of the checklist item entered by the technician.

    int_value : int or None
        An integer value of the checklist item entered by the technician.

    bool_value : bool or None
        A boolean value of the checklist item entered by the technician.

    timestamp_value : bool or None
        A timestamp value of the checklist item entered by the technician.

    comment : str or None
        A comment about the checklist item entered by the technician.

    completed_by : str or None
        The user that marked the checklist item as complete. Foreign key to
        :attr:`streamlit_passwordless.User.user_id`. Is indexed.

    completed_at : datetime or None
        The timestamp at which the checklist item was completed.

    updated_at : datetime or None
        The timestamp at which the order checklist item was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the order checklist item.

    created_at : datetime
        The timestamp at which the order checklist item was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the order checklist item.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_id',
        'checklist_item_id',
        'text_value',
        'float_value',
        'int_value',
        'bool_value',
        'timestamp_value',
        'comment',
        'completed_by',
        'completed_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_checklist_item'

    order_id: Mapped[int] = mapped_column(
        ForeignKey(Order.order_id, ondelete='CASCADE'), primary_key=True
    )
    checklist_item_id: Mapped[int] = mapped_column(
        ForeignKey(ChecklistItem.checklist_item_id), primary_key=True
    )
    text_value: Mapped[str | None]
    float_value: Mapped[float | None]
    int_value: Mapped[int | None]
    bool_value: Mapped[bool | None]
    timestamp_value: Mapped[bool | None]
    comment: Mapped[str | None]
    completed_by: Mapped[str | None] = mapped_column(ForeignKey(User.user_id, ondelete='SET NULL'))
    completed_at: Mapped[datetime | None]

    checklist_item: Mapped[ChecklistItem] = relationship(back_populates='order_checklist_items')
    order: Mapped[Order] = relationship(back_populates='checklist_items')


Index(f'{OrderChecklistItem.__tablename__}_completed_by_ix', OrderChecklistItem.completed_by)


class Image(ModifiedAndCreatedColumnMixin, Base):
    r"""Images associated with orders and facilities.

    Technicians may take images to document their work.

    Parameters
    ----------
    image_id : int
        The unique ID of the image. The primary key of the table.

    order_id : int
        The ID of the order that the image belongs to. Foreign key to
        :attr:`Order.order_id`. Is indexed.

    facility_id : int
        The ID of the facility that the image belongs to. Foreign key to
        :attr:`Facility.facility_id`. Is indexed.

    path : str
        The absolute file path to the image on the disk where it is stored.

    name : str or None
        The name of the image.

    caption : str or None
        A caption describing the image.

    image_taken_at : datetime or None
        The timestamp when the image was taken (UTC).

    updated_at : datetime or None
        The timestamp at which the image was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the image.

    created_at : datetime
        The timestamp at which the image was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the image.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'image_id',
        'order_id',
        'facility_id',
        'path',
        'name',
        'caption',
        'image_taken_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'image'

    image_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey(Order.order_id, ondelete='SET NULL'))
    facility_id: Mapped[int] = mapped_column(ForeignKey(Facility.facility_id, ondelete='SET NULL'))
    path: Mapped[str]
    name: Mapped[str | None]
    caption: Mapped[str | None]
    image_taken_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())

    order: Mapped[Order] = relationship(back_populates='images')
    facility: Mapped[Facility] = relationship(back_populates='images')


Index(f'{Image.__tablename__}_order_id_ix', Image.order_id)
Index(f'{Image.__tablename__}_facility_ix', Image.facility_id)


class OrderComment(ModifiedAndCreatedColumnMixin, Base):
    r"""Comments on an order from a user.

    Parameters
    ----------
    order_comment_id : int
        The unique ID of the order comment. The primary key of the table.

    order_id : int
        The ID of the order that the comment references. Foreign key to
        :attr:`Order.order_id`. Is indexed.

    user_id : str
        The user that placed the comment. Foreign key to
        :attr:`streamlit_passwordless.User.user_id`. Is indexed.

    comment : str
        The comment on the order.

    referenced_order_id : int or None
        The ID of another order that the comment references.
        Foreign key to :attr:`Order.order_id`.

    updated_at : datetime or None
        The timestamp at which the order comment was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the order comment.

    created_at : datetime
        The timestamp at which the order comment was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the order comment.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_comment_id',
        'order_id',
        'user_id',
        'comment',
        'referenced_order_id',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_comment'

    order_comment_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey(Order.order_id, ondelete='CASCADE'))
    user_id: Mapped[str] = mapped_column(ForeignKey(User.user_id, ondelete='SET NULL'))
    comment: Mapped[str]
    referenced_order_id: Mapped[int | None] = mapped_column(
        ForeignKey(Order.order_id, ondelete='SET NULL')
    )

    order: Mapped[Order] = relationship(back_populates='order_comments', foreign_keys=[order_id])


Index(f'{OrderComment.__tablename__}_order_id_ix', OrderComment.order_id)
Index(f'{OrderComment.__tablename__}_user_id_ix', OrderComment.user_id)


class OrderScheduleLog(ModifiedAndCreatedColumnMixin, Base):
    r"""Information when orders have been scheduled and to which technician.

    Parameters
    ----------
    order_id : int
        The unique ID of the order. Part of primary key of the table.

    user_id : str
        The ID of the technician that was assigned to the order.
        Foreign key to :attr:`streamlit_passwordless.User.user_id`.

    start_at : datetime
        The scheduled start time. Part of primary key of the table.

    end_at : datetime or None
        The scheduled end time.

    updated_at : datetime or None
        The timestamp at which the order schedule log was last updated (UTC).

    updated_by : str or None
        The ID of the user that last updated the order schedule log.

    created_at : datetime
        The timestamp at which the order schedule log was created (UTC).
        Defaults to current timestamp.

    created_by : str or None
        The ID of the user that created the order schedule log.
    """

    columns__repr__: ClassVar[tuple[str, ...]] = (
        'order_id',
        'user_id',
        'start_at',
        'end_at',
        'updated_at',
        'updated_by',
        'created_at',
        'created_by',
    )

    __tablename__ = 'order_schedule_log'

    order_id: Mapped[int] = mapped_column(
        ForeignKey(Order.order_id), onupdate='CASCADE', primary_key=True
    )
    user_id: Mapped[str] = mapped_column(ForeignKey(User.user_id), primary_key=True)
    start_at: Mapped[datetime] = mapped_column(TIMESTAMP(), primary_key=True)
    end_at: Mapped[datetime | None] = mapped_column(TIMESTAMP())

    order: Mapped[Order] = relationship(back_populates='order_schedules')
