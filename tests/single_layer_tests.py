import unittest

from http.server import BaseHTTPRequestHandler, HTTPServer

from flask import jsonify

import server
import socket
from threading import Thread


class MockEmptyServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, "")
        self.end_headers()
        return


# class MockValidServerRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200, "sss")
#         self.end_headers()
#         return
#

def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class SingleJsonLayerTest(unittest.TestCase):
    def setUp(self):
        self.app = server.app.test_client()

    def test_missing_fields(self):
        rv = self.app.get('/single-layer')
        self.assertEqual(400, rv.status_code)
        self.assertEqual(b'Params healthCheckUrl and appName are mandatory', rv.data)

    def test_missing_appName(self):
        rv = self.app.get('/single-layer?healthCheckUrl=abc')
        self.assertEqual(400, rv.status_code)
        self.assertEqual(b'Params healthCheckUrl and appName are mandatory', rv.data)

    def test_missing_healthCheckUrl(self):
        rv = self.app.get('/single-layer?appName=abc')
        self.assertEqual(400, rv.status_code)
        self.assertEqual(b'Params healthCheckUrl and appName are mandatory', rv.data)

    def test_empty_payload(self):
        mock_server_port = get_free_port()
        mock_server = HTTPServer(('localhost', mock_server_port), MockEmptyServerRequestHandler)
        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()

        health_check_url = "http://localhost:" + str(mock_server_port)
        print(health_check_url)

        rv = self.app.get('/single-layer?healthCheckUrl=' + health_check_url + '&appName=abc')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'{\n  "name": "abc"\n}\n', rv.data)

    # def test_valid_payload(self):
    #     mock_server_port = get_free_port()
    #     mock_server = HTTPServer(('localhost', mock_server_port), MockValidServerRequestHandler)
    #     mock_server_thread = Thread(target=mock_server.serve_forever)
    #     mock_server_thread.setDaemon(True)
    #     mock_server_thread.start()
    #
    #     health_check_url = "http://localhost:" + str(mock_server_port)
    #     print(health_check_url)
    #
    #     rv = self.app.get('/single-layer?healthCheckUrl=' + health_check_url + '&appName=abc')
    #     self.assertEqual(200, rv.status_code)
    #     self.assertEqual(b'{\n  "name": "abc"\n}\n', rv.data)


if __name__ == '__main__':
    unittest.main()
