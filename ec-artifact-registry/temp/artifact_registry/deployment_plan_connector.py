
from pydash.arrays import uniq
from pydash.collections import find
from boto3.dynamodb.conditions import Key
from shared.connector import Connector
from shared.artifact_registry.models import (
    GenerateDeploymentPlanRequest,
    DeploymentPlan
)

class DeploymentPlanConnector(Connector):

    def __init__(self, dynamodb, table_name):
        super().__init__(dynamodb, table_name)

    def generate_deployment_plan(self, request: GenerateDeploymentPlanRequest) -> DeploymentPlan:  # noqa E501
        keyCondition = Key('DeploymentSelector').eq(request.deployment_selector)
        entities = self._make_scan(keyCondition)
        deployment_plan = DeploymentPlanBuilder(entities).build_plan()
        return deployment_plan

class DeploymentPlanBuilder(object):

    def __init__(self, items):
        self._items = items

    def get_artifact_arns(self) -> list:
        return uniq([
            item.get('Arn') for item in self._items
        ])

    def build_dependent_artifacts_list(self) -> list:
        '''
            Builds a unique list of the artifact's that are dependencies

            An artifact is dependent if another artifact in self._items has its arn specified
            in  some artifact in the list of items has the artifact
                as a dependency in it's DependentArtifacts list)

            Any artifact in this list that does not have another artifact
                specified in its DependentArtifact list is a 'root' dependency

        '''
        return uniq([
            artifact
            for item in self._items
            for artifact in item.get('DependentArtifacts', []) if artifact
        ])

    def find_root_artifacts(self, dependent_artifacts_list: list) -> list:
        ''' find the artifacts that are depended upon, but do not have dependencies '''
        return [
            item.get('Arn')
            for item in self._items
            if item.get('DependentArtifacts') is None and item.get('Arn') in dependent_artifacts_list
        ]

    def find_stem_artifacts(self, dependent_artifacts_list: list) -> list:
        ''' find the artifacts that are depended upon, and also are dependent upon other artifacts '''
        # need to check if any stem artifacts depend on another stem artifact
        #  if so, then they need to be ordered

        # stem_artifacts = [
        #     (item.get('Arn'), item.get('DependentArtifacts'))
        #     for item in self._items
        #     if item.get('DependentArtifacts') is not None and item.get('Arn') in dependent_artifacts_list
        # ]

        # return stem_artifacts

        return [
            item.get('Arn')
            for item in self._items
            if item.get('DependentArtifacts') is not None and item.get('Arn') in dependent_artifacts_list
        ]

    def sort_stem_artifacts(self, stem_artifacts: list) -> list:
        '''
            sort_stem_artifacts

            1. iterate over stem artifacts

            for each artifact:
            2. find corresponding artifact in _items
            3. determine if the artifact has a dependency that is another stem depnendency
            4. if dependency exists, set order

        '''

        for artifact in stem_artifacts:
            item = find(self._items, lambda x: x.get('Arn') == artifact)
            if item is not None:
                print(f'>>>> item: {item}')
        return stem_artifacts

    def find_leaf_artifacts(self, dependent_artifacts_list: list) -> list:
        ''' find the artifacts that are not depended upon '''
        return [
            item.get('Arn')
            for item in self._items
            if item.get('Arn') not in dependent_artifacts_list
        ]

    def build_plan(self) -> DeploymentPlan:
        '''
            root_artifacts:
                - Do not depend on another artifact
                - Other artifacts depend on it
            stem_artifacts:
                - Depends on other artifacts
                - Other artifacts depend on it
            leaf_artifacts:
                - Depends on other artifacts
                - Other artifacts do not depend on it
        '''
        dependent_artifacts_list = self.build_dependent_artifacts_list()
        root_artifacts = self.find_root_artifacts(dependent_artifacts_list)
        stem_artifacts = self.find_stem_artifacts(dependent_artifacts_list)
        stem_artifacts = self.sort_stem_artifacts(stem_artifacts)
        leaf_artifacts = self.find_leaf_artifacts(dependent_artifacts_list)
        deployment_plan = DeploymentPlan(**{
            'root_artifacts': root_artifacts,
            'stem_artifacts': stem_artifacts,
            'leaf_artifacts': leaf_artifacts
        })
        return deployment_plan
