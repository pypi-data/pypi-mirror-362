from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "adc.reader",
            "adc.reader.classification",
            "adc.reader.speech",
        ],
        "seppl.io.Filter": [
            "adc.filter",
            "adc.filter.classification",
            "adc.filter.speech",
        ],
        "seppl.io.Writer": [
            "adc.writer",
            "adc.writer.classification",
            "adc.writer.speech",
        ],
        "adc.api.Generator": [
            "adc.generator",
        ],
    }
