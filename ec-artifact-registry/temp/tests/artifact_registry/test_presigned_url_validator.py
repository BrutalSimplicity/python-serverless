
import unittest

from shared.artifact_registry.models import PresignedURLRequest
from shared.artifact_registry.presigned_url_validator import (
    PresignedURLRequestValidator
)

class PresignedURLValidatorTest(unittest.TestCase):
    ''' PresignedURLValidatorTest '''

    def test_is_self_dependent(self):

        testcases = [
            {
                'name': 'validate:is_self_dependent:not_self_dependent',
                'input': PresignedURLRequest(**{
                    "resource": "/registry",
                    "path": "/registry/presigned_url",
                    "httpMethod": "GET",
                    "body": {
                        "stack_name": "Landing-Zone-Test",
                        "artifact_key": "/e2e-test/LandingZoneTest.zip",
                        "owner_account_id": "775698200277",
                        "aws_region": "us-east-1",
                        "deployment_selector": "dev"
                    },
                    "isBase64Encoded": False
                }),
                'expected': False,
                'skip': False,
                'should_fail': False
            },
            {
                'name': 'validate:is_self_dependent:is_self_dependent',
                'input': PresignedURLRequest(**{
                    "resource": "/registry",
                    "path": "/registry/presigned_url",
                    "httpMethod": "GET",
                    "body": {
                        "stack_name": "Landing-Zone-Test",
                        "artifact_key": "/e2e-test/LandingZoneTest.zip",
                        "owner_account_id": "775698200277",
                        "aws_region": "us-east-1",
                        "deployment_selector": "dev",
                        "dependent_artifacts": [
                            "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                        ]
                    },
                    "isBase64Encoded": False
                }),
                'expected': True,
                'skip': False,
                'should_fail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                validator = PresignedURLRequestValidator(case.get('input'))
                actual = validator.is_self_dependent()
                self.assertEqual(actual, case.get('expected'))

    def test_validate(self):

        testcases = [
            {
                'name': 'validate:is_self_dependent:not_self_dependent',
                'input': PresignedURLRequest(**{
                    "resource": "/registry",
                    "path": "/registry/presigned_url",
                    "httpMethod": "GET",
                    "body": {
                        "stack_name": "Landing-Zone-Test",
                        "artifact_key": "/e2e-test/LandingZoneTest.zip",
                        "owner_account_id": "775698200277",
                        "aws_region": "us-east-1",
                        "deployment_selector": "dev"
                    },
                    "isBase64Encoded": False
                }),
                'expected': [],
                'skip': False,
                'should_fail': False
            },
            {
                'name': 'validate:is_self_dependent:is_self_dependent',
                'input': PresignedURLRequest(**{
                    "resource": "/registry/artifact/presigned_url",
                    "path": "/registry/artifact/presigned_url",
                    "httpMethod": "GET",
                    "body": {
                        "stack_name": "Landing-Zone-Test",
                        "artifact_key": "/e2e-test/LandingZoneTest.zip",
                        "owner_account_id": "775698200277",
                        "aws_region": "us-east-1",
                        "deployment_selector": "dev",
                        "dependent_artifacts": [
                            "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                        ]
                    },
                    "isBase64Encoded": False
                }),
                'expected': [
                    'PresignedURLRequest with ARN: arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev, includes its own ARN in the dependent_artifacts array, thereby creating a circular dependency with iteself.'  # noqa E501
                ],
                'skip': False,
                'should_fail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                validator = PresignedURLRequestValidator(case.get('input'))
                actual = validator.validate()
                self.assertEqual(actual, case.get('expected'))
