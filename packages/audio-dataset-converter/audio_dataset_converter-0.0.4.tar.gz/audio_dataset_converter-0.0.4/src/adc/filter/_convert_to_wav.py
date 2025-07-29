import os
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from adc.api import AudioData, AudioClassificationData, SpeechData, make_list, flatten_list, FORMAT_WAV, FORMAT_EXTENSIONS


class ConvertToWav(Filter):
    """
    Turns the audio into WAV format.
    """

    def __init__(self, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "convert-to-wav"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Turns the audio into WAV format."

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AudioData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [AudioClassificationData, SpeechData]

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            if item.audio_format == FORMAT_WAV:
                result.append(item)
            else:
                self.logger().info("Converting to WAV: %s" % item.audio_name)
                audio_name_new = os.path.splitext(item.audio_name)[0] + FORMAT_EXTENSIONS[FORMAT_WAV]
                item_new = type(item)(audio_name=audio_name_new, audio=item.audio,
                                      audio_format=FORMAT_WAV, duration=item.duration,
                                      sample_rate=item.sample_rate, metadata=item.get_metadata(),
                                      annotation=item.annotation)
                result.append(item_new)

        return flatten_list(result)
