# Logging


## Intro

You can use the logging module in this library to make your logging clean, simple, and effective. It attempts to make structured logging the default logging for all of your cloud requirements, but takes a small shift in thinking about how you approach logging to make it most effective.

## Rationale

In many cases, as developers, we tend to stick logging in as apart of our normal development process. This is good a thing. You should be concerned with logging information necesssary to annotate the behavior of your system. The problem arises when this logging begins to clutter our code, making it difficult for ourself and other developers in the future to suss out its original intent. In small scripts and code bases this may not be a problem, but when you have larger platforms and interconnected services, this small blight can suddenly become a nuisance, clouding your code's intent and infesting your logs with barely parseable information that wreaks havoc on an effective logging strategy.

Let's begin with an example to shed light on the problem. Below is an example of a lambda handler fetching an account ID from the query string parameters of its event object, and then fetching the account from a Dynamodb table.

```python
import logging

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AccountsTable')

def handler(event, context):
    params = event['queryStringParameters']
    logging.info('QueryParams: {}', params)
    account = params.get('account')
    if not account:
        logging.error('Missing account parameter')
        raise Exception('missing account parameter')

    logging.info('Get account details {}', account)
    response = table.get_item(
        Key=account
    )
    if 'Item' not in response:
        raise Exception('Failed to fetch account: {}', account)
    logging.info()

        
    logging.info('Account ID: {}, ')

```

### Using the `@log_it` decorator



### Using the `@use_logging_context` decorator
