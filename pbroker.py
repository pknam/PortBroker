#!/usr/bin/env python3
# author : pknam
# TCP Port broker (local port-forwading)

import socket
import _thread
import signal
import sys

# open "listening_port" serves same functionality of "local_port"
listening_port = 8989
local_port = 80


def sigint_handler(signal, frame):
    print()
    print("[*] Ctrl+C  Pressed")
    sys.exit(0)


def with_cli(in_sock, out_sock):
    while True:
        try:
            data = out_sock.recv(1024)
            if not data:
                break
            in_sock.send(data)
            # print("wc")
        except socket.error as e:
            print(e)
            break
    in_sock.close()
    out_sock.close()
    print("[*] Disconnected")


def with_serv(in_sock, out_sock):
    while True:
        try:
            data = in_sock.recv(1024)
            if not data:
                break
            out_sock.send(data)
            # print("ws")
        except socket.error as e:
            print(e)
            break


input_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
input_s.bind(('', listening_port))
input_s.listen(5)
print("[*] Server Started")
print("[*] {} Port Listening..".format(listening_port))
print("[*] Press Ctrl+C to exit")
signal.signal(signal.SIGINT, sigint_handler)


# support multi-connection
while True:
    conn, addr = input_s.accept()
    conn.settimeout(30)

    output_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    output_s.connect(('127.0.0.1', local_port))
    output_s.settimeout(30)
    print("[*] {} Port Connected".format(local_port))

    _thread.start_new_thread(with_cli, (conn, output_s))
    _thread.start_new_thread(with_serv, (conn, output_s))
