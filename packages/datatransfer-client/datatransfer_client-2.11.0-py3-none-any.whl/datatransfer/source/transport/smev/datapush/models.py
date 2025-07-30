# coding: utf-8

from __future__ import absolute_import

from datatransfer.common import constants
from datatransfer.common.constants import MODE_ALL
from datatransfer.common.constants import MODE_UPDATED

from spyne.model import ComplexModel
from spyne.model import Enum
from spyne.model import Unicode


class ComplexModelWithNamespace(ComplexModel):
    __namespace__ = constants.DATAPUSH_NAMESPACE


class DataPushRequest(ComplexModelWithNamespace):
    AuthorizationKey = Unicode
    SessionID = Unicode
    Mode = Enum(MODE_ALL, MODE_UPDATED, type_name='Mode')


class DataPushResponse(ComplexModel):
    __namespace__ = constants.DATAPUSH_NAMESPACE + '/response'
    SessionID = Unicode
    Message = Unicode


class FeedbackRequest(ComplexModelWithNamespace):
    AuthorizationKey = Unicode
    SessionID = Unicode


class FeedbackResponse(DataPushResponse):
    pass
