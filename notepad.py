import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class Notepad(ScrolledText):

    def __init__(self, master, **kw):
        ScrolledText.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-g>', self.gen)
        #generatedText = contentGen("brush makeup for blonds")
        #self.clipboard_append(generatedText)


    def gen(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        generatedText = contentGen(text)
        self.insert('insert', generatedText)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event=None):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event=None):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)


if __name__ == '__main__':
    root = tk.Tk()
    menu = tk.Menu(root)
    root.config(menu=menu)

    root.title('Written in Python')
    root.minsize(width=100, height=100)
    root.geometry('800x500+350+150') #Height, Width, X, Y coordinates of the program

    #NotePad
    notepad = Notepad(root, width=1000, height=100)
    #Height and width of notepad
    notepad.pack()

    editMenu = tk.Menu(menu)
    menu.add_cascade(label="Edit", menu=editMenu)
    editMenu.add_separator()
    editMenu.add_command(label="Cut", command=notepad.cut)
    editMenu.add_command(label="Copy", command=notepad.copy)
    editMenu.add_command(label="Paste", command=notepad.paste)


    root.mainloop()