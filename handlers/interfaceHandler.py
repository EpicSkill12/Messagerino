import tkinter as tk
from tkinter import ttk
from sys import exit
from config.constants import AUFLOESUNG, FONT, BIG_FONT, TITLEFONT, MINSIZEX, MINSIZEY, DEV_USER
from custom_types.baseTypes import User
from helpers.validationHelper import validatePassword, validateUser
from helpers.formattingHelper import formatTime
from handlers.networkHandler import getChats

class Benutzeroberflaeche():
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title("Massagerino")
        self.__window.geometry(AUFLOESUNG)
        self.__window.minsize(MINSIZEX, MINSIZEY)

        self.__window.protocol("WM_DELETE_WINDOW", self.beenden)

        self.zeigeLoginScreen()

    def zeigeLoginScreen(self) -> None:
        """
        Vor.: -
        Eff.: Fenster öffnet sich, mit Felder für den Benutzernamen und Passwort
        Erg.: -
        """
        for widget in self.__window.winfo_children():
            widget.destroy()

        
        #* Titel:
        tk.Label(
            self.__window,
            text = "Messagerino",
            font = TITLEFONT
        ).pack(pady = 20)

        self.__login_frame:tk.Frame = tk.Frame(self.__window)
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
        ttk.Checkbutton(
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
        for widget in self.__window.winfo_children():
            widget.destroy()
        tk.Label(
            self.__window,
            text = "Registrieren",
            font = TITLEFONT
        ).pack(pady = 20)
        self.__register_frame:tk.Frame = tk.Frame(self.__window)
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
        ttk.Checkbutton(
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
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        tk.Label(
            self.__window,
            text = f"Willkommen, {self.__currentUser}!",
            font = FONT
        ).pack(pady=20)

        tk.Button(
            self.__window,
            text = "Abmelden",
            font = FONT,
            command = self.zeigeLoginScreen
            ).pack()

    #* CHATS
    
    def debugLogin(self) -> None:
        self.__currentUser: User = DEV_USER
        self.showChatsMenu()
    
    def showChatsMenu(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        tk.Label(
            self.__window,
            text = f"{self.__currentUser.getDisplayName()}s Chats", # TODO: sophisticated s removal/adding
            font = FONT
        ).pack()
        chatsCanvas = tk.Canvas(self.__window).pack()
        chatsFrame = tk.Frame(chatsCanvas).pack()
        self.__chats = []
        for chat in getChats():
            self.__chats.append(
                (_currentChat := tk.Frame(chatsFrame, bd=2, relief="solid")).pack(fill="x", side="top", anchor="n")
            )
            _currentChat.columnconfigure(0, weight=0)
            _currentChat.columnconfigure(1, weight=1)
            # pfpPlaceholder
            tk.Label(_currentChat, text="🖼️", font=TITLEFONT).grid(column=0, row=0, sticky="w")
            # chatTextFrame
            (_chatTextFrame := tk.Frame(_currentChat)).grid(column=1, row=0, sticky="w")
            _chatTextFrame.columnconfigure(0, weight=5)
            _chatTextFrame.columnconfigure(1, weight=1)
            # recipientName
            tk.Label(_chatTextFrame, text=chat.getRecipient().getDisplayName() ,font = BIG_FONT).grid(row=0, column=0, sticky="w")
            # lastMessageTime
            tk.Label(_chatTextFrame, text=formatTime(chat.getLastMessage().getSendTime()), font=FONT).grid(row=0, column=1, sticky="e")
            # message
            tk.Label(_chatTextFrame, text=chat.getLastMessage().getContent(), font=FONT).grid(row=1, column=0, sticky="w")
    
    def run(self) -> None:
        self.__window.mainloop()
    
    def beenden(self) -> None:
        exit(0)

benutzeroberflaeche:Benutzeroberflaeche = Benutzeroberflaeche()