---
title: ECArtifactRegistry-${terraform_workspace} v0.0.1
language_tabs:
  - go: Go
  - javascript: JavaScript
  - python: Python
toc_footers: []
includes: []
search: true
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="ecartifactregistry-terraform_workspace-">ECArtifactRegistry-${terraform_workspace} v0.0.1</h1>

# Authentication

* API Key (sigv4)
    - Parameter Name: **Authorization**, in: header. [Signature Version 4](https://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html) is the process to add authentication information to AWS requests sent by HTTP.

<h1 id="ecartifactregistry-terraform_workspace--default">Default</h1>

## get__

`GET /`

endpoint for ALB health checks

> Example responses

> 200 Response

```json
"string"
```

<h3 id="get__-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|None|

<aside class="success">
This operation does not require authentication
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://registry.ec.swacorp.com/", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://registry.ec.swacorp.com/',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('https://registry.ec.swacorp.com/', headers = headers)

print(r.json())

```

## options__

`OPTIONS /`

> Example responses

> 200 Response

```json
{}
```

<h3 id="options__-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|200 response|[Empty](#schemaempty)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|200 response|[Empty](#schemaempty)|

<aside class="success">
This operation does not require authentication
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("OPTIONS", "https://registry.ec.swacorp.com/", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json'
};

fetch('https://registry.ec.swacorp.com/',
{
  method: 'OPTIONS',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.options('https://registry.ec.swacorp.com/', headers = headers)

print(r.json())

```

## ListArtifacts

<a id="opIdListArtifacts"></a>

`GET /registry/artifacts`

Retrieves a list of Artifacts from the Registry

<h3 id="listartifacts-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|deployment_selector|query|[DeploymentSelector](#schemadeploymentselector)|false|none|
|owner_account_id|query|[OwnerAccountId](#schemaowneraccountid)|false|none|

#### Enumerated Values

|Parameter|Value|
|---|---|
|deployment_selector|dev|
|deployment_selector|qa|
|deployment_selector|prod|

> Example responses

> 200 Response

```json
{
  "artifacts": [
    {
      "stack_name": "Stack-Name",
      "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector",
      "manifest_template": "string",
      "dependent_artifacts": [
        "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
      ],
      "deployment_selector": "dev"
    }
  ]
}
```

<h3 id="listartifacts-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|200 Successful|[ListArtifactsResponse](#schemalistartifactsresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
sigv4
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
        "Authorization": []string{"API_KEY"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://registry.ec.swacorp.com/registry/artifacts", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json',
  'Authorization':'API_KEY'
};

fetch('https://registry.ec.swacorp.com/registry/artifacts',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'API_KEY'
}

r = requests.get('https://registry.ec.swacorp.com/registry/artifacts', headers = headers)

print(r.json())

```

## DescribeArtifact

<a id="opIdDescribeArtifact"></a>

`GET /registry/artifact`

Retrieves an Artifact from the Registry

<h3 id="describeartifact-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|arn|query|[Arn](#schemaarn)|true|Arn for the Registry Artifact|

> Example responses

> 200 Response

```json
{
  "stack_name": "Stack-Name",
  "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector",
  "manifest_template": "string",
  "dependent_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "deployment_selector": "dev"
}
```

<h3 id="describeartifact-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|200 Successful|[RegistryArtifact](#schemaregistryartifact)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
sigv4
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
        "Authorization": []string{"API_KEY"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://registry.ec.swacorp.com/registry/artifact", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json',
  'Authorization':'API_KEY'
};

fetch('https://registry.ec.swacorp.com/registry/artifact?arn=arn%3Aaws%3Aec-artifact-registry%3Aus-east-1%3A1234567890%3Aartifact%2FStackName%2FDeploymentSelector',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'API_KEY'
}

r = requests.get('https://registry.ec.swacorp.com/registry/artifact', params={
  'arn': 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector'
}, headers = headers)

print(r.json())

```

## DeleteArtifact

<a id="opIdDeleteArtifact"></a>

`DELETE /registry/artifact`

Deletes an Artifact from the Artifact Registry

<h3 id="deleteartifact-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|arn|query|[Arn](#schemaarn)|true|Arn for the Registry Artifact|

> Example responses

> 202 Response

```json
"string"
```

<h3 id="deleteartifact-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|202|[Accepted](https://tools.ietf.org/html/rfc7231#section-6.3.3)|202 Accepted|[DeleteRegsitryArtifactResponse](#schemadeleteregsitryartifactresponse)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
sigv4
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
        "Authorization": []string{"API_KEY"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("DELETE", "https://registry.ec.swacorp.com/registry/artifact", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json',
  'Authorization':'API_KEY'
};

fetch('https://registry.ec.swacorp.com/registry/artifact?arn=arn%3Aaws%3Aec-artifact-registry%3Aus-east-1%3A1234567890%3Aartifact%2FStackName%2FDeploymentSelector',
{
  method: 'DELETE',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'API_KEY'
}

r = requests.delete('https://registry.ec.swacorp.com/registry/artifact', params={
  'arn': 'arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector'
}, headers = headers)

print(r.json())

```

## GetDeploymentArtifact

<a id="opIdGetDeploymentArtifact"></a>

`GET /registry/artifact/deployment/{artifact_arn}`

Retrieves the Artifact binary from the Artifact Registry Bucket

<h3 id="getdeploymentartifact-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|artifact_arn|path|[Arn](#schemaarn)|true|Arn for the Registry Artifact|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="getdeploymentartifact-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|200 Successful|[ArtifactBinary](#schemaartifactbinary)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
sigv4
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
        "Authorization": []string{"API_KEY"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://registry.ec.swacorp.com/registry/artifact/deployment/{artifact_arn}", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json',
  'Authorization':'API_KEY'
};

fetch('https://registry.ec.swacorp.com/registry/artifact/deployment/{artifact_arn}',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'API_KEY'
}

r = requests.get('https://registry.ec.swacorp.com/registry/artifact/deployment/{artifact_arn}', headers = headers)

print(r.json())

```

## GeneratePresignedURL

<a id="opIdGeneratePresignedURL"></a>

`POST /registry/artifact/presigned_url`

Creates a URL that is used to store the DDE Artifact for new Accounts.

> Body parameter

```json
{
  "stack_name": "Stack-Name",
  "artifact_key": "/some/artifact.zip",
  "owner_account_id": 1234567890,
  "deployment_selector": "dev",
  "aws_region": "us-east-1",
  "dependent_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ]
}
```

<h3 id="generatepresignedurl-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[GeneratePresignedURLRequest](#schemageneratepresignedurlrequest)|false|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="generatepresignedurl-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|[#/components/responses/400](#schema#/components/responses/400)|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Unauthorized request for the resource|[#/components/responses/401](#schema#/components/responses/401)|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|[#/components/responses/403](#schema#/components/responses/403)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|[#/components/responses/404](#schema#/components/responses/404)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
sigv4
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Content-Type": []string{"application/json"},
        "Accept": []string{"application/json"},
        "Authorization": []string{"API_KEY"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("POST", "https://registry.ec.swacorp.com/registry/artifact/presigned_url", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript
const inputBody = '{
  "stack_name": "Stack-Name",
  "artifact_key": "/some/artifact.zip",
  "owner_account_id": 1234567890,
  "deployment_selector": "dev",
  "aws_region": "us-east-1",
  "dependent_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ]
}';
const headers = {
  'Content-Type':'application/json',
  'Accept':'application/json',
  'Authorization':'API_KEY'
};

fetch('https://registry.ec.swacorp.com/registry/artifact/presigned_url',
{
  method: 'POST',
  body: inputBody,
  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'API_KEY'
}

r = requests.post('https://registry.ec.swacorp.com/registry/artifact/presigned_url', headers = headers)

print(r.json())

```

## GenerateDeploymentPlan

<a id="opIdGenerateDeploymentPlan"></a>

`GET /registry/deployment_plan`

Generates a Deployment Plan for a specific Deployment Selector

<h3 id="generatedeploymentplan-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|deployment_selector|query|[DeploymentSelector](#schemadeploymentselector)|true|none|

#### Enumerated Values

|Parameter|Value|
|---|---|
|deployment_selector|dev|
|deployment_selector|qa|
|deployment_selector|prod|

> Example responses

> 200 Response

```json
{
  "root_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "stem_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "leaf_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ]
}
```

<h3 id="generatedeploymentplan-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|200 Successful|[DeploymentPlan](#schemadeploymentplan)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|Invalid Request|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Forbidden|None|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not Found|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|Internal Server Error|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
sigv4
</aside>

> Code samples

```go
package main

import (
       "bytes"
       "net/http"
)

func main() {

    headers := map[string][]string{
        "Accept": []string{"application/json"},
        "Authorization": []string{"API_KEY"},
    }

    data := bytes.NewBuffer([]byte{jsonReq})
    req, err := http.NewRequest("GET", "https://registry.ec.swacorp.com/registry/deployment_plan", data)
    req.Header = headers

    client := &http.Client{}
    resp, err := client.Do(req)
    // ...
}

```

```javascript

const headers = {
  'Accept':'application/json',
  'Authorization':'API_KEY'
};

fetch('https://registry.ec.swacorp.com/registry/deployment_plan?deployment_selector=dev',
{
  method: 'GET',

  headers: headers
})
.then(function(res) {
    return res.json();
}).then(function(body) {
    console.log(body);
});

```

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'API_KEY'
}

r = requests.get('https://registry.ec.swacorp.com/registry/deployment_plan', params={
  'deployment_selector': 'dev'
}, headers = headers)

print(r.json())

```

# Schemas

<h2 id="tocS_Arn">Arn</h2>
<!-- backwards compatibility -->
<a id="schemaarn"></a>
<a id="schema_Arn"></a>
<a id="tocSarn"></a>
<a id="tocsarn"></a>

<!-- Arn

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Arn|string|false|none|none

```json
"arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"

```

<h2 id="tocS_ArtifactKey">ArtifactKey</h2>
<!-- backwards compatibility -->
<a id="schemaartifactkey"></a>
<a id="schema_ArtifactKey"></a>
<a id="tocSartifactkey"></a>
<a id="tocsartifactkey"></a>

<!-- ArtifactKey

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ArtifactKey|string|false|none|S3 Key for the Artifact

```json
"/some/artifact.zip"

```

<h2 id="tocS_ArtifactBinary">ArtifactBinary</h2>
<!-- backwards compatibility -->
<a id="schemaartifactbinary"></a>
<a id="schema_ArtifactBinary"></a>
<a id="tocSartifactbinary"></a>
<a id="tocsartifactbinary"></a>

<!-- ArtifactBinary

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ArtifactBinary|string(binary)|false|none|none

```json
"string"

```

<h2 id="tocS_ManifestTemplate">ManifestTemplate</h2>
<!-- backwards compatibility -->
<a id="schemamanifesttemplate"></a>
<a id="schema_ManifestTemplate"></a>
<a id="tocSmanifesttemplate"></a>
<a id="tocsmanifesttemplate"></a>

<!-- ManifestTemplate

 -->

<a href="https://docs.dde.ec.prod.aws.swacorp.com/user_guide/manifest.html">Distributed Deployment Engine (DDE) Documentation</a>

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|ManifestTemplate|string|false|none|Distributed Deployment Engine (DDE) Manifest

```json
"string"

```

<h2 id="tocS_Limit">Limit</h2>
<!-- backwards compatibility -->
<a id="schemalimit"></a>
<a id="schema_Limit"></a>
<a id="tocSlimit"></a>
<a id="tocslimit"></a>

<!-- Query Limit

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Query Limit|integer|false|none|query response size limit

```json
10

```

<h2 id="tocS_Ascending">Ascending</h2>
<!-- backwards compatibility -->
<a id="schemaascending"></a>
<a id="schema_Ascending"></a>
<a id="tocSascending"></a>
<a id="tocsascending"></a>

<!-- Ascending

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Ascending|boolean|false|none|apply ascending order to responses

```json
true

```

<h2 id="tocS_LastEvaluatedKey">LastEvaluatedKey</h2>
<!-- backwards compatibility -->
<a id="schemalastevaluatedkey"></a>
<a id="schema_LastEvaluatedKey"></a>
<a id="tocSlastevaluatedkey"></a>
<a id="tocslastevaluatedkey"></a>

<!-- LastEvaluatedKey

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|LastEvaluatedKey|string|false|none|Key from previous query.  Identifies where to begin the next query results.

```json
"string"

```

<h2 id="tocS_DeleteRegsitryArtifactResponse">DeleteRegsitryArtifactResponse</h2>
<!-- backwards compatibility -->
<a id="schemadeleteregsitryartifactresponse"></a>
<a id="schema_DeleteRegsitryArtifactResponse"></a>
<a id="tocSdeleteregsitryartifactresponse"></a>
<a id="tocsdeleteregsitryartifactresponse"></a>

<!-- DeleteArtifact

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|DeleteArtifact|string|false|none|none

```json
"string"

```

<h2 id="tocS_DependentArtifacts">DependentArtifacts</h2>
<!-- backwards compatibility -->
<a id="schemadependentartifacts"></a>
<a id="schema_DependentArtifacts"></a>
<a id="tocSdependentartifacts"></a>
<a id="tocsdependentartifacts"></a>

<!-- DependentArtifacts

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|DependentArtifacts|[[Arn](#schemaarn)]|false|none|Arn for Artifact(s) that must be deployed before this Artifact can be deployed.

```json
[
  "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
]

```

<h2 id="tocS_DeploymentSelector">DeploymentSelector</h2>
<!-- backwards compatibility -->
<a id="schemadeploymentselector"></a>
<a id="schema_DeploymentSelector"></a>
<a id="tocSdeploymentselector"></a>
<a id="tocsdeploymentselector"></a>

<!-- DeploymentSelector

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|DeploymentSelector|string|false|none|Defines the type of account this artifact will be deployed to when created.

```json
"dev"

```

#### Enumerated Values

|Property|Value|
|---|---|
|DeploymentSelector|dev|
|DeploymentSelector|qa|
|DeploymentSelector|prod|

<h2 id="tocS_Empty">Empty</h2>
<!-- backwards compatibility -->
<a id="schemaempty"></a>
<a id="schema_Empty"></a>
<a id="tocSempty"></a>
<a id="tocsempty"></a>

<!-- Empty

 -->

*None*

```json
{}

```

<h2 id="tocS_OwnerAccountId">OwnerAccountId</h2>
<!-- backwards compatibility -->
<a id="schemaowneraccountid"></a>
<a id="schema_OwnerAccountId"></a>
<a id="tocSowneraccountid"></a>
<a id="tocsowneraccountid"></a>

<!-- OwnerAccountId

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|OwnerAccountId|string|false|none|AWS Account ID for the Account that 'owns' the Artifact.

```json
1234567890

```

<h2 id="tocS_StackName">StackName</h2>
<!-- backwards compatibility -->
<a id="schemastackname"></a>
<a id="schema_StackName"></a>
<a id="tocSstackname"></a>
<a id="tocsstackname"></a>

<!-- StackName

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|StackName|string|false|none|CloudFormation Stack Name contained within the Artifact

```json
"Stack-Name"

```

<h2 id="tocS_Region">Region</h2>
<!-- backwards compatibility -->
<a id="schemaregion"></a>
<a id="schema_Region"></a>
<a id="tocSregion"></a>
<a id="tocsregion"></a>

<!-- AWS Region

 -->

<a href="https://aws.amazon.com/about-aws/global-infrastructure/regions_az/">Regions and Availability Zones</a>

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|AWS Region|string|false|none|AWS Region

```json
"us-east-1"

```

#### Enumerated Values

|Property|Value|
|---|---|
|AWS Region|us-east-1|
|AWS Region|us-west-2|

<h2 id="tocS_RegistryArtifact">RegistryArtifact</h2>
<!-- backwards compatibility -->
<a id="schemaregistryartifact"></a>
<a id="schema_RegistryArtifact"></a>
<a id="tocSregistryartifact"></a>
<a id="tocsregistryartifact"></a>

<!-- RegistryArtifact

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|stack_name|[StackName](#schemastackname)|false|none|CloudFormation Stack Name contained within the Artifact
|arn|[Arn](#schemaarn)|false|none|none
|manifest_template|[ManifestTemplate](#schemamanifesttemplate)|false|none|Distributed Deployment Engine (DDE) Manifest
|dependent_artifacts|[DependentArtifacts](#schemadependentartifacts)|false|none|Arn for Artifact(s) that must be deployed before this Artifact can be deployed.
|deployment_selector|[DeploymentSelector](#schemadeploymentselector)|false|none|Defines the type of account this artifact will be deployed to when created.

```json
{
  "stack_name": "Stack-Name",
  "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector",
  "manifest_template": "string",
  "dependent_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "deployment_selector": "dev"
}

```

<h2 id="tocS_ListArtifactsResponse">ListArtifactsResponse</h2>
<!-- backwards compatibility -->
<a id="schemalistartifactsresponse"></a>
<a id="schema_ListArtifactsResponse"></a>
<a id="tocSlistartifactsresponse"></a>
<a id="tocslistartifactsresponse"></a>

<!-- ListArtifactsResponse

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|artifacts|[[RegistryArtifact](#schemaregistryartifact)]|false|none|none

```json
{
  "artifacts": [
    {
      "stack_name": "Stack-Name",
      "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector",
      "manifest_template": "string",
      "dependent_artifacts": [
        "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
      ],
      "deployment_selector": "dev"
    }
  ]
}

```

<h2 id="tocS_DescribeArtifactResponse">DescribeArtifactResponse</h2>
<!-- backwards compatibility -->
<a id="schemadescribeartifactresponse"></a>
<a id="schema_DescribeArtifactResponse"></a>
<a id="tocSdescribeartifactresponse"></a>
<a id="tocsdescribeartifactresponse"></a>

<!-- DescribeArtifactResponse

 -->

*None*

```json
{
  "stack_name": "Stack-Name",
  "arn": "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector",
  "manifest_template": "string",
  "dependent_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "deployment_selector": "dev"
}

```

<h2 id="tocS_GeneratePresignedURLRequest">GeneratePresignedURLRequest</h2>
<!-- backwards compatibility -->
<a id="schemageneratepresignedurlrequest"></a>
<a id="schema_GeneratePresignedURLRequest"></a>
<a id="tocSgeneratepresignedurlrequest"></a>
<a id="tocsgeneratepresignedurlrequest"></a>

<!-- GeneratePresignedURLRequest

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|stack_name|[StackName](#schemastackname)|true|none|CloudFormation Stack Name contained within the Artifact
|artifact_key|[ArtifactKey](#schemaartifactkey)|true|none|S3 Key for the Artifact
|owner_account_id|[OwnerAccountId](#schemaowneraccountid)|true|none|AWS Account ID for the Account that 'owns' the Artifact.
|deployment_selector|[DeploymentSelector](#schemadeploymentselector)|true|none|Defines the type of account this artifact will be deployed to when created.
|aws_region|[Region](#schemaregion)|true|none|AWS Region
|dependent_artifacts|[DependentArtifacts](#schemadependentartifacts)|false|none|Arn for Artifact(s) that must be deployed before this Artifact can be deployed.

```json
{
  "stack_name": "Stack-Name",
  "artifact_key": "/some/artifact.zip",
  "owner_account_id": 1234567890,
  "deployment_selector": "dev",
  "aws_region": "us-east-1",
  "dependent_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ]
}

```

<h2 id="tocS_GetDeploymentArtifactResponse">GetDeploymentArtifactResponse</h2>
<!-- backwards compatibility -->
<a id="schemagetdeploymentartifactresponse"></a>
<a id="schema_GetDeploymentArtifactResponse"></a>
<a id="tocSgetdeploymentartifactresponse"></a>
<a id="tocsgetdeploymentartifactresponse"></a>

<!-- GetDeploymentArtifactResponse

 -->

*None*

```json
"string"

```

<h2 id="tocS_DeploymentPlan">DeploymentPlan</h2>
<!-- backwards compatibility -->
<a id="schemadeploymentplan"></a>
<a id="schema_DeploymentPlan"></a>
<a id="tocSdeploymentplan"></a>
<a id="tocsdeploymentplan"></a>

<!-- Deployment Plan

 -->

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|root_artifacts|[[Arn](#schemaarn)]|false|none|Artifacts that are depended upon, but have no dependencies
|stem_artifacts|[[Arn](#schemaarn)]|false|none|Artifacts that are depended upon, and depend on other artifacts
|leaf_artifacts|[[Arn](#schemaarn)]|false|none|Artifacts that are not depended upon, but depend on other artifacts

```json
{
  "root_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "stem_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ],
  "leaf_artifacts": [
    "arn:aws:ec-artifact-registry:us-east-1:1234567890:artifact/StackName/DeploymentSelector"
  ]
}

```

