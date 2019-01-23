from src.DefaultEmojis import emojis
import re
import unittest


class TestEmojiFormat(unittest.TestCase):
    def test_string_format(self):
        r = re.compile(r'^:[a-zA-Z0-9\-+_]+:$')
        for emoji in emojis:
            self.assertTrue(bool(r.match(emoji)), emoji)


if __name__ == '__main__':
    unittest.main()
