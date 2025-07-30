# coding: utf-8

from __future__ import absolute_import

from datatransfer.common import constants

from spyne.model import ComplexModel
from spyne.model import Unicode


class ComplexModelWithNamespace(ComplexModel):
    __namespace__ = constants.DATAPUSH_NAMESPACE


class GetPrivilegeRequest(ComplexModelWithNamespace):
    AuthorizationKey = Unicode
    SessionID = Unicode


class GetPrivilegeResponse(ComplexModelWithNamespace):
    __namespace__ = constants.DATAPUSH_NAMESPACE + '/response'
    SessionID = Unicode
    Message = Unicode
