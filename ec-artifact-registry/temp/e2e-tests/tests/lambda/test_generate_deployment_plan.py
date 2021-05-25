
import json
from . import BaseLambdaTestCase


class GenerateDeploymentPlanTest(BaseLambdaTestCase):

    def test_should_successfully_generate_a_plan(self):
        ''' test_should_successfully_generate_a_plan '''

        deployment_selector = "dev"
        _data = json.dumps({
            "resource": "/registry/deployment_plan",
            "path": "/registry/deployment_plan",
            "queryStringParameters": {
                "deployment_selector": deployment_selector
            },
            "httpMethod": "GET",
            "isBase64Encoded": False
        })

        response = self._call(_data, self._generate_deployment_plan_function_name)
        _payload = response['Payload']
        payload = json.loads(_payload.read().decode('utf8'))
        # did we get a successful status code?
        self.assertEqual(payload.get('statusCode'), 200)
