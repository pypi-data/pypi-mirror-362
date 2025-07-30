# coding: utf-8
from __future__ import absolute_import

from io import StringIO
import datetime
import json

from lxml import etree
from suds.plugin import MessagePlugin
import six

from datatransfer.common import constants
from datatransfer.common.helpers import get_error
from datatransfer.source import configs as dt_settings
from datatransfer.source.common.configuration import get_object


LoggedClient = get_object('client_class')
LoggedClient.log_model = get_object('log_model')


class ResponseHandler(object):

    extracted_values = {
        'TicketGUID': six.text_type,
        'MessageText': six.text_type,
        'Errors': six.text_type,
        'RetryAfter': int,
        'Status': six.text_type
    }

    def __init__(self, response):
        f = StringIO(response.decode('utf-8'))
        tree = etree.parse(f)

        for k, v in six.iteritems(self.extracted_values):
            element = tree.find(".//%s" % k)
            if element is not None:
                setattr(self, k, self.extracted_values[k](element.text))


class FixSendPacketRequest(MessagePlugin):

    def marshalled(self, context):
        request = context.envelope.childAtPath('/Body/SendPacketRequest')
        if request is None:
            return
        message = context.envelope.childAtPath(
            '/Body/SendPacketRequest/Message'
        )
        message_data = context.envelope.childAtPath(
            '/Body/SendPacketRequest/MessageData'
        )
        app_data = context.envelope.childAtPath(
            '/Body/SendPacketRequest/MessageData/AppData'
        )
        ais_guid = context.envelope.childAtPath(
            '/Body/SendPacketRequest/MessageData/AppData/AIS_GUID'
        )
        (kte_prefix, _) = request.namespace()
        (smev_prefix, _) = app_data.namespace()
        message.walk(lambda this: this.setPrefix(smev_prefix))
        message_data.setPrefix(smev_prefix)
        app_data.setPrefix(smev_prefix)
        app_data.set('xsi:type', '{0}:SendPacketRequest'.format(kte_prefix))
        ais_guid.setPrefix(kte_prefix)


class FixGetResultRequest(MessagePlugin):

    def marshalled(self, context):
        request = context.envelope.childAtPath('/Body/GetResultRequest')
        if request is None:
            return
        message = context.envelope.childAtPath(
            '/Body/GetResultRequest/Message'
        )
        message_data = context.envelope.childAtPath(
            '/Body/GetResultRequest/MessageData'
        )
        app_data = context.envelope.childAtPath(
            '/Body/GetResultRequest/MessageData/AppData'
        )
        ticket_guid = context.envelope.childAtPath(
            '/Body/GetResultRequest/MessageData/AppData/TicketGUID'
        )
        (kte_prefix, _) = request.namespace()
        (smev_prefix, _) = app_data.namespace()
        message.walk(lambda this: this.setPrefix(smev_prefix))
        message_data.setPrefix(smev_prefix)
        app_data.setPrefix(smev_prefix)
        app_data.set('xsi:type', '{0}:GetResultRequest'.format(kte_prefix))
        ticket_guid.setPrefix(kte_prefix)


class KteLabsClient(LoggedClient):
    """СМЭВ клиент сервиса КТЕ Лабс"""

    # Описание сервиса и его методов
    SERVICE_META = {
        'code': u"KteLabs",
        'name': u"Сервис интеграции с Контингентом КТЕ Лабс",
        'methods': {
            'SendPacket': u"Передача пакета данных (Контингент КТЕ Лабс)"}}

    def __init__(self, *args, **kwargs):
        params = dict(
            url=dt_settings.DATATRANSFER_WSDL,
            timeout=dt_settings.WEBSERVICE_TIMEOUT,
            private_key_path=dt_settings.SMEV_PRIVATE_KEY_FILE,
            private_key_pass=dt_settings.SMEV_PRIVATE_KEY_PASSWORD,
            certificate_path=dt_settings.SMEV_CERTIFICATE_FILE,
            in_certificate_path=dt_settings.SMEV_CERTIFICATE_FILE,
            digest_method=str(dt_settings.SMEV_DIGEST_METHOD),
            plugins=[FixSendPacketRequest(), FixGetResultRequest()],
            retxml=True,
            autoblend=True)

        super(KteLabsClient, self).__init__(**params)

    def SendPacket(self, encoded_file_name, request_code):
        method = 'SendPacketRequest'

        request = self.factory.create(method)

        request.Message.Sender.Code = (
            dt_settings.SMEV_MNEMONICS)
        request.Message.Sender.Name = (
            dt_settings.SMEV_NAME)

        request.Message.Recipient.Code = (
            dt_settings.DATATRANSFER_MNEMONICS)
        request.Message.Recipient.Name = (
            dt_settings.DATATRANSFER_NAME)

        request.Message.ServiceName = dt_settings.DATATRANSFER_MNEMONICS
        request.Message.TypeCode = constants.SMEV_TYPE_CODE
        request.Message.Status = constants.SMEV_STATUS
        request.Message.Date = datetime.datetime.now()
        request.Message.ExchangeType = 1

        request.MessageData.AppData.AIS_GUID = dt_settings.KTE_AIS_GUID
        request.MessageData.AppDocument.RequestCode = request_code

        with open(encoded_file_name, "r") as f:
            request.MessageData.AppDocument.BinaryData = f.read()

        response = None
        error = None
        try:
            response = self.service.SendPacket(
                request.Message,
                request.MessageData
            )
        except Exception as e:
            error = get_error(e)

        self.log_request(method, error=error)

        handler = ResponseHandler(response)

        ticket_guid = getattr(handler, 'TicketGUID', None)

        return ticket_guid

    def GetResult(self, ticket_guid):
        method = 'GetResultRequest'

        request = self.factory.create(method)

        request.Message.Sender.Code = (
            dt_settings.SMEV_MNEMONICS)
        request.Message.Sender.Name = (
            dt_settings.SMEV_NAME)

        request.Message.Recipient.Code = (
            dt_settings.DATATRANSFER_MNEMONICS)
        request.Message.Recipient.Name = (
            dt_settings.DATATRANSFER_NAME)

        request.Message.ServiceName = dt_settings.DATATRANSFER_MNEMONICS
        request.Message.TypeCode = constants.SMEV_TYPE_CODE
        request.Message.Status = constants.SMEV_STATUS
        request.Message.Date = datetime.datetime.now()
        request.Message.ExchangeType = 1

        request.MessageData.AppData.TicketGUID = ticket_guid

        response = None
        error = None
        try:
            response = self.service.GetResult(
                request.Message,
                request.MessageData
            )
        except Exception as e:
            error = get_error(e)

        log = self.log_request(method, error=error)

        handler = ResponseHandler(response)

        message_text = getattr(handler, 'MessageText', None)
        errors = getattr(handler, 'Errors', None)
        retry_after = getattr(handler, 'RetryAfter', None)
        status = getattr(handler, 'Status', None)

        log.response = response
        log.result = message_text
        if errors:
            log.result += u'\nОшибки:\n'
            fmt = u'{error} (блок: {object-type}, id: {uid} поле: {field})'
            log.result += u'\n'.join(
                fmt.format(**err) for err in json.loads(errors)
            )
        log.save()

        return (message_text,
                errors,
                retry_after,
                status)
