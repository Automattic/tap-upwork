from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
    ObjectType,
    BooleanType,
    DateTimeType,
    NumberType,
)


GENERIC_ORGANIZATION_PROPERTIES = PropertiesList(
    Property('id', StringType, description='ID of the current organization'),
    Property('rid', StringType, description='ID of the current organization'),
    Property('name', StringType, description='Name of the current organization'),
    Property('type', StringType, description='Type of the Organization'),
    Property('legacyType', StringType, description='Legacy type of the Organization'),
    Property(
        'flag',
        ObjectType(
            Property('client', BooleanType),
            Property('vendor', BooleanType),
            Property('agency', BooleanType),
            Property('individual', BooleanType),
        ),
        description='Flag associated with the Organization',
    ),
    Property(
        'active',
        BooleanType,
        description='Indicates whether this organization is active.',
    ),
    Property(
        'hidden',
        BooleanType,
        description='Indicates whether this organization/team is hidden.',
    ),
    Property('creationDate', StringType),
)


GENERIC_USER_PROPERTIES = PropertiesList(
    Property('id', StringType, description='Unique user identifier'),
    Property('nid', StringType, description='Nickname ID of a user'),
    Property('rid', StringType, description='Record ID of a user'),
    Property('name', StringType, description='First name + abbreviated last name'),
    Property('email', StringType, description='email of user'),
)


CONTRACT_DETAILS_PROPERTIES = PropertiesList(
    Property('id', StringType, description='basic contract data'),
    Property('title', StringType),
    Property('status', StringType),
    Property('deliveryModel', StringType),
    Property('createDate', BooleanType),
    Property('modifyDate', BooleanType),
    Property('startDate', BooleanType),
    Property('endDate', BooleanType),
)


TIME_REPORT_PROPERTIES = PropertiesList(
    Property('dateWorkedOn', DateTimeType, description='Date of the time report'),
    Property('weekWorkedOn', DateTimeType, description='Week of the time report'),
    Property('monthWorkedOn', DateTimeType, description='Month of the time report'),
    Property('yearWorkedOn', DateTimeType, description='Year of the time report'),
    Property(
        'freelancer',
        GENERIC_USER_PROPERTIES,
        description='User associated with the time report',
    ),
    Property(
        'team',
        GENERIC_ORGANIZATION_PROPERTIES,
        description='Team associated with the time report',
    ),
    Property(
        'contract',
        CONTRACT_DETAILS_PROPERTIES,
        description='Contract-Offer associated with the time report',
    ),
    Property('task', StringType, description='Task associated with the time report'),
    Property(
        'taskDescription',
        StringType,
        description='Task description associated with the time report',
    ),
    Property('memo', StringType, description='Memo associated with the time report'),
    Property(
        'totalHoursWorked',
        NumberType,
        description='Total hours worked for the time report',
    ),
    Property(
        'totalCharges', NumberType, description='Total charges made for the time report'
    ),
    Property(
        'totalOnlineHoursWorked',
        NumberType,
        description='Total online hours worked for the time report',
    ),
    Property(
        'totalOnlineCharge',
        NumberType,
        description='Total charges made for online work for the time report',
    ),
    Property(
        'totalOfflineHoursWorked',
        NumberType,
        description='Total offline hours worked for the time report',
    ),
    Property(
        'totalOfflineCharge',
        NumberType,
        description='Total charges made for offline work for the time report',
    ),
)
