import tkinter as tk
from tkinter import ttk


class QueueSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic Queue System")
        self.geometry("300x500")
        self.queue = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'h', 'i', 'j', 'k']
        self.current_customer = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # 创建一个标签来显示当前客户
        self.current_label = ttk.Label(self, textvariable=self.current_customer)
        self.current_label.pack(pady=(20, 0))

        # 创建一个列表框来显示等待的客户
        self.waiting_list = tk.Listbox(self, height=5)
        self.waiting_list.pack(pady=(0, 20))

    def call_next(self, info):
        # 如果有等待的客户，则叫下一个
        #if self.queue:
        #next_customer = self.queue.pop(0)
        #self.current_customer.set(next_customer)
        self.current_customer.set(info)
        #self.waiting_list.insert(tk.END, next_customer)

    def end_call(self):
        # 结束当前客户的服务
        if self.queue:
            self.waiting_list.delete(0)
            self.current_customer.set("Waiting for next customer...")

    def add_customer(self):
        # 添加一个新客户到等待列表
        customer_num = len(self.queue) + 1
        new_customer = f"Customer {customer_num}"
        self.queue.append(new_customer)
        self.waiting_list.insert(tk.END, new_customer)


app = QueueSystem()
#app.mainloop()
