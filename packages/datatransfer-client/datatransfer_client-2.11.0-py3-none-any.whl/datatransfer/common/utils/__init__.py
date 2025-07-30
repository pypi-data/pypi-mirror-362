# coding: utf-8

from __future__ import absolute_import

import base64
import os
import re
import sys
import tempfile
import zipfile

from six import unichr
import celery
import six


def archive_xml(filename):
    """Выполняем архивирование XML c данными.
    :param filename: Имя файла
    :return: Имя архива с файлом
    """

    dir_name, file_name = (
        os.path.dirname(filename), os.path.basename(filename))
    archive_name = os.path.join(
        dir_name,
        "{0}.zip".format(filename))

    with zipfile.ZipFile(
            archive_name,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True) as zf:
        zf.write(filename, file_name)

    return archive_name


def archive_append(archive_filename, filename):
    file_name = os.path.basename(filename)

    with zipfile.ZipFile(
            archive_filename,
            mode="a",
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True) as zf:
        zf.write(filename, file_name)


def encode_archive(archive_name):
    """Выполнение кодирования архива
    :param archive_name: Имя архива
    :return: Имя времянного файла
    """

    with open(archive_name, "rb") as f:
        with tempfile.NamedTemporaryFile(delete=False) as encoded_file:
            base64.encode(f, encoded_file)
            encoded_file_name = encoded_file.name

    return encoded_file_name


def compile_illegal_unichrs_regex():
    u"""
    Returns complied regex to replace illegal unicode chars.

    http://stackoverflow.com/questions/1707890/fast-way-to-filter-illegal-xml-unicode-chars-in-python
    """
    _illegal_unichrs = [
        (0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F),
        (0x7F, 0x84), (0x86, 0x9F),
        (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)
    ]

    if sys.maxunicode >= 0x10000:  # not narrow build
        _illegal_unichrs.extend([
            (0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF),
            (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF),
            (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF),
            (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF),
            (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF),
            (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF),
            (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF),
            (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)
        ])

    _illegal_ranges = [
        "%s-%s" % (unichr(low), unichr(high))
        for (low, high) in _illegal_unichrs
    ]

    return re.compile(u'[%s]' % u''.join(_illegal_ranges))


illegal_unichrs_regex = compile_illegal_unichrs_regex()


def xml_escape(s):
    if type(s) in (str, six.text_type):
        s = illegal_unichrs_regex.subn('', s)[0]
    return s


def register_task(task):
    u"""Регистрирует задание в Celery.

    Начиная с Celery 4.x появилась необходимость регистрировать задания,
    основанные на классах с помощью метода
    :meth:`~celery.app.base.Celery.register_task`. В более ранних версиях
    Celery задания регистрируются автоматически.

    :rtype: celery.app.task.Task
    """
    if celery.VERSION < (4, 0, 0):
        return task

    elif celery.VERSION == (4, 0, 0):
        # В Celery 4.0.0 нет метода для регистрации заданий,
        # исправлено в 4.0.1
        raise Exception(u'Use Celery 4.0.1 or later.')

    else:
        app = celery.app.app_or_default()
        return app.register_task(task)
