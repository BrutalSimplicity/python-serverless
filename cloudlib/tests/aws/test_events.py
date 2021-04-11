import unittest

import botocore.session
from botocore.stub import Stubber

from cloudtools.aws.events import event as event_handler
from cloudtools.aws.sns import sns_message
from cloudtools.common.json import encoder
from cloudtools.common.utils import filter_empty_properties, generate_timestamp


class AwsEventsTests(unittest.TestCase):

    def test_should_filter_empty_properties(self):
        input = {
            'a': 1,
            'b': None,
            'c': 1
        }

        output = filter_empty_properties(input)

        expected = {'a': 1, 'c': 1}

        self.assertCountEqual(output, expected)

    def test_sns_event_should_publish_message(self):
        sns_client = botocore.session.get_session().create_client('sns', region_name='us-east-1')

        with Stubber(sns_client) as stubber:
            topic_arn = 'arn:aws:sns:us-east-1:topic/some-topic'
            subject = 'test'
            response = {
                'test': True
            }
            stubber.add_response('publish', {}, {
                'TopicArn': topic_arn,
                'Subject': subject,
                'Message': encoder(response)
            })

            sns_event = sns_message(sns_client, topic_arn, subject)

            @sns_event
            def event_it():
                return response

            result = event_it()

            self.assertEqual(response, result)
            stubber.assert_no_pending_responses()


    def test_event_should_publish_events_to_event_bridge(self):
        event_client = botocore.session.get_session().create_client('events', region_name='us-east-1')

        with Stubber(event_client) as stubber:
            source = 'source'
            detail_type = 'detail_type'
            bus_name = 'event_bus_name'
            time = generate_timestamp()
            response = {
                'test': True
            }

            stubber.add_response('put_events', {}, {
                'Entries': [{
                    'Source': source,
                    'Detail': encoder(response),
                    'DetailType': detail_type,
                    'EventBusName': bus_name,
                    'Time': time
                }]
            })

            event = event_handler(event_client, source, detail_type, bus_name, time=time)

            @event
            def event_it():
                return response

            result = event_it()

            self.assertEqual(response, result)
            stubber.assert_no_pending_responses()
