# tkinter：GUI功能需要
from tkinter import *
import socket
# time：通讯事件携带时间族
import time
# threading：支持多线程
import threading
from tkinter import scrolledtext

import tkinter

# 定义一个server类
class server():
    def __init__(self):
        # 绘制主窗口、设置title、设置主窗口大小
        self.root = Tk()
        self.root.title('Server Dialog')
        self.root.geometry('600x400')

        # 设置默认的IP地址和端口号，可手动配置
        # 注意：IP地址和端口号存在限制，随意输入可能无法创建socket
        # 1.端口号：不能小于1024（用于标准服务），且不能大于9999，也不能存在冲突
        # 2.IP地址：建议使用默认地址、或者本机IP地址
        self.server_ip = '127.0.0.1'
        self.server_port = int(8888)
        # 创建接收区缓存、发送区缓存
        self.recvbuf = str()
        self.sendbuf = str()
        self.recvstr = StringVar(value=self.recvbuf)
        self.sendstr = StringVar(value=self.sendbuf)
        # 设置IP地址和端口号的输入组件。注意：Port的输入默认是Str，需要转到INT
        self.ip = StringVar(value=self.server_ip)
        self.port = IntVar(value=self.server_port)
        # 设置标签
        self.ip_label = Label(self.root, text='输入服务器IP地址')
        self.port_label = Label(self.root, text='输入服务器端口号（需大于1024）')
        self.s_label = Label(self.root, text='输入框')
        self.c_label = Label(self.root, text='当前收到')
        self.recorde_label = Label(self.root, text='通讯记录（连接后显示）')
        # 文本框
        self.ip_entry = Entry(self.root, textvariable=self.ip)
        self.port_entry = Entry(self.root, textvariable=self.port)
        self.c_entry = Entry(self.root, textvariable=self.sendstr)
        self.s_entry = Entry(self.root, textvariable=self.recvstr, state='disabled')
        self.recorde = scrolledtext.ScrolledText(self.root, width=50, height=10)
        # 按钮
        self.btn0 = Button(self.root, text='建立连接', command=lambda: self.starting())
        self.btn1 = Button(self.root, text='发送', command=lambda: self.sending())
        # 窗口布局、排列
        self.s_label.grid(row=0, column=0)
        self.c_entry.grid(row=0, column=1)
        self.c_label.grid(row=1, column=0)
        self.s_entry.grid(row=1, column=1)
        self.btn0.grid(row=2, column=0)
        self.btn1.grid(row=2, column=1)
        self.ip_entry.grid(row=3, column=1)
        self.ip_label.grid(row=3, column=0)
        self.port_entry.grid(row=4, column=1)
        self.port_label.grid(row=4, column=0)
        self.recorde_label.grid(row=5, column=1)
        self.recorde.grid(row=6, column=1)
        # 每0.5s，self组件刷新空间的当前时间簇
        self.root.after(500, self.update)
        # 主事件循环：检测到事件即刷新主窗口
        self.root.mainloop()

    # 开始连接
    def started(self):
        # 创建一个socket
        self.s = socket.socket()
        # 绑定socket的ip地址和端口号
        #self.s.bind(('127.0.0.1', 8888))
        self.s.bind((self.server_ip, self.server_port))
        # 开始进行监听，设置最大监听数：5
        self.s.listen(5)
        # 窗口上显示等待消息
        self.recorde.insert(INSERT, 'waiting...\n')
        # 被动式等待Client端链接
        self.client, self.addr = self.s.accept()
        # 窗口显示ip地址和端口号信息、时间簇
        self.recorde.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S') + '当前连接到IP为' + str(self.addr[0]) + '端口号为' + str(
            self.addr[1]) + '\n')
        return

    # 发送数据
    def senddata(self):
        # 从输入框获取输入字符
        self.sendbuf = self.sendstr.get()
        # 发送数据
        self.client.send(bytes(self.sendbuf, 'utf8'))
        # 窗口显示
        self.recorde.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S') + ' 服务器:' + self.sendbuf + '\n')
        return

    # 接收数据（Server按理先接收、再发送）
    def recvdata(self):
        try:
            # 尝试接收数据
            self.recvbuf = str(self.client.recv(1024), 'utf8')
            # 异常处理机制
            if not self.recvbuf:
                return
            # 保存在接收缓冲区并且打印到窗口中
            self.recvstr.set(self.recvbuf)
            self.recorde.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S') + ' 客户端:' + self.recvbuf + '\n')
        # 异常处理打印
        except Exception as e:
            print(e)
        return

    # 对start(),senddata()和recvdata()方法采用多线程
    def starting(self):
        threading.Thread(target=self.started).start()
        return

    def sending(self):
        threading.Thread(target=self.senddata).start()
        return

    def recving(self):
        threading.Thread(target=self.recvdata).start()
        return

    # 更新缓存区
    def update(self):
        try:
            self.recving()
        except Exception as e:
            print(e)
        self.root.after(500, self.update)
        return


if __name__ == '__main__':
    ser = server()
