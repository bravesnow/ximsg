# -*- coding: cp936 -*-
import wx,socket
'''���ڿ����'''
class MyFrame(wx.Frame):
    def __init__(self,parent,id):
        #��ʼ������
        wx.Frame.__init__(self,parent,id,"IMClient",size=(600,600))
        #��������
        panel=wx.Panel(self,-1)
        panel.SetBackgroundColour('white')
        #�ڻ����ϣ����찴ť���ı���
        self.button_conn=wx.Button(panel,label='����')
        self.button_send=wx.Button(panel,label='����')
        self.button_recv=wx.Button(panel,label='����')
        self.button_disconn=wx.Button(panel,label='�Ͽ�')
        self.text_content=wx.TextCtrl(panel)
        self.list_history=wx.ListBox(panel,-1,style=wx.LB_SINGLE)
        #�����ߴ������
        hbox=wx.BoxSizer()
        hbox.Add(self.text_content,proportion=1,flag=wx.EXPAND)
        hbox.Add(self.button_send,proportion=0,flag=wx.LEFT,border=5)
        hbox.Add(self.button_recv,proportion=0,flag=wx.LEFT,border=5)        
        ebox=wx.BoxSizer()
        ebox.Add(self.button_conn,proportion=0,flag=wx.LEFT,border=5)
        ebox.Add(self.button_disconn,proportion=0,flag=wx.LEFT,border=5)
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(ebox,proportion=0,flag=wx.TOP,border=5)
        vbox.Add(self.list_history,proportion=1,
                 flag=wx.EXPAND,border=5)
        vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.BOTTOM,border=5)
        panel.SetSizer(vbox)

class MyApp(wx.App):
    def OnInit(self):
        #����ʵ����
        self.frame=MyFrame(parent=None,id=-1)
        self.SetTopWindow(self.frame)
        self.frame.Show()        
        #���¼���Ӧ����
        self.Bind(wx.EVT_BUTTON,self.SendMsg,self.frame.button_send)
        self.Bind(wx.EVT_BUTTON,self.RecvMsg,self.frame.button_recv)
        self.Bind(wx.EVT_BUTTON,self.Connecting,self.frame.button_conn)
        self.Bind(wx.EVT_BUTTON,self.Disconnect,self.frame.button_disconn)
        return True
    def Connecting(self,event):
        self.s=socket.socket()
        host=socket.gethostname()
        port=1234
        self.s.connect((host,port))
        rmsg=self.s.recv(1024)
        self.frame.list_history.Append(rmsg)
        #wx.MessageBox('Connect Success!','MSG:',wx.OK)
    def SendMsg(self,event):
        smsg=self.frame.text_content.GetValue()
        self.s.send(smsg)
        self.frame.list_history.Append('Client:'+smsg)
        #wx.MessageBox("���ͳɹ���","MSG:",wx.OK)
    def RecvMsg(self,event):
        rmsg=self.s.recv(1024)
        self.frame.list_history.Append('Server:'+rmsg)
        #wx.MessageBox(rmsg,"MSG:",wx.OK)
    def Disconnect(self,event):
        pass
        #self.Close(True)
        

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
