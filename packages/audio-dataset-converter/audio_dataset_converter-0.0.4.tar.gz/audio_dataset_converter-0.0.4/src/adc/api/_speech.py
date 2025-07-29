import numpy as np

from typing import Dict

from ._data import AudioData


class SpeechData(AudioData):
    """
    The annotations are the transcript.
    """

    def __init__(self, source: str = None, audio_name: str = None, data: bytes = None,
                 audio: np.ndarray = None, audio_format: str = None,
                 duration: float = None, sample_rate: float = None,
                 metadata: Dict = None, annotation: str = None):

        super().__init__(source=source, audio_name=audio_name, data=data,
                         audio=audio, audio_format=audio_format,
                         duration=duration, sample_rate=sample_rate,
                         metadata=metadata, annotation=annotation)

    def has_annotation(self) -> bool:
        """
        Checks whether annotations are present.

        :return: True if annotations present
        :rtype: bool
        """
        return (self.annotation is not None) and (len(self.annotation) > 0)

    def _annotation_to_dict(self):
        """
        Turns the annotations into a dictionary.

        :return: the generated dictionary
        :rtype: dict
        """
        return {"transcript": self.annotation}
