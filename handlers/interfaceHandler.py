import tkinter as tk
from tkinter import messagebox

AUFLOESUNG:str = "300x200"
FONT:tuple[str,int] = ("Arial",12)

class Benutzeroberflaeche():
    def __init__(self):
        self.__fenster = tk.Tk()
        self.__fenster.title("Massagerino")
        self.__fenster.geometry(AUFLOESUNG)
    
        self.zeigeLoginScreen()

#öffne...Menu - Methoden
    def zeigeLoginScreen(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()
        tk.Label(self.__fenster, text = "Nutzername", font = FONT).pack(pady = 10)
        self.__eingabe_benutzer = tk.Entry(self.__fenster, font = FONT)
        self.__eingabe_benutzer.pack()

        tk.Button(
            self.__fenster,
            text = "Anmelden",
            font = FONT,
            command = self.login
        ).pack(pady=15)
    
    def login(self) -> None:
        benutzername = self.__eingabe_benutzer.get().strip()
        if not benutzername:
            messagebox.showwarning(title = "Einagbefehler", message = "Bitte gib einen Benutzernamen ein.") # type: ignore (für pylance)
            return
        self.__aktueller_benutzer = benutzername

        self.zeigeMainScreen()

    def zeigeMainScreen(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.__fenster,
            text = f"Wilommen, {self.__aktueller_benutzer}!",
            font = FONT
        ).pack(pady=20)

        tk.Button(
            self.__fenster,
            text = "Abmelden",
            font = FONT,
            command = self.zeigeLoginScreen
            ).pack()

    def run(self) -> None:
        self.__fenster.mainloop()

benutzeroberflaeche:Benutzeroberflaeche = Benutzeroberflaeche()