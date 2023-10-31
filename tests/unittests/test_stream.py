from functools import partial
from unittest import TestCase
from unittest.mock import patch, create_autospec

import pendulum

from tap_upwork.streams import ContractTimeReportStream


class TestContractTimeReportStream(TestCase):
    def setUp(self):
        self.mock_contract_time_report_stream = create_autospec(
            ContractTimeReportStream, instance=True
        )
        self.mock_contract_time_report_stream.get_url_params = partial(
            ContractTimeReportStream.get_url_params,
            self.mock_contract_time_report_stream,
        )

    @patch('tap_upwork.streams.pendulum.now')
    @patch('tap_upwork.streams.pendulum.instance')
    def test_get_url_params(self, mock_instance, mock_now):
        mock_now.return_value = pendulum.datetime(2023, 10, 30)
        mock_instance.return_value = pendulum.datetime(2023, 10, 25)

        # Test with min_days_to_sync > state
        self.mock_contract_time_report_stream.config = {
            'organization_id': '12345',
            'min_days_to_sync': 7,
        }

        expected_params = {
            'filter': {
                'organizationId_eq': '12345',
                'timeReportDate_bt': {
                    'rangeStart': '2023-10-23',
                    'rangeEnd': '2023-10-30',
                },
            },
            'pagination': {'first': 500},
        }
        result = self.mock_contract_time_report_stream.get_url_params(None, None)
        self.assertEqual(result, expected_params)

        # Test with next_page_token
        expected_params['pagination']['after'] = 'token123'
        result = self.mock_contract_time_report_stream.get_url_params(None, 'token123')
        self.assertEqual(result, expected_params)

        # Test without min_days_to_sync
        self.mock_contract_time_report_stream.config = {
            'organization_id': '12345',
        }

        expected_params = {
            'filter': {
                'organizationId_eq': '12345',
                'timeReportDate_bt': {
                    'rangeStart': '2023-10-25',
                    'rangeEnd': '2023-10-30',
                },
            },
            'pagination': {'first': 500},
        }
        result = self.mock_contract_time_report_stream.get_url_params(None, None)
        self.assertEqual(result, expected_params)

        # Test without min_days_to_sync < state
        self.mock_contract_time_report_stream.config = {
            'organization_id': '12345',
            'min_days_to_sync': 3,
        }

        result = self.mock_contract_time_report_stream.get_url_params(None, None)
        self.assertEqual(result, expected_params)
