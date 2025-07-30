# coding: utf-8
from datatransfer.common import constants
from spyne.model import ComplexModel
from spyne.model import Unicode


class ComplexModelWithNamespace(ComplexModel):
    __namespace__ = constants.DATAPUSH_NAMESPACE


class EnrollGetDataPushRequest(ComplexModelWithNamespace):
    AuthorizationKey = Unicode
    SessionID = Unicode


class EnrollGetDataPushResponse(ComplexModelWithNamespace):
    __namespace__ = constants.DATAPUSH_NAMESPACE + '/response'
    SessionID = Unicode
    Message = Unicode
