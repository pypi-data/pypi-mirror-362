# This file is placed in the Public Domain.


"clients"


import threading
import time


from .handler import Handler


"client"


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.olock  = threading.RLock()
        Fleet.add(self)

    def announce(self, txt):
        pass

    def display(self, event):
        with self.olock:
            for tme in sorted(event.result):
                self.dosay(event.channel, event.result[tme])

    def dosay(self, channel, txt):
        self.say(channel, txt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


"fleet"


class Fleet:

    clients = {}

    @staticmethod
    def add(client):
        Fleet.clients[repr(client)] = client

    @staticmethod
    def all():
        return Fleet.clients.values()

    @staticmethod
    def announce(txt):
        for client in Fleet.all():
            client.announce(txt)

    @staticmethod
    def dispatch(evt):
        client = Fleet.get(evt.orig)
        client.put(evt)

    @staticmethod
    def display(evt):
        client = Fleet.get(evt.orig)
        client.display(evt)

    @staticmethod
    def first():
        clt =  list(Fleet.all())
        res = None
        if clt:
            res = clt[0]
        return res

    @staticmethod
    def get(orig):
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        client = Fleet.get(orig)
        if client:
            client.say(channel, txt)

    @staticmethod
    def shutdown():
        for client in Fleet.all():
            client.stop()

    @staticmethod
    def wait():
        time.sleep(0.1)
        for client in Fleet.all():
            client.wait()


"interface"


def __dir__():
    return (
        'Client',
        'Fleet'
    )
