
import unittest

from shared.artifact_registry.registry_connector import (
    ArtifactRegistryEntity
)

class RegistryConnectorTest(unittest.TestCase):

    def test_artifact_registry_entity(self):
        testcases = [
            {
                'name': 'without dependent_artifacts',
                'input': {
                    'GSI1PK': 'stack-name#Describe-Artifact-E2E-Test#dev',
                    'OwnerAccountId': '1234567890',
                    'ArtifactKey': '/test/artifact.zip',
                    'ManifestTemplate': "{'Template': {'Name': 'LandingZoneTest.yml'}, 'CloudFormation': {'RequestKWArgs': {'StackName': 'landing-zone-e2e-test', 'Capabilities': ['CAPABILITY_IAM']}}, 'Targets': {'AccountIds': [775698200277]}, 'Regions': ['us-east-1']}",  # noqa E501
                    'StackName': 'Describe-Artifact-E2E-Test',
                    'SK': 'owner-account-id#1234567890',
                    'GSI1SK': 'owner-account-id#1234567890#2020-10-28T18:23:22.784Z',
                    'PK': 'stack-name#Describe-Artifact-E2E-Test#dev',
                    'Arn': 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev',
                    'DeploymentSelector': 'dev',
                    'VersionId': '1ztSTtEiirD0S0vMGClH3VmScdxspVSR',
                    'AwsRegion': 'us-east-1'
                },
                'expected': {},
                'shouldFail': False,
                'skip': False
            },
            {
                'name': 'with dependent_artifacts',
                'input': {
                    'GSI1PK': 'stack-name#Describe-Artifact-E2E-Test#dev',
                    'OwnerAccountId': '1234567890',
                    'ArtifactKey': '/test/artifact.zip',
                    'ManifestTemplate': "{'Template': {'Name': 'LandingZoneTest.yml'}, 'CloudFormation': {'RequestKWArgs': {'StackName': 'landing-zone-e2e-test', 'Capabilities': ['CAPABILITY_IAM']}}, 'Targets': {'AccountIds': [775698200277]}, 'Regions': ['us-east-1']}",  # noqa E501
                    'StackName': 'Describe-Artifact-E2E-Test',
                    'SK': 'owner-account-id#1234567890',
                    'GSI1SK': 'owner-account-id#1234567890#2020-10-28T18:23:22.784Z',
                    'PK': 'stack-name#Describe-Artifact-E2E-Test#dev',
                    'Arn': 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test/dev',
                    'DeploymentSelector': 'dev',
                    'DependentArtifacts': [
                        'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/Describe-Artifact-E2E-Test-Dependent/dev'  # noqa E501
                    ],
                    'VersionId': '1ztSTtEiirD0S0vMGClH3VmScdxspVSR',
                    'AwsRegion': 'us-east-1'
                },
                'expected': {},
                'shouldFail': False,
                'skip': False
            }
        ]
        for case in testcases:
            with self.subTest(case.get('name')):
                artifact_registry_entity = ArtifactRegistryEntity.create(case.get('input'))
                self.assertIsNotNone(artifact_registry_entity)
