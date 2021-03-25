from tkinter import *
from tkinter import filedialog,colorchooser
from tkinter.filedialog import asksaveasfilename, askopenfilename
import tkinter.messagebox as msgbox
import clipboard as cp
import webbrowser
fileopen = False
clickno = 0

class gui(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("TextPad")
        self.filepath = ""
        self.openedtext = ""
        self.show = BooleanVar()
        self.show.set(True)
        
# drawing widgets
    def draw_menus(self):
        self.filemenu =  Menu(self)
        m1 = Menu(self.filemenu,tearoff=0) 
        m1.add_command(label="New Project",command=lambda : self.new(False))
        m1.add_command(label="Save",command=lambda : self.savefile(False))
        m1.add_command(label="Save As",command=lambda : self.saveasfile(False))
        m1.add_command(label="Open",command=lambda : self.openfile(False))
        m1.add_separator()
        m1.add_command(label="Print",command=lambda : self.print_doc(False))
        m1.add_separator()
        m1.add_command(label="Exit",command=exit)
        self.filemenu.add_cascade(label="File",menu=m1)
        self.config(menu=self.filemenu)
        m2 = Menu(self.filemenu,tearoff=0)  
        
        m2.add_command(label="Undo",command=self.text.edit_undo)
        m2.add_command(label="Redo",command=self.text.edit_redo)
        
        m2.add_separator()
        m2.add_command(label="Cut",command=self.cut)
        m2.add_command(label="Copy",command=self.copy)
        m2.add_command(label="Paste",command=self.paste)
        m2.add_command(label="Delete",command=self.delete)
        m2.add_separator()
        m2.add_command(label="Find",command=lambda:self.find(None))

        m2.add_separator()
        self.filemenu.add_cascade(label="Edit",menu=m2)
        m3 = Menu(self.filemenu,tearoff=0)
        m3.add_checkbutton(label="Word Wrap",onvalue=1,offvalue= 0,variable= self.show,command=self.wrap)
        m3.add_command(label="Dark Theme",command=lambda:self.theme(False,"b"))
        m3.add_command(label="Light Theme",command= lambda:self.theme(False,"w"))
        m3.add_command(label="Font..",command= lambda:self.font(False))
        m3.add_command(label="Text Color",command= lambda:self.fontcolor(False))
        self.filemenu.add_cascade(label="Format",menu=m3)
        m4 = Menu(self.filemenu,tearoff=0)
        m4.add_command(label="Help",command= self.helpwin)
        m4.add_command(label="About TextPad",command=self.aboutwin)
        
        self.filemenu.add_cascade(label="Help",menu=m4)

    def draw_text(self,wraps):
        self.vsb = Scrollbar(self)
        self.hsb = Scrollbar(self, orient="horizontal")
        self.vsb.pack(side="right",fill="y")
        self.hsb.pack(side="bottom",fill="x")
        self.text = Text(self,yscrollcommand = self.vsb.set,xscrollcommand = self.hsb.set,wrap="word",undo=True)
        self.text.pack(fill=BOTH,expand=True)

        self.vsb.configure(command=self.text.yview)
        self.hsb.configure(command=self.text.xview)
    
    # detecting keypresses
    def keypress(self):
        self.bind_all("<Control-Key-s>",self.savefile)
        self.bind_all("<Control-Key-o>",self.openfile)
        self.bind_all("<Control-Key-p>",self.print_doc)
        self.bind_all("<Control-Key-n>",self.new)
        self.bind_all("<Control-S>",self.saveasfile)
        self.bind_all("<Control-Key-z>",self.undo)
        self.bind_all("<Control-Key-y>",self.redo)
        self.bind_all("<Control-Key-q>",self.test)
        self.bind_all("<Control-Key-F>",self.font)
        self.bind_all("<Control-Key-w>",self.wrapText)
        self.bind_all("<Control-Key-d>",lambda eff : self.theme(eff,type="b"))
        self.bind_all("<Control-Key-l>",lambda eff : self.theme(eff,type="w"))
        self.bind_all("<Control-Key-C>",self.fontcolor)

    
    def test(self,event):
        # print(f"123{self.text.get(1.0, END)}123",f"321{fileopen}123")
        # print(f"123{self.filepath}123")
        print(win.filepath == "" )
        print((win.openedtext != win.text.get(1.0, END) and fileopen==True))
       
    # protocols 
    def protocols(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


    # functions

    def set_file_path(self,path):
        
        self.filepath = path

    def new(self,event):
        cando("new")

                
    def savefile(self,event):
        if self.filepath == "":
            filename = asksaveasfilename(filetypes=[('Python Files', '*.py'),("All files","*"),("txt file","*.txt")])
        else:
            filename = self.filepath
        if filename != "":
            with open(filename,"w") as f:
                text2save = str(self.text.get(1.0, END))
                f.write(text2save)
                self.set_file_path(filename)

        
    def openfile(self,event):
        if win.text.get(1.0, END) != "\n" :
            cando("open")
        else:
            openfile()
    
    def saveasfile(self,event):
        filename = asksaveasfilename(filetypes=[('Python Files', '*.py'),("All files","*"),("txt file","*.txt")])
        if filename != "":
            with open(filename,"w") as f:
                text2save = str(self.text.get(1.0, END))
                f.write(text2save)
                self.set_file_path(filename)

    def print_doc(self,event):
        import os,tempfile
        file = tempfile.mktemp(".txt")
        with open(file,"w") as f:
            f.write(self.text.get(1.0, END))
        os.startfile(file, "print")
    def on_closing(self):
        if win.text.get(1.0, END) != "\n":
            cando("quit")
        else:
            exit()

    def cut(self):
        if self.text.selection_get() != "":
            cp.copy(self.text.selection_get())
            self.text.delete("sel.first","sel.last")
        print(self.tell_if_wrap)
        
        
            
    def copy(self):
        if self.text.selection_get():
            cp.copy(self.text.selection_get())
    def paste(self):
        if cp.paste()!="":
            pos = self.text.index(INSERT)
            self.text.insert(pos,cp.paste())
    def delete(self):
        self.text.delete("sel.first","sel.last")
    
    def wrap(self):
        
        if not self.show.get():
            self.text.configure(wrap="none")
        else:
            self.text.configure(wrap="word")
    def wrapText(self,event):
        global clickno
        clickno+=1
        if clickno%2!=0:
            self.text.configure(wrap="none")
        else  :
            self.text.configure(wrap="word")

    def font(self,event):
        print("hi")
        def font_changed(font):
            self.text['font'] = font

        self.tk.call('tk', 'fontchooser', 'configure', '-font', 'helvetica 24', '-command', self.register(font_changed))
        self.tk.call('tk', 'fontchooser', 'show')


    def undo(self,event):
        self.text.edit_undo
    def redo(self,event):
        self.text.edit_redo

    def theme(self,eff,type):
        if type == "b":
            self.text.configure(bg="#a6a6a6")
        elif type == "w":
            self.text.configure(bg="white")
    def fontcolor(self,event):
        mycolor = colorchooser.askcolor()[1]
        self.text.configure(fg=mycolor)
        print(mycolor)
    def helpwin(self):
        newwin = Toplevel(self)
        newwin.title("Help")
        Label(newwin,text="Shortcut keys :- \n\nCtrl+shift+f - Select Font\n\nCtrl+w - Unwrap or Wrap Text\n\nCtrl+d - Enable Dark Mode\n\nCtrl+l - Enable light Mode\n\nctal+shift+c - Choose Font Color ",font="comicsans 10 italic bold").pack()
        
    def aboutwin(self):
        newwin = Toplevel(self)
        newwin.title("About TextPad")
        def openweb():
            webbrowser.open("https://github.com/Charchit-beginner",new=1)
        Label(newwin,text="TextPad \nVersion 1.0.0 cross-platform\nCopyright © 2021 tkinter lovers community. All rights reserved.\n Detected Issues - Font chooser dialog is not working properly in ubuntu and macOS",font="comicsans 13 bold").pack()
        Button(newwin,text="Want to meet developer. Click here!!",command=openweb,font="comicsans 13 ",bg="grey").pack()

    def find(self,event):
        findvar = StringVar()
        newwin = Toplevel(self)
        newwin.title("Find")
        newwin.geometry("350x100")
        newwin.minsize(350,100)
        newwin.maxsize(350,100)
        def find():
            idx = '1.0'
    
            self.text.tag_remove('found', '1.0', END) 
        
            idx = self.text.search(findvar.get(), idx, nocase = 1, 
                                    stopindex = END)
            
            self.text.tag_add("found",idx,f"{idx}+{len(findvar.get())}c")
            self.text.tag_config("found",foreground="red")
            def on_closing():
                self.text.tag_remove("found","1.0",END)
                newwin.destroy()
            newwin.protocol("WM_DELETE_WINDOW", on_closing)
            
        Label(newwin,text="Find What:").grid(row=0,column=0,padx=5)
        Entry(newwin,textvariable=findvar).grid(row=0,column=1,padx=5)
        Button(newwin,text="Find",padx=10,command=find).grid(row=0,column=2,padx=10)



def cando(allow_var):
    if win.filepath == "" or (win.openedtext != win.text.get(1.0, END) and fileopen==True):
        ques = msgbox.askyesnocancel("Notebook","Do you want to save file before continuing")
        if allow_var == "open" :
            if ques == YES:
                win.savefile(False)
                openfile()
            if ques == NO:
                openfile()
                
        elif allow_var=="new":
            if ques == YES:
                win.savefile(False)
                win.text.delete(1.0, END)
            if ques == NO:
                win.text.delete(1.0, END)
        elif allow_var=="quit" :
            if ques == YES:
                win.savefile(1)
                exit()
            if ques == NO:
                exit()
        if ques == "cancel":
            return 
    else:
        if allow_var == "open":
            openfile()
        elif allow_var=="new":
            win.savefile(False)
            win.text.delete(1.0, END)
        elif allow_var=="quit":
            exit()

def openfile():
    global fileopen
    fileopen = True
    filename = askopenfilename( filetypes =[('Python Files', '*.py'),("text file","*.txt"),("All Files","*")])
    if filename != "":
        with open(filename,"r") as f:
            win.text2open = f.read()
            win.text.delete(1.0, END) 
            win.text.insert(END,win.text2open)
            win.set_file_path(filename)
            win.openedtext = win.text2open



if __name__ == '__main__':
    win = gui()
    win.draw_text("none")
    win.draw_menus()
    win.keypress()
    win.protocols()

    win.mainloop()