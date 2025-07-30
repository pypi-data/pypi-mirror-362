# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os


def get_option(config=None, key=None):
    return getattr(config, key)


# точное наименование модуля настроек
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')


def option_full_name(option):
    # получение полного имени настройки
    return "%s.%s" % (settings_module, option)


# Базовые примитивы и параметры конфигурации специфичные для ИС
ioc_config = {
    # Модель логирования СМЭВ запросов
    "log_model": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "educommon.ws_log.models.SmevLog"
        },
        "web_edu": {
            "__realization__": "educommon.ws_log.models.SmevLog"
        },
        "ssuz": {
            "__realization__": "educommon.ws_log.models.SmevLog"
        },
        "eduadnl": {
            "__realization__": "extedu.ws_logs.utils.LogAdapter"
        },
        "genius": {
            "__realization__": "educommon.ws_log.models.SmevLog"
        },
    },
    # Базовый класс логирующего СМЭВ клиента
    "client_class": {
        "__default__": {
            "__type__": "static",
            "__realization__": "datatransfer.source.transport.smev."
                               "client.base.LogClient",
        },
        "kinder": {},
        "web_edu": {},
        "ssuz": {},
        "eduadnl": {},
        "genius": {},
    },
    # Базовый класс логирующей асинхронной задачи
    "task_class": {
        "__default__": {
            "__type__": "static",
        },
        "kinder": {
            "__realization__": "kinder.core.async_tasks.tasks.AsyncTask"
        },
        "web_edu": {
            "__realization__": "web_edu.core.async_task.tasks.AsyncTask"
        },
        "ssuz": {
            "__realization__": "ssuz.async_tasks.tasks.AsyncTask"
        },
        "eduadnl": {
            "__realization__": "educommon.async_tasks.tasks.AsyncTask"
        },
        "genius": {
            "__realization__": "educommon.async.tasks.AsyncTask"
        },
    },
    # Правила извлечения и преобразования данных (KTE)
    "kte_extractor_mapping_rules": {
        "__default__": {
            "__type__": "static"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.etl.kte.sendpacket.mapping.rules"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.etl.kte.sendpacket.mapping.rules"
        },
        "kinder": {
            "__realization__": "kinder.plugins.contingent.etl.kte.sendpacket.mapping.rules"
        },
    },
    # Правила извлечения и преобразования данных (DataTransfer)
    "dt_extractor_mapping_rules": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.plugins.contingent.etl.bars.datatransfer.mapping.rules"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.etl.bars.datatransfer.mapping.rules"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.etl.bars.datatransfer.mapping.rules"
        },
        "eduadnl": {
            "__realization__": "extedu.contingent.etl.bars.datatransfer.mapping.rules"
        },
        "genius": {
            "__realization__": "genius.contingent.etl.bars.datatransfer.mapping.rules"
        }
    },
    # Правила извлечения и преобразования данных (GetData)
    "get_data_mapping_rules": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.plugins.contingent.etl.bars.getdata.mapping.rules"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.etl.bars.getdata.mapping.rules"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.etl.bars.getdata.mapping.rules"
        },
        "eduadnl": {
            "__realization__": "extedu.contingent.etl.bars.getdata.mapping.rules"
        },
        "genius": {
            "__realization__": "genius.contingent.etl.bars.getdata.mapping.rules"
        }
    },
    # Правила извлечения и преобразования данных о привилегиях (GetPrivilege)
    # TODO добавить, когда плагин будет подключен в другие РИС
    #     "kinder": {
    #         "__realization__": "kinder.plugins.contingent.etl.bars.getprivilege.mapping.rules"
    #     },
    # Правила извлечения данных (GetPrivilege)
    "get_privilege_mapping_rules": {
        "__default__": {
            "__type__": "static"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.etl.bars.getprivilege.mapping.rules"
        },
    },
    # Правила сопоставления вернувшейся от КО льготы (код льготы в справочнике Privilege)
    # и id льготы в локальном справочнике Exemption (GetPrivilege)
    "get_privilege_mapping": {
        "__default__": {
            "__type__": "static"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.etl.bars.getprivilege.mapping.privilege_mapping"
        },
    },
    # Модель ФЛ
    "person_models": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.core.children.models.Children"
        },
        "web_edu": {
            "__realization__": "web_edu.core.person.models.Person"
        },
        "ssuz": {
            "__realization__": "ssuz.student.models.Student"
        },
        "eduadnl": {
            "__realization__": "extedu.person.models.Person"
        },
        "genius": {
            "__realization__": "genius.person.models.Person"
        }
    },
    # Модель документов ФЛ
    "document_models": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.core.children.models.Children"
        },
        "web_edu": {
            "__realization__": "web_edu.core.person.models.PersonCertificate"
        },
        "ssuz": {
            "__realization__": "ssuz.student.student_docs.models.StudentPersonConfirmDocument"
        },
        "eduadnl": {
            "__realization__": "extedu.core.models.Document"
        },
        "genius": {
            "__realization__": "genius.core.models.Document"
        }
    },
    # Модель пользовательского профиля
    "userprofile_models": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.users.models.UserProfile"
        },
        "web_edu": {
            "__realization__": "web_edu.core.users.models.UserProfile"
        },
        "ssuz": {
            "__realization__": "ssuz.users.models.UserProfile"
        },
        "eduadnl": {
            "__realization__": "extedu.user.models.User"
        },
        "genius": {
            "__realization__": "genius.user.models.User"
        }
    },
    # Специфики модели проектов
    "project_models_class": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.plugins.contingent.etl.bars.feedback.mapping.ProjectModels"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.etl.bars.feedback.mapping.ProjectModels"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.etl.bars.feedback.mapping.ProjectModels"
        },
        "eduadnl": {
            "__realization__": "extedu.contingent.etl.bars.feedback.mapping.ProjectModels"
        },
        "genius": {
            "__realization__": "genius.contingent.etl.bars.feedback.mapping.ProjectModels"
        }
    },
    # Права на пак
    "feedback_pack_permissions": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "datatransfer.source.catalog.permissions.KINDER_SUB_PERMISSIONS"
        },
        "web_edu": {
            "__realization__": "datatransfer.source.catalog.permissions.SCHOOL_SUB_PERMISSIONS"
        },
        "ssuz": {
            "__realization__": "datatransfer.source.catalog.permissions.COLLEGE_SUB_PERMISSIONS"
        },
        "eduadnl": {
            "__realization__": "datatransfer.source.catalog.permissions.EXTEDU_SUB_PERMISSIONS"
        },
        "genius": {
            "__realization__": "datatransfer.source.catalog.permissions.GENIUS_SUB_PERMISSIONS"
        }
    },
    # Права на пак отправки данных в КТЕ
    "kte_pack_permissions": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "datatransfer.source.permissions.KTE_SUB_PERMISSIONS"
        },
        "web_edu": {
            "__realization__": "datatransfer.source.permissions.WEB_EDU_KTE_SUB_PERMISSIONS"
        },
        "ssuz": {
            "__realization__": "datatransfer.source.permissions.KTE_SUB_PERMISSIONS"
        },
        "eduadnl": {
            "__realization__": "datatransfer.source.permissions.KTE_SUB_PERMISSIONS"
        },
        "genius": {
            "__realization__": "datatransfer.source.permissions.KTE_SUB_PERMISSIONS"
        }
    },
    "kte_organization_select_pack": {
        "__default__": {
            "__type__": "static"
        },
        "web_edu": {
            "__realization__": "web_edu.core.school.actions.SchoolDictROPack"
        },
        "kinder": {
            "__realization__": "kinder.core.unit.actions.UnitDictPack"
        },
        "ssuz": {
            "__realization__": "ssuz.unit.change_unit_status.actions.ProxyUnitPack"
        },
    },
    # Функция получения текущего учреждения в системе
    "current_unit_function": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": "kinder.core.helpers.get_current_unit"
        },
        "web_edu": {
            "__realization__": "web_edu.core.school.helpers.get_current_school"
        },
        "ssuz": {
            "__realization__": "ssuz.global_state.get_current_unit"
        }
    },
    "get_data_extensions": {
        "__default__": {
            "__type__": "static"
        },
        "eduadnl": {
            "__realization__": "extedu.contingent.get_data.changes.extensions.Extensions"
        },
        "kinder": {
            "__realization__": "kinder.plugins.contingent.get_data.changes.extensions.Extensions"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.get_data.changes.extensions.Extensions"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.ssuz_get_data.changes.extensions.Extensions"
        },
        "genius": {
            "__realization__": "genius.contingent.get_data.changes.extensions.Extensions"
        },
    },
    # Настройки заполнения полей для get_data
    "get_data_config": {
        "__default__": {
            "__type__": "static",
        },
        "eduadnl": {
            "__realization__": "extedu.contingent.get_data.settings.ExtEduSettingsConfig"
        },
        "kinder": {
            "__realization__": "kinder.plugins.contingent.get_data.settings.KinderSettingsConfig"
        },
        "web_edu": {
            "__realization__": "web_edu.plugins.contingent.get_data.settings.WebEduSettingsConfig"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.ssuz_get_data.settings.SsuzSettingsConfig"
        },
        "genius": {
            "__realization__": "genius.contingent.get_data.settings.GeniusSettingsConfig"
        },
    },
    # "Живые" настройки ЭШ
    "liveconfig": {
        "__default__": {
            "__type__": "static",
        },
        "config": {
            "__realization__": "web_edu.livesettings.config"
        },
    },
    # Системная мнемоника
    "smev_mnemonics": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": option_full_name("SMEV_SYS_MNEMONICS")
        },
        "web_edu": {
            "__type__": "singleton",
            "__realization__": "datatransfer.source.common.configuration.configuration.get_option",
            "config:liveconfig": "config",
            "$key": "SMEV_SYS_MNEMONICS"
        },
        "ssuz": {
            "__realization__": option_full_name("SMEV_SYS_MNEMONICS")
        },
        "eduadnl": {
            "__realization__": option_full_name("SMEV_SYS_MNEMONICS")
        },
        "genius": {
            "__realization__": option_full_name("SMEV_SYS_MNEMONICS")
        }
    },
    # Системное имя
    "smev_name": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": option_full_name("SMEV_SYS_NAME")
        },
        "web_edu": {
            "__type__": "singleton",
            "__realization__": "datatransfer.source.common.configuration.configuration.get_option",
            "config:liveconfig": "config",
            "$key": "SMEV_SYS_NAME"
        },
        "ssuz": {
            "__realization__": option_full_name("SMEV_SYS_NAME")
        },
        "eduadnl": {
            "__realization__": option_full_name("SMEV_SYS_NAME")
        },
        "genius": {
            "__realization__": option_full_name("SMEV_SYS_NAME")
        }


    },
    # Контейнер содержащий сертификат и закрытый ключ
    "smev_pem": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": option_full_name("SMEV_CERT_AND_KEY")
        },
        "web_edu": {
            "__type__": "singleton",
            "__realization__": "datatransfer.source.common.configuration.configuration.get_option",
            "config:liveconfig": "config",
            "$key": "SMEV_CERT_AND_KEY"
        },
        "ssuz": {
            "__realization__": option_full_name("SMEV_CERT_AND_KEY")
        },
        "eduadnl": {
            "__realization__": option_full_name("SMEV_CERT_AND_KEY")
        },
        "genius": {
            "__realization__": option_full_name("SMEV_CERT_AND_KEY")
        }
    },
    # Пароль закрытого ключа
    "smev_private_key_password": {
        "__default__": {
            "__type__": "static"
        },
        "kinder": {
            "__realization__": option_full_name("SMEV_PRIVKEY_PASS")
        },
        "web_edu": {
            "__type__": "singleton",
            "__realization__": "datatransfer.source.common.configuration.configuration.get_option",
            "config:liveconfig": "config",
            "$key": "SMEV_PRIVKEY_PASS"
        },
        "ssuz": {
            "__realization__": option_full_name("SMEV_PRIVKEY_PASS")
        },
        "eduadnl": {
            "__realization__": option_full_name("SMEV_PRIVKEY_PASS")
        },
        "genius": {
            "__realization__": option_full_name("SMEV_PRIVKEY_PASS")
        }
    },
    # Обратная связь при зачислении абитуриентов.
    "enroll_get_data_mapping_rules": {
        "__default__": {
            "__type__": "static"
        },
        "ssuz": {
            "__realization__": "ssuz.plugins.contingent.etl.bars.enrollgetdata.mapping.rules"
        },
    }
}
