# coding: utf-8

from __future__ import absolute_import

import datetime
import logging
import os
import traceback

from datatransfer.common import constants
from datatransfer.common.helpers import get_error
from datatransfer.source import configs as dt_settings
from datatransfer.source.common.configuration import get_object

LoggedClient = get_object('client_class')
LoggedClient.log_model = get_object('log_model')


class DataTransferClient(LoggedClient):
    """СМЭВ клиент сервиса DataTransfer"""

    # Описание сервиса и его методов
    SERVICE_META = {
        'code': u"DataTransfer",
        'name': u"Контингент обучающихся (РС)",
        'methods': {
            'DataTransfer': u"Передача пакета данных (РС)"}}

    def __init__(self, *args, **kwargs):
        params = dict(
            url=dt_settings.DATATRANSFER_WSDL,
            timeout=dt_settings.WEBSERVICE_TIMEOUT,
            private_key_path=dt_settings.SMEV_PRIVATE_KEY_FILE,
            private_key_pass=dt_settings.SMEV_PRIVATE_KEY_PASSWORD,
            certificate_path=dt_settings.SMEV_CERTIFICATE_FILE,
            in_certificate_path=dt_settings.SMEV_CERTIFICATE_FILE,
            digest_method=str(dt_settings.SMEV_DIGEST_METHOD),
            autoblend=True)

        super(DataTransferClient, self).__init__(**params)

    def DataTransfer(self, session_id, encoded_file_name, filename):
        method = 'DataTransfer'

        request = self.factory.create(method)
        (_, smev_namespace) = (
            request.Message.__metadata__.sxtype.namespace())

        request.Message.Sender.Code = (
            dt_settings.SMEV_MNEMONICS)
        request.Message.Sender.Name = (
            dt_settings.SMEV_NAME)

        request.Message.Recipient.Code = (
            dt_settings.DATATRANSFER_MNEMONICS)
        request.Message.Recipient.Name = (
            dt_settings.DATATRANSFER_NAME)

        request.Message.Service = self.factory.create(
            '{{{0}}}ServiceType'.format(smev_namespace))
        request.Message.Service.Mnemonic = dt_settings.DATATRANSFER_MNEMONICS
        request.Message.Service.Version = (
            constants.DATATRANSFER_SERVICE_VERSION
        )
        request.Message.TypeCode = constants.SMEV_TYPE_CODE
        request.Message.Status = constants.SMEV_STATUS

        request.Message.Date = datetime.datetime.now()
        request.Message.ExchangeType = constants.SMEV_EXCHANGE_TYPE

        request.MessageData.AppData.DataTransferRequest.AuthorizationKey = (
            dt_settings.DATATRANSFER_AUTHORIZATION_KEY)
        request.MessageData.AppData.DataTransferRequest.SessionID = session_id

        request.MessageData.AppDocument.RequestCode = os.path.basename(
            filename)

        with open(encoded_file_name, "rb") as f:
            request.MessageData.AppDocument.BinaryData = f.read().decode()

        error = None
        try:
            self.service.DataTransfer(request.Message, request.MessageData)
        except Exception as e:
            error = get_error(e)

            logger = logging.getLogger(__package__)
            logging.basicConfig(format='%(asctime)s %(message)s')
            logger.error(error)
            logger.error(traceback.format_exc())

        self.log_request(method, error=error)
