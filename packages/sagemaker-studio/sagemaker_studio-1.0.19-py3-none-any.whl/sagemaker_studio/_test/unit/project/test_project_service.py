import unittest
from unittest.mock import Mock

from botocore.exceptions import ClientError

from sagemaker_studio.exceptions import AWSClientException
from sagemaker_studio.projects import ProjectService


class TestProjectService(unittest.TestCase):
    def setUp(self):
        self.mock_datazone_api = Mock()
        self.project_service = ProjectService(self.mock_datazone_api)

    def test_is_default_environment_present(self):
        self.mock_datazone_api.list_environment_blueprints.return_value = {
            "items": [{"id": "test_environment_id"}]
        }
        self.mock_datazone_api.list_environments.return_value = {
            "items": [{"id": "test_environment_id"}]
        }
        result = self.project_service.is_default_environment_present(
            domain_identifier="test_domain",
            project_identifier="test_project",
            blueprint_name="DataLake",
        )
        self.assertTrue(result)

    def test_is_default_environment_present_no_blueprints(self):
        self.mock_datazone_api.list_environment_blueprints.return_value = {"items": []}
        with self.assertRaises(ValueError) as context:
            self.project_service.is_default_environment_present(
                domain_identifier="test_domain",
                project_identifier="test_project",
                blueprint_name="DataLake",
            )
        self.assertIn("DataLake environment blueprint not found", str(context.exception))

    def test_is_default_environment_present_no_environments(self):
        self.mock_datazone_api.list_environment_blueprints.return_value = {
            "items": [{"id": "blueprint_id_123"}]
        }
        self.mock_datazone_api.list_environments.return_value = {"items": []}
        result = self.project_service.is_default_environment_present(
            domain_identifier="test_domain",
            project_identifier="test_project",
            blueprint_name="DataLake",
        )
        self.assertFalse(result)

    def test_get_project_default_environment_throws_validation_exception(self):
        error_response = {
            "Error": {
                "Code": "ValidationException",
                "Message": "ValidationException",
            },
            "ResponseMetadata": {
                "RequestId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "HTTPStatusCode": 403,
                "HTTPHeaders": {
                    "x-amzn-requestid": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "content-type": "application/json",
                    "content-length": "0",
                    "date": "Fri, 01 Jan 1970 00:00:00 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.mock_datazone_api.list_environment_blueprints.return_value = {
            "items": [{"id": "blueprint_id_123"}]
        }
        self.mock_datazone_api.list_environments.side_effect = ClientError(
            error_response, "ListEnvironments"
        )

        with self.assertRaises(ValueError) as context:
            self.project_service.get_project_default_environment("dzd_1234", "abc1244")
            self.assertTrue("Invalid input parameters" in context.exception)

    def test_get_project_default_environment_throws_other_exception(self):
        error_response = {
            "Error": {
                "Code": "ResourceNotFoundException",
                "Message": "The environment blueprint could not be found",
            },
            "ResponseMetadata": {
                "RequestId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "HTTPStatusCode": 403,
                "HTTPHeaders": {
                    "x-amzn-requestid": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "content-type": "application/json",
                    "content-length": "0",
                    "date": "Fri, 01 Jan 1970 00:00:00 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.mock_datazone_api.list_environment_blueprints.return_value = {
            "items": [{"id": "blueprint_id_123"}]
        }
        self.mock_datazone_api.list_environments.side_effect = ClientError(
            error_response, "ListEnvironments"
        )

        with self.assertRaises(AWSClientException) as context:
            self.project_service.get_project_default_environment("dzd_1234", "abc1244")
            self.assertTrue("ResourceNotFoundException" in context.exception)

    def test_get_project_sagemaker_environment_throws_value_error(self):
        error_response = {
            "Error": {
                "Code": "ValidationException",
                "Message": "ValidationException",
            },
            "ResponseMetadata": {
                "RequestId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "HTTPStatusCode": 403,
                "HTTPHeaders": {
                    "x-amzn-requestid": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "content-type": "application/json",
                    "content-length": "0",
                    "date": "Fri, 01 Jan 1970 00:00:00 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.mock_datazone_api.list_environments.side_effect = ClientError(
            error_response, "ListEnvironments"
        )

        with self.assertRaises(ValueError) as context:
            self.project_service.get_project_sagemaker_environment("dzd_1234", "abc1244")
            self.assertTrue("Invalid input parameters" in context.exception)

    def test_get_project_sagemaker_environment_throws_other_error(self):
        error_response = {
            "Error": {
                "Code": "ResourceNotFoundException",
                "Message": "ResourceNotFoundException",
            },
            "ResponseMetadata": {
                "RequestId": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "HTTPStatusCode": 403,
                "HTTPHeaders": {
                    "x-amzn-requestid": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "content-type": "application/json",
                    "content-length": "0",
                    "date": "Fri, 01 Jan 1970 00:00:00 GMT",
                },
                "RetryAttempts": 0,
            },
        }
        self.mock_datazone_api.list_environments.side_effect = ClientError(
            error_response, "ListEnvironments"
        )

        with self.assertRaises(AWSClientException) as context:
            self.project_service.get_project_sagemaker_environment("dzd_1234", "abc1244")
            self.assertTrue("ResourceNotFoundException" in context.exception)
