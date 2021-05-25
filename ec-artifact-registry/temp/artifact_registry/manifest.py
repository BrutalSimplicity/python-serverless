''' Manifest '''

import os
import yamale
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from yamale.validators import DefaultValidators
from shared.artifact_registry.validators.arn_validator import ARN
from shared.artifact_registry.validators.json_validator import Json
from shared.artifact_registry.validators.url_validator import URL

class Manifest:
    '''
        Represents a Manifest
        A manifestation of a manifest, if you will.
    '''

    def __init__(self, manifest=None):
        ''' __init__ '''
        validators = DefaultValidators.copy()
        validators[ARN.tag] = ARN
        validators[Json.tag] = Json
        validators[URL.tag] = URL

        self._schema_file = "{}/validators/manifest.schema.yaml".format(os.path.dirname(os.path.realpath(__file__)))
        self.schema = yamale.make_schema(self._schema_file, validators=validators)

        if manifest is not None:
            self._yaml = load(str(manifest), Loader=Loader)
            self._set_attr_()

    def _set_attr_(self):
        for key, value in self._yaml.items():
            self.__setattr__(key, value)

    def yaml_load(self, fp):
        ''' yaml_load '''
        self._yaml = load(fp, Loader=Loader)
        self._set_attr_()

    def yaml_loads(self, s: str):
        ''' yaml_loads '''
        self._yaml = load(s, Loader=Loader)
        self._set_attr_()

    def is_valid(self):
        ''' is_valid '''
        try:
            yamale.validate(self.schema, [(self._yaml, '')], strict=True)
        except ValueError:
            return False
        return True

    def validation_reasons(self):
        '''
        validation_reasons
        returns a list of reasons why the manifest was not valid
        returns an empty list if the manifest is valid
        '''
        try:
            yamale.validate(self.schema, [(self._yaml, '')], strict=True)
        except ValueError as ve:
            reasons = str(ve).strip().splitlines()
            reasons.pop(0)
            return [reason.strip() for reason in reasons]
        return []

    def __eq__(self, other):
        ''' __eq__ '''
        return type(other) == type(self)

    def __str__(self):
        return "{}".format(self._yaml)
