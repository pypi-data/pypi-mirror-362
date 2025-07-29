import json
import os
import queue
import socket
import threading
import time
import unittest

from wmk.messenger import Messenger


class TestMessenger(unittest.TestCase):
    def setUp(self):
        self.server_socket = "/tmp/test_server.sock"
        self.client_socket = "/tmp/test_client.sock"

        # Clean up any existing socket files
        for sock in [self.server_socket, self.client_socket]:
            if os.path.exists(sock):
                os.unlink(sock)

        # Create communication queues
        self.server_messages = queue.Queue()
        self.server_running = True

        # Start server thread
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        # Create messenger instance
        self.messenger = Messenger(
            self.server_socket,
            self.client_socket,
            connection_retry_interval=0.1,
            connection_timeout=1.0,
        )
        self.messenger.register_event_type("test")

        # Wait for server to be ready
        time.sleep(0.5)

    def _run_server(self):
        """Run the test server in a separate thread"""
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(self.server_socket)
        self.server.settimeout(0.1)

        while self.server_running:
            try:
                data, addr = self.server.recvfrom(4096)
                if data:
                    try:
                        message = json.loads(data.decode("utf-8"))
                        self.server_messages.put((message, addr))
                    except json.JSONDecodeError:
                        pass
            except TimeoutError:
                continue
            except Exception as e:
                print(f"Server error: {e}")
                break

        self.server.close()

    def send_from_server(self, message: dict):
        """Helper method to send message from server to client"""
        data = json.dumps(message).encode("utf-8")
        self.server.sendto(data, self.client_socket)

    def get_server_message(self, timeout=1.0):
        """Get next message received by server"""
        try:
            return self.server_messages.get(timeout=timeout)[0]
        except queue.Empty:
            self.fail("Timeout waiting for server message")

    def tearDown(self):
        self.messenger.stop()
        self.server_running = False
        self.server_thread.join(timeout=1.0)

        # Clean up socket files
        for sock in [self.server_socket, self.client_socket]:
            if os.path.exists(sock):
                os.unlink(sock)

    def test_connection_establishment(self):
        """Test that messenger successfully connects to the server"""
        self.messenger.start()
        time.sleep(0.2)  # Allow time for connection
        self.assertTrue(self.messenger.running)
        self.assertIsNotNone(self.messenger.sock)

    def test_message_sending(self):
        """Test sending messages to the server"""
        self.messenger.start()
        time.sleep(0.2)  # Allow time for connection

        test_message = {"type": "test", "data": "hello"}
        self.messenger.send_message(test_message)

        received = self.get_server_message()
        self.assertEqual(received, test_message)

    def test_message_receiving(self):
        """Test receiving and handling messages from the server"""
        received_messages = []

        def message_handler(message):
            received_messages.append(message)

        self.messenger.set_handler("test", message_handler)
        self.messenger.start()
        time.sleep(0.2)

        test_message = {"type": "test", "data": "hello"}
        self.send_from_server(test_message)

        # Wait for message processing
        time.sleep(0.2)

        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0], test_message)

    def test_multiple_listeners(self):
        """Test multiple listeners for the same message type"""
        counter1 = 0
        counter2 = 0

        def handler1(message):
            nonlocal counter1
            counter1 += 1

        def handler2(message):
            nonlocal counter2
            counter2 += 1

        self.messenger.push_handlers(test=handler1)
        self.messenger.push_handlers(test=handler2)
        self.messenger.start()
        time.sleep(0.2)

        test_message = {"type": "test", "data": "hello"}
        self.send_from_server(test_message)

        time.sleep(0.2)

        self.assertEqual(counter1, 1)
        self.assertEqual(counter2, 1)

    def test_listener_removal(self):
        """Test removing message listeners"""
        counter = 0

        def handler(message):
            nonlocal counter
            counter += 1

        self.messenger.set_handler("test", handler)
        self.messenger.start()
        time.sleep(0.2)

        # Send first message
        test_message = {"type": "test", "data": "hello"}
        self.send_from_server(test_message)
        time.sleep(0.2)

        # Remove listener
        self.messenger.remove_handler("test", handler)

        # Send second message
        self.send_from_server(test_message)
        time.sleep(0.2)

        self.assertEqual(counter, 1)

    def test_context_manager(self):
        """Test using messenger as a context manager"""
        with Messenger(self.server_socket, self.client_socket) as messenger:
            time.sleep(0.2)
            self.assertTrue(messenger.running)
            self.assertIsNotNone(messenger.sock)

    def test_partial_message_handling(self):
        """Test handling of partial JSON messages"""
        received_messages = []

        def handler(message):
            received_messages.append(message)

        self.messenger.set_handler("test", handler)
        self.messenger.start()
        time.sleep(0.2)

        # Send a message in parts
        message = {"type": "test", "data": "hello"}
        json_str = json.dumps(message)
        part1 = json_str[:5]
        part2 = json_str[5:]

        self.server.sendto(part1.encode("utf-8"), self.client_socket)
        time.sleep(0.1)
        self.server.sendto(part2.encode("utf-8"), self.client_socket)
        time.sleep(0.2)

        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0], message)

    def test_bidirectional_communication(self):
        """Test both sending and receiving messages"""
        received_messages = []

        def message_handler(message):
            received_messages.append(message)
            # Echo back the message with a different type
            echo = {"type": "echo", "data": message["data"]}
            self.messenger.send_message(echo)

        self.messenger.set_handler("test", message_handler)
        self.messenger.start()
        time.sleep(0.2)

        # Send message from server
        test_message = {"type": "test", "data": "hello"}
        self.send_from_server(test_message)

        # Wait for response
        echo_message = self.get_server_message()

        self.assertEqual(len(received_messages), 1)
        self.assertEqual(received_messages[0], test_message)
        self.assertEqual(echo_message["type"], "echo")
        self.assertEqual(echo_message["data"], "hello")


if __name__ == "__main__":
    unittest.main()
