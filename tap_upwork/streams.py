"""Stream type classes for tap-upwork."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional, Dict, Any

import pendulum
import requests
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_upwork.client import UpWorkStream


TIME_REPORT_PROPERTIES = [
    th.Property('dateWorkedOn', th.DateTimeType, description='Date of the time report'),
    th.Property('weekWorkedOn', th.DateTimeType, description='Week of the time report'),
    th.Property('monthWorkedOn', th.DateTimeType, description='Month of the time report'),
    th.Property('yearWorkedOn', th.DateTimeType, description='Year of the time report'),

    # th.Property(
    #     'freelancer',
    #     th.ObjectType(
    #         th.Property('id', th.IntegerType, description='Unique user identifier'),
    #         th.Property('nid', th.IntegerType, description='Nickname ID of a user'),
    #         th.Property('rid', th.IntegerType, description='Record ID of a user'),
    #         th.Property('name', th.StringType),
    #         th.Property('photoUrl', th.StringType),
    #         th.Property('publicUrl', th.StringType),
    #         th.Property('email', th.StringType),
    #         th.Property('ciphertext', th.StringType)
    #     ),
    #     description='User associated with the time report'
    # ),
    # th.Property(
    #     'team',
    #     th.ObjectType(
    #         th.Property('id', th.IntegerType, description='ID of the current organization'),
    #         th.Property('rid', th.IntegerType, description='Record ID of the organization'),
    #         th.Property('legacyId', th.IntegerType, description='Record ID of a user'),
    #         th.Property('name', th.StringType),
    #         th.Property('type', th.StringType),
    #         th.Property('legacyType', th.StringType)
    #     ),
    #     description='Team associated with the time report'
    # ),
    # th.Property(
    #     'contract',
    #     th.ObjectType(
    #         th.Property('id', th.IntegerType, description='basic contract data'),
    #         th.Property('title', th.StringType),
    #         th.Property('status', th.StringType)
    #     )
    # ),

    th.Property('task', th.StringType, description='Task associated with the time report'),
    th.Property('taskDescription', th.StringType, description='Task description associated with the time report'),
    th.Property('memo', th.StringType, description='Memo associated with the time report'),
    th.Property('totalHoursWorked', th.NumberType, description='Total hours worked for the time report'),
    th.Property('totalCharges', th.NumberType, description='Total charges made for the time report'),
    th.Property('totalOnlineHoursWorked', th.NumberType, description='Total online hours worked for the time report'),
    th.Property('totalOnlineCharge', th.NumberType, description='Total charges made for online work for the time '
                                                                'report'),
    th.Property('totalOfflineHoursWorked', th.NumberType, description='Total offline hours worked for the time report'),
    th.Property('totalOfflineCharge', th.NumberType, description='Total charges made for offline work for the time '
                                                                 'report'),
]


class ContractTimeReportStream(UpWorkStream):
    """Define contract time report stream."""

    name = 'contractTimeReport'
    schema = th.PropertiesList(
        *TIME_REPORT_PROPERTIES
    ).to_dict()
    primary_keys = []
    replication_key = 'dateWorkedOn'
    query = """
    contractTimeReport($filter: TimeReportFilter, $pagination: Pagination) {
      contractTimeReport(filter: $filter, pagination: $pagination) {
        totalCount
        edges {
          node {
            dateWorkedOn,
            weekWorkedOn
            monthWorkedOn
            yearWorkedOn
            task
            taskDescription
            memo
            totalHoursWorked
            totalCharges
            totalOnlineHoursWorked
            totalOnlineCharge
            totalOfflineHoursWorked
            totalOfflineCharge
          }
        }
      }
    }
        """


class TimeReportStream(UpWorkStream):
    """Define time report stream
    https://www.upwork.com/developer/documentation/graphql/api/docs/index.html#query-timeReport
    """

    name = 'contractTimeReport'
    schema = th.PropertiesList(
        *TIME_REPORT_PROPERTIES
    ).to_dict()
    primary_keys = []
    replication_key = 'dateWorkedOn'
    query = """
        timeReport($filter: TimeReportFilter) {
          timeReport(filter: $filter) {
            dateWorkedOn
            weekWorkedOn
            monthWorkedOn
            yearWorkedOn
            task
            taskDescription
            memo
            totalHoursWorked
            totalCharges
            totalOnlineHoursWorked
            totalOnlineCharge
            totalOfflineHoursWorked
            totalOfflineCharge
          }
        }
        """

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[datetime]) -> Dict[str, Any]:
        """Return a dictionary of values to be as variables in the GraphQL query."""
        start_date = pendulum.instance(
            self.get_starting_timestamp(context)
            or pendulum.from_timestamp(0)
        )
        return {
            "filter": {
                "organizationId_eq": self.config.get("organization_id"),
                "timeReportDate_bt": {
                    "rangeStart": start_date.strftime("%Y%m%d"),
                    "rangeEnd": pendulum.now().strftime("%Y%m%d"),
                }
            }
        }


class OrganizationStream(UpWorkStream):
    """Define organization stream.
    https://www.upwork.com/developer/documentation/graphql/api/docs/index.html#query-organization
    """

    name = 'organization'
    schema = th.PropertiesList(
        th.Property('id', th.IntegerType),
        th.Property('name', th.StringType),
    ).to_dict()
    primary_keys = ['id']
    replication_key = None  # Incremental bookmarks not needed
    query = """
        organization {
            id,
            name
          }
        """

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        yield response.json().get('data', {}).get(self.name, {})
