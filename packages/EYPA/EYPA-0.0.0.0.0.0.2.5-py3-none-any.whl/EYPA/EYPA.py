import tkinter as tk
from tkinter import PhotoImage
import time

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
    if Obj == "Character":
        try:
            char_widget = globals()[f"{ID}_Char"]
            current_x = char_widget.winfo_x()
            current_y = char_widget.winfo_y()

            if Obj_Set_A == "Xpos":
                char_widget.place(x=Obj_Set_B, y=current_y)
            elif Obj_Set_A == "Ypos":
                char_widget.place(x=current_x, y=Obj_Set_B)

        except KeyError:
            print(f"Hata: '{ID}_Char' adında bir widget bulunamadı. ID'yi kontrol edin.")
        except Exception as e:
            print(f"Konumlandırma hatası: {e}")
            

def GetInfo(InfoContent):
    global root
    if InfoContent == "Version":
        return "Pre-P-0.0.1", 1
    if InfoContent == "ScreenSize":
        return root.winfo_geometry()

def SetScreenSize(x, y):
    global root
    root.geometry(f"{x}x{y}")

def AddShape(PATH, ImageID, Height, Width):
    Photo = PhotoImage(file=PATH, height=Height, width=Width)
    globals()[f"{ImageID}_Image"] = Photo

def AddCharacter(CharID, ImageID, StartX, StartY):
        Character = tk.Label(root, image=globals()[f"{ImageID}_Image"])
        Character.place(x=StartX, y=StartY)

        globals()[f"{CharID}_Char"] = Character


def Wait(Value, Type):
    if Type == "Second":
        time.sleep(Value)
    if Type == "Minute":
        time.sleep(Value*60)
    if Type == "Hour":
        time.sleep(((Value*60)*60))
    if Type == "SplitSecond":
        time.sleep(Value/60)
    if Type == "SplitSecond":
        time.sleep(Value/60)

def GetCharacterX(CharID):
    return globals()[f"{CharID}_Char"].winfo_x()

def GetCharacterY(CharID):
    return globals()[f"{CharID}_Char"].winfo_y()

