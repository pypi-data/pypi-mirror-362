import tkinter as tk

def GetScreen(Title, Width, Height):
    global root
    root = tk.Tk()
    root.title(Title)
    root.geometry(f"{Width}x{Height}")

def UpdateScreen():
    global root
    root.update()

def LoopScreen():
    root.mainloop()


def AddTextButton(ButtonID, Xpos, Ypos, text, command):
    text_button_object = tk.Button(root, text=text, command=command)
    text_button_object.place(x=Xpos, y=Ypos)

    globals()[f"{ButtonID}_Button"] = text_button_object

def Config(Obj, ButtonID, Obj_Set_A, Obj_Set_B):
    if Obj == "TextButton":
        if Obj_Set_A == "text":
            globals()[f"{ButtonID}_Button"].config(text=Obj_Set_B)


def GetVersionInfo():
    return "Pre-P-0.0.1", 1