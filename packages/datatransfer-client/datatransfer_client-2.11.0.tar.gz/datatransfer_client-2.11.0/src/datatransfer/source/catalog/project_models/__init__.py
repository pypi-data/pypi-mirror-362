# -*- coding: utf-8 -*-


class BaseProjectModels(object):

    class ModelNotFound(Exception):
        u"""Модель не найдена."""

    class SpecificNotFound(Exception):
        u"""Специфика не найдена."""

    # Должне представлять из себя словарь вида
    # {
    #     model_tag: {
    #         specific_tag_1: value1,
    #         specific_tag_2: value2
    #     }
    # }
    rules = {

    }

    @classmethod
    def _get_project_model_specific(cls, model_tag, specific_key):
        u"""Получение специфики для модели.
        :param model_tag: Наименования тега модели.
        :param specific_key: Наименование специфики.
        :return: value or None
        """

        model_specifics = cls.rules.get(model_tag, None)
        if not model_specifics:
            raise cls.ModelNotFound

        specific = model_specifics.get(specific_key, None)
        if not specific:
            raise cls.SpecificNotFound

        return specific

    @classmethod
    def get_model(cls, model_tag):
        return cls._get_project_model_specific(model_tag, "model")

    @classmethod
    def get_unit_filter(cls, model_tag):
        return cls._get_project_model_specific(model_tag, "unit_filter")
