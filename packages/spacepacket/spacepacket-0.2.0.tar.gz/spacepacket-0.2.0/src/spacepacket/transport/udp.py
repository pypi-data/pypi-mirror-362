import socket
import threading
import traceback

from .base import Transport


DEFAULT_MAXIMUM_PACKET_LENGTH = 4096


class UdpTransport(Transport):
    def __init__(
        self, routing=None, maximum_packet_length=DEFAULT_MAXIMUM_PACKET_LENGTH
    ):
        super().__init__()
        self.routing = routing
        self.maximum_packet_length = maximum_packet_length
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._thread = threading.Thread(target=self._incoming_pdu_handler)
        self._thread.kill = False
        self._addr = None

    def bind(self, host, port):
        self._addr = (host, port)
        self._socket.bind((host, port))
        self._thread.kill = False
        self._thread.start()

    def unbind(self):
        self._thread.kill = True
        self._socket.sendto(b"0", self._addr)  # needed to break pdu handler loop
        self._thread.join()
        self._socket.close()

    def request(self, pdu):
        if self.routing and "*" in self.routing:
            for address in self.routing["*"]:
                host, port = address
                port = int(port)
                self._socket.sendto(pdu, (host, port))

    def _incoming_pdu_handler(self):
        thread = threading.current_thread()
        buffer_size = 10 * self.maximum_packet_length

        while not thread.kill:
            try:
                pdu, addr = self._socket.recvfrom(buffer_size)
                if thread.kill:
                    break
                # forward-route the received pdu
                if self.routing and addr in self.routing:
                    for dest in self.routing[addr]:
                        self._socket.sendto(pdu, dest)
                self.indication(pdu)
            except Exception as e:
                print(
                    f"Exception in CustomUdpTransport._incoming_pdu_handler: {e} from {addr}"
                )
                print(traceback.format_exc())
                continue  # Continue listening even after an exception
