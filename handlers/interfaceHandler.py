import tkinter as tk
from tkinter import ttk
from sys import exit
from config.constants import AUFLOESUNG, FONT, TITLEFONT, MINSIZEX, MINSIZEY
from custom_types.baseTypes import User
from helpers.validationHelper import validatePassword, validateUser

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
        self.__entryLoginPassword = tk.Entry(self.__login_frame, font = FONT, show = "*")
        self.__entryLoginPassword.pack()
        
        # *Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        checkboxShowPassword = ttk.Checkbutton(
            self.__login_frame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.togglePassword
        ).pack(pady = 15)

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

        self.__fehlermeldung:tk.Label = tk.Label(self.__login_frame, text = "", font = FONT, fg = "red")
        self.__fehlermeldung.pack()

        #! Debug-Anmeldungs-Knopf
        tk.Button(
            self.__login_frame,
            text = "Debug (Anmeldung)",
            font = FONT,
            command = self.debugLogin
        ).pack(pady=15)

        self.__fehlermeldung:tk.Label = tk.Label(self.__login_frame, text = "", font = FONT, fg = "red")
        self.__fehlermeldung.pack()
        
    def togglePassword(self) -> None:
        if self.showPasswordVar.get():
            self.__entryLoginPassword.config(show="")
        else:
            self.__entryLoginPassword.config(show="*")
    
    def toggleRegisterPassword(self) -> None:
        if self.showPasswordVar.get():
            self.__entryRegisterPassword1.config(show="")
            self.__entryRegisterPassword2.config(show="")
        else:
            self.__entryRegisterPassword1.config(show="*")
            self.__entryRegisterPassword2.config(show="*")

   
    def login(self) -> None:
        benutzername:str = self.__eingabe_benutzer.get().strip()

        passwort:str = self.__entryLoginPassword.get().strip()

        if not benutzername or not passwort:
            self.__fehlermeldung.config(text = "Bitte gib einen Nutzernamen und ein Passwort ein.")
            return

        self.__currentUser: User = User(UUID=-1, username=benutzername, displayName=benutzername)
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
        self.__entryRegisterPassword1 = tk.Entry(self.__register_frame, font = FONT, show = "*")
        self.__entryRegisterPassword1.pack()

        tk.Label(
            self.__register_frame, 
            text = "Passwort wiederholen", 
            font = FONT
        ).pack(pady = 10)
        self.__entryRegisterPassword2 = tk.Entry(self.__register_frame, font = FONT, show = "*")
        self.__entryRegisterPassword2.pack()
        
        self.__fehlermeldung:tk.Label = tk.Label(self.__register_frame, text = "", font = FONT, fg = "red")
        self.__fehlermeldung.pack()
        
        # *Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        checkboxShowPassword = ttk.Checkbutton(
            self.__register_frame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.toggleRegisterPassword
        ).pack(pady = 15)

        #* Erstellen-Knopf
        tk.Button(
            self.__register_frame,
            text = "Account erstellen",
            font = FONT,
            command = self.registrieren
        ).pack(pady=15)
    
    def registrieren(self) -> None:

        password1:str = self.__entryRegisterPassword1.get().strip()
        password2:str = self.__entryRegisterPassword2.get().strip()
        benutzername:str = self.__eingabe_registrieren_benutzer.get().strip()
        anzeigename:str = self.__eingabe_registrieren_anzeigename.get().strip()

        if not password1 or not password2 or  not benutzername or not anzeigename:
            self.__fehlermeldung.config(text = "Unvollständige Eingabe!")
            return
        
        successPw, errorMessage = validatePassword(password1, password2)
        if not successPw:
           self.__fehlermeldung.config(text = errorMessage)
           return
        
        succesUser, errorMessage2 = validateUser(benutzername, anzeigename)
        if not succesUser:
            self.__fehlermeldung.config(text = errorMessage2)
            return
        

        self.zeigeLoginScreen()



    def zeigeMainScreen(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.__fenster,
            text = f"Willkommen, {self.__currentUser}!",
            font = FONT
        ).pack(pady=20)

        tk.Button(
            self.__fenster,
            text = "Abmelden",
            font = FONT,
            command = self.zeigeLoginScreen
            ).pack()

    #* CHATS
    
    def debugLogin(self) -> None:
        self.__currentUser: User = User(UUID=-1, username="debugy", displayName="Debugy")
        self.showChatsMenu()
    
    def showChatsMenu(self) -> None:
        for widget in self.__fenster.winfo_children():
            widget.destroy()
        tk.Label(
            self.__fenster,
            text = f"{self.__currentUser.getDisplayName()}s Chats", # TODO: sophisticated s removal/adding
            font = FONT
        ).pack()
    
    def run(self) -> None:
        self.__fenster.mainloop()
    
    def beenden(self) ->None:
        exit(0)

benutzeroberflaeche:Benutzeroberflaeche = Benutzeroberflaeche()