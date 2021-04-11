from typing import Any, Dict, Mapping

from boto3.dynamodb.transform import TypeDeserializer, TypeSerializer


def encoder(obj: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    serializer = TypeSerializer()
    return {k: serializer.serialize(v) for k, v in obj.items()}

def decoder(obj: Mapping[str, Any]) -> Dict[str, Any]:
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in obj.items()}
