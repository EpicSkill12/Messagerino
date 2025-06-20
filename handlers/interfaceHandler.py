import tkinter as tk
from tkinter import ttk
from sys import exit
from config.constants import RESOLUTION, FONT, BIG_FONT, TITLE_FONT, MIN_SIZE_X, MIN_SIZE_Y, DEV_USER, NAME
from custom_types.baseTypes import User
from helpers.validationHelper import validatePassword, validateUser
from helpers.formattingHelper import formatTime
from handlers.networkHandler import getChats
from uuid import uuid1

class InterfaceHandler():
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title(NAME)
        self.__window.geometry(RESOLUTION)
        self.__window.minsize(MIN_SIZE_X, MIN_SIZE_Y)

        self.__window.protocol("WM_DELETE_WINDOW", self.quit)

        self.showLoginScreen()

#================
#= Menü-Änderung
#================

    def showLoginScreen(self) -> None:
        """
        Vor.: -
        Eff.: Fenster öffnet sich, mit Felder für den Benutzernamen und Passwort
        Erg.: -
        """
        for widget in self.__window.winfo_children():
            widget.destroy()

        
        # Titel
        tk.Label(
            self.__window,
            text = NAME,
            font = TITLE_FONT
        ).pack(pady = 20)

        self.__loginFrame: tk.Frame = tk.Frame(self.__window)
        self.__loginFrame.pack(expand = True)
        
        # Nutzernamen Zeile
        tk.Label(
            self.__loginFrame, 
            text = "Nutzername", 
            font = FONT
        ).pack(pady = 10)
        self.__userNameInput = tk.Entry(self.__loginFrame, font = FONT)
        self.__userNameInput.pack()

        # Passwort Zeile:
        tk.Label(
            self.__loginFrame, text = "Passwort",
            font = FONT
        ).pack(pady = 10)
        self.__loginPasswordInput = tk.Entry(self.__loginFrame, font = FONT, show = "*")
        self.__loginPasswordInput.pack()
        
        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        ttk.Checkbutton(
            self.__loginFrame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.togglePassword
        ).pack(pady = 15)

        # Anmelden-Knopf
        tk.Button(
            self.__loginFrame,
            text = "Anmelden",
            font = FONT,
            command = self.login
        ).pack(pady=15)

        # Registrieren-Knopf
        tk.Button(
            self.__loginFrame,
            text = "Registrieren",
            font = FONT,
            command = self.showRegisterScreen
        ).pack(pady=15)

        self.__errorMessage: tk.Label = tk.Label(self.__loginFrame, text = "", font = FONT, fg = "red")
        self.__errorMessage.pack()

        #! Debug-Anmeldungs-Knopf
        tk.Button(
            self.__loginFrame,
            text = "Debug (Anmeldung)",
            font = FONT,
            command = self.debugLogin
        ).pack(pady=15)

        self.__errorMessage: tk.Label = tk.Label(self.__loginFrame, text = "", font = FONT, fg = "red")
        self.__errorMessage.pack()

    def showRegisterScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        # Registrieren-Überschrift
        tk.Label(
            self.__window,
            text = "Registrieren",
            font = TITLE_FONT
        ).pack(pady = 20)
        self.__register_frame:tk.Frame = tk.Frame(self.__window)
        self.__register_frame.pack(expand = True)
        
        # Nutzername-Eingabe
        tk.Label(
            self.__register_frame, 
            text = "Nutzername", 
            font = FONT
        ).pack(pady = 10)
        
        self.__registerUsernameInput = tk.Entry(self.__register_frame, font = FONT)
        self.__registerUsernameInput.pack()
        
        # Anzeigename-Eingabe
        tk.Label(
            self.__register_frame, 
            text = "Anzeigename", 
            font = FONT
        ).pack(pady = 10)
        self.__registerDisplayNameInput = tk.Entry(self.__register_frame, font = FONT)
        self.__registerDisplayNameInput.pack()

        # Passwört-Überschrift 1
        tk.Label(
            self.__register_frame, 
            text = "Passwort", 
            font = FONT
        ).pack(pady = 10)
        self.__registerPasswordInput1 = tk.Entry(self.__register_frame, font = FONT, show = "*")
        self.__registerPasswordInput1.pack()

        # Passwört-Überschrift 2
        tk.Label(
            self.__register_frame, 
            text = "Passwort wiederholen", 
            font = FONT
        ).pack(pady = 10)
        
        # Passwort-Eingabe 1
        self.__registerPasswordInput2 = tk.Entry(self.__register_frame, font = FONT, show = "*")
        self.__registerPasswordInput2.pack()
        
        # Passwort-Eingabe 2
        self.__errorMessage:tk.Label = tk.Label(self.__register_frame, text = "", font = FONT, fg = "red")
        self.__errorMessage.pack()
        
        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        ttk.Checkbutton(
            self.__register_frame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.toggleRegisterPassword
        ).pack(pady = 15)

        # Account-Erstellen-Knopf
        tk.Button(
            self.__register_frame,
            text = "Account erstellen",
            font = FONT,
            command = self.register
        ).pack(pady=15)

    def showMainScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        # Willkommen-Überschrift
        tk.Label(
            self.__window,
            text = f"Willkommen, {self.__currentUser}!",
            font = FONT
        ).pack(pady=20)

        # Abmelden-Button
        tk.Button(
            self.__window,
            text = "Abmelden",
            font = FONT,
            command = self.showLoginScreen
            ).pack()

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
        self.__chats: list[tk.Frame] = []
        for chat in getChats():
            self.__chats.append(
                (_currentChat := tk.Frame(chatsFrame, bd=2, relief="solid"))
            )
            _currentChat.pack(fill="x", side="top", anchor="n")

            _currentChat.columnconfigure(0, weight=0)
            _currentChat.columnconfigure(1, weight=1)
            # pfpPlaceholder
            tk.Label(_currentChat, text="🖼️", font=TITLE_FONT).pack(side="left")
            # chatTextFrame
            (_chatTextFrame := tk.Frame(_currentChat)).pack(side="left")
            (_nameDateFrame := tk.Frame(_chatTextFrame)).pack(side="top", fill="x")
            (_messageFrame := tk.Frame(_chatTextFrame)).pack(side="top", fill="x")
            # recipientName
            tk.Label(_nameDateFrame, text=chat.getRecipient().getDisplayName(), font = BIG_FONT).pack(side="left", anchor="w")
            # lastMessageTime
            tk.Label(_nameDateFrame, text=formatTime(chat.getLastMessage().getSendTime()), font=FONT).pack(side="right", anchor="e")
            # message
            tk.Label(_messageFrame, text=chat.getLastMessage().getContent(), font=FONT).pack(side="left", anchor="w")



# === Passwörter zeigen/verstecken ===

    def togglePassword(self) -> None:
        if self.showPasswordVar.get():
            self.__loginPasswordInput.config(show="")
        else:
            self.__loginPasswordInput.config(show="*")
    
    def toggleRegisterPassword(self) -> None:
        if self.showPasswordVar.get():
            self.__registerPasswordInput1.config(show="")
            self.__registerPasswordInput2.config(show="")
        else:
            self.__registerPasswordInput1.config(show="*")
            self.__registerPasswordInput2.config(show="*")


#==================
#= Knopf-Funktionen
#==================
    def login(self) -> None:
        username:str = self.__userNameInput.get().strip()

        passwort:str = self.__loginPasswordInput.get().strip()

        if not username or not passwort:
            self.__errorMessage.config(text = "Bitte gib einen Nutzernamen und ein Passwort ein.")
            return

        self.__currentUser: User = User(UUID= uuid1(-1), username=username, displayName=username)
        self.__currentPassword = passwort # ! Sicherheit (super-sicher ;) ))
        self.showMainScreen()

    def register(self) -> None:

        password1: str = self.__registerPasswordInput1.get().strip()
        password2: str = self.__registerPasswordInput2.get().strip()
        username: str = self.__registerUsernameInput.get().strip()
        displayName: str = self.__registerDisplayNameInput.get().strip()

        if not password1 or not password2 or  not username or not displayName:
            self.__errorMessage.config(text = "Unvollständige Eingabe!")
            return
        
        successPw, errorMessage = validatePassword(password1, password2)
        if not successPw:
           self.__errorMessage.config(text = errorMessage)
           return
        
        successUser, errorMessage2 = validateUser(username, displayName)
        if not successUser:
            self.__errorMessage.config(text = errorMessage2)
            return

        self.showLoginScreen()

    def debugLogin(self) -> None:
        self.__currentUser: User = DEV_USER
        self.showChatsMenu()
    

#==================
#= Basis-Funktionen
#==================

    def run(self) -> None:
        self.__window.mainloop()
    
    def quit(self) -> None:
        exit(0)

# === CODE ===
interface: InterfaceHandler = InterfaceHandler()