import importlib
import inspect
import io
import librosa
import numpy as np
import os
import soundfile as sf
import tempfile
import traceback

from typing import Optional, Union, List, Callable, Tuple


def strip_suffix(path: str, suffix: str) -> str:
    """
    Removes the suffix from the file, if possible.

    :param path: the filename to process
    :type path: str
    :param suffix: the suffix to remove (including extension); ignored if None or ""
    :type suffix: str
    :return: the (potentially) updated filename
    :rtype: str
    """
    if suffix is not None:
        if len(suffix) == 0:
            suffix = None
    if suffix is not None:
        if path.endswith(suffix):
            return path[0:-len(suffix)]
    return path


def locate_file(path: str, ext: Union[str, List[str]], rel_path: str = None, suffix: str = None) -> List[str]:
    """
    Tries to locate the associate files for the given path by replacing its extension by the provided ones.

    :param path: the base path to use
    :type path: str
    :param ext: the extension(s) to look for (incl dot)
    :type ext: str or list
    :param suffix: the suffix to strip from the files, ignored if None or ""
    :type suffix: str
    :param rel_path: the relative path to the annotation to use for looking for associated files, ignored if None
    :type rel_path: str
    :return: the located files
    :rtype: list
    """
    result = []
    if rel_path is not None:
        parent_path = os.path.dirname(path)
        name = os.path.basename(path)
        path = os.path.join(parent_path, rel_path, name)
    path = strip_suffix(path, suffix)
    noext = os.path.splitext(path)[0]
    for current in ext:
        path = noext + current
        if os.path.exists(path):
            result.append(path)
    return result


def locate_audio(path: str, rel_path: str = None, suffix: str = None) -> Optional[str]:
    """
    Tries to locate the audio file (mp3 or wav) for the given path by replacing its extension.

    :param path: the base path to use
    :type path: str
    :param rel_path: the relative path to the annotation to use for looking for audio files, ignored if None
    :type rel_path: str
    :param suffix: the suffix to strip from the files, ignored if None or ""
    :type suffix: str
    :return: the located audio, None if not found
    :rtype: str
    """
    ext = [".mp3", ".MP3", ".wav", ".WAV"]
    audio_files = locate_file(path, ext, rel_path=rel_path, suffix=suffix)
    if len(audio_files) == 0:
        return None
    else:
        return audio_files[0]


def load_function(function: str) -> Callable:
    """
    Parses the function definition and returns the function.
    The default format is "module_name:function_name".
    Raises exceptions if wrong format, missing or not an actual function.

    :param function: the function definition to parse
    :type function: str
    :return: the parsed function
    """
    if ":" not in function:
        raise Exception("Expected format 'module_name:function_name' but got: %s" % function)
    else:
        module_name, func_name = function.split(":")

    try:
        module = importlib.import_module(module_name)
    except:
        raise Exception("Failed to import class lister module: %s" % module_name)

    if hasattr(module, func_name):
        func = getattr(module, func_name)
        if inspect.isfunction(func):
            return func
        else:
            raise Exception("Not an actual function: %s" % function)
    else:
        raise Exception("Function '%s' not found in module '%s'!" % (func_name, module_name))


def load_audio_from_file(path: str) -> Union[Tuple[np.ndarray, int], Tuple[None, None]]:
    """
    Loads the audio from the file.

    :param path: the file to load the audio from
    :type path: str
    :return: the audio data tuple (audio/np.ndarray, sample_rate/int), None if failed to load
    :rtype: tuple
    """
    try:
        return sf.read(path)
    except:
        try:
            return librosa.load(path)
        except:
            print("Failed to read: %s" % path)
            traceback.print_exc()
            return None, None


def load_audio_from_bytes(data: bytes, ext: str) -> Union[Tuple[np.ndarray, int], Tuple[None, None]]:
    """
    Loads the audio from the bytes. Falls back loading from disk, if not possible.

    :param data: the bytes to load the audio from
    :type data: bytes
    :param ext: the audio extension to use
    :type ext: str
    :return: the audio data, None if failed to load
    :rtype: np.ndarray
    """
    path = None
    try:
        buf = io.BytesIO(data)
        result = sf.read(buf)
    except:
        with tempfile.NamedTemporaryFile(suffix=ext, delete_on_close=False) as fp:
            fp.write(data)
            fp.close()
            path = fp.name
            result = load_audio_from_file(path)
    finally:
        if path is not None:
            os.remove(path)
    return result
