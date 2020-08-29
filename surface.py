from tkinter import *
from tkinter import filedialog
from tkinter import ttk

from PIL import Image, ImageTk


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        pw = PanedWindow(self.master, orient='horizontal', sashrelief='sunken')
        pw.pack(fill=BOTH, expand=1)

        separator = ttk.Separator(self.master).pack(fill='x', padx=5)
        status_frame = Frame(self.master, relief='raised').pack(fill='x')
        label_status = Label(status_frame, text='状态栏').pack(side='left', fill='x')
        sizegrip = ttk.Sizegrip(status_frame).pack(anchor='ne')

        self.left_frame, self.right_frame = Frame(pw, width=600, relief='flat'), Frame(pw, relief='flat')
        pw.add(self.left_frame), pw.add(self.right_frame)

        self.image_path = StringVar()
        get_img_btn = Button(self.left_frame, text='选择图片', command=self.chooseFile).grid(row=1, column=0)
        img_path_entry = Entry(self.left_frame, width=60, textvariable=self.image_path).grid(row=1, column=1)
        show_img_btn = Button(self.left_frame, text='显示图片', command=self.showImg).grid(row=1, column=2)

    def chooseFile(self):
        file_path = filedialog.askopenfilename(title='选择文件')
        self.image_path.set(file_path)

    def showImg(self):
        load = Image.open(self.image_path.get())
        render = ImageTk.PhotoImage(load)
        img = Label(self.left_frame, image=render)
        img.image = render
        # img.place(x=200, y=100)
        img.grid()


if __name__ == '__main__':
    root = Tk()
    root.geometry('1200x800+100+100')
    root.title('医疗信息识别系统')
    app = Application(master=root)
    root.mainloop()
