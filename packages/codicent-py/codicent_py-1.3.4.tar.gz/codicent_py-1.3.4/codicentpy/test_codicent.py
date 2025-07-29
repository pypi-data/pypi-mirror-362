import unittest
from unittest.mock import patch
from codicentpy import Codicent
import os

class TestCodicent(unittest.TestCase):
    def setUp(self):
        self.token = os.getenv("CODICENT_TOKEN")
        if not self.token:
            raise ValueError("CODICENT_TOKEN environment variable not set")
        self.codicent = Codicent(self.token)

    @patch('codicentpy.requests.post')
    def test_upload(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {"id": "123"}
        file = ("testfile.txt", "dummy content")
        response_id = self.codicent.upload(file)
        self.assertEqual(response_id, "123")
        mock_post.assert_called_once()

    @patch('codicentpy.requests.post')
    def test_post_message(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {"id": "456"}
        message = "Test message"
        response_id = self.codicent.post_message(message)
        self.assertEqual(response_id, "456")
        mock_post.assert_called_once()

    @patch('codicentpy.requests.get')
    def test_get_messages(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"messages": []}
        messages = self.codicent.get_messages()
        self.assertEqual(messages, {"messages": []})
        mock_get.assert_called_once()

    @patch('codicentpy.requests.post')
    def test_post_chat_reply(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.text = "Test reply"
        message = "Svara med exakta texten HEJ"
        reply = self.codicent.post_chat_reply(message)
        print("REPLY====", reply, "====REPLY")
        self.assertIsNotNone(reply["id"])
        self.assertEqual(reply["content"], "HEJ")
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()