import EYPA

VVV, VV = EYPA.GetInfo("Version")
if VV >= 1:

    EYPA.GetScreen("Merhaba EYPA!", "950", "700")
    EYPA.ScreenResizable(False, False)

    Mode = True

    def Button_COMMAND():
        global Mode
        print("OK.")
        if Mode:
            EYPA.Config("TextButton", "ButtonZMMN5567", "Text", "Bana basmak sen, yazı değişmek!")
            Mode = False
        else:
            EYPA.Config("TextButton", "ButtonZMMN5567", "Text", "Bana basarsan yazım değişir!")
            Mode = True

    EYPA.AddTextButton("ButtonZMMN5567", 99, 70, "Bana basarsan yazım değişir!", Button_COMMAND)

    TextLabelLL = EYPA.AddTextLabel("SELAMMMM", 50, 300, "")

    while True:
        EYPA.UpdateScreen()
        XAY = EYPA.GetInfo("ScreenSize")
        X, Y = XAY.split("x", 1)
        EYPA.SetScreenSize(950, Y)
        Y, XX = Y.split("+", 1)
        EYPA.Config("TextLabel", "SELAMMMM", "Text", f"Screen Y size: {Y}")

else:
    print("Not supposed EYPA version!")