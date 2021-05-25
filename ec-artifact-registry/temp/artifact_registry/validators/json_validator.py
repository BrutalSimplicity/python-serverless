''' Json Validator '''

import json

from yamale.validators import Validator

class Json(Validator):

    tag = 'json'

    def _is_valid(self, value):
        ''' _is_valid '''
        # does the value parse into json
        # if the value is already a python object, then it should validate
        #  but convert it to a string first 
        if isinstance(value, (dict, list)):
            value = json.dumps(value)

        try:
            json.loads(value)
        except json.JSONDecodeError as e:
            print(">>>e: {}".format(e))
            return False
        return True
