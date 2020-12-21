import zipfile
import sys
import tkinter as tk
import threading
import queue



class BRUTE_ZIP(object):
    def __init__(self):
        self.flag=False  #  用来判断是否在字典中找到密码，找到标记成True
        self.q=queue.Queue()
        self.thread_list=[]
        window = tk.Tk()
        window.title('暴力破解zip压缩文件小工具1.0')
        window.geometry('500x500')
        self.zip_file=tk.StringVar()
        self.dict_file=tk.StringVar()
        self.dict_file.set('english.dic')
        self.thread_num=tk.IntVar()
        self.thread_num.set(2)
        tk.Label(window,text='压缩文件').place(x=100,y=100)
        tk.Label(window, text='字典文件').place(x=100, y=150)
        tk.Label(window, text='线程数').place(x=100, y=200)
        tk.Entry(window,textvariable=self.zip_file).place(x=150,y=100)
        tk.Entry(window, textvariable=self.dict_file).place(x=150, y=150)
        tk.Entry(window, textvariable=self.thread_num).place(x=150, y=200)
        tk.Label(window, text='输出框').place(x=50, y=300)
        self.t=tk.Text(window,height=3,width=40)
        self.t.place(x=100,y=300)
        tk.Button(window,text='攻击',command=self.run).place(x=250,y=400)
        tk.Button(window,text='结束攻击',command=self.exit_exploit).place(x=300,y=400)
        window.mainloop()
    def brute(self):
        #print('线程')
        try:
            zip=zipfile.ZipFile(self.zip_file.get())
            while True:
                if self.q.empty() or self.flag:
                    break
                password=self.q.get()
                try:
                    zip.extractall(pwd=password.encode('utf-8'))
                    self.t.delete(0.0, 'end')
                    self.t.insert('insert','zip密码：'+password)
                    self.flag=True
                except Exception as e:
                    #print(password)
                    pass

        except Exception as e:
            self.t.delete(0.0,'end')
            self.t.insert('insert','压缩文件不存在')

    def exit_exploit(self):
        sys.exit()
    def run(self):

        try:
            with open(self.dict_file.get(),'r') as fp:
                for password in fp.readlines():
                    self.q.put(password.strip())
        except Exception as e:
            self.t.delete(0.0, 'end')
            self.t.insert('insert', '字典并不存在')
        for i in range(self.thread_num.get()):
            self.thread_list.append(threading.Thread(target=self.brute))
        for i in range(self.thread_num.get()):
            self.thread_list[i].start()

if __name__ == '__main__':
    brute=BRUTE_ZIP()


