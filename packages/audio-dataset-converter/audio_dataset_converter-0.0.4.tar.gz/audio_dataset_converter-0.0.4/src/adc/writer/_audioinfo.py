import argparse
import csv
import json
import os
import sys
from typing import List, Iterable

from wai.logging import LOGGING_WARNING

from adc.api import AudioData, AudioClassificationData, SpeechData, BatchWriter
from seppl.placeholders import placeholder_list, PlaceholderSupporter, expand_placeholders

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]


class AudioInfoWriter(BatchWriter, PlaceholderSupporter):

    def __init__(self, output_file: str = None, output_format: str = OUTPUT_FORMAT_TEXT,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the writer.

        :param output_file: the file to write the audio info to
        :type output_file: str
        :param output_format: the file format to use
        :type output_format: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_format = output_format
        self._data = None
        self._additional_label = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-audioinfo"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Outputs information about the audio files."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, help="The file to store the audio information in; outputs to stdout if no file provided. " + placeholder_list(obj=self), required=False, default=None)
        parser.add_argument("-f", "--output_format", choices=OUTPUT_FORMATS, help="The format to use for the output.", required=False, default=OUTPUT_FORMAT_TEXT)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output_file
        self.output_format = ns.output_format

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AudioData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        self._data = []
        self._additional_label = None

    def append_info(self, file_name, file_size, sample_rate, is_mono, duration, additional):
        """
        Appends the information.

        :param file_name: the file name
        :param file_size: the file size (length of data)
        :param sample_rate: the sample rate
        :param is_mono: whether the data is mono
        :param duration: the duration in seconds
        :param additional: the additional data
        """
        self._data.append([file_name, file_size, sample_rate, is_mono, duration, additional])

    def output_text(self, use_stdout, additional_label):
        """
        Outputs the information in simple textual format.

        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        :param additional_label: the label to use for the additional data
        :type additional_label: str
        """
        info = []
        for row in self._data:
            info.append("%s\n  - file_size: %d\n  - sample_rate: %d\n  - mono: %s\n  - duration (sec): %f\n  - %s: %s"
                        % (row[0], row[1], row[2], str(row[3]), row[4], additional_label, str(row[5])))

        if use_stdout:
            print("\n".join(info))
        else:
            with open(expand_placeholders(self.output_file), "w") as fp:
                fp.write("\n".join(info))

    def output_csv(self, use_stdout, additional_label):
        """
        Outputs the information in CSV format.

        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        :param additional_label: the label to use for the additional data
        :type additional_label: str
        """
        if use_stdout:
            writer = csv.writer(sys.stdout)
            f = None
        else:
            f = open(expand_placeholders(self.output_file), "w")
            writer = csv.writer(f)

        writer.writerow(["file_name", "file_size", "sample_rate", "mono", "duration_seconds", additional_label])
        for row in self._data:
            writer.writerow(row)

        if f is not None:
            f.close()

    def output_json(self, use_stdout, additional_label):
        """
        Outputs the information in json format.

        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        :param additional_label: the label to use for the additional data
        :type additional_label: str
        """
        data = []
        for row in self._data:
            file_data = {
                "file_name": row[0],
                "file_size": row[1],
                "sample_rate": row[2],
                "mono": row[3],
                "duration_seconds": row[4],
                additional_label: row[5],
            }
            data.append(file_data)

        if use_stdout:
            print(json.dumps(data, indent=2))
        else:
            with open(expand_placeholders(self.output_file), "w") as f:
                json.dump(data, f, indent=2)

    def output_info(self):
        """
        Outputs the information.
        """
        additional_label = "additional"
        if hasattr(self, "_additional_label") and (self._additional_label is not None):
            additional_label = self._additional_label
        use_stdout = (self.output_file is None) or (len(self.output_file) == 0)

        if self.output_format == OUTPUT_FORMAT_TEXT:
            self.output_text(use_stdout, additional_label)
        elif self.output_format == OUTPUT_FORMAT_CSV:
            self.output_csv(use_stdout, additional_label)
        elif self.output_format == OUTPUT_FORMAT_JSON:
            self.output_json(use_stdout, additional_label)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def _file_size(self, item) -> int:
        """
        Determines the file size.

        :param item: the audio item to get the file size for
        :return: the file size, -1 if failed to determine
        :rtype: int
        """
        if item.data is not None:
            return len(item.data)
        elif item.source is not None:
            return os.path.getsize(item.source)
        else:
            return -1

    def write_batch(self, data: Iterable):
        """
        Saves the data in one go.

        :param data: the data to write
        :type data: Iterable
        """
        for item in data:
            if isinstance(item, AudioClassificationData):
                self.append_info(
                    item.audio_name,
                    self._file_size(item),
                    item.sample_rate,
                    item.is_mono,
                    item.duration,
                    item.annotation)
                if self._additional_label is None:
                    self._additional_label = "label"
            elif isinstance(item, SpeechData):
                self.append_info(
                    item.audio_name,
                    self._file_size(item),
                    item.sample_rate,
                    item.is_mono,
                    item.duration,
                    item.annotation)
                if self._additional_label is None:
                    self._additional_label = "transcript"

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.output_info()
