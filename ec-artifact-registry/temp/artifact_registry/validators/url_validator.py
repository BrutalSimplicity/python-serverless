''' URL Validator '''

from urllib.parse import urlparse
from yamale.validators import Validator

class URL(Validator):

    tag = 'url'

    def _is_valid(self, value):
        ''' _is_valid '''
        try:
            result = urlparse(value)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False
