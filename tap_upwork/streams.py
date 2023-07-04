"""Stream type classes for tap-upwork."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional, Dict, Any

import pendulum
import requests

from tap_upwork.client import UpWorkStream
from tap_upwork.schemas import TIME_REPORT_PROPERTIES, GENERIC_ORGANIZATION_PROPERTIES


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
