import unittest

from script import encode, decode, shuffle_string, unshuffle_string

MESSAGE = 'This is a long looong test sentence, with some big (biiiiig) words!'


class ShuffleStringTestCase(unittest.TestCase):
    def test_shuffle(self):
        self.assertNotEqual('kayak', shuffle_string('kayak', ['a', 'y', 'a']))
        self.assertNotEqual('rotator', shuffle_string('rotator', ['o', 't', 'a', 't', 'o']))


class UnshuffleStringTestCase(unittest.TestCase):
    def test_unshuffle(self):
        self.assertEqual('kayak', unshuffle_string('kayak', ['kayak', 'kaaak']))
        self.assertEqual('kayak', unshuffle_string('kyaak', ['kayak', 'kaaak']))
        self.assertEqual('kaayk', unshuffle_string('kayak', ['kaayk', 'kyaak']))
        self.assertNotEqual('kaayk', unshuffle_string('kayak', ['kyaak', 'kaayk']))


class EncodeStringTestCase(unittest.TestCase):
    def test_is_encoded(self):
        self.assertNotEqual('this', encode('this'))
        self.assertNotEqual('lonnng', encode('lonnng'))
        self.assertNotEqual('sentence', encode('sentence'))
        self.assertNotEqual('fghjkl, werty', encode('fghjkl, werty'))
        self.assertNotEqual(MESSAGE, encode(MESSAGE))
        self.assertNotEqual('looong', encode('looong'))
        self.assertEqual('\n—weird—\nbiiiig\n—weird—\n', encode('biiiig'))
        self.assertEqual('\n—weird—\nan, a, the, is, of, in\n—weird—\n', encode('an, a, the, is, of, in'))


class DecodeStringTestCase(unittest.TestCase):
    def test_is_decoded(self):
        self.assertEqual(decode(encode(MESSAGE)), MESSAGE)
        self.assertEqual(decode(encode('Mamma Mia!')), 'Mamma Mia!')
        self.assertNotEqual(decode(encode('Mamma Mia!')), 'Maama Mia!')
        self.assertEqual(decode(encode('an, a, the, is, of, in')), 'an, a, the, is, of, in')
        self.assertEqual(decode(encode('long, long, looong story')), 'long, long, looong story')
        self.assertEqual(decode(encode('This test is a good tset example, guess why.')), 'This test is a good tset example, guess why.')
        self.assertNotEqual(decode(encode('This tset is a good test example, guess why.')), 'This tset is a good test example, guess why.')

    def test_decoder_to_fail(self):
        self.assertNotEqual(decode(encode('!@#$%^&* test')), '!@#$%^&* test')


if __name__ == "__main__":
    unittest.main()
