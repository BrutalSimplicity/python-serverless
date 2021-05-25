''' ARN Validator '''

from yamale.validators import Validator

class ARN(Validator):

    tag = 'arn'

    def parse_arn(self, arn):
        ''' parse_arn '''
        # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
        elements = arn.split(':', 5)
        result = {
            'arn': elements[0],
            'partition': elements[1],
            'service': elements[2],
            'region': elements[3],
            'account': elements[4],
            'resource': elements[5],
            'resource_type': None
        }
        if '/' in result['resource']:
            result['resource_type'], result['resource'] = result['resource'].split('/',1)
        elif ':' in result['resource']:
            result['resource_type'], result['resource'] = result['resource'].split(':',1)
        return result

    def _is_valid(self, value):
        ''' _is_valid '''
        elements = value.strip().split(':', 5)
        # The length of the elements array should be at least 6
        return len(elements) >= 6

