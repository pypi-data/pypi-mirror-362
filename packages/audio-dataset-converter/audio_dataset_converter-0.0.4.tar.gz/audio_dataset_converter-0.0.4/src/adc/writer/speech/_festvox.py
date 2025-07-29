import argparse
import os
from typing import List, Iterable

from wai.logging import LOGGING_WARNING

from adc.api import SpeechData, SplittableBatchWriter, AnnotationsOnlyWriter, add_annotations_only_param
from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter


class FestVoxSpeechWriter(SplittableBatchWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, rel_path: str = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None, split_group: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_dir: the output directory to save the audio file/annotations in
        :type output_dir: str
        :param rel_path: the path for the audio files relative to the annotation file
        :type rel_path: str
        :param annotations_only: whether to output only the annotations and not the images
        :type annotations_only: bool
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param split_group: the regular expression with a single group used for keeping items in the same split, e.g., for identifying the base name of a file or the ID
        :type split_group: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, split_group=split_group, logger_name=logger_name, logging_level=logging_level)
        self.output_dir = output_dir
        self.rel_path = rel_path
        self.annotations_only = annotations_only
        self._splits = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-festvox-sp"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the speech data in Festvox format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the audio/.txt files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--rel_path", type=str, help="The relative path to the audio files.", required=False, default=".")
        add_annotations_only_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.rel_path = ns.rel_path
        self.annotations_only = ns.annotations_only

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [SpeechData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        if self.rel_path is None:
            self.rel_path = "."
        if self.annotations_only is None:
            self.annotations_only = False
        self._splits = dict()

    def write_batch(self, data: Iterable):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        for item in data:
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next(item=item.audio_name)
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            # write audio
            path = os.path.join(sub_dir, self.rel_path, item.audio_name)
            if not self.annotations_only:
                self.logger().info("Writing audio to: %s" % path)
                item.save_audio(path, make_dirs=True)

            # append annotations
            if sub_dir not in self._splits:
                self._splits[sub_dir] = []
            if item.has_annotation():
                wav_filename = os.path.splitext(item.audio_name)[0]
                transcript = item.annotation
                self._splits[sub_dir].append("( %s \"%s\" )" % (wav_filename, transcript))

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()

        for sub_dir, annotations in self._splits.items():
            # save annotations
            if not os.path.exists(sub_dir):
                self.logger().info("Creating sub dir: %s" % sub_dir)
                os.makedirs(sub_dir)
            path = os.path.join(sub_dir, "annotations.txt")
            with open(path, "w") as fp:
                for line in annotations:
                    fp.write(line)
                    fp.write("\n")
