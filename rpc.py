from djangorpc import RpcRouter, Msg


class MainApiClass(object):

    def hello(self, username, user):
        return Msg(u'Hello, %s!' % username)

rpc_router = RpcRouter({
    'MainApi': MainApiClass(),
})