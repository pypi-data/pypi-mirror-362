import argparse
import librosa
import os
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from adc.api import AudioData, AudioClassificationData, SpeechData, make_list, flatten_list, FORMAT_WAV, FORMAT_EXTENSIONS

RESAMPLE_TYPE_DEFAULT = "kaiser_best"

RESAMPLE_TYPES = [
    RESAMPLE_TYPE_DEFAULT,
    "kaiser_fast",
    "fft",
    "polyphase",
    "linear",
    "zero_order_hold",
    "sinc_best",
    "sinc_medium",
    "sinc_fastest",
    "soxr_vhq",
    "soxr_hq",
    "soxr_mq",
    "soxr_lq",
    "soxr_qq",
]


class Resample(Filter):
    """
    Resamples the audio data with the supplied sample rate.
    """

    def __init__(self, sample_rate: int = None, resample_type: str = RESAMPLE_TYPE_DEFAULT,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param sample_rate: the new sample rate to use
        :type sample_rate: int
        :param resample_type: how to perform the resampling
        :type resample_type: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.sample_rate = sample_rate
        self.resample_type = resample_type

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "resample"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Resamples the audio data with the supplied sample rate."

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

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-s", "--sample_rate", type=int, help="The sample rate to use for the audio.", default=22050, required=False)
        parser.add_argument("-t", "--resample_type", choices=RESAMPLE_TYPES, help="The resampling type to apply.", default=RESAMPLE_TYPE_DEFAULT, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.sample_rate = ns.sample_rate
        self.resample_type = ns.resample_type

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.sample_rate is None:
            self.sample_rate = 22050
        if self.resample_type is None:
            self.resample_type = RESAMPLE_TYPE_DEFAULT

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            if item.sample_rate == self.sample_rate:
                result.append(item)
            else:
                self.logger().info("Resampling with %d/%s: %s" % (self.sample_rate, self.resample_type, item.audio_name))
                audio_new = librosa.resample(item.audio, orig_sr=item.sample_rate, target_sr=self.sample_rate,
                                             res_type=self.resample_type)
                audio_name_new = os.path.splitext(item.audio_name)[0] + FORMAT_EXTENSIONS[FORMAT_WAV]
                item_new = type(item)(audio_name=audio_name_new, audio=audio_new,
                                      audio_format=FORMAT_WAV, duration=item.duration,
                                      sample_rate=self.sample_rate, metadata=item.get_metadata(),
                                      annotation=item.annotation)
                result.append(item_new)

        return flatten_list(result)
