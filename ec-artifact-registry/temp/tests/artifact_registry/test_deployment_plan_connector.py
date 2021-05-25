import json
import os
import random
import unittest

from shared.artifact_registry.deployment_plan_connector import DeploymentPlanBuilder
from shared.artifact_registry.models import DeploymentPlan

class DeploymentPlanConnectorTest(unittest.TestCase):

    def test_get_artifact_arns(self):
        ''' test_get_artifact_arns '''
        testcases = [
            {
                'name': 'case 1',
                'input': 'items.1.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'case 2',
                'input': 'items.2.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'case 3',
                'input': 'items.3.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                ],
                'skip': False,
                'shouldFail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
                builder = DeploymentPlanBuilder(items)
                artifact_arns = builder.get_artifact_arns()
                self.assertIsNotNone(artifact_arns)
                self.assertEqual(artifact_arns, case.get('expected'))

    def test_build_dependent_artifacts_list(self):
        ''' test_build_dependent_artifacts_list '''

        testcases = [
            {
                'name': 'no_dependencies',
                'input': 'items.1.json',
                'expected': [],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'single_dependency',
                'input': 'items.2.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'multiple_dependencies_single_dependent',
                'input': 'items.3.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'multiple_dependencies_multiple_dependencies',
                'input': 'items.4.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'multiple_dependencies_multiple_dependencies_2',
                'input': 'items.5.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'multiple_dependencies_multiple_dependencies_3',
                'input': 'items.6.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev"
                ],
                'skip': False,
                'shouldFail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
                builder = DeploymentPlanBuilder(items)
                dependent_artifacts_list = builder.build_dependent_artifacts_list()
                self.assertIsNotNone(dependent_artifacts_list)
                self.assertEqual(dependent_artifacts_list, case.get('expected'))


    def test_find_root_artifacts(self):
        ''' test_find_root_artifacts '''

        testcases = [
            {
                'name': 'root artifacts - 1',
                'input': 'items.1.json',
                'expected': [],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'root artifacts - 2',
                'input': 'items.2.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'root artifacts - 3',
                'input': 'items.3.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'root artifacts - 4',
                'input': 'items.4.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'root artifacts - 5',
                'input': 'items.5.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'two root nodes',
                'input': 'items.7.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'chain',
                'input': 'items.8.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
                builder = DeploymentPlanBuilder(items)
                dependent_artifacts_list = builder.build_dependent_artifacts_list()
                self.assertIsNotNone(dependent_artifacts_list)
                root_artifacts = builder.find_root_artifacts(dependent_artifacts_list)
                self.assertIsNotNone(root_artifacts)
                self.assertEqual(root_artifacts, case.get('expected'))

    def test_find_stem_artifacts(self):
        ''' test_find_stem_artifacts '''

        testcases = [
            {
                'name': 'stem artifacts - 1',
                'input': 'items.1.json',
                'expected': [],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 2',
                'input': 'items.2.json',
                'expected': [],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 3',
                'input': 'items.3.json',
                'expected': [],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 4',
                'input': 'items.4.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 7',
                'input': 'items.7.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'chain',
                'input': 'items.8.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                ],
                'skip': False,
                'shouldFail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
                builder = DeploymentPlanBuilder(items)
                dependent_artifacts_list = builder.build_dependent_artifacts_list()
                self.assertIsNotNone(dependent_artifacts_list)
                stem_artifacts = builder.find_stem_artifacts(dependent_artifacts_list)
                self.assertIsNotNone(stem_artifacts)
                self.assertEqual(stem_artifacts, case.get('expected'))


    def test_find_leaf_artifacts(self):
        ''' test_find_leaf_artifacts '''

        testcases = [
            {
                'name': 'stem artifacts - 1',
                'input': 'items.1.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 2',
                'input': 'items.2.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 3',
                'input': 'items.3.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 4',
                'input': 'items.4.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 7',
                'input': 'items.7.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev",
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-5/dev"
                ],
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 8',
                'input': 'items.8.json',
                'expected': [
                    "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev"
                ],
                'skip': False,
                'shouldFail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
                builder = DeploymentPlanBuilder(items)
                dependent_artifacts_list = builder.build_dependent_artifacts_list()
                self.assertIsNotNone(dependent_artifacts_list)
                leaf_artifacts = builder.find_leaf_artifacts(dependent_artifacts_list)
                self.assertIsNotNone(leaf_artifacts)
                self.assertEqual(leaf_artifacts, case.get('expected'))


    def test_build_plan(self):
        ''' test_build_plan '''

        testcases = [
            {
                'name': 'stem artifacts - 1',
                'input': 'items.1.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [],
                    'stem_artifacts': [],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 2',
                'input': 'items.2.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ],
                    'stem_artifacts': [],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 3',
                'input': 'items.3.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ],
                    'stem_artifacts': [],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 4',
                'input': 'items.4.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ],
                    'stem_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                    ],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 5',
                'input': 'items.5.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ],
                    'stem_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                    ],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-5/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 6',
                'input': 'items.6.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ],
                    'stem_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                    ],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-5/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 7',
                'input': 'items.7.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                    ],
                    'stem_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                    ],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-5/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - 8',
                'input': 'items.8.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test/dev"
                    ],
                    'stem_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-2/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-3/dev"
                    ],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-4/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            },
            {
                'name': 'stem artifacts - chain - 1',
                'input': 'items.chain.1.json',
                'expected': DeploymentPlan(**{
                    'root_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-A/dev"
                    ],
                    'stem_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-B/dev",
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-D/dev"
                    ],
                    'leaf_artifacts': [
                        "arn:aws:ec-artifact-registry:us-east-1:775698200277:artifact/Landing-Zone-Test-C/dev"
                    ]
                }),
                'skip': False,
                'shouldFail': False
            }
        ]

        for case in testcases:
            with self.subTest(case.get('name')):
                items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
                builder = DeploymentPlanBuilder(items)
                deployment_plan = builder.build_plan()
                self.assertIsNotNone(deployment_plan)
                self.assertEqual(deployment_plan, case.get('expected'))

        # for case in testcases:
        #     with self.subTest(f'{case.get("name")}-shuffled'):
        #         # shuffle the items, then see if we get the same results
        #         items = json.load(open(f'{os.getcwd()}/tests/artifact_registry/testdata/{case.get("input")}'))
        #         random.shuffle(items)
        #         builder = DeploymentPlanBuilder(items)
        #         deployment_plan = builder.build_plan()
        #         self.assertIsNotNone(deployment_plan)
        #         self.assertEqual(deployment_plan, case.get('expected'))
