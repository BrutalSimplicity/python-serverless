# EC New Account Artifact Registry

## Purpose

The EC New Account Artifact Registry is the central repository for Distributed Deployment Engine (DDE) Artifacts.  The Registry's main function is to provision new accounts with DDE Artifacts.

## How this is different from the DDE

The Distributed Deployment Engine (DDE) deploys artifacts as soon as they are uploaded via the api.  The EC New Account Artifact Registry does not deploy artifacts, it just facilitates deploying artifacts via the DDE.

Additionally, the EC New Account Artifact Registry is capable of generatin a deployment plan for a new Account, based on the type of Account being created.

## Deployment Plan

!!!see
    [Generate Deployment Plan](api.md#generatedeploymentplan)

A Deployment Plan is a 'roadmap' for deploying artifacts in a new Account.  The Deployment Plan lists the Artifacts that should be deployed, based on environment criteria.

## New Account Artifact Deployment

When a new AWS Account is created, a CloudWatch Event is sent that triggers this process.  The Deployer will generate a deployment plan, and then use that deployment plan to begin deploying artifacts to the new account.
