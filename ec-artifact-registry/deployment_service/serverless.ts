import { base, ExtendedServerlessConfig } from "./resources/serverless";

const serverlessConfig: ExtendedServerlessConfig = {
  service: "ec-artifact-deployment-service",
  unresolvedVariablesNotificationMode: "error",
  provider: {
    ...base.provider,
    eventBridge: {
      useCloudFormation: true,
    },
  },
  custom: {
    ...base.custom,
  },
  plugins: [...base.plugins],
  package: {
    ...base.package,
  },
  functions: {
    artifactDeploymentContinuationTrigger: {
      tracing: "Active",
      name: "artifact-deployment-continuation-trigger-${opt:stage}",
      handler: "src/continuation_trigger/entrypoint.lambda_handler",
      layers: [
        {
          Ref: "PythonRequirementsLambdaLayer",
        },
      ],
      iamRoleStatementsInherit: true,
      iamRoleStatementsName:
        "ArtifactDeploymentContinuationTriggerRole-${opt:stage}",
      iamRoleStatements: [
        {
          Effect: "Allow",
          Action: [
            "states:GetTaskActivity",
            "states:SendTaskSuccess",
            "states:SendTaskHeartbeat",
            "states:SendTaskFailure",
          ],
          Resource: ["arn:aws:states:*:*:stateMachine:*"],
        },
      ],
    },
    artifactDeploymentStepTrigger: {
      tracing: "Active",
      name: "artifact-deployment-step-trigger-${opt:stage}",
      handler: "src/step_trigger/entrypoint.lambda_handler",
      layers: [
        {
          Ref: "PythonRequirementsLambdaLayer",
        },
      ],
      iamRoleStatementsInherit: true,
      iamRoleStatementsName: "ArtifactDeploymentStepTriggerRole-${opt:stage}",
      iamRoleStatements: [
        {
          Effect: "Allow",
          Action: [
            "states:GetTaskActivity",
            "states:SendTaskSuccess",
            "states:SendTaskHeartbeat",
            "states:SendTaskFailure",
          ],
          Resource: ["arn:aws:states:*:*:stateMachine:*"],
        },
      ],
    },
    artifactDeploymentEventTrigger: {
      tracing: "Active",
      name: "artifact-deployment-event-trigger-${opt:stage}",
      handler: "src/event_trigger/entrypoint.lambda_handler",
      layers: [
        {
          Ref: "PythonRequirementsLambdaLayer",
        },
      ],
      iamRoleStatementsInherit: true,
      iamRoleStatementsName: "ArtifactDeploymentEventTriggerRole-${opt:stage}",
      iamRoleStatements: [
        {
          Effect: "Allow",
          Action: [
            "states:CreateStateMachine",
            "states:StartExecution",
            "states:StopExecution",
            "states:DescribeStateMachine",
            "states:DeleteStateMachine",
            "states:ListExecutions",
            "states:UpdateStateMachine",
          ],
          Resource: ["arn:aws:states:*:*:stateMachine:*"],
        },
      ],
      events: [
        {
          eventBridge: {
            pattern: {
              source: ["${self:custom.variables.event_sources.status}"],
            },
          },
        },
      ],
    },
    artifactDeploymentApi: {
      tracing: "Active",
      name: "artifact-deployment-api-${opt:stage}",
      handler: "src/api/entrypoint.lambda_handler",
      layers: [
        {
          Ref: "PythonRequirementsLambdaLayer",
        },
      ],
      iamRoleStatementsInherit: true,
      iamRoleStatementsName: "ArtifactDeployomentServiceRole-${opt:stage}",
      iamRoleStatements: [
        {
          Effect: "Allow",
          Action: [
            "states:CreateStateMachine",
            "states:StartExecution",
            "states:StopExecution",
            "states:DescribeStateMachine",
            "states:DeleteStateMachine",
            "states:ListExecutions",
            "states:UpdateStateMachine",
          ],
          Resource: ["arn:aws:states:*:*:stateMachine:StateMachinePrefix*"],
        },
      ],
      events: [
        {
          http: {
            path: "plans/{selector}",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  selector: true,
                },
              },
            },
          },
        },
        {
          http: {
            path: "plans/{selector}/status/{etag}",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  selector: true,
                  id: true,
                },
              },
            },
          },
        },
        {
          http: {
            path: "plans",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                querystrings: {
                  selectors: false,
                },
              },
            },
          },
        },
        {
          http: {
            path: "plans",
            method: "post",
            authorizer: {
              type: "aws_iam",
            },
          },
        },
        {
          http: {
            path: "plans/{selector}/artifact/{artifact_key}",
            method: "post",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  selector: true,
                  artifact: true,
                },
              },
            },
          },
        },
        {
          http: {
            path: "plans/{selector}/artifact/{artifact_key}",
            method: "delete",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  selector: true,
                  artifact: true,
                },
              },
            },
          },
        },
        {
          http: {
            path: "plans/_trigger",
            method: "post",
            authorizer: {
              type: "aws_iam",
            },
          },
        },
        {
          http: {
            path: "status/{id}",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  id: true,
                },
              },
            },
          },
        },
        {
          http: {
            path: "deployments",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                querystrings: {
                  selector: false,
                },
              },
            },
          },
        },
      ],
    },
  },
};

module.exports = serverlessConfig;
