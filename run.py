import sys, re, urllib2, json, random, unicodedata, yaml
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup as Soup
from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.web.client import getPage
from twisted.application import internet, service

with open('config.yml') as f:
    config = yaml.load(f.read())
HOST, PORT = config['host'], config['port']

class CaveJohnsonProtocol(irc.IRCClient):
    nickname = 'CaveJohnson'
    password = config['password']
    username = 'CaveJohnson'
    versionName = 'CaveJohnson'
    versionNum = 'v1.0'
    realname = 'Cave Johnson'
 
    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
 
    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        message = message
        if message[0:5] == "!cave":
            id = random.choice(range(116, 191))
            data = json.loads(urllib2.urlopen("http://p2sounds.blha303.com.au/portal2/" + str(id)).read())
            self._send_message(unicodedata.normalize('NFKD', data["text"]).encode('ascii', 'ignore'), channel)

    def _send_message(self, msg, target, nick=None):
        if nick:
            msg = '%s, %s' % (nick, msg)
        self.msg(target, msg)
 
    def _show_error(self, failure):
        return failure.getErrorMessage()
 
class CaveJohnsonFactory(protocol.ReconnectingClientFactory):
    protocol = CaveJohnsonProtocol
    channels = ['#xD']
 
if __name__ == '__main__':
    reactor.connectTCP(HOST, PORT, CaveJohnsonFactory())
    log.startLogging(sys.stdout)
    reactor.run()
 
elif __name__ == '__builtin__':
    application = service.Application('CaveJohnson')
    ircService = internet.TCPClient(HOST, PORT, CaveJohnsonFactory())
    ircService.setServiceParent(application)
