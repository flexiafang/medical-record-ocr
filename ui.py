import time
import tkinter as tk
import tkinter.scrolledtext
import tkinter.tix as tix
import tkinter.ttk as ttk


def progressbar():
    for i in range(100):
        progressbar1['value'] = i
        root.update()
        time.sleep(0.01)
    progressbar2.start()


def paint(event):
    print(event)
    x1, y1 = (event.x, event.y)
    x2, y2 = (event.x, event.y)
    canvas.create_rectangle(x1, y1, x2, y2)


def show_popupmenu(event):
    popupmenu.post(event.x_root, event.y_root)

def toplevel():
    top = tk.Toplevel()


root = tix.Tk()
root.geometry('1200x800+100+100')

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='文件', menu=filemenu)
filemenu.add_command(label='打开')
filemenu.add_command(label='新建')
filemenu.add_command(label='保存')
root.config(menu=menubar)

pw = tk.PanedWindow(root, orient='vertical', sashrelief='sunken')
pw.pack(fill='both', expand=1)

separator = ttk.Separator(root).pack(fill='x', padx=5)
status_frame = ttk.Frame(root, relief='raised').pack(fill='x')
label_status = ttk.Label(status_frame, text='状态栏').pack(side='left', fill='x')
sizegrip = ttk.Sizegrip(status_frame).pack(anchor='ne')

pw_1 = tk.PanedWindow(pw, orient='horizontal', sashrelief='sunken')
pw_2 = tk.PanedWindow(pw, orient='horizontal', sashrelief='sunken')
left_frame, right_frame, bottom_frame = ttk.Frame(pw_1, width=500, relief='flat'), \
                                        ttk.Frame(pw_1, height=700, relief='flat'), \
                                        ttk.Frame(pw_2, height=20, relief='flat')
pw.add(pw_1), pw.add(pw_2), pw_1.add(left_frame), pw_1.add(right_frame), pw_2.add(bottom_frame)

button, label, entry, radiobutton, checkbutton = ttk.Button(left_frame, text='按钮', command=progressbar), \
                                                 ttk.Label(left_frame, text='标签'), \
                                                 ttk.Entry(left_frame), \
                                                 ttk.Radiobutton(left_frame, text='选项按钮'), \
                                                 ttk.Checkbutton(left_frame, text='复选框')
button.pack(pady=2), label.pack(pady=2), entry.pack(pady=2), radiobutton.pack(pady=2), checkbutton.pack(pady=2)

scale, labeled_scale, spinbox = tk.Scale(left_frame, from_=0, to=10, length=200, orient='horizontal'), \
                                ttk.LabeledScale(left_frame, from_=0, to=10), \
                                ttk.Spinbox(left_frame, from_=0, to=20, increment=2)
scale.pack(pady=2), labeled_scale.pack(pady=2), spinbox.pack(pady=2)

label_frame = ttk.LabelFrame(left_frame, text='标签框架')
scrollbar = ttk.Scrollbar(label_frame)
listbox = tk.Listbox(label_frame, height=6, width=5, yscrollcommand=scrollbar.set)
for i in range(1, 21):
    listbox.insert('end', i)
scrollbar.config(command=listbox.yview)
label_frame.pack(pady=2), scrollbar.pack(side='right', pady=2, fill='y'), listbox.pack(side='left', pady=2)

stringvar1, stringvar2 = tk.StringVar(), tk.StringVar()
option_menu = ttk.OptionMenu(left_frame, stringvar1, 'Python', 'Python', 'Java', 'Matlab')
combobox = ttk.Combobox(left_frame, textvariable=stringvar2, values=('Python', 'Java', 'Matlab'))
option_menu.pack(pady=2), combobox.pack(pady=2)

progressbar1 = ttk.Progressbar(left_frame, orient='horizontal', value=0, length=200, mode='determinate')
progressbar2 = ttk.Progressbar(left_frame, orient='horizontal', value=0, length=200, mode='indeterminate')
progressbar1.pack(pady=2), progressbar2.pack(pady=2)

menubutton = ttk.Menubutton(right_frame, text='单选按钮')
menubutton.pack()
separator = ttk.Separator(right_frame).pack(fill='x', padx=5)
mb_menu = tk.Menu(menubutton, tearoff=0)
mb_menu.add_command(label='命令按钮')
mb_menu.add_radiobutton(label='单选按钮')
mb_menu.add_checkbutton(label='复选按钮')
mb_menu.add_separator()
mb_menu.add_command(label='退出', command=root.destroy)
menubutton.config(menu=mb_menu)

treeview_sheet = ttk.Treeview(right_frame, height=10, columns=('图标栏'), selectmode='extended')
treeview_sheet.heading('#0', text='图标栏1')
treeview_sheet.heading('#1', text='图标栏2')
for i in range(30):
    treeview_sheet.insert('', index='end', text=i, values=i)
treeview_tree = ttk.Treeview(right_frame, height=10, show='tree')
treeview_tree_parents = treeview_tree.insert('', index='end', text='结构树')
for i in range(30):
    treeview_tree.insert(treeview_tree_parents, index='end', text=i)
treeview_sheet.pack(side='left', padx=5), treeview_tree.pack(side='left', padx=5)

frame_nb1, frame_nb2 = ttk.Frame(right_frame), ttk.Frame(right_frame)
notebook = ttk.Notebook(right_frame, height=200, width=200)
notebook.add(frame_nb1, text='选项卡1'), notebook.add(frame_nb2, text='选项卡2')
notebook.pack(side='left', padx=5)

canvas = tk.Canvas(right_frame, bg='white', height=300, width=300)
canvas.create_line(10, 10, 20, 30, 40, 70)
canvas.bind('<B1-Motion>', paint)
canvas.pack(side='left', padx=5)

text = tkinter.scrolledtext.ScrolledText(bottom_frame, height=5).pack(side='left', fill='both', expand=1)

balloon = tix.Balloon(right_frame)
balloon.bind_widget(menubutton, balloonmsg='这是一个气泡提示')

popupmenu = tk.Menu(root, tearoff=0)
popupmenu.add_command(label='最小化', command=root.iconify)
popupmenu.add_command(label='退出', command=root.destroy)
root.bind('<Button-3>', show_popupmenu)

button_top = ttk.Button(right_frame, text='顶层窗口', command=toplevel)
button_top.pack()

root.mainloop()
