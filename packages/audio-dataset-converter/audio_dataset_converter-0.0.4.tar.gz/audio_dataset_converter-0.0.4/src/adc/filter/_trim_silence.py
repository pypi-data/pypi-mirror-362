import argparse
import librosa
import os
from typing import List

from seppl.io import Filter
from wai.logging import LOGGING_WARNING
from adc.api import AudioData, AudioClassificationData, SpeechData, make_list, flatten_list, FORMAT_WAV, FORMAT_EXTENSIONS


class TrimSilence(Filter):
    """
    Resamples the audio data with the supplied sample rate.
    """

    def __init__(self, top_db: int = None, frame_length: int = None, hop_length: int = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param top_db: the threshold (in decibels) below reference to consider as silence
        :type top_db: int
        :param frame_length: the number of samples per analysis frame
        :type frame_length: str
        :param hop_length: the number of samples between analysis frames
        :type hop_length: int
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.top_db = top_db
        self.frame_length = frame_length
        self.hop_length = hop_length

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "trim-silence"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Trims silence from audio files."

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
        parser.add_argument("--top_db", type=int, help="The threshold (in decibels) below reference to consider as silence.", default=60, required=False)
        parser.add_argument("--frame_length", type=int, help="The number of samples per analysis frame.", default=2048, required=False)
        parser.add_argument("--hop_length", type=int, help="The number of samples between analysis frames.", default=512, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.top_db = ns.top_db
        self.frame_length = ns.frame_length
        self.hop_length = ns.hop_length

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.top_db is None:
            self.top_db = 60
        if self.frame_length is None:
            self.frame_length = 2048
        if self.hop_length is None:
            self.hop_length = 512

    def _do_process(self, data):
        """
        Processes the data record(s).

        :param data: the record(s) to process
        :return: the potentially updated record(s)
        """
        result = []
        for item in make_list(data):
            self.logger().info("before trim: %s" % str(item.audio.shape))
            audio_new, index = librosa.effects.trim(item.audio, top_db=self.top_db, frame_length=self.frame_length,
                                                    hop_length=self.hop_length)
            audio_name_new = os.path.splitext(item.audio_name)[0] + FORMAT_EXTENSIONS[FORMAT_WAV]
            self.logger().info("after trim: %s" % str(audio_new.shape))
            item_new = type(item)(audio_name=audio_name_new, audio=audio_new,
                                  audio_format=FORMAT_WAV, duration=item.duration,
                                  sample_rate=item.sample_rate, metadata=item.get_metadata(),
                                  annotation=item.annotation)
            result.append(item_new)

        return flatten_list(result)
