# -*- coding: utf-8 -*-
from __future__ import absolute_import

from educommon import ioc

from .actions import ErrorDetailPack
from .actions import FeedBackPack
from .actions import StatisticFeedBackPack


def register_actions():

    ioc.get("main_controller").packs.extend([
        FeedBackPack(), StatisticFeedBackPack(), ErrorDetailPack()
    ])
