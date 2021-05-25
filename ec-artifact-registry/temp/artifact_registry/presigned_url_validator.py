'''
Need to Validate the following:

    - circular dependency: dependent_artifact does not refer to itself
    - circular dependency: dependent_artifact does not refer to an artifact
        that in turn dependens on this artifact
    - dependent artifacts exist
'''
import json
from shared.artifact_registry.models import PresignedURLRequest, PresignedURLRequestBody

class PresignedURLRequestValidator():
    ''' Methods to handle PresignedURLRequest Validation '''

    def __init__(self, request: PresignedURLRequest):
        ''' init '''
        self._request = request
        if isinstance(request.body, str):
            self._body = PresignedURLRequestBody(
                **json.loads(str(request.body))
            )
        else:
            self._body = PresignedURLRequestBody(**request.body)

    def is_self_dependent(self) -> bool:
        ''' does dependent_artifacts array include this artifact arn? '''

        # if no dependent artifacts specified, then it cant be self-dependent
        if self._body.dependent_artifacts is None:
            return False

        # if no dependent artifacts specified, then it cant be self-dependent
        if len(self._body.dependent_artifacts) == 0:
            return False

        # if this arn is in the dependent_artifacts arn array, we have a problem
        return self._request.build_arn() in self._body.dependent_artifacts

    def validate(self):
        ''' validate '''
        errors = []
        if self.is_self_dependent() is True:
            errors.append(
                f'PresignedURLRequest with ARN: {self._request.build_arn()}, includes its own ARN in the dependent_artifacts array, thereby creating a circular dependency with iteself.'  # noqa E501                
            )
        return errors
