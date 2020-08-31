from tkinter import *
from tkinter import scrolledtext, filedialog, messagebox

from PIL import Image, ImageTk
from aip import AipOcr


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.resizable(False, False)
        self.boolShowImg = False
        self.filename = ''
        self.imgDict = {}
        self.createWidget()
        self.pack(side=LEFT, expand=YES, fill=BOTH)

    def createWidget(self):
        f1 = Frame(self)
        self.text = scrolledtext.ScrolledText(f1, width=20, height=12)
        self.text.config(font=('微软雅黑', 10, 'bold'))
        self.text.delete(1.0, END)
        self.text.pack(side=TOP, padx=3, pady=3, expand=YES, fill=BOTH)
        f2 = Frame(f1)
        self.btnOpen = Button(f2, text='打开图片', command=self.openImg)
        self.btnOpen.pack(side=LEFT, padx=3, pady=3, expand=YES, fill=BOTH)
        self.btnSave = Button(f2, text='保存文本', command=self.saveTxt)
        self.btnSave.pack(side=LEFT, padx=3, pady=3, expand=YES, fill=BOTH)
        self.btnShowImg = Button(f2, text='显示图片', state=DISABLED, command=self.showImg)
        self.btnShowImg.pack(side=RIGHT, padx=3, pady=3, expand=YES, fill=BOTH)
        f2.pack(side=BOTTOM, padx=3, pady=3, expand=YES, fill=BOTH)
        f1.pack(side=LEFT, padx=3, pady=3, expand=YES, fill=BOTH)
        self.f3 = Frame(self)
        self.img = Label(self.f3, relief=RIDGE, border=5)
        self.img.pack_forget()
        self.f3.pack_forget()

    def openImg(self):
        if self.text.get(1.0, END) != '\n':
            question = messagebox.askokcancel('是否保存', '检测到文本框中有内容，是否保存？')
            if question:
                self.saveTxt()
                return '保存成功'

        self.filename = filedialog.askopenfilename(title='选择要输出文字的图片',
                                                   defaultextension='.jpg',
                                                   filetypes=[('jpg格式图片', '.jpg'),
                                                              ('png格式图片', '.png'),
                                                              ('所有文件', '.*')])
        if self.filename:
            self.btnOpen.config({'text': '请稍后，图片处理中'})
            self.btnOpen.config({'state': DISABLED})
            txt = self.getWord(self.filename)
            if txt:
                self.text.delete(1.0, END)
                self.text.insert(1.0, txt)
            else:
                self.text.insert(1.0, '未获取到内容')
            self.btnOpen.config({'text': '打开图片'})
            self.btnOpen.config({'state': NORMAL})
        else:
            self.text.insert(1.0, '请选择要输出的图片文件')

    @staticmethod
    def getWord(filename=''):
        result = ''
        APPID = '19612165'
        APIKEY = 'imggz3EqEBHwS3Hqe7Kx6AEq'
        SECRETKEY = 'DlfkAyKxN7Hdl3roThN7QVz99ySSQ0Kq'
        c = AipOcr(APPID, APIKEY, SECRETKEY)
        img = open(filename, 'rb').read()
        message = c.basicGeneral(img)
        for item in message.get('words_result', 'None'):
            result += item['words'] + '\n'
        return result

    def saveTxt(self):
        sfilename = filedialog.asksaveasfilename(title='将图片内文字保存为文本文件',
                                                 defaultextension='.txt',
                                                 filetypes=[('txt文本文件', '.txt'),
                                                            ('所有文件', '.*')])
        if sfilename:
            stxt = self.text.get(1.0, END)
            try:
                with open(sfilename, 'w') as f:
                    f.write(stxt)
                messagebox.showinfo('提示', '文件保存成功')
            except Exception as e:
                messagebox.showinfo('提示', '出错了，可能原因是：{}'.format(str(e)))
        else:
            messagebox.showinfo('提示', '未选择文件名称，保存失败')

    def showImg(self):
        if self.imgDict:
            self.btnShowImg.config({'state': NORMAL})
        if not self.boolShowImg:
            image = Image.open(self.filename)
            resize_img = self.resize(400, 300, image)
            tk_img = ImageTk.PhotoImage(resize_img)
            self.img.config({'image': tk_img})
            self.btnShowImg.config({'text': '隐藏图片'})
            self.boolShowImg = True
            self.img.pack(side=LEFT, expand=YES, fill=BOTH)
            self.f3.pack(side=RIGHT, padx=3, pady=3, fill=BOTH)
            self.master.geometry('1000x300+100+100')
            self.imgDict[self.filename] = tk_img
            return tk_img
        else:
            self.boolShowImg = False
            self.btnShowImg.config({'text': '显示图片'})
            self.img.pack_forget()
            self.f3.pack_forget()
            self.master.geometry('1000x300+100+100')
            return None

    @staticmethod
    def resize(w_box, h_box, image):
        w, h = image.size
        f1 = 1.0 * w_box / w
        f2 = 1.0 * h_box / h
        fac = min([f1, f2])
        width = int(w * fac)
        height = int(h * fac)
        return image.resize((width, height), Image.ANTIALIAS)


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x300+100+100')
    root.title('医疗信息识别系统')
    app = Application(master=root)
    root.mainloop()
