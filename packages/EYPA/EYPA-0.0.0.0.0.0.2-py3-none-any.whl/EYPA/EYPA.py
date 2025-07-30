import tkinter as tk

def GetScreen(Title, Width, Height):
    global root
    root = tk.Tk()
    root.title(Title)
    root.geometry(f"{Width}x{Height}")

def ScreenResizable(Widht, Height):
    global root
    root.resizable(Widht, Height)

def UpdateScreen():
    global root
    root.update()

def LoopScreen():
    root.mainloop()


def AddTextButton(ButtonID, Xpos, Ypos, text, command):
    text_button_object = tk.Button(root, text=text, command=command)
    text_button_object.place(x=Xpos, y=Ypos)

    globals()[f"{ButtonID}_Button"] = text_button_object

def AddTextLabel(LabelID, Xpos, Ypos, text):
    text_label_object = tk.Label(root, text=text)
    text_label_object.place(x=Xpos, y=Ypos)

    globals()[f"{LabelID}_Label"] = text_label_object

def Config(Obj, ID, Obj_Set_A, Obj_Set_B):
    if Obj == "TextButton":
        if Obj_Set_A == "Text":
            globals()[f"{ID}_Button"].config(text=Obj_Set_B)
    if Obj == "TextLabel":
        if Obj_Set_A == "Text":
            globals()[f"{ID}_Label"].config(text=Obj_Set_B)

def GetInfo(InfoContent):
    global root
    if InfoContent == "Version":
        return "Pre-P-0.0.1", 1
    if InfoContent == "ScreenSize":
        return root.winfo_geometry()

def SetScreenSize(x, y):
    global root
    root.geometry(f"{x}x{y}")