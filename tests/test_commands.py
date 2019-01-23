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

    def test_list_guilds(self):
        self.assertTrue(CMD.LIST_GUILDS.match('/list_guilds'))
        self.assertFalse(CMD.LIST_GUILDS.match(' /list_guilds'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_guilds '))
        self.assertFalse(CMD.LIST_GUILDS.match('/'))
        self.assertFalse(CMD.LIST_GUILDS.match('/l'))
        self.assertFalse(CMD.LIST_GUILDS.match('/li'))
        self.assertFalse(CMD.LIST_GUILDS.match('/lis'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_g'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_gu'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_gui'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_guil'))
        self.assertFalse(CMD.LIST_GUILDS.match('/list_guild'))

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

    def test_join_guild(self):
        self.assertTrue(CMD.JOIN_GUILD.match('/join_guild someguild'))
        self.assertTrue(CMD.JOIN_GUILD.match('/join_guild some guild'))
        self.assertTrue(CMD.JOIN_GUILD.match('/join_guild some-guild'))
        self.assertTrue(CMD.JOIN_GUILD.match('/join_guild     some-guild  ds das d'))
        self.assertFalse(CMD.JOIN_GUILD.match('/join_guild          '))
        self.assertFalse(CMD.JOIN_GUILD.match('/join_guild '))
        self.assertFalse(CMD.JOIN_GUILD.match('/join_guil dsadasdadasd'))

    def test_join_channel(self):
        self.assertTrue(CMD.JOIN_CHANNEL.match('/join_channel #someguild'))
        self.assertTrue(CMD.JOIN_CHANNEL.match('/join_channel #🤔🤔🤔🤔🤔🤔'))
        self.assertTrue(CMD.JOIN_CHANNEL.match('/join_channel #some-guild'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel #some guild'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel someguild'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel some-guild'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel     some-guild  ds das d'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel some guild'))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel          '))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channel '))
        self.assertFalse(CMD.JOIN_CHANNEL.match('/join_channe dsadasdadasd'))


if __name__ == '__main__':
    unittest.main()
