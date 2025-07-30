# coding: utf-8

from __future__ import absolute_import

from spyne_smev.client import Client


class LogClient(Client):
    """Смэв клиент с логированием
    Для логирования необходимо вызвать log_request

    Пример использования:
    try:
        client.service.SomeMethod(**someparams)
    except SomeException as e:
        error = get_error(e)
    else:
        error = None

    client.log_request("SomeMethod", error)
    """

    # Описание сервиса и его методов
    SERVICE_META = {
        'code': u"",
        'name': u"",
        'methods': {}}

    def log_request(self, method, error=""):
        log_record = self.log_model(
            service_address=self.wsdl.url,
            method_name=method,
            method_verbose_name=self.SERVICE_META['methods'].get(method, ''),
            direction=self.log_model.OUTGOING,
            interaction_type=self.log_model.IS_SMEV,
            request=self.last_sent(method),
            response=self.last_received(method),
            result=error
        )

        log_record.save()

        return log_record

    def last_sent(self, method):
        last_sent = super(LogClient, self).last_sent()

        if last_sent:
            binary_data_element = last_sent.childAtPath(
                'Envelope/Body/{0}/MessageData/AppDocument/BinaryData'.format(
                    method))

            if binary_data_element is not None:
                binary_data_element.setText('')

            text = last_sent.plain()
        else:
            text = u""

        return text

    def last_received(self, method):
        last_received = super(LogClient, self).last_received()

        return last_received.plain() if last_received else u""
