import { AWS } from "@serverless/typescript";
import { readFileSync } from "fs";
import * as YAML from "yaml";
import * as path from "path";

const runwayVariables = YAML.parse(
  readFileSync(path.join(__dirname, "..", "variables.yml")).toString("utf-8")
);

export type ExtendedServerlessConfig = AWS & {
  functions: {
    [name: string]: {
      iamRoleStatementsName: string;
      iamRoleStatementsInherit: boolean;
      iamRoleStatements?: [
        {
          Effect: "Allow" | "Deny";
          Action: string[];
          Resource: string[];
          Condition?: Record<string, any>;
        }
      ];
    };
  };
  plugins?: string[];
};

type BaseServerlessConfig = Omit<
  ExtendedServerlessConfig,
  "service" | "functions"
>;

export const base: BaseServerlessConfig = {
  provider: {
    name: "aws",
    runtime: "python3.8",
    endpointType: "regional",
    apiName: "${self:custom.apiGatewayName}",
    deploymentBucket: {
      name:
        "${cf:static-artifact-registry-deployment-setup.ServerlessDeploymentBucketName}",
      serverSideEncryption: "AES256",
    },
    environment: {
      PYTHONPATH: "/var/task/src:/opt/python",
      ARTIFACTS_REGISTRY_TABLE: "${self:custom.registryTableName}",
      ARTIFACTS_REGISTRY_BUCKET: "${self:custom.registryBucketName}",
      EVENT_SOURCES: "${self:custom.eventSource}",
      LOGLEVEL: "${self:custom.loglevel}",
    },
    lambdaHashingVersion: "20201221",
    iamRoleStatements: [
      {
        Effect: "Allow",
        Action: [
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
        ],
        Resource: ["${self:custom.registryTableArn}"],
      },
    ],
  },
  custom: {
    pythonRequirements: {
      layer: true,
    },
    lambdaDefaults: {
      kms: {
        kmsKeyArn: "${self:custom.kmsKeyArn}",
      },
    },
    ssmPublish: {
      enabled: true,
      params: [
        {
          path: "${self:custom.ssmNamespace}/${self:service}/api_gateway",
          value: "${self:custom.apiGatewayName}",
          secure: false,
        },
      ],
    },
    kmsKeyArn: "${cf:EC-KmsKey.KmsKeyArn}",
    variables: `\${file(${__dirname}/../variables.yml)}`,
    ssmNamespace: "${self:custom.variables.ssm_namespace}/${opt:stage}",
    apiGatewayName: "${self:service}-api-${opt:stage}",
    registryTableName: "${ssm:${self:custom.ssmNamespace}/registry_table/name}",
    registryTableArn: "${ssm:${self:custom.ssmNamespace}/registry_table/arn}",
    registryBucketName:
      "${ssm:${self:custom.ssmNamespace}/registry_bucket/name}",
    registryBucketArn: "${ssm:${self:custom.ssmNamespace}/registry_bucket/arn}",
    eventSource: JSON.stringify(runwayVariables.event_sources),
    loglevel: "${self:custom.variables.loglevel.${opt:stage},'DEBUG'}",
  },
  package: {
    exclude: ["**/*"],
    include: ["!.**", "src/**/*.py"],
  },
  plugins: [
    "serverless-python-requirements",
    "serverless-lambda-defaults-plugin",
    "serverless-ssm-publish",
    "serverless-iam-roles-per-function",
  ],
};
