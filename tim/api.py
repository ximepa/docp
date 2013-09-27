# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from djangorpc import RpcRouter, Error, Msg, RpcHttpResponse
from .actions import MainApiClass
from planning.actions import CalendarApiClass

router = RpcRouter('router', {
    'MainApi': MainApiClass(),
    'CalendarApi': CalendarApiClass(),
})

