import tkinter as tk
from sys import exit

AUFLOESUNG:str = "1000x1000"
FONT:tuple[str,int] = ("Arial",12)
TITLEFONT:tuple[str, int, str] = ("Arial", 20, "bold")

class Benutzeroberflaeche():
    def __init__(self):
        self.__fenster = tk.Tk()
        self.__fenster.title("Massagerino")
        self.__fenster.geometry(AUFLOESUNG)
    
        self.__fenster.protocol("WM_DELETE_WINDOW", self.beenden)

        self.zeigeLoginScreen()

    def zeigeLoginScreen(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()

        self.__login_frame:tk.Frame = tk.Frame(self.__fenster)
        self.__login_frame.pack(expand = True)

        #* Titel:
        tk.Label(
            self.__fenster,
            text = "Messangerino",
            font = TITLEFONT
        ).pack(pady = 20)
        # *Nutzernamen Zeile: 
        tk.Label(
            self.__login_frame, 
            text = "Nutzername", 
            font = FONT
        ).pack(pady = 10)
        self.__eingabe_benutzer = tk.Entry(self.__login_frame, font = FONT)
        self.__eingabe_benutzer.pack()

        # *Passwort Zeile:
        tk.Label(
            self.__login_frame, text = "Passwort",
            font = FONT
        ).pack(pady = 10)
        self.__eingabe_passwort = tk.Entry(self.__login_frame, font = FONT, show = "*")
        self.__eingabe_passwort.pack()

        # *Anmelden-Knopf
        tk.Button(
            self.__login_frame,
            text = "Anmelden",
            font = FONT,
            command = self.login
        ).pack(pady=15)

        self.__fehlermedlung:tk.Label = tk.Label(self.__login_frame, text = "", font = FONT, fg = "red")
        self.__fehlermedlung.pack()
    
    def login(self) -> None:
        benutzername:str = self.__eingabe_benutzer.get().strip()

        passwort:str = self.__eingabe_passwort.get().strip()

        if not benutzername or not passwort:
            self.__fehlermedlung.config(text = "Bitte gib einen Nutzernamen und ein Passwort ein.")
            return

        self.__aktueller_benutzer = benutzername
        self.__aktuelles_pw = passwort # ! Sicherheit (super-sicher ;) ))
        self.zeigeMainScreen()

    def zeigeMainScreen(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.__fenster,
            text = f"Willkommen, {self.__aktueller_benutzer}!",
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
    
    def beenden(self) ->None:
        exit(0)

benutzeroberflaeche:Benutzeroberflaeche = Benutzeroberflaeche()