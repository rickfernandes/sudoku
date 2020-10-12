from tkinter import *

main = Tk()

def clearwin(event=None):
    '''Clear the main windows frame of all widgets'''
    pass


def myClick():
    for child in main.winfo_children():
        if(isinstance(child,Label)):
            child.destroy()
    myLabel = Label(main, text='clicked')
    myLabel.pack()

myButton = Button(main, text='click', command=myClick)
myButton.pack()

main.mainloop()