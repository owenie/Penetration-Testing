#!/usr/bin/python3.6
# -*- coding=utf-8 -*-

import sys
import socket
import getopt
import threading
import subprocess

listen                  =     False
command                 =     False
upload                  =     False
execute                 =     ""
target                  =     ""
upload_destination      =     ""
port                    =     0

def usage():
    print()
    print("Usage: NetCat.py -t target_host -p port")
    print("-l --listen                    - listen on [host]:[port] for incoming connections")
    print("-e --execute file_to_run        - excute to given file upon receiving a coonection")
    print("-c --command                    - initialize a command shell")
    print("-u --upload destination        - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Client Examples:")
    print("./NetCat.py -t 202.100.1.224 -p 5555")
    print("./NetCat.py -t 202.100.1.224 -p 5555 -u \'upload_src.txt\'")
    print("./NetCat.py -t 202.100.1.224 -p 5555")
    print("Server Examples:")
    print("./NetCat.py -l -p 5555 -c")
    print("./NetCat.py -l -p 5555 -u \'upload_dst.txt\'")
    print("./NetCat.py -l -p 5555 -e \'cat /etc/passwd\'")
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
        #http://blog.csdn.net/tianzhu123/article/details/7655499
        #“hp:i:”
        #短格式 --- h 后面没有冒号：表示后面不带参数，p：和 i：后面有冒号表示后面需要参数
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
    if not listen and len(target) and port > 0 and not upload_destination:
        buffer = input()
        client_sender(buffer)

    if not listen and len(target) and port > 0 and upload_destination:
        upload_file(upload_destination)
        #print(upload_destination)
        #file_to_upload = open(upload_destination, "rb")
        #file_to_upload_fragment = file_to_upload.read(1024)
        #while file_to_upload_fragment:    
        #    client_sender(file_to_upload_fragment)#发送数据分片（如果分片的话）
        #    file_to_upload_fragment = file_to_upload.read(1024)#继续读取数据

    if listen:
        server_loop()

def upload_file(file):#客户端上传文件
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))#连接远端socket
        file_to_upload = open(file, "rb")#读取本地文件
        file_to_upload_fragment = file_to_upload.read(1024)#每次读取1024字节
        while file_to_upload_fragment:    
            client.send(file_to_upload_fragment)#发送数据分片（如果分片的话）
            file_to_upload_fragment = file_to_upload.read(1024)#继续读取数据

    except Exception as e:
        print(e)
        print("[*] Exception! Uploadfile Exiting.")
        client.close()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))#连接到远端socket
        if len(buffer):#首先把传入的buffer，发送到远端的socket
            client.send(buffer.encode())

        while True:
        #下面的操作就是接受客户输入，发送输入数据，并且打印响应数据
            recv_len = 1
            response = ""
            while recv_len:
                data        =    client.recv(4096).decode()
                recv_len    =    len(data)
                response   +=     data

                if recv_len < 4096:
                    break
            print(response,end=" ")

            buffer  = input("")
            buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print(e)
        print("[*] Exception! Exiting.")
        client.close()

def server_loop():
#启动服务器，并且使用多线程调用client_handler来处理客户请求
    global target

    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):#执行命令，并且返回结果
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        #print(e)
        output = "Failed to execute command.\r\n"

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):#如果是上传文件
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)
            print(data)
            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            str_to_send = "Successfully saved file to %s\r\n" % upload_destination
            client_socket.send(str_to_send.encode())
        except Exception as e:
            #print(e)
            str_to_send = "Failed to save file to %s\r\n" % upload_destination
            client_socket.send(str_to_send.encode())

    if len(execute):#如果要执行一个命令，就回显命令结果
        output = run_command(execute)
        client_socket.send(output)

    if command:#如果要shell交互
        while True:
            client_socket.send("<360:#> ".encode())
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()
                try:
                    response = run_command(cmd_buffer)
                    client_socket.send(response)
                except:
                    response = b"Failed to execute command.\n"
                    client_socket.send(response)                

if __name__ == '__main__':
    main()
