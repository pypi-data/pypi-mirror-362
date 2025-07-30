# coding: utf-8

from __future__ import (
    absolute_import,
)

from django.utils.encoding import (
    smart_str,
)
from six.moves.configparser import (
    NoOptionError,
    NoSectionError,
    SafeConfigParser,
)


class ExtendedConfigParser(SafeConfigParser, object):
    def __init__(self, defaults=None, *args, **kwargs):
        super(ExtendedConfigParser, self).__init__(None, *args, **kwargs)

        self._extended_defaults = defaults

    def get(self, section, option, *args, **kwargs):
        try:
            result = smart_str(super(ExtendedConfigParser, self).get(section, option, *args, **kwargs))
        except Exception as e:
            if isinstance(e, (NoSectionError, NoOptionError)):
                try:
                    result = self._extended_defaults[(section, option)]
                except:  # noqa
                    raise e
            else:
                raise e

        return result
