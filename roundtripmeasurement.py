"""
Measure round-trip packet latencies.
"""

import measurement
import socket
import multiprocessing
import time
import pickle
import sys

class RoundTripMeasurement(measurement.Measurement):

    description = """Measure round-trip UDP packet latency.
On your server host, run:
    $ ./echo.py --server
On your client host(s), run:
    $ ./echo.py --client <IP address of server host>
echo.py on your client host will spit out a file containing the round-trip
latencies of each packet received back from the server."""

    def run_client(self, target_address, n_packets, payload_len,
            send_rate_kbytes_per_s, device):
        """
        Start the two client threads: one to send packets, and one to receive them.
        """
        #sock_sgnl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock_sgnl.connect((target_address[0], 8088))
        #print("TCP Signaling Connected...")
        print (str(target_address))
        sender = multiprocessing.Process(
            target=self.send_packets,
            args=(target_address, n_packets, payload_len, send_rate_kbytes_per_s, device))

        #data = sock_sgnl.recv(10)
        listen_port = target_address[1]
        output_filename = self.test_output_filename
        receiver = multiprocessing.Process(
            target=self.recv_packets,
            args=(target_address[0], listen_port, n_packets, payload_len, output_filename))

        sender.start()
        receiver.start()

        sender.join()
        receiver.join()


    @staticmethod
    def pre_send(n_packets, sock_out):
        return

    def run_server(self, listen_port, recv_buffer_size):
        """
        Listen for UDP packets on listen_port, and when a packet is
        received, immediately send it back to the host it came from (to
        port listen_port + 1).
        """
        sock_in = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock_in.bind(("0.0.0.0", listen_port))

        sock_out = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        #sock_sgnl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock_sgnl.bind((socket.gethostname(), 8088))
        #sock_sgnl.listen(2)
        #conn, addr = sock_sgnl.accept()
        print("UDP server running...")
        fist_package = True
        while True:
            try:
                data, recv_addr = sock_in.recvfrom(recv_buffer_size)
                print (str(data))
                if  (str(data)[1]=='*'):
                    continue
                send_addr = (recv_addr[0], listen_port+1)
                if fist_package:
                    #conn.send(str(recv_addr[1]).zfill(10).encode('ascii'))
                    first_package = False
                    ##print (str(send_addr))
                if not data:
                    break
                sock_in.sendto(data, send_addr)
            except KeyboardInterrupt:
                break
        print("Closing...")
        sock_out.close()
        sys.exit(0)

    @classmethod
    def get_packet_payload(cls, packet_n):
        send_time_seconds = time.time()
        payload = pickle.dumps((packet_n, send_time_seconds))
        return payload

    @classmethod
    def recv_packets(cls, recv_addr, listen_port, n_packets_expected, payload_len,
                     output_filename):
        """
        Receive packets bounced back from the server. Calculate the round-trip
        latency for each packet by comparing the transmission timestamp contained
        within the packet to the system time at time of packet receipt.
        """
        print (listen_port)
        sock_in = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock_in.bind(("0.0.0.0", listen_port+1))

        timeout_seconds = 5
        sock_in.settimeout(timeout_seconds)
        send_addr = (recv_addr, listen_port)
        sock_in.sendto('*'*payload_len, send_addr)
        #print ('i was here')
        packets = []
        try:
            while len(packets) < n_packets_expected:
                print (len(packets))
                print (n_packets_expected)
                packet = sock_in.recv(payload_len)
                recv_time = time.time()
                payload = packet.rstrip("a")
                (packet_n, send_time) = pickle.loads(payload)
                latency_us = (recv_time - send_time) * 1e6
                packets.append((packet_n, latency_us))
        except socket.timeout:
            print("Note: timed out waiting to receive packets")
            print("So far, had received %d packets" % len(packets))

        print("Received %d/%d packets back from server" % (len(packets),
                                                           n_packets_expected))

        cls.save_packet_latencies(packets, n_packets_expected, output_filename)
        sock_in.close()
