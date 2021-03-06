from utils import Filehandler
from ConfigParser import SafeConfigParser

class PostboxMgmtFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def help(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        helpmsg = "!postbox list <user> - Check if <user> has a postbox.\n"
        helpmsg += "!postbox add <user> - Add postbox for <user>.\n"
        helpmsg += "!postbox del <user> - Delete postbox for <user>.\n"
        callback.msg(nck, helpmsg)

    def _say(self, callback, channel, msg):
        callback.say(channel, msg)

    def postbox(self, channel, callback, msg=None, pb=None, **kwargs):

        accessfile = pb.accessfile

        #Sanitize msg[1]
        msg[1]=msg[1].translate(None, './')
        if len(msg) < 2:
            self._say(callback, channel, 'Syntax: !postbox list|add|del [user]')

        if msg[0] == 'add':
            mbstatus = self.fhandler.onaccesslist(msg[1], accessfile)
            if mbstatus == 1:
                self._say(callback, channel, '{0} already has a mailbox.'.format(msg[1]))
            elif mbstatus == 0:
                mbstatus = self.fhandler.addtoaccesslist(msg[1], accessfile)
                if mbstatus:
                    self._say(callback, channel, 'Failed to create mailbox.')
                else:
                    self._say(callback, channel, 'Created Mailbox for {0}.'.format(msg[1]))
            else:
                self._say(callback, channel, 'Ooops something is broken')

        elif msg[0] == 'del':
            mbstatus = self.fhandler.deletefromaccesslist(msg[1], accessfile)
            if mbstatus:
                self._say(callback, channel, 'Failed to delete mailbox.')
            else:
                self._say(callback, channel, 'Deleted mailbox for {0}.'.format(msg[1]))

        elif msg[0] == 'list':
            mbstatus = self.fhandler.onaccesslist(msg[1], accessfile)
            if mbstatus < 0:
                self._say(callback, channel, 'Ooops something is broken')
            elif mbstatus == 1:
                self._say(callback, channel, '{0} already has a mailbox.'.format(msg[1]))
            else:
                self._say(callback, channel, '{0} has no mailbox.'.format(msg[1]))

        else:
            self._say(callback, channel, 'Syntax: !postbox list|add|del [user]')
