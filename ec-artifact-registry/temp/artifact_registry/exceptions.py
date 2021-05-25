
class Error(Exception):
    ''' Base class for Exceptions '''
    pass

class ArtifactNotFoundError(Error):
    ''' Raised when an Artifact is not found in the DynamoDB Table '''

    def __init__(self, message):
        self.message = message
