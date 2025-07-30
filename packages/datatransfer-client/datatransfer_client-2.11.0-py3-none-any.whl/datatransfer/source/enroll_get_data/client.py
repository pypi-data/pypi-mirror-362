# coding: utf-8
import datetime
import os

from datatransfer.common import constants
from datatransfer.source import configs as dt_settings
from datatransfer.source.transport.smev.datatransfer.client import (
    DataTransferClient)


class EnrollGetDataClient(DataTransferClient):
    """СМЭВ клиент сервиса DataTransfer (метод EnrollGetData)"""

    def __init__(self, *args, **kwargs):
        self.SERVICE_META['methods']['EnrollGetData'] = (
            "Запрос пакета данных (РС)"
        )

        params = dict(
            url=dt_settings.DATATRANSFER_WSDL,
            timeout=dt_settings.WEBSERVICE_TIMEOUT,
            private_key_path=dt_settings.SMEV_PRIVATE_KEY_FILE,
            private_key_pass=dt_settings.SMEV_PRIVATE_KEY_PASSWORD,
            certificate_path=dt_settings.SMEV_CERTIFICATE_FILE,
            in_certificate_path=dt_settings.SMEV_CERTIFICATE_FILE,
            digest_method=str(dt_settings.SMEV_DIGEST_METHOD),
            autoblend=True)

        super().__init__(**params)

    def EnrollGetData(self, session_id, encoded_file_name, filename):
        method = 'EnrollGetData'

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

        request.MessageData.AppData.EnrollGetDataRequest.AuthorizationKey = (
            dt_settings.DATATRANSFER_AUTHORIZATION_KEY)
        request.MessageData.AppData.EnrollGetDataRequest.SessionID = session_id

        request.MessageData.AppDocument.RequestCode = os.path.basename(
            filename)

        with open(encoded_file_name, "r") as f:
            request.MessageData.AppDocument.BinaryData = f.read()

        error = None
        try:
            self.service.EnrollGetData(request.Message, request.MessageData)
        except Exception as e:  # pylint:disable=broad-except
            error = e.message

        self.log_request(method, error=error)
