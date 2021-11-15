# tkinter：GUI功能需要
from tkinter import *
import socket
# time：支持时间簇
import time
# threading：支持多线程
import threading
from tkinter import scrolledtext


# 定义一个client类
class client():
    def __init__(self):
        # 创建主窗口
        self.root = Tk()
        # 设置主窗口Title
        self.root.title('Client Dialog')
        # 设置主窗口大小
        self.root.geometry('600x400')
        # 建立socket通讯
        self.sk = socket.socket()
        # 设置IP地址和端口号（默认，可手动配置）
        # 注意：IP地址和端口号存在限制，随意输入可能无法创建socket
        # 1.端口号：不能小于1024（用于标准服务），且不能大于9999，也不能存在冲突
        # 2.IP地址：建议使用默认地址、或者本机IP地址
        self.server_ip = '127.0.0.1'
        self.server_port = int(8888)
        # 创建接收区缓存、发送区缓存
        self.recvbuf = str()
        self.sendbuf = str()
        # StringVar作窗口，跟踪变量值变化
        self.recvstr = StringVar(value=self.recvbuf)
        self.sendstr = StringVar(value=self.sendbuf)
        # 填入默认的ip地址和端口号
        self.ip = StringVar(value=self.server_ip)
        self.port = IntVar(value=self.server_port)
        # 在主窗口上设置5个label的标签（IP地址、端口号、输入框、收到框、通讯记录框）
        self.ip_label = Label(self.root, text='输入服务器IP地址')
        self.port_label = Label(self.root, text='输入服务器端口号(大于1024)')
        self.c_label = Label(self.root, text='输入框')
        self.s_label = Label(self.root, text='当前收到')
        self.recorde_label = Label(self.root, text='通讯记录（连接后显示）')
        # 在主窗口上配置5个文本框（IP地址、端口号、输入框、收到框、通讯记录框）
        self.ip_entry = Entry(self.root, textvariable=self.ip)
        self.port_entry = Entry(self.root, textvariable=self.port)
        self.c_entry = Entry(self.root, textvariable=self.sendstr)
        self.s_entry = Entry(self.root, textvariable=self.recvstr, state='disabled')
        self.recorde = scrolledtext.ScrolledText(self.root, width=50, height=10)
        # 设置2个按钮（建立连接、发送）
        self.btn0 = Button(self.root, text='建立连接', command=lambda: self.started(self.ip, self.port))
        self.btn1 = Button(self.root, text='发送', command=lambda: self.sending(self.sk))
        # 对主窗口进行布局
        # grid(option)
        # row:插件摆放的行，从0开始，默认值为未摆放的下一个数值
        # column：插件摆放的列，从0开始，默认值为0
        self.c_label.grid(row=0, column=0)
        self.c_entry.grid(row=0, column=1)
        self.s_label.grid(row=1, column=0)
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
    def started(self, ip, port):
        # 窗口显示信息
        self.recorde.insert(INSERT, 'waiting...\n')
        # 主动连接ip地址和端口号
        self.sk.connect((self.server_ip, self.server_port))
        # socket发送和接收时间等待时间不能超过20秒
        # s.settimeout(20)
        print('连接成功')
        # 显示连接信息到窗口中，包含动作时间
        self.recorde.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S') + ' connected\n')
        return

    # 发送数据
    def senddata(self, s):
        # 从窗口中获取用户输入
        self.sendbuf = self.sendstr.get()
        # 发送数据
        s.send(bytes(self.sendbuf, 'utf8'))
        # 显示数据，包含时间簇
        self.recorde.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S') + ' 客户端:' + self.sendbuf + '\n')
        return

    # 接收数据
    def recvdata(self, s):
        try:
            # 接收数据
            self.recvbuf = str(s.recv(1024), 'utf8')
            if not self.recvbuf:
                return
            #存入接收区缓存、并显示在窗口中
            self.recvstr.set(self.recvbuf)
            self.recorde.insert(INSERT, time.strftime('%Y-%m-%d %H:%M:%S') + ' 服务器:' + self.recvbuf + '\n')
        # 异常处理处理
        except Exception as e:
            print(e)
        return

    # 对senddata()和recvdata()方法采用多线程
    def sending(self, s):
        threading.Thread(target=self.senddata, args=(s,)).start()
        return

    def recving(self, s):
        threading.Thread(target=self.recvdata, args=(s,)).start()
        return

    # 更新缓存区
    def update(self):
        try:
            self.recving(self.sk)
        except Exception as e:
            print(e)
        self.root.after(500, self.update)
        return


if __name__ == '__main__':
    app = client()
