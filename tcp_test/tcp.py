import socket
from multiprocessing import Process
import time
from redis import Redis

def send_client_message(clientSocket, clientInfo):
    # 在子进程中循环接受客户端发来的信息，直到客户端发送的为空时,结束接收,并断开连接
    while True:
        try:
            
            recv_data = clientSocket.recv(100)
            
            if len(recv_data) == 0:
                # continue
                break
            else:
                recv_string = recv_data.decode("utf-8","ignore")
                recv_list = recv_string.split(";")
                id = ""
                temperature = ""
                weight = ""
                light = ""

                print("消息来源%s:%s" % (clientInfo, recv_data.decode("utf-8","ignore")))

        except:
            print("An exception occurred")
    print("客户端%s连接断开" % (clientInfo,))
    clientSocket.close()
 
 
def get_client_message(clientSocket, clientInfo):
    # 在子进程中循环接受客户端发来的信息，直到客户端发送的为空时,结束接收,并断开连接
    try:
        while True:
            
            # clientSocket.send("web\r\n".encode("utf-8"))
            send_data = ""
            if (not send_data == None) and send_data != "":
                send_list = send_data.split("|")
                
                for data in send_list:
                    
                    if not len(data.split("#")) == 2:
                        continue
                    id = data.split("#")[0]
                    if not len(id) == 4:
                        continue
                    addr = id[0]+id[1]
                    channel = id[2]+id[3]
                    b = bytes([0,int(addr),int(channel)])
                    data = b + (data.split("#")[1]+"\r\n").encode("utf-8")
                    #r.set("buf", data)
                    clientSocket.send(data)
                #r.set("send_list", "")
            time.sleep(0.01)
    except:
        print("客户端%s连接断开" % (clientInfo,))
        clientSocket.close()
 
 
if __name__ == '__main__':
    # 创建服务端socket对象
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addre = ("0.0.0.0", 8266)
    # 绑定地址和端口号
    serverSocket.bind(addre)
    # 开启监听,数字表示可同时监听的客户端数目
    serverSocket.listen(10)
    while True:
        # 接受客户端的socket对象和客户端ip,端口信息,
        # accept()方法返回的是一个元组,直接进行解包
        #r.set("foo","hhh")
        clientSocket, clientInfo = serverSocket.accept()
        # 创建子进程,并执行任务
        process1 = Process(target=get_client_message, args=(clientSocket, clientInfo))
        process2 = Process(target=send_client_message, args=(clientSocket, clientInfo))
        process1.start()
        # process1.join()
        process2.start()
        # process2.join()
    serverSocket.close()

