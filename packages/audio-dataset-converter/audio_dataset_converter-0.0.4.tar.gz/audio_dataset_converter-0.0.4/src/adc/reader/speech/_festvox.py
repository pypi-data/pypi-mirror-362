import argparse
import os
import re
from typing import List, Iterable, Union

from seppl.io import locate_files
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from wai.logging import LOGGING_WARNING

from adc.api import Reader
from adc.api import SpeechData

# The regular expression which matches a single line from a festvox file
LINE_REGEX = '^\\( (?P<filename>.*) "(?P<transcription>.*)" \\)$'

# The compiled regex
LINE_PATTERN = re.compile(LINE_REGEX)


class FestVoxSpeechReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 rel_path: str = None, resume_from: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param rel_path: the relative path to the audio files
        :type rel_path: str
        :param resume_from: the file to resume from (glob)
        :type resume_from: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.rel_path = rel_path
        self.resume_from = resume_from
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-festvox-sp"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Reads the speech data in Festvox format."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the text file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the text files to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("--resume_from", type=str, help="Glob expression matching the file to resume from, e.g., '*/012345.txt'", required=False)
        parser.add_argument("-r", "--rel_path", type=str, help="The relative path to the audio files.", required=False, default=".")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.rel_path = ns.rel_path
        self.resume_from = ns.resume_from

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [SpeechData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.txt", resume_from=self.resume_from)
        if self.rel_path is None:
            self.rel_path = "."

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        with open(self.session.current_input) as fp:
            lines = [line.strip() for line in fp.readlines()]

        basedir = os.path.dirname(self.session.current_input)
        for line in lines:
            if len(line) == 0:
                continue

            match = re.match(LINE_PATTERN, line.strip())
            if match is None:
                raise ValueError("Bad FestVox line: %s" % line)

            wav_filename, transcription = match.group("filename"), match.group("transcription")
            if not wav_filename.lower().endswith(".wav"):
                wav_filename += ".wav"

            audio = os.path.join(basedir, self.rel_path, wav_filename)
            if not os.path.exists(audio):
                self.logger().warning("Audio file not found: %s" % audio)
                yield None

            yield SpeechData(source=audio, annotation=transcription)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
