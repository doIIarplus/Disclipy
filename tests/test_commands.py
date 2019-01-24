import unittest
from src.ChatCommands import ChatCommands as CMD


class TestCommandMatching(unittest.TestCase):
    def test_help(self):
        self.assertTrue(CMD.HELP.match('/help'))
        self.assertFalse(CMD.HELP.match(' /help'))
        self.assertFalse(CMD.HELP.match('/help '))
        self.assertFalse(CMD.HELP.match('/'))
        self.assertFalse(CMD.HELP.match('/h'))
        self.assertFalse(CMD.HELP.match('/he'))
        self.assertFalse(CMD.HELP.match('/hel'))

    def test_list_servers(self):
        self.assertTrue(CMD.LIST_SERVERS.match('/list_servers'))
        self.assertFalse(CMD.LIST_SERVERS.match(' /list_servers'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_servers '))
        self.assertFalse(CMD.LIST_SERVERS.match('/'))
        self.assertFalse(CMD.LIST_SERVERS.match('/l'))
        self.assertFalse(CMD.LIST_SERVERS.match('/li'))
        self.assertFalse(CMD.LIST_SERVERS.match('/lis'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_s'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_se'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_ser'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_serv'))
        self.assertFalse(CMD.LIST_SERVERS.match('/list_serve'))

    def test_list_channels(self):
        self.assertTrue(CMD.LIST_CHANNELS.match('/list_channels'))
        self.assertFalse(CMD.LIST_CHANNELS.match(' /list_channels'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_channels '))
        self.assertFalse(CMD.LIST_CHANNELS.match('/'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/l'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/li'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/lis'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_c'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_ch'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_cha'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_chan'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_chann'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_channe'))
        self.assertFalse(CMD.LIST_CHANNELS.match('/list_channel'))

    def test_join_server(self):
        self.assertTrue(CMD.JOIN_SERVER.match('/join_server 0'))
        self.assertTrue(CMD.JOIN_SERVER.match('/join_server 08'))
        self.assertTrue(CMD.JOIN_SERVER.match('/join_server 189631'))
        self.assertTrue(CMD.JOIN_SERVER.match('/join_server     0    '))
        self.assertFalse(CMD.JOIN_SERVER.match('/join_server          '))
        self.assertFalse(CMD.JOIN_SERVER.match('/join_server '))
        self.assertFalse(CMD.JOIN_SERVER.match('/join_serve dsadasdadasd'))

    def test_join_channel(self):
        self.assertTrue(CMD.JOIN_CHANNEL.match('/join_channel #someserver'))
        self.assertTrue(CMD.JOIN_CHANNEL.match('/join_channel #🤔🤔🤔🤔🤔🤔'))
        self.assertTrue(CMD.JOIN_CHANNEL.match('/join_channel #some-server'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel #some server'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel someserver'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel some-server'))
        self.assertFalse(CMD.JOIN_CHANNEL.match(
            '/join_channel     some-server  ds das d'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel some server'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel          '))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel '))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channe dsadasdadasd'))


if __name__ == '__main__':
    unittest.main()
