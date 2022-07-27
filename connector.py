import socket
import logging


class Connector:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.socket = None

    def connect(self):
        logging.info("Connecting to printer {0} [{1}:{2}]...".format(self.name, self.ip, self.port))
        self.socket = socket.socket(socket.AF_INET)
        self.socket.settimeout(30)

        try:
            self.socket.connect((self.ip, self.port))
            logging.info("Connected to printer {0} [{1}:{2}].".format(self.name, self.ip, self.port))
            return True
        except (TimeoutError, OSError) as e:
            logging.info("Printer {0} [{1}:{2}] is currently offline.".format(self.name, self.ip, self.port))
            return False

    def send_command(self, command):
        """
        Sends a given command to the connected printer and returns the printers reply.
        :param command: The command that needs to be executed. Example: M115 or M25
        :return: A list of the printers response split by every newline.
        """

        logging.debug("Sending command {0}...".format(command))
        try:
            self.socket.sendall(('~' + command + "\r\n").encode("utf-8"))
            reply = self.socket.recv(1024).decode("utf-8").split("\r\n")
            logging.debug("Printer answered with:\n" + "\n".join(reply))
            return reply
        except socket.timeout:
            return False
        except BrokenPipeError:
            logging.info("Sending command {0} failed: BrokenPipeError - returning False.".format(command))
            return False
        except ConnectionResetError:
            logging.info("Sending command {0} failed: ConnectionResetError - returning False.".format(command))
            return False
        except OSError:
            logging.info("Sending command {0} failed: OSError [Maybe no Route? "
                         "Check network connectivity] - returning False.".format(command))
            return False

    def send_commands(self, commands):
        replies = []
        for entry in commands:
            replies += self.send_command(entry)
        return replies

    def disconnect(self):
        if self.socket:
            self.socket.close()
            logging.info("Connection to printer [{0}:{1}] closed.".format(self.ip, self.port))
