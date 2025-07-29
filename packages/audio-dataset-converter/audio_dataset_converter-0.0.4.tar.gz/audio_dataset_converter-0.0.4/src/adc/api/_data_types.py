from ._classification import AudioClassificationData
from ._speech import SpeechData


DATATYPE_CLASSIFICATION = "cl"
DATATYPE_SPEECH = "sp"
DATATYPES = [
    DATATYPE_CLASSIFICATION,
    DATATYPE_SPEECH,
]


def data_type_to_class(data_type: str):
    if data_type == DATATYPE_CLASSIFICATION:
        return AudioClassificationData
    elif data_type == DATATYPE_SPEECH:
        return SpeechData
    else:
        raise Exception("Unsupported data type: %s" % data_type)
