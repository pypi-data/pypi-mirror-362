import json
import unittest
from unittest.mock import MagicMock, patch

from src.neural_bridge import NeuralBridge


class TestNeuralBridge(unittest.TestCase):
    @patch('redis.from_url')
    def test_register_capability(self, from_url):
        fake = MagicMock()
        from_url.return_value = fake
        bridge = NeuralBridge(url='redis://test')
        cap = {'id': 'cap:test', 'intent': 'demo'}
        bridge.register_capability(cap)
        fake.hset.assert_called_with('cap:cap:test', mapping=cap)
        fake.publish.assert_called_with('channel:capabilities:new', json.dumps(cap))

    @patch('redis.from_url')
    def test_register_script_capability(self, from_url):
        fake = MagicMock()
        from_url.return_value = fake
        bridge = NeuralBridge(url='redis://test')
        bridge.register_script_capability('cap:s', 'echo hi', intent='demo', parameters=['msg'])
        expected = {
            'id': 'cap:s',
            'intent': 'demo',
            'implementation': {'bash': 'echo hi'},
            'parameters': ['msg'],
        }
        fake.hset.assert_called_with('cap:cap:s', mapping=expected)
        fake.publish.assert_called_with('channel:capabilities:new', json.dumps(expected))

    @patch('redis.from_url')
    def test_handoff_task(self, from_url):
        fake = MagicMock()
        from_url.return_value = fake
        bridge = NeuralBridge(url='redis://test')
        handoff = {'id': 'h1'}
        bridge.handoff_task(handoff)
        fake.publish.assert_called_with('channel:agent:handoff', json.dumps(handoff))

    @patch('redis.from_url')
    def test_listen(self, from_url):
        fake = MagicMock()
        pubsub = MagicMock()
        pubsub.listen.return_value = [{'type': 'message', 'data': json.dumps({'hi': 1})}]
        fake.pubsub.return_value = pubsub
        from_url.return_value = fake
        bridge = NeuralBridge(url='redis://test')
        gen = bridge.listen('demo')
        msg = next(gen)
        self.assertEqual(msg, {'hi': 1})
        gen.close()
        pubsub.subscribe.assert_called_with('demo')

