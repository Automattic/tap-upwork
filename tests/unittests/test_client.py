from unittest import TestCase

from singer_sdk.typing import (
    PropertiesList,
    Property,
    StringType,
    IntegerType,
    NumberType,
    ObjectType,
)

from tap_upwork.client import UpWorkStream


class TestClient(TestCase):
    def test_property_list_to_graphql_query(self):
        """
        Test that property_list_to_graphql_query returns an expected fragment of GraphQL query
        """
        property_list = PropertiesList(
            Property('string', StringType),
            Property('integer', IntegerType),
            Property('number', NumberType),
            Property(
                'object',
                ObjectType(
                    Property(
                        'object_nested_field1',
                        ObjectType(
                            Property('object_nested_field1_field1', StringType),
                        ),
                    ),
                    Property('object_nested_field2', StringType),
                ),
            ),
            Property(
                'property_list',
                PropertiesList(
                    Property('property_list_nested_field1', IntegerType),
                    Property(
                        'property_list_nested_field2',
                        PropertiesList(
                            Property('property_list_nested_field2_field1', StringType),
                        ),
                    ),
                ),
            ),
        )

        expected_query = (
            'string integer number object { '
            'object_nested_field1 { object_nested_field1_field1 } object_nested_field2 } '
            'property_list { property_list_nested_field1 property_list_nested_field2 { property_list_nested_field2_field1 } }'
        )
        result_query = UpWorkStream.property_list_to_graphql_query(property_list)

        self.assertEqual(expected_query, result_query)
