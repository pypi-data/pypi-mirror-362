r"""The default data of the tables."""

# Local
from cambiato.database.core import Session
from cambiato.database.models.core import (
    CoordinateSystem,
    DType,
    KeyType,
    Unit,
    Utility,
    ValueColumnName,
)
from cambiato.database.models.relations import (
    ContactMethod,
    CustomerType,
    DeviceLocationType,
    DeviceState,
    DeviceType,
    FacilityAccessMethod,
    LocationType,
    MountType,
    OrderStatus,
    OrderType,
    PhoneType,
)

# DType
text_dtype = DType(dtype_id=1, name='TEXT')
float_dtype = DType(dtype_id=2, name='FLOAT')
int_dtype = DType(dtype_id=3, name='INT')
bool_dtype = DType(dtype_id=4, name='BOOLEAN')
timestamp_dtype = DType(dtype_id=5, name='TIMESTAMP')

# Unit
kWh_unit = Unit(unit_id=1, name='kWh', description='kilo Watt hours')
kVArh_unit = Unit(unit_id=2, name='kVArh', description='kilo Volt Ampere reactive hours')
MWh_unit = Unit(unit_id=3, name='MWh', description='Mega Watt hours')
m3_unit = Unit(unit_id=4, name='m3', description='Cubic Meters')
degrees_celsius_unit = Unit(unit_id=5, name='°C', description='Degrees Celsius')

# ValueColumnName
text_column_name = ValueColumnName(
    value_column_name_id=1, dtype_id=1, name='text_value', description='A text column.'
)
float_column_name = ValueColumnName(
    value_column_name_id=2, dtype_id=2, name='float_value', description='A float column.'
)
int_column_name = ValueColumnName(
    value_column_name_id=3, dtype_id=3, name='int_value', description='An integer column.'
)
bool_column_name = ValueColumnName(
    value_column_name_id=4, dtype_id=4, name='bool_value', description='A boolean column.'
)
timestamp_column_name = ValueColumnName(
    value_column_name_id=5,
    dtype_id=5,
    name='timestamp_value',
    description='A timestamp column.',
)

# Utility
el_utility = Utility(utility_id=1, name='Electricity', description='The electricity utility.')
dh_utility = Utility(
    utility_id=2, name='District Heating', description='The district heating utility.'
)
dc_utility = Utility(
    utility_id=3, name='District Cooling', description='The district cooling utility.'
)
water_utility = Utility(utility_id=4, name='Water', description='The water utility.')
water_utility = Utility(utility_id=5, name='Gas', description='The gas utility.')

# CoordinateSystem
wgs84_coord_system = CoordinateSystem(
    coordinate_system_id=1, name='WGS84', description='The WGS84 coordinate system.'
)
sweref991200_coord_system = CoordinateSystem(
    coordinate_system_id=2,
    name='SWEREF991200',
    description='The SWEREF99 coordinate system with the 12:00 projection.',
)

# KeyType
analog_key_type = KeyType(key_type_id=1, name='Analog', description='An analog regular key.')
tag_key_type = KeyType(
    key_type_id=2,
    name='Tag',
    description='A tag that can be "blipped" to gain access to a resource.',
)
card_key_type = KeyType(
    key_type_id=3,
    name='Card',
    description='A card that can be "swiped" to gain access to a resource.',
)

# LocationType
customer_loc_type = LocationType(
    location_type_id=1,
    name='Customer Location',
    description=(
        'Where a customer facility can be located. '
        'To be used when the exact type of location is unknown.'
    ),
)
house_loc_type = LocationType(location_type_id=2, name='House', description='A house.')
apartment_loc_type = LocationType(location_type_id=3, name='Apartment', description='An apartment')
multi_residential_loc_type = LocationType(
    location_type_id=4,
    name='Multi-Residential Building',
    description='A multi-residential building',
)
receiver_loc_type = LocationType(
    location_type_id=5, name='Receiver Station', description='An electricity receiver station.'
)
grid_station_loc_type = LocationType(
    location_type_id=6, name='Grid Station', description='An electricity grid station.'
)
cable_cabinet_loc_type = LocationType(
    location_type_id=7, name='Cable Cabinet', description='An electricity cable cabinet.'
)

# CustomerType
private_person_customer_type = CustomerType(
    customer_type_id=1,
    name='Private Person',
    description='A private person customer. Not a company.',
)
company_customer_type = CustomerType(
    customer_type_id=2,
    name='Company',
    description='A company customer. Can be used for any sized company.',
)
small_business_customer_type = CustomerType(
    customer_type_id=3, name='Small Business', description='A small business customer.'
)
school_customer_type = CustomerType(customer_type_id=4, name='School', description='A school.')

# ContactMethod
sms_contact_method = ContactMethod(
    contact_method_id=1, name='SMS', description='Short Message Service.'
)
email_contact_method = ContactMethod(contact_method_id=2, name='Email', description='Email.')
call_contact_method = ContactMethod(
    contact_method_id=3,
    name='Call',
    description='A customer who prefers to be called when contact is needed.',
)
note_in_mailbox_contact_method = ContactMethod(
    contact_method_id=4,
    name='Note in Mailbox',
    description=(
        'A customer who is hard to reach and the most likely method '
        'to get in touch is leaving a physical note in the mailbox.'
    ),
)

# PhoneType
private_phone_type = PhoneType(
    phone_type_id=1, name='Private', description='A private number of a customer.'
)
work_phone_type = PhoneType(
    phone_type_id=2, name='Work', description='A number to the workplace of the customer.'
)

# DeviceType
electricity_meter_device_type = DeviceType(
    device_type_id=1,
    name='Electricity Meter',
    table_name='electricity_meter',
    description='An electricity meter.',
)

# DeviceState
enabled_device_state = DeviceState(
    device_state_id=1, name='Enabled', description='A device which is enabled on a facility.'
)
disabled_device_state = DeviceState(
    device_state_id=2,
    name='Disabled',
    description='A device which has been disabled from a facility.',
)
revision_device_state = DeviceState(
    device_state_id=3, name='Revision', description='A device which has been sent for revision.'
)
scrapped_device_state = DeviceState(
    device_state_id=4,
    name='Scrapped',
    description='A device that has been scrapped and is out of service.',
)

# DeviceLocationType
facade_meter_box_device_loc_type = DeviceLocationType(
    device_loc_type_id=1,
    name='Facade Meter Box',
    description='A device that is located in a facade meter box normally on the outside of a house.',
)
basement_loc_type = DeviceLocationType(
    device_loc_type_id=2,
    name='Basement',
    description='A device that is located in the basement of a building.',
)
meter_room_loc_type = DeviceLocationType(
    device_loc_type_id=3,
    name='Meter Room',
    description='A device that is located in a meter room with other meters.',
)

# FacilityAccessMethod
free_access_fa_method = FacilityAccessMethod(
    facility_access_method_id=1,
    name='Free Access',
    description='The technician can access the facility without the customer being present.',
)

booked_access_fa_method = FacilityAccessMethod(
    facility_access_method_id=2,
    name='Booked Access',
    description='The technician needs to book a time slot when the facility can be accessed.',
)

# MountType
thread_mount_type = MountType(
    mount_type_id=1,
    name='Threaded',
    description=(
        'A threaded mount type where the device should be mounted to the facility device place.'
    ),
)
flange_mount_type = MountType(
    mount_type_id=2,
    name='Flange',
    description=(
        'A flange mount type where the device should be mounted to the facility device place.'
    ),
)

# OrderType
el_device_change_order_type = OrderType(
    order_type_id=1,
    utility_id=el_utility.utility_id,
    name='Device Change',
    description='An electricity meter change on a facility.',
)
el_enable_device_order_type = OrderType(
    order_type_id=2,
    utility_id=el_utility.utility_id,
    name='Enable Device',
    description='Enable a new electricity meter on a facility.',
)
el_disable_device_order_type = OrderType(
    order_type_id=3,
    utility_id=el_utility.utility_id,
    name='Disable Device',
    description='Disable an electricity meter on a facility.',
)
el_comm_point_change_order_type = OrderType(
    order_type_id=4,
    utility_id=el_utility.utility_id,
    name='Communication Point Change',
    description='Change a communication point.',
)
el_manual_reading_order_type = OrderType(
    order_type_id=5,
    utility_id=el_utility.utility_id,
    name='Manual Reading',
    description='The technician needs to perform a manual reading of an electricity meter.',
)
el_meter_alarm_order_type = OrderType(
    order_type_id=6,
    utility_id=el_utility.utility_id,
    name='Meter Alarm',
    description='The technician needs to investigate an alarm from a meter.',
)

# OrderStatus
to_do_order_status = OrderStatus(
    order_status_id=1, name='To do', description='An order that has yet not been started.'
)
assigned_order_status = OrderStatus(
    order_status_id=2,
    name='Assigned',
    description='An order that is assigned to a technician, but it is yet not started.',
)
in_progress_order_status = OrderStatus(
    order_status_id=3, name='In Progress', description='An order that is in progress.'
)
on_hold_order_status = OrderStatus(
    order_status_id=4,
    name='On Hold',
    description='An order that is on hold and should not be worked on.',
)
completed_by_technician_order_status = OrderStatus(
    order_status_id=5,
    name='Completed by Technician',
    description='An order that has been completed by a technician.',
)
completed_order_status = OrderStatus(
    order_status_id=6, name='Completed', description='An order that has been fully completed.'
)


def add_default_models_to_session(session: Session) -> None:
    r"""Create the default models in the database.

    Parameters
    ----------
    session : cambiato.db.Session
        An active database session.

    Returns
    -------
    None
    """

    session.add_all(
        (
            # DType
            text_dtype,
            float_dtype,
            int_dtype,
            bool_dtype,
            timestamp_dtype,
            # Unit
            kWh_unit,
            kVArh_unit,
            MWh_unit,
            m3_unit,
            degrees_celsius_unit,
            # ValueColumnName
            text_column_name,
            float_column_name,
            int_column_name,
            bool_column_name,
            timestamp_column_name,
            # Utility
            el_utility,
            dh_utility,
            dc_utility,
            water_utility,
            water_utility,
            # CoordinateSystem
            wgs84_coord_system,
            sweref991200_coord_system,
            # KeyType
            analog_key_type,
            tag_key_type,
            card_key_type,
            # LocationType
            customer_loc_type,
            house_loc_type,
            apartment_loc_type,
            multi_residential_loc_type,
            receiver_loc_type,
            grid_station_loc_type,
            cable_cabinet_loc_type,
            # CustomerType
            private_person_customer_type,
            company_customer_type,
            small_business_customer_type,
            school_customer_type,
            # ContactMethod
            sms_contact_method,
            email_contact_method,
            call_contact_method,
            note_in_mailbox_contact_method,
            # PhoneType
            private_phone_type,
            work_phone_type,
            # DeviceType
            electricity_meter_device_type,
            # DeviceState
            enabled_device_state,
            disabled_device_state,
            revision_device_state,
            scrapped_device_state,
            # DeviceLocationType
            facade_meter_box_device_loc_type,
            basement_loc_type,
            meter_room_loc_type,
            # FacilityAccessMethod
            free_access_fa_method,
            booked_access_fa_method,
            # MountType
            thread_mount_type,
            flange_mount_type,
            # OrderType
            el_device_change_order_type,
            el_enable_device_order_type,
            el_disable_device_order_type,
            el_comm_point_change_order_type,
            el_manual_reading_order_type,
            el_meter_alarm_order_type,
            # OrderStatus
            to_do_order_status,
            assigned_order_status,
            in_progress_order_status,
            on_hold_order_status,
            completed_by_technician_order_status,
            completed_order_status,
        )
    )
