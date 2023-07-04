"""Stream type classes for tap-upwork."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional, Dict, Any

import pendulum
import requests
from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
    ObjectType,
    BooleanType,
    DateTimeType,
    NumberType,
)

from tap_upwork.client import UpWorkStream


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
    Property('publicUrl', StringType, description='The public user url'),
    Property('email', StringType, description='email of user'),
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


class ContractTimeReportStream(UpWorkStream):
    """Define contract time report stream.
    https://www.upwork.com/developer/documentation/graphql/api/docs/index.html#query-contractTimeReport
    """

    name = 'contractTimeReport'
    schema = TIME_REPORT_PROPERTIES.to_dict()
    primary_keys = []
    replication_key = 'dateWorkedOn'
    query = f"""
    query contractTimeReport($filter: TimeReportFilter, $pagination: Pagination) {{
      contractTimeReport(filter: $filter, pagination: $pagination) {{
        totalCount
        edges {{
          node {{
            {UpWorkStream.property_list_to_graphql_query(TIME_REPORT_PROPERTIES)}
          }}
        }}
       pageInfo {{
          endCursor
          hasNextPage
        }}
      }}
    }}
    """

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[datetime]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be as variables in the GraphQL query."""
        start_date = pendulum.instance(
            self.get_starting_timestamp(context) or pendulum.from_timestamp(0)
        )
        return {
            'filter': {
                'organizationId_eq': self.config.get('organization_id'),
                'timeReportDate_bt': {
                    'rangeStart': start_date.strftime('%Y%m%d'),
                    'rangeEnd': pendulum.now().strftime('%Y%m%d'),
                },
            },
            'pagination': {'start': 1},
        }


class TimeReportStream(UpWorkStream):
    """Define time report stream
    https://www.upwork.com/developer/documentation/graphql/api/docs/index.html#query-timeReport
    """

    name = 'timeReport'
    schema = TIME_REPORT_PROPERTIES.to_dict()
    primary_keys = []
    replication_key = 'dateWorkedOn'
    query = f"""
        query timeReport($filter: TimeReportFilter) {{
          timeReport(filter: $filter) {{
            {UpWorkStream.property_list_to_graphql_query(TIME_REPORT_PROPERTIES)}
          }}
        }}
        """

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[datetime]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be as variables in the GraphQL query."""
        start_date = pendulum.instance(
            self.get_starting_timestamp(context) or pendulum.from_timestamp(0)
        )
        return {
            'filter': {
                'organizationId_eq': self.config.get('organization_id'),
                'timeReportDate_bt': {
                    'rangeStart': start_date.strftime('%Y%m%d'),
                    'rangeEnd': pendulum.now().strftime('%Y%m%d'),
                },
            }
        }


class OrganizationStream(UpWorkStream):
    """Define organization stream.
    https://www.upwork.com/developer/documentation/graphql/api/docs/index.html#query-organization
    """

    name = 'organization'
    schema = GENERIC_ORGANIZATION_PROPERTIES.to_dict()
    primary_keys = ['id']
    replication_key = None  # Incremental bookmarks not needed
    query = f"""
        query {{
            organization {{
                {UpWorkStream.property_list_to_graphql_query(GENERIC_ORGANIZATION_PROPERTIES)}
            }}
        }}"""

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield response.json().get('data', {}).get(self.name, {})
