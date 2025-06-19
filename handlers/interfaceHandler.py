import tkinter as tk
from sys import exit
from config.constants import AUFLOESUNG, FONT, TITLEFONT, MINSIZEX, MINSIZEY
from string import punctuation

class Benutzeroberflaeche():
    def __init__(self):
        self.__fenster = tk.Tk()
        self.__fenster.title("Massagerino")
        self.__fenster.geometry(AUFLOESUNG)
        self.__fenster.minsize(MINSIZEX, MINSIZEY)

        self.__fenster.protocol("WM_DELETE_WINDOW", self.beenden)

        self.zeigeLoginScreen()

    def zeigeLoginScreen(self) -> None:
        """
        Vor.: -
        Eff.: Fenster öffnet sich, mit Felder für den Benutzernamen und Passwort
        Erg.: -
        """
        for widget in self.__fenster.winfo_children():
            widget.destroy()

        
        #* Titel:
        tk.Label(
            self.__fenster,
            text = "Messagerino",
            font = TITLEFONT
        ).pack(pady = 20)

        self.__login_frame:tk.Frame = tk.Frame(self.__fenster)
        self.__login_frame.pack(expand = True)
        
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

        #* Registrieren-Knopf
        tk.Button(
            self.__login_frame,
            text = "Registrieren",
            font = FONT,
            command = self.zeigeRegistrierenScreen
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

    def zeigeRegistrierenScreen(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()
        tk.Label(
            self.__fenster,
            text = "Registrieren",
            font = TITLEFONT
        ).pack(pady = 20)
        self.__register_frame:tk.Frame = tk.Frame(self.__fenster)
        self.__register_frame.pack(expand = True)
        
        tk.Label(
            self.__register_frame, 
            text = "Nutzername", 
            font = FONT
        ).pack(pady = 10)
        self.__eingabe_registrieren_benutzer = tk.Entry(self.__register_frame, font = FONT)
        self.__eingabe_registrieren_benutzer.pack()

        tk.Label(
            self.__register_frame, 
            text = "Anzeigename", 
            font = FONT
        ).pack(pady = 10)
        self.__eingabe_registrieren_anzeigename = tk.Entry(self.__register_frame, font = FONT)
        self.__eingabe_registrieren_anzeigename.pack()

        tk.Label(
            self.__register_frame, 
            text = "Passwort", 
            font = FONT
        ).pack(pady = 10)
        self.__input_register_password1 = tk.Entry(self.__register_frame, font = FONT, show = "*")
        self.__input_register_password1.pack()

        tk.Label(
            self.__register_frame, 
            text = "Passwort wiederholen", 
            font = FONT
        ).pack(pady = 10)
        self.__input_register_password2 = tk.Entry(self.__register_frame, font = FONT, show = "*")
        self.__input_register_password2.pack()
        
        self.__fehlermedlung:tk.Label = tk.Label(self.__register_frame, text = "", font = FONT, fg = "red")
        self.__fehlermedlung.pack()

        #* Erstellen-Knopf
        tk.Button(
            self.__register_frame,
            text = "Account erstellen",
            font = FONT,
            command = self.registrieren
        ).pack(pady=15)
    
    def registrieren(self) -> None:

        password1:str = self.__input_register_password1.get().strip()
        password2:str = self.__input_register_password2.get().strip()
        benutzername:str = self.__eingabe_registrieren_benutzer.get().strip()
        anzeigename:str = self.__eingabe_registrieren_anzeigename.get().strip()

        if not password1 or not password2 or  not benutzername or not anzeigename:
            self.__fehlermedlung.config(text = "Unvollständige Eingabe!")
            return
        
        if password1 != password2:
            self.__fehlermedlung.config(text = "Passwort stimmt nicht überein!")
            return
        
        if len(password1) < 8 or len(password2) < 8:
            self.__fehlermedlung.config(text = "Passwort muss mindestens 8 Zeichen lang sein!")
            return
        
        if not any(c.isupper() for c in password1):
            self.__fehlermedlung.config(text = "Das Passwort muss mindestens einen Großbuchstaben enthalten!")
            return
        
        if not any(c in punctuation for c in password1):
            self.__fehlermedlung.config(text = "Mindestens ein Sonderzeichen wie !@#%$ fehlt!")
            return
        

        self.zeigeLoginScreen()



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