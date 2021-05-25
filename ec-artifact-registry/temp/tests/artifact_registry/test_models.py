
import json
import unittest

from shared.artifact_registry.models import (
    ListArtifactsRequest,
    PresignedURLRequest,
    DescribeArtifactRequest
)

class PresignedURLRequestTest(unittest.TestCase):

    def test_presigned_url_request(self):
        request = PresignedURLRequest(**{
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
        })
        self.assertIsNotNone(request)
        url_meta = request.build_presigned_url_meta()
        self.assertIsNotNone(url_meta)
        # self.assertEqual('eyJhcnRpZmFjdF9rZXkiOiAiL2UyZS10ZXN0L0xhbmRpbmdab25lVGVzdC56aXAiLCAic3RhY2tfbmFtZSI6ICJMYW5kaW5nLVpvbmUtVGVzdCIsICJtYW5pZmVzdF90ZW1wbGF0ZSI6ICJRMnh2ZFdSR2IzSnRZWFJwYjI0NkNpQWdJQ0FnSUNBZ0lDQWdJRkpsY1hWbGMzUkxWMEZ5WjNNNkNpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCVGRHRmphMDVoYldVNklFeGhibVJwYm1jdFdtOXVaUzFVWlhOMENpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCVVlXZHpPZ29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdMU0JMWlhrNklGTlhRVHBQZDI1bGNnb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ1ZtRnNkV1U2SUVWdWRHVnljSEpwYzJVZ1EyeHZkV1FLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQzBnUzJWNU9pQlRWMEU2UTI5emRFTmxiblJsY2dvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnVm1Gc2RXVTZJQ0l5TkRBeE15SUtJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDMGdTMlY1T2lCVFYwRTZVRWxFQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0JXWVd4MVpUb2dTVTh0T0RBd09EUTFDaUFnSUNBZ0lDQWdJQ0FnSUNBZ0lDQXRJRXRsZVRvZ1UxZEJPa1Z1ZG1seWIyNXRaVzUwQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0JXWVd4MVpUb2dSR1YyQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0F0SUV0bGVUb2dVMWRCT2tOdmJtWnBaR1Z1ZEdsaGJHbDBlUW9nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdWbUZzZFdVNklGTlhRU0JKYm5SbGNtNWhiQ0JQYm14NUNpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBdElFdGxlVG9nVTFkQk9rSjFjMmx1WlhOelUyVnlkbWxqWlFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnVm1Gc2RXVTZJRVZEQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0F0SUV0bGVUb2dVMWRCT2tOdmJYQnNhV0Z1WTJVS0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUZaaGJIVmxPaUJPUVFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnTFNCTFpYazZJRVZET2xOMFlXTnJWbVZ5YzJsdmJnb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ1ZtRnNkV1U2SUNJeExqQWlDaUFnSUNBZ0lDQWdJQ0FnSUNBZ0lDQXRJRXRsZVRvZ1UxZEJPazVoYldVS0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUZaaGJIVmxPaUJNWVc1a2FXNW5MVnB2Ym1VdFZHVnpkQW9nSUNBZ0lDQWdJQ0FnSUNCU1pXZHBiMjV6T2dvZ0lDQWdJQ0FnSUNBZ0lDQXRJSFZ6TFdWaGMzUXRNUW9nSUNBZ0lDQWdJQ0FnSUNBdElIVnpMWGRsYzNRdE1nb2dJQ0FnSUNBZ0lDQWdJQ0JVWVhKblpYUnpPZ29nSUNBZ0lDQWdJQ0FnSUNCQlkyTnZkVzUwU1dSek9nb2dJQ0FnSUNBZ0lDQWdJQ0F0SURjM05UWTVPREl3TURJM053b2dJQ0FnSUNBZ0lDQWdJQ0JVWlcxd2JHRjBaVG9LSUNBZ0lDQWdJQ0FnSUNBZ1NXNWFhWEJHYVd4bE9pQk1ZVzVrYVc1bldtOXVaVlJsYzNRdWVtbHdDaUFnSUNBZ0lDQWdJQ0FnSUU1aGJXVTZJRXhoYm1ScGJtZGFiMjVsVkdWemRDNTViV3dLSUNBZ0lDQWdJQ0E9IiwgIm93bmVyX2FjY291bnRfaWQiOiAiNzc1Njk4MjAwMjc3IiwgImRlcGxveW1lbnRfc2VsZWN0b3IiOiAiZGV2IiwgImF3c19yZWdpb24iOiAidXMtZWFzdC0xIiwgImRlcGVuZGVudF9hcnRpZmFjdHMiOiBbImFybjphd3M6ZWMtYXJ0aWZhY3QtcmVnaXN0cnk6dXMtZWFzdC0xOjc3NTY5ODIwMDI3NzphcnRpZmFjdC9MYW5kaW5nLVpvbmUtVGVzdC9kZXYiXX0=', url_meta)  # noqa E501
        arn = request.build_arn()
        self.assertIsNotNone(arn)
        self.assertEqual(arn, 'arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev')
        self.assertEqual(request.get_body().artifact_key, "/e2e-test/LandingZoneTest.zip")

    def test_presigned_url_request_body_is_string(self):
        request = PresignedURLRequest(**{
            "resource": "/registry/artifact/presigned_url",
            "path": "/registry/artifact/presigned_url",
            "httpMethod": "GET",
            "body": json.dumps({
                "stack_name": "Landing-Zone-Test",
                "artifact_key": "/e2e-test/LandingZoneTest.zip",
                "owner_account_id": "775698200277",
                "aws_region": "us-east-1",
                "deployment_selector": "dev",
                "dependent_artifacts": [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ]
            }),
            "isBase64Encoded": False
        })
        self.assertIsNotNone(request)
        url_meta = request.build_presigned_url_meta()
        self.assertIsNotNone(url_meta)
        # self.assertEqual('eyJhcnRpZmFjdF9rZXkiOiAiL2UyZS10ZXN0L0xhbmRpbmdab25lVGVzdC56aXAiLCAic3RhY2tfbmFtZSI6ICJMYW5kaW5nLVpvbmUtVGVzdCIsICJtYW5pZmVzdF90ZW1wbGF0ZSI6ICJRMnh2ZFdSR2IzSnRZWFJwYjI0NkNpQWdJQ0FnSUNBZ0lDQWdJRkpsY1hWbGMzUkxWMEZ5WjNNNkNpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCVGRHRmphMDVoYldVNklFeGhibVJwYm1jdFdtOXVaUzFVWlhOMENpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNCVVlXZHpPZ29nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdMU0JMWlhrNklGTlhRVHBQZDI1bGNnb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ1ZtRnNkV1U2SUVWdWRHVnljSEpwYzJVZ1EyeHZkV1FLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJQzBnUzJWNU9pQlRWMEU2UTI5emRFTmxiblJsY2dvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnVm1Gc2RXVTZJQ0l5TkRBeE15SUtJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lDMGdTMlY1T2lCVFYwRTZVRWxFQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0JXWVd4MVpUb2dTVTh0T0RBd09EUTFDaUFnSUNBZ0lDQWdJQ0FnSUNBZ0lDQXRJRXRsZVRvZ1UxZEJPa1Z1ZG1seWIyNXRaVzUwQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0JXWVd4MVpUb2dSR1YyQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0F0SUV0bGVUb2dVMWRCT2tOdmJtWnBaR1Z1ZEdsaGJHbDBlUW9nSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdWbUZzZFdVNklGTlhRU0JKYm5SbGNtNWhiQ0JQYm14NUNpQWdJQ0FnSUNBZ0lDQWdJQ0FnSUNBdElFdGxlVG9nVTFkQk9rSjFjMmx1WlhOelUyVnlkbWxqWlFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnVm1Gc2RXVTZJRVZEQ2lBZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0F0SUV0bGVUb2dVMWRCT2tOdmJYQnNhV0Z1WTJVS0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUZaaGJIVmxPaUJPUVFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnTFNCTFpYazZJRVZET2xOMFlXTnJWbVZ5YzJsdmJnb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ1ZtRnNkV1U2SUNJeExqQWlDaUFnSUNBZ0lDQWdJQ0FnSUNBZ0lDQXRJRXRsZVRvZ1UxZEJPazVoYldVS0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnSUZaaGJIVmxPaUJNWVc1a2FXNW5MVnB2Ym1VdFZHVnpkQW9nSUNBZ0lDQWdJQ0FnSUNCU1pXZHBiMjV6T2dvZ0lDQWdJQ0FnSUNBZ0lDQXRJSFZ6TFdWaGMzUXRNUW9nSUNBZ0lDQWdJQ0FnSUNBdElIVnpMWGRsYzNRdE1nb2dJQ0FnSUNBZ0lDQWdJQ0JVWVhKblpYUnpPZ29nSUNBZ0lDQWdJQ0FnSUNCQlkyTnZkVzUwU1dSek9nb2dJQ0FnSUNBZ0lDQWdJQ0F0SURjM05UWTVPREl3TURJM053b2dJQ0FnSUNBZ0lDQWdJQ0JVWlcxd2JHRjBaVG9LSUNBZ0lDQWdJQ0FnSUNBZ1NXNWFhWEJHYVd4bE9pQk1ZVzVrYVc1bldtOXVaVlJsYzNRdWVtbHdDaUFnSUNBZ0lDQWdJQ0FnSUU1aGJXVTZJRXhoYm1ScGJtZGFiMjVsVkdWemRDNTViV3dLSUNBZ0lDQWdJQ0E9IiwgIm93bmVyX2FjY291bnRfaWQiOiAiNzc1Njk4MjAwMjc3IiwgImRlcGxveW1lbnRfc2VsZWN0b3IiOiAiZGV2IiwgImF3c19yZWdpb24iOiAidXMtZWFzdC0xIiwgImRlcGVuZGVudF9hcnRpZmFjdHMiOiBbImFybjphd3M6ZWMtYXJ0aWZhY3QtcmVnaXN0cnk6dXMtZWFzdC0xOjc3NTY5ODIwMDI3NzphcnRpZmFjdC9MYW5kaW5nLVpvbmUtVGVzdC9kZXYiXX0=', url_meta)  # noqa E501
        arn = request.build_arn()
        self.assertIsNotNone(arn)
        self.assertEqual(arn, 'arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev')
        self.assertEqual(request.get_body().artifact_key, "/e2e-test/LandingZoneTest.zip")

    def test_describe_artifact_request(self):
        ''' test_describe_artifact_request '''

        request = DescribeArtifactRequest(**{
            "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev"
        })
        self.assertIsNotNone(request)
        self.assertEqual(request.arn, "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev")  # noqa E501

    def test_list_artifacts_request_empty(self):
        ''' test_list_artifacts_request_empty '''
        request = ListArtifactsRequest(**{})
        self.assertIsNotNone(request)
        self.assertIsNone(request.deployment_selector)
        self.assertIsNone(request.owner_account_id)

    def test_list_artifacts_request_deployment_selector(self):
        ''' test_list_artifacts_request_deployment_selector '''
        request = ListArtifactsRequest(**{
            'deployment_selector': 'dev'
        })
        self.assertIsNotNone(request)
        self.assertIsNotNone(request.deployment_selector)
        self.assertIsNone(request.owner_account_id)
        self.assertEqual(request.deployment_selector, 'dev')

    def test_list_artifacts_request_owner_account_id(self):
        ''' test_list_artifacts_request_owner_account_id '''
        request = ListArtifactsRequest(**{
            'owner_account_id': '1234567890'
        })
        self.assertIsNotNone(request)
        self.assertIsNone(request.deployment_selector)
        self.assertIsNotNone(request.owner_account_id)
        self.assertEqual(request.owner_account_id, '1234567890')

    def test_list_artifacts_request_all(self):
        ''' test_list_artifacts_request_all '''
        request = ListArtifactsRequest(**{
            'deployment_selector': 'dev',
            'owner_account_id': '1234567890'
        })
        self.assertIsNotNone(request)
        self.assertIsNotNone(request.deployment_selector)
        self.assertIsNotNone(request.owner_account_id)
        self.assertEqual(request.deployment_selector, 'dev')
        self.assertEqual(request.owner_account_id, '1234567890')