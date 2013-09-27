# -*- encoding: utf-8 -*-
__author__ = 'maxim'

# -*- encoding: utf-8 -*-
from rpc import Error, Msg, RpcHttpResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from datetime import datetime
import time
from abills.models import User

class MainApiClass(object):

    def hello(self, user):
        return Msg("Hello")

    def find_login(self, term, user):
        return [u['login'] for u in list(User.objects.filter(login__icontains=term).values('login'))]

    def find_pi(self, login, user):
        try:
            u = User.objects.get(login__iexact=login)
        except User.DoesNotExist:
            return Error("user `%s` not found" % login)
        else:
            return {
                'success': True,
                'login': u.login,
                'address': "%s %s" % (u.pi.street.name, u.pi.house.name),
                'kv': u.pi.kv,
            }