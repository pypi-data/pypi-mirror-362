# coding: utf-8

from __future__ import absolute_import

import datetime
import os

from datatransfer.common import constants
from datatransfer.source import configs as dt_settings
from datatransfer.source.get_data.service.models import GetDataPushRequest
from datatransfer.source.get_data.service.models import GetDataPushResponse
from datatransfer.source.get_data.tasks import get_data_push_task

from spyne.decorator import rpc
from spyne.error import Fault


@rpc(GetDataPushRequest,
     _returns=GetDataPushResponse)
def GetDataPush(context, GetDataPushRequest):
    InMessage = context.udc.in_smev_message
    OutMessage = context.udc.out_smev_message

    response = GetDataPushResponse()

    response.SessionID = GetDataPushRequest.SessionID

    OutMessage.Service.Mnemonic = (
        dt_settings.SMEV_MNEMONICS)
    OutMessage.Service.Version = (
        constants.DATAPUSH_SERVICE_VERSION)
    OutMessage.Sender.Code = (
        dt_settings.SMEV_MNEMONICS)
    OutMessage.Sender.Name = (
        dt_settings.SMEV_NAME)
    OutMessage.TypeCode = (
        constants.SMEV_TYPE_CODE)

    try:
        if InMessage.Service.Mnemonic != dt_settings.SMEV_MNEMONICS:
            raise Fault(faultcode=u"INVALID", faultstring=u"Неизвестная мнемоника сервиса")

        if InMessage.Service.Version != constants.DATAPUSH_SERVICE_VERSION:
            raise Fault(faultcode=u"INVALID", faultstring=u"Некорректная версия сервиса")

        if InMessage.Recipient.Code != dt_settings.SMEV_MNEMONICS:
            raise Fault(faultcode=u"INVALID", faultstring=u"Неизвестный получатель")

        if not (InMessage.Sender.Code == dt_settings.DATATRANSFER_MNEMONICS
                and GetDataPushRequest.AuthorizationKey == dt_settings.DATAPUSH_AUTHORIZATION_KEY):
            raise Fault(faultcode=u"INVALID", faultstring=u"Неавторизованный запрос")

        now = datetime.datetime.now()
        today = datetime.date.today()

        archive_path = os.path.join(
            dt_settings.STORAGE_MAILBOX_PATH,
            constants.CONFIGURATION_ARCHIVE_IN,
            str(today.year), str(today.month), str(today.day))

        AppDocument = context.udc.in_smev_appdoc
        archive_filename = os.path.join(
            archive_path,
            u"{0}_{1}_{2}.zip".format(
                InMessage.Sender.Code, AppDocument.RequestCode,
                now.strftime('%Y%m%d_%H%M%S')))

        try:
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)

            with open(archive_filename, 'w+b') as decoded_file:
                decoded_file.write(AppDocument.BinaryData.data[-1])
        except Exception as e:
            raise Fault(
                faultcode=u"FAILURE",
                faultstring=u"Ошибка доступа к файлу: {0}".format(str(e)),
            )

        if not InMessage.TestMsg:
            get_data_push_task.apply_async((
                AppDocument.RequestCode,
                archive_filename,
                GetDataPushRequest.SessionID
            ), kwargs={})

    except Fault as e:
        OutMessage.Status = e.faultcode
        response.Message = e.faultstring

    return response
