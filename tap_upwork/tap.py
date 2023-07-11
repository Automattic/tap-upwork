"""UpWork tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_upwork import streams


class TapUpWork(Tap):
    """UpWork tap class."""

    name = 'tap-upwork'

    config_jsonschema = th.PropertiesList(
        th.Property(
            'client_id',
            th.StringType,
            required=True,
            description='The client_id used to generate the OAuth token.',
        ),
        th.Property(
            'client_secret',
            th.StringType,
            required=True,
            secret=True,
            description='The client_secret used to generate the OAuth token.',
        ),
        th.Property(
            'organization_id',
            th.DateTimeType,
            description='Organization ID to be used in time report filter',
        ),
        th.Property(
            'start_date',
            th.DateTimeType,
            description='The earliest record date to sync',
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.UpWorkStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.OrganizationStream(self),
            streams.TimeReportStream(self),
            streams.ContractTimeReportStream(self),
        ]


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    TapUpWork.cli()
