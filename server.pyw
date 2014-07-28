# -*- coding: cp936 -*-
import wx,socket
'''窗口框架类'''
class MyFrame(wx.Frame):
    def __init__(self,parent,id):
        #初始化窗口
        wx.Frame.__init__(self,parent,id,"IMServer",size=(600,600))
        #创建画板
        panel=wx.Panel(self,-1)
        panel.SetBackgroundColour('white')
        #在画板上，构造按钮和文本框
        self.button_conn=wx.Button(panel,label="开启服务器")
        self.button_recvconn=wx.Button(panel,label="连接客户端")
        self.button_send=wx.Button(panel,label='发送')
        self.button_recv=wx.Button(panel,label='接收')
        self.button_disconn=wx.Button(panel,label='关闭服务器')
        self.text_content=wx.TextCtrl(panel)
        self.list_history=wx.ListBox(panel,-1,style=wx.LB_SINGLE)
        #创建尺寸管理器
        hbox=wx.BoxSizer()
        hbox.Add(self.text_content,proportion=1,flag=wx.EXPAND)
        hbox.Add(self.button_send,proportion=0,flag=wx.LEFT,border=5)
        hbox.Add(self.button_recv,proportion=0,flag=wx.LEFT,border=5)       
        ebox=wx.BoxSizer()
        ebox.Add(self.button_conn,proportion=1,flag=wx.LEFT,border=5)
        ebox.Add(self.button_recvconn,proportion=1,flag=wx.LEFT,border=5)
        ebox.Add(self.button_disconn,proportion=1,flag=wx.LEFT,border=5)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ebox,proportion=0,flag=wx.EXPAND,border=5)
        vbox.Add(self.list_history,proportion=1,
                 flag=wx.EXPAND,border=5)        
        vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.BOTTOM,border=5)
        panel.SetSizer(vbox)

class MyApp(wx.App):
    def OnInit(self):
        #对象实例画
        self.frame=MyFrame(parent=None,id=-1)
        self.SetTopWindow(self.frame)
        self.frame.Show()        
        #绑定事件响应函数
        self.Bind(wx.EVT_BUTTON,self.SendMsg,self.frame.button_send)
        self.Bind(wx.EVT_BUTTON,self.RecvMsg,self.frame.button_recv)
        self.Bind(wx.EVT_BUTTON,self.Connecting,self.frame.button_conn)
        #self.Bind(wx.EVT_BUTTON,self.RecvConn,self.frame.button_recvconn)
        self.Bind(wx.EVT_BUTTON,self.Disconnect,self.frame.button_disconn)
        return True
    def Connecting(self,event):
        self.s=socket.socket()
        host=socket.gethostname()
        port=1234
        self.s.bind((host,port))
        self.s.listen(5)        
        wx.MessageBox('成功开启服务器！','MSG:',wx.OK)
        exitflag=0
        while exitflag==0:
            self.c,addr=self.s.accept()
            wx.MessageBox('客户端请求连接……','MSG:',wx.OK)
            self.c.send("Welcome to my server!")
            exitflag=1
    def SendMsg(self,event):
        smsg=self.frame.text_content.GetValue()          
        self.c.send(smsg)
        self.frame.list_history.Append("Server:"+smsg)
        #wx.MessageBox('发送成功！','MSG:',wx.OK)
    def RecvMsg(self,event):
        rmsg=self.c.recv(1024)
        self.frame.list_history.Append("Client:"+rmsg)
        #wx.MessageBox(rmsg,"MSG:",wx.OK)
    def Disconnect(self,event):
        self.c.close()

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
