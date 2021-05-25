import { base, ExtendedServerlessConfig } from "./resources/serverless";

const serverlessConfig: ExtendedServerlessConfig = {
  service: "ec-artifact-registry-service",
  unresolvedVariablesNotificationMode: "error",
  provider: {
    ...base.provider,
  },
  custom: {
    ...base.custom,
  },
  plugins: [...base.plugins],
  package: {
    ...base.package,
  },
  functions: {
    artifactS3Trigger: {
      iamRoleStatementsName: "ArtifactRegistryS3TriggerRole-${opt:stage}",
      iamRoleStatementsInherit: true,
      tracing: "Active",
      name: "artifact-registry-s3-trigger-${opt:stage}",
      handler: "src/s3_trigger/entrypoint.lambda_handler",
      layers: [
        {
          Ref: "PythonRequirementsLambdaLayer",
        },
      ],
      events: [
        {
          s3: {
            bucket: "${self:custom.registryBucketName}",
            event: "s3:ObjectCreated:*",
            existing: true,
          },
        },
      ],
    },
    artifactRegistryApi: {
      iamRoleStatementsInherit: true,
      iamRoleStatementsName: "ArtifactRegistryS3ApiRole-${opt:stage}",
      iamRoleStatements: [
        {
          Effect: "Allow",
          Action: ["s3:PutObject"],
          Resource: [
            "${self:custom.registryBucketArn}",
            "${self:custom.registryBucketArn}/*",
          ],
        },
      ],
      tracing: "Active",
      name: "artifact-registry-api-${opt:stage}",
      handler: "src/api/entrypoint.lambda_handler",
      layers: [
        {
          Ref: "PythonRequirementsLambdaLayer",
        },
      ],
      events: [
        {
          http: {
            path: "{artifact_key}",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  key: true,
                },
                querystrings: {
                  version: false,
                },
              },
            },
          },
        },
        {
          http: {
            path: "",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
          },
        },
        {
          http: {
            path: "upload/status/{etag}",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                paths: {
                  etag: true,
                },
              },
            },
          },
        },
        {
          http: {
            path: "upload",
            method: "get",
            authorizer: {
              type: "aws_iam",
            },
            request: {
              parameters: {
                querystrings: {
                  s3_key: true,
                },
              },
            },
          },
        },
      ],
    },
  },
};

// @ts-ignore: node-style export
module.exports = serverlessConfig;
