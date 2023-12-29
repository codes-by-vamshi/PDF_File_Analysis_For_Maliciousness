import re
import logging
import subprocess

from multiprocessing import Process
from tempfile import TemporaryDirectory

logger = logging.getLogger(__name__)


def _create_subprocess(bin, args, proc_timeout=30, **kwargs):
    cmd = [bin] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE, timeout=proc_timeout, **kwargs)
    return result.stdout, result.stderr


def create_sig(sig_info, cur_line=None):
    """
    Create and add the signatures found in the document
    :param sig_info: Signatures found in the document.
    :param cur_line: Line in which the signatures are found.
    :return: None.
    """
    # TODO remove after
    return {
        'families': list(),
        "name": sig_info['name'],
        "description": sig_info['description'],
        "severity": int(sig_info['severity']),
        "references": list(),
        "marks": re.sub(r'\u001b\[.*?[@-~]', '', cur_line).strip() if sig_info['name'] == "CVE" else []
    }


def exception_handler(func):
    """
    Decorator function for to log exceptions
    :param func: function to run and handle exceptions
    :return: function object
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.warning(f'Failed {func.__module__} to process {args[1]} error: {exc}')
    return wrapper


def tmp_file_handler(func):
    """
    Decorator function to handle temporary files and exceptions
    :param func: function to run and store temporary files
    :return: function object
    """
    def wrapper(*args, **kwargs):
        with TemporaryDirectory() as tmp_dir:
            logger.info(f'Files processed in temp dir {tmp_dir}')
            return func(*args, tmp_dir=tmp_dir, **kwargs)
    return wrapper


def time_limit_handler(func):
    # Warning: This is deprecated, New process is spawned every time and the prop_spec object updates will be lost.
    """
    Decorator function to limit
    :param func: function to run
    :return: function object
    """
    def wrapper(*args, **kwargs):
        p = Process(target=func, args=args, kwargs=kwargs)
        p.start()

        p.join(55)

        # If thread is active
        if p.is_alive():

            # Terminate func
            p.terminate()
            p.join()
    return wrapper
