# coding: utf-8
import datetime
import os

from datatransfer.common import constants
from datatransfer.source import configs as dt_settings
from spyne.decorator import rpc
from spyne.error import Fault

from ..tasks import enroll_get_data_push_task
from .models import EnrollGetDataPushRequest
from .models import EnrollGetDataPushResponse


# pylint:disable=redefined-outer-name
@rpc(EnrollGetDataPushRequest,
     _returns=EnrollGetDataPushResponse)
def EnrollGetDataPush(context, EnrollGetDataPushRequest):
    InMessage = context.udc.in_smev_message
    OutMessage = context.udc.out_smev_message

    response = EnrollGetDataPushResponse()

    response.SessionID = EnrollGetDataPushRequest.SessionID

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
            raise Fault(
                faultcode="INVALID",
                faultstring="Неизвестная мнемоника сервиса"
            )

        if InMessage.Service.Version != constants.DATAPUSH_SERVICE_VERSION:
            raise Fault(
                faultcode="INVALID",
                faultstring="Некорректная версия сервиса"
            )

        if InMessage.Recipient.Code != dt_settings.SMEV_MNEMONICS:
            raise Fault(
                faultcode="INVALID",
                faultstring="Неизвестный получатель"
            )
        auth_key = EnrollGetDataPushRequest.AuthorizationKey
        if not (
            InMessage.Sender.Code == dt_settings.DATATRANSFER_MNEMONICS and
            auth_key == dt_settings.DATAPUSH_AUTHORIZATION_KEY
        ):
            raise Fault(
                faultcode="INVALID",
                faultstring="Неавторизованный запрос"
            )

        now = datetime.datetime.now()
        today = datetime.date.today()

        archive_path = os.path.join(
            dt_settings.STORAGE_MAILBOX_PATH,
            constants.CONFIGURATION_ARCHIVE_IN,
            str(today.year), str(today.month), str(today.day))

        AppDocument = context.udc.in_smev_appdoc
        archive_filename = os.path.join(
            archive_path,
            "{0}_{1}_{2}.zip".format(
                InMessage.Sender.Code, AppDocument.RequestCode,
                now.strftime('%Y%m%d_%H%M%S')))

        try:
            if not os.path.exists(archive_path):
                os.makedirs(archive_path)
            with open(archive_filename, 'w+b') as decoded_file:
                binary_data = AppDocument.BinaryData.data
                if isinstance(binary_data, tuple):
                    binary_data = list(binary_data)
                decoded_file.write(binary_data.pop())
        except Exception as e:
            raise Fault(
                faultcode="FAILURE",
                faultstring="Ошибка доступа к файлу: {0}".format(str(e)),
            )

        if not InMessage.TestMsg:
            enroll_get_data_push_task.apply((
                AppDocument.RequestCode,
                archive_filename,
                EnrollGetDataPushRequest.SessionID
            ), kwargs={})

    except Fault as e:
        OutMessage.Status = e.faultcode
        response.Message = e.faultstring

    return response
