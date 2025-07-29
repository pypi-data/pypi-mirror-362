import argparse
from random import Random
from typing import List

import librosa
from wai.logging import LOGGING_WARNING

from adc.api import AudioData, AudioClassificationData, SpeechData, FORMAT_WAV
from ._base_audio_augmentation import BaseAudioAugmentationFilter, AUG_MODE_REPLACE


class TimeStretch(BaseAudioAugmentationFilter):
    """
    Resamples the audio data with the supplied sample rate.
    """

    def __init__(self, mode: str = AUG_MODE_REPLACE, suffix: str = None,
                 seed: int = None, seed_augmentation: bool = False, threshold: float = 0.0,
                 from_rate: float = None, to_rate: float = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param mode: the augmentation mode to use
        :type mode: str
        :param suffix: the suffix to use for the file names in case of augmentation mode 'add'
        :type suffix: str
        :param seed: the seed value to use for the random number generator; randomly seeded if not provided
        :type seed: int
        :param seed_augmentation: whether to seed the augmentation; if specified, uses the seeded random generator to produce a seed value
        :type seed_augmentation: bool
        :param threshold: the threshold to use for Random.rand(): if equal or above, augmentation gets applied; range: 0-1; default: 0 (= always)
        :type threshold: float
        :param from_rate: the minimum (fractional) steps to shift
        :type from_rate: float
        :param to_rate: the maximum (fractional) steps to shift
        :type to_rate: float
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(mode=mode, suffix=suffix, seed=seed,
                         seed_augmentation=seed_augmentation, threshold=threshold,
                         logger_name=logger_name, logging_level=logging_level)
        self.from_rate = from_rate
        self.to_rate = to_rate

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "time-stretch"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Augmentation method for stretching the time of audio files (speed up/slow down)."

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
        parser.add_argument("-f", "--from_rate", type=float, help="The minimum stretch factor (<1: slow down, 1: same, >1: speed up).", default=None, required=False)
        parser.add_argument("-t", "--to_rate", type=float, help="The maximum stretch factor (<1: slow down, 1: same, >1: speed up).", default=None, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.from_rate = ns.from_rate
        self.to_rate = ns.to_rate

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-stretched"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.from_rate is not None) and (self.to_rate is not None)

    def _augment(self, item: AudioData, aug_seed: int, audio_name: str) -> AudioData:
        """
        Augments the audio data.

        :param item: the data to augment
        :type item: AudioData
        :param aug_seed: the seed value to use, can be None
        :type aug_seed: int
        :param audio_name: the new audio name
        :type audio_name: str
        :return: the potentially updated audio data
        :rtype: AudioData
        """

        # determine steps
        rate = None
        if (self.from_rate is not None) and (self.to_rate is not None):
            if self.from_rate == self.to_rate:
                rate = self.from_rate
            else:
                rnd = Random(aug_seed)
                rate = rnd.random() * (self.to_rate - self.from_rate) + self.from_rate
            self.logger().info("rate: %f" % rate)

        if rate is None:
            return item
        else:
            # apply shift
            audio_new = librosa.effects.time_stretch(item.audio, rate=rate)
            item_new = type(item)(audio=audio_new, audio_format=FORMAT_WAV, audio_name=audio_name, sample_rate=item.sample_rate, metadata=item.get_metadata(), annotation=item.annotation)
            return item_new
