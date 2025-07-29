import argparse
from random import Random
from typing import List

import librosa
from wai.logging import LOGGING_WARNING

from adc.api import AudioData, AudioClassificationData, SpeechData, FORMAT_WAV
from ._base_audio_augmentation import BaseAudioAugmentationFilter, AUG_MODE_REPLACE
from ._resample import RESAMPLE_TYPES, RESAMPLE_TYPE_DEFAULT


class PitchShift(BaseAudioAugmentationFilter):
    """
    Resamples the audio data with the supplied sample rate.
    """

    def __init__(self, mode: str = AUG_MODE_REPLACE, suffix: str = None,
                 seed: int = None, seed_augmentation: bool = False, threshold: float = 0.0,
                 from_steps: float = None, to_steps: float = None,
                 bins_per_octave: int = None, resample_type: str = RESAMPLE_TYPE_DEFAULT,
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
        :param from_steps: the minimum (fractional) steps to shift
        :type from_steps: float
        :param to_steps: the maximum (fractional) steps to shift
        :type to_steps: float
        :param bins_per_octave: how many steps per octave
        :type bins_per_octave: int
        :param resample_type: how to perform the resampling
        :type resample_type: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(mode=mode, suffix=suffix, seed=seed,
                         seed_augmentation=seed_augmentation, threshold=threshold,
                         logger_name=logger_name, logging_level=logging_level)
        self.from_steps = from_steps
        self.to_steps = to_steps
        self.bins_per_octave = bins_per_octave
        self.resample_type = resample_type

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "pitch-shift"

    def description(self) -> str:
        """
        Returns a description of the handler.

        :return: the description
        :rtype: str
        """
        return "Augmentation method for shifting the pitch of audio files."

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
        parser.add_argument("-f", "--from_steps", type=float, help="The minimum (fractional) steps to shift.", default=None, required=False)
        parser.add_argument("-t", "--to_steps", type=float, help="The maximum (fractional) steps to shift.", default=None, required=False)
        parser.add_argument("--bins_per_octave", type=int, help="How many steps per octave.", default=12, required=False)
        parser.add_argument("--resample_type", choices=RESAMPLE_TYPES, help="The resampling type to apply.", default=RESAMPLE_TYPE_DEFAULT, required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.from_steps = ns.from_steps
        self.to_steps = ns.to_steps
        self.bins_per_octave = ns.bins_per_octave
        self.resample_type = ns.resample_type

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.bins_per_octave is None:
            self.bins_per_octave = 12
        if self.resample_type is None:
            self.resample_type = RESAMPLE_TYPE_DEFAULT

    def _default_suffix(self):
        """
        Returns the default suffix to use for images when using "add" rather than "replace" as mode.

        :return: the default suffix
        :rtype: str
        """
        return "-shifted"

    def _can_augment(self):
        """
        Checks whether augmentation can take place.

        :return: whether can augment
        :rtype: bool
        """
        return (self.from_steps is not None) and (self.to_steps is not None)

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
        steps = None
        if (self.from_steps is not None) and (self.to_steps is not None):
            if self.from_steps == self.to_steps:
                steps = self.from_steps
            else:
                rnd = Random(aug_seed)
                steps = rnd.random() * (self.to_steps - self.from_steps) + self.from_steps
            self.logger().info("steps: %f" % steps)

        if steps is None:
            return item
        else:
            # apply shift
            audio_new = librosa.effects.pitch_shift(item.audio, sr=item.sample_rate, n_steps=steps, bins_per_octave=self.bins_per_octave, res_type=self.resample_type)
            item_new = type(item)(audio=audio_new, audio_format=FORMAT_WAV, audio_name=audio_name, sample_rate=item.sample_rate, metadata=item.get_metadata(), annotation=item.annotation)
            return item_new
