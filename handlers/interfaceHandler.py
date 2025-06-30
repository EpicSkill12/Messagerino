import tkinter as tk
from tkinter import ttk
from sys import exit
from typing import Literal

from config.constants import (BIG_FONT, CHAT_HEIGHT, CHATS_WIDTH, FONT, ICON_PATH, LOGO_PATH,
    MAX_SIZE_X, MAX_SIZE_Y, MESSAGE_HEIGHT, MESSAGE_WIDTH, MIN_SIZE_X, MIN_SIZE_X2, MIN_SIZE_Y, MIN_SIZE_Y2, NAME,
    RESOLUTION, SIDEBAR_WIDTH, THEMES, TITLE_FONT, TOTAL_CHATS_WIDTH, RESOLUTION_SECOND)
from helpers.validationHelper import validatePassword, validateUser
from helpers.formattingHelper import formatTime, getPossessive
from handlers.loginHandler import (getChats, getMessages, getOwnUsername, tryLogin, trySignup,
    updateUser, getUserSuggestions, sendMessage)
from PIL import Image, ImageTk


class InterfaceHandler():
    def __init__(self):
        self.__window = tk.Tk()
        self.__window.title(NAME)
        self.__window.geometry(RESOLUTION)
        self.__window.minsize(MIN_SIZE_X, MIN_SIZE_Y)
        self.__window.maxsize(MAX_SIZE_X, MAX_SIZE_Y)
        self.__window.iconbitmap(ICON_PATH) #type:ignore

        self.__window.protocol("WM_DELETE_WINDOW", self.quit)

        self.__theme: Literal["light", "dark"] = "dark" 
        self.__style = ttk.Style(self.__window)
        self.__style.theme_use("default")
        self.applyTheme()

        self.showLoginScreen()

        

    def applyTheme(self) -> None:
        theme = THEMES[self.__theme]
        self.__window.configure(bg=theme["background"])
        self.__entryBG = THEMES[self.__theme]["buttonBG"]
        self.__entryFG = THEMES[self.__theme]["buttonFG"]
        self.__bg = THEMES[self.__theme]["background"]
        self.__fg = THEMES[self.__theme]["foreground"]
        self.__highlight = THEMES[self.__theme]["highlight"]
        self.__style.configure( #type: ignore
            style="Custom.TCheckbutton", 
            background = self.__bg, 
            foreground=self.__fg, 
            highlight=self.__highlight
        )
        self.__style.map( # type: ignore
            "Custom.TCheckbutton",
            background=[("active", self.__highlight)],
            foreground=[("active", self.__entryFG)]
        ) 
    
    def setTheme(self, theme_name: Literal["light", "dark"]) -> None:
        self.__theme = theme_name
        self.applyTheme()
        self.showSettingsScreen()

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


        # Logo
        logo = ImageTk.PhotoImage(Image.open(LOGO_PATH).resize((100, 100))) # type: ignore
        logoLabel = tk.Label(
            self.__window,
            image=logo
        )
        logoLabel.img = logo # type: ignore
        logoLabel.pack()

        # Titel
        tk.Label(
            self.__window,
            text = NAME,
            font = TITLE_FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack()

        self.__loginFrame: tk.Frame = tk.Frame(self.__window, bg=self.__bg)
        self.__loginFrame.pack(expand = True, anchor="n", pady=50)
        
        # Nutzernamen Zeile
        tk.Label(
            self.__loginFrame, 
            text = "Nutzername", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__userNameInput = tk.Entry(self.__loginFrame, font = FONT, bg=self.__entryBG, fg=self.__fg,highlightthickness=2, highlightbackground=THEMES[self.__theme]["buttonBG"], highlightcolor=self.__highlight)
        self.__userNameInput.pack()

        # Passwort Zeile:
        tk.Label(
            self.__loginFrame, text = "Passwort",
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__loginPasswordInput = tk.Entry(self.__loginFrame, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__loginPasswordInput.pack()
        
        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        ttk.Checkbutton(
            self.__loginFrame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.togglePassword,
            style="Custom.TCheckbutton"
        ).pack(pady = 15)
        # Anmelden-Knopf
        tk.Button(
            self.__loginFrame,
            text = "Anmelden",
            font = FONT,
            bg=self.__entryBG,
            fg=self.__entryFG,
            command = self.login
        ).pack(pady=15)

        # Registrieren-Knopf
        tk.Button(
            self.__loginFrame,
            text = "Registrieren",
            font = FONT,
            bg=self.__entryBG,
            fg=self.__entryFG,
            command = self.showRegisterScreen
        ).pack(pady=15)

        self.__errorMessage: tk.Label = tk.Label(self.__loginFrame, text = "", font = FONT, fg = "red", bg=self.__bg)
        self.__errorMessage.pack()

        self.__errorMessage: tk.Label = tk.Label(self.__loginFrame, text = "", font = FONT, fg = "red", bg=self.__bg)
        self.__errorMessage.pack()

    def showRegisterScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        # Registrieren-Überschrift
        tk.Label(
            self.__window,
            text = "Registrieren",
            font = TITLE_FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 20)

        self.__register_frame:tk.Frame = tk.Frame(self.__window, bg=self.__bg)
        self.__register_frame.pack(expand = True)
        
        # Nutzername-Eingabe
        tk.Label(
            self.__register_frame, 
            text = "Nutzername", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        
        self.__registerUsernameInput = tk.Entry(self.__register_frame, font = FONT, bg=self.__entryBG, fg=self.__fg)
        self.__registerUsernameInput.pack()
        
        # Anzeigename-Eingabe
        tk.Label(
            self.__register_frame, 
            text = "Anzeigename", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__registerDisplayNameInput = tk.Entry(self.__register_frame, font = FONT, bg=self.__entryBG, fg=self.__fg)
        self.__registerDisplayNameInput.pack()

        # Passwört-Überschrift 1
        tk.Label(
            self.__register_frame, 
            text = "Passwort", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__registerPasswordInput1 = tk.Entry(self.__register_frame, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__registerPasswordInput1.pack()

        # Passwört-Überschrift 2
        tk.Label(
            self.__register_frame, 
            text = "Passwort wiederholen", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__registerPasswordInput2 = tk.Entry(self.__register_frame, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__registerPasswordInput2.pack()
        
        self.__errorMessage:tk.Label = tk.Label(self.__register_frame, text = "", font = FONT, fg = "red", bg=self.__bg)
        self.__errorMessage.pack()
        
        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        ttk.Checkbutton(
            self.__register_frame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.toggleRegisterPassword,
            style="Custom.TCheckbutton"
        ).pack(pady = 15)

        # Account-Erstellen-Knopf
        tk.Button(
            self.__register_frame,
            text = "Account erstellen",
            font = FONT,
            command = self.register,
            bg=self.__entryBG,
            fg=self.__entryFG
        ).pack(pady=15)

    def showMainScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()

        self.__window.update_idletasks()

        window_width = self.__window.winfo_width()
        separator_x = TOTAL_CHATS_WIDTH + ((window_width - TOTAL_CHATS_WIDTH) * 0.01)  # kleine Einrückung

        #Hauptcontainer
        mainContainer = tk.Frame(self.__window, bg=self.__bg)
        mainContainer.pack(fill="both", expand=True)

        # Vertikale Trennlinie
        separator = tk.Frame(self.__window, bg=self.__entryBG, width=2)
        separator.place(x=separator_x, y=0, relheight=1.0)

        # Seitenleiste
        sideBarFrame = tk.Frame(mainContainer, width=SIDEBAR_WIDTH, bg=self.__bg)
        sideBarFrame.pack(side="left", fill="y")
        
        #Linke Spalte
        chatListFrame = tk.Frame(mainContainer, width=TOTAL_CHATS_WIDTH, bg=self.__bg)
        chatListFrame.pack(side="left", fill="y")

        #Rechte Spalte
        self.contentFrame = tk.Frame(mainContainer, bg=self.__bg)
        self.contentFrame.pack(side="right", fill="both", expand=True)

        settingsButton = tk.Button(
            sideBarFrame,
            text = "⚙️",
            command = self.showSettingsScreen,
            bd = 0,
            highlightthickness = 0,
            relief = "flat",
            bg = self.__bg,
            fg = self.__fg,
            font = BIG_FONT,
            activebackground = self.__bg
        )
        settingsButton.place(x=10, y=10)

        moreButton = tk.Button(
            sideBarFrame,
            text = "➕",
            command= self.showUserSuggestions,
            bd = 0,
            highlightthickness = 0,
            relief = "flat",
            bg = self.__bg,
            fg = self.__fg,
            font = BIG_FONT,
            activebackground = self.__bg
        )
        moreButton.place(x=10, y=60)

        #Chat-Übersicht
        tk.Label(
            chatListFrame, 
            text=f"{getPossessive(self.__currentName)} Chats",
            font=BIG_FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(anchor="n") 
        
        chatsFrame = tk.Frame(
            chatListFrame,
            width=CHATS_WIDTH,
            bg=self.__bg
        )
        chatsFrame.pack(anchor="ne")
        
        for chat in getChats():
            _currentChat = tk.Frame(
                chatsFrame,
                width=CHATS_WIDTH,
                height=CHAT_HEIGHT,
                bg=self.__bg,
                bd=2,
                relief="solid"
            )
            _currentChat.pack_propagate(False)
            _currentChat.pack(anchor="ne", fill="x", expand=True)
            _currentChat.columnconfigure(0, weight=0)
            _currentChat.columnconfigure(1, weight=1)
            def _currentOpenFunc(event: tk.Event, recipient: str = chat["Recipient"]) -> None:
                self.openChat(recipient)
            _currentChat.bind("<Button-1>", _currentOpenFunc)

            pfpPlaceholder = tk.Label(_currentChat, text="🖼️", font=TITLE_FONT, bg=self.__bg, fg=self.__fg)
            pfpPlaceholder.pack(side="left")
            pfpPlaceholder.bind("<Button-1>", _currentOpenFunc)

            (_chatTextFrame := tk.Frame(_currentChat, bg=self.__bg)).pack(side="left")
            _chatTextFrame.bind("<Button-1>", _currentOpenFunc)
            (_nameDateFrame := tk.Frame(_chatTextFrame, bg=self.__bg)).pack(side="top", fill="x")
            _nameDateFrame.bind("<Button-1>", _currentOpenFunc)
            (_messageFrame := tk.Frame(_chatTextFrame, bg=self.__bg)).pack(side="top", fill="x")
            _messageFrame.bind("<Button-1>", _currentOpenFunc)

            recipientName = tk.Label(_nameDateFrame, text=chat["Recipient"], font = BIG_FONT, bg=self.__bg, fg=self.__fg)
            recipientName.pack(side="left", anchor="w")
            recipientName.bind("<Button-1>", _currentOpenFunc)

            lastMessageTime = tk.Label(_nameDateFrame, text=formatTime(chat["LastMessage"]["SendTime"]), font=FONT, bg=self.__bg, fg=self.__fg)
            lastMessageTime.pack(side="right", anchor="e")
            lastMessageTime.bind("<Button-1>", _currentOpenFunc)
            # message
            messageAndStatusFrame = tk.Frame(_messageFrame, bg=self.__bg)
            messageAndStatusFrame.pack(fill="x", anchor="w", padx=2)

            message = tk.Label(
                messageAndStatusFrame,
                text=chat["LastMessage"]["Content"],
                font=FONT,
                bg=self.__bg,
                fg=self.__fg,
                anchor="w",
                justify="left",
                wraplength=CHATS_WIDTH - 60 
            )
            message.pack(side="left")
            message.bind("<Button-1>", _currentOpenFunc)

            isMine = chat["LastMessage"]["Sender"] == self.__currentName
            read_indicator = "✔️✔️" if chat["LastMessage"]["Read"] else "✔️"
            readLabel = tk.Label(
                messageAndStatusFrame,
                text=read_indicator if isMine else "",
                font=FONT,
                bg=self.__bg,
                fg=self.__fg
            )
            readLabel.pack(side="right", padx=5)
            readLabel.bind("<Button-1>", _currentOpenFunc)

        #Inhalt-Übersicht
        tk.Label(
            self.contentFrame, 
            text="Willkommen bei Messagerino! 👋", 
            font=BIG_FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady=30)
        tk.Label(
            self.contentFrame, 
            text="Wähle links einen Chat aus, um die Unterhaltung zu starten.", 
            font=FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(expand=True, fill="y")
        
    def openChat(self, recipient: str) -> None:
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        messagesFrame = tk.Frame(self.contentFrame, bg=self.__bg)
        messagesFrame.pack(fill="both", expand=True)

        typingBox = tk.Frame(self.contentFrame, bg=self.__bg)
        typingBox.pack(side="bottom", fill="x")

        self.__messageEntry = tk.Entry(
            typingBox,
            font=FONT,
            bg=self.__entryBG,
            fg=self.__fg,
            highlightthickness=2,
            highlightbackground=self.__entryBG,
            highlightcolor=self.__highlight
        )
        self.__messageEntry.pack(side="left", fill="x", expand=True, padx=20, pady=5)
        
        def sendCurrentMessage() -> None:
            content = self.__messageEntry.get().strip()
            if content:
                sendMessage(content, recipient)
                self.openChat(recipient)
                self.__messageEntry.delete(0, tk.END)

        sendButton = tk.Button(
            typingBox,
            text="Senden",
            command=sendCurrentMessage,
            font=FONT,
            bg=self.__entryBG,
            fg=self.__entryFG,
            activebackground=self.__highlight
        )
        sendButton.pack(side="right", padx=5, pady=5)

        

        tk.Label(
            messagesFrame, 
            text=recipient,
            font=TITLE_FONT,
            bg=self.__bg,
            fg=self.__fg
        ).pack()

        for message in getMessages(recipient):
            mine = message["Receiver"] == recipient

            _currentMessage = tk.Frame(
                messagesFrame,
                width=MESSAGE_WIDTH,
                height=MESSAGE_HEIGHT,
                bg=self.__bg,
                bd=2,
                relief="solid"
            )
            _currentMessage.pack(anchor="ne" if mine else "nw", padx=20, pady=10)

            _info = tk.Frame(_currentMessage, background=self.__bg)
            _info.pack(side="right" if mine else "left", anchor="e" if mine else "w")

            tk.Label(_info, text=formatTime(message["SendTime"]), font=FONT, bg=self.__bg, fg=self.__fg).grid(row=0)
            tk.Label(_info, text="✔️✔️" if message["Read"] == 1 else "✔️", font=BIG_FONT, bg=self.__bg, fg=self.__fg).grid(row=1)

            tk.Label(
                _currentMessage,
                text=message["Content"],
                font=BIG_FONT,
                bg=self.__bg,
                fg=self.__fg,
                anchor="w",
                justify="left",
                wraplength=400
            ).pack(fill="x", side="left" if not mine else "right")
            
            
    
    def showSettingsScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        self.applyTheme()

        mainContainer = tk.Frame(self.__window, bg=self.__bg)
        mainContainer.pack(fill="both", expand=True)

        #Verlassen
        settingsButton = tk.Button(
            mainContainer,
            text = "❌",
            command = self.showMainScreen,
            bd = 0,
            highlightthickness = 0,
            relief = "flat",
            bg = self.__bg,
            fg = self.__fg,
            activebackground = self.__bg,
            font = BIG_FONT
        )
        settingsButton.place(x=10, y=10)

        #Inhalt-Übersicht
        tk.Label(
            mainContainer, 
            text="Einstellungen", 
            font=TITLE_FONT,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=30)

        # Theme-Auswahl
        tk.Label(
            mainContainer,
            text="Design auswählen:",
            font=BIG_FONT,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=10)

        tk.Button(
            mainContainer,
            text="Light Theme",
            font=FONT,
            bg=THEMES["light"]["buttonBG"],
            fg=THEMES["light"]["buttonFG"],
            command=lambda: self.setTheme("light")
        ).pack(pady=5)

        tk.Button(
            mainContainer,
            text="Dark Theme",
            font=FONT,
            bg=THEMES["dark"]["buttonBG"],
            fg=THEMES["dark"]["buttonFG"],
            command=lambda: self.setTheme("dark")
        ).pack(pady=5)

        #Profilbearbeitung
        tk.Label(
            mainContainer,
            text="Profilbearbeitung:",
            font=BIG_FONT,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=10)

        #aktueller Nutzer
        tk.Label(
            mainContainer,
            text = f"Aktueller Nutzer: {getOwnUsername()}",
            font=FONT,
            bd=2,
            relief="solid",
            padx=10, pady=5,
            bg=self.__bg,
            fg = self.__fg
        ).pack()

        #neuer anzeigename
        tk.Label(
            mainContainer,
            text = "Neuer Anzeigename",
            font=FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady=10)
        displayNameVAR = tk.StringVar()
        self.__newDisplayName = tk.Entry(mainContainer, font = FONT, show = "", bg=self.__entryBG, fg=self.__fg, textvariable=displayNameVAR)
        displayNameVAR.set(self.__currentName)
        self.__newDisplayName.pack()
        

        #neues PW
        # Passwört-Überschrift 1
        tk.Label(
            mainContainer, 
            text = "Neues Passwort", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__newPasswordInput1 = tk.Entry(mainContainer, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__newPasswordInput1.pack()

        # Passwört-Überschrift 2
        tk.Label(
            mainContainer, 
            text = "Passwort wiederholen", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__newPasswordInput2 = tk.Entry(mainContainer, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__newPasswordInput2.pack()

        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        ttk.Checkbutton(
            mainContainer,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.toggleNewPassword,
            style="Custom.TCheckbutton"
        ).pack(pady = 15)

        #Knopf um final zu bestätigen
        self.finalConfirmPwVAR = tk.BooleanVar()
        tk.Button(
            mainContainer,
            text = "Änderung bestätigen",
            font = FONT,
            command = self.finalConfirm,
            bg=self.__entryBG,
            fg=self.__entryFG
        ).pack(pady=15)


        # Checkbox zum Bestätigen des neuen Passwortes
        self.confirmPwVAR = tk.BooleanVar()
        ttk.Checkbutton(
            mainContainer,
            text = "Neues Passwort bestätigen",
            variable = self.confirmPwVAR,
            style="Custom.TCheckbutton"
        ).pack(pady = 15)

        self.__errorMessage:tk.Label = tk.Label(mainContainer, text = "", font = FONT, fg = "red", bg=self.__bg)
        self.__errorMessage.pack(pady=15)

        self.__successMessage:tk.Label = tk.Label(mainContainer, text = "", font=FONT, fg = "green", bg = self.__bg)
        self.__successMessage.pack(pady=15)

        #Abmelden-Button
        tk.Button(
            mainContainer,
            text="Abmelden",
            font=FONT,
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            command=self.showLoginScreen
        ).pack(pady=15)

    def showUserSuggestions(self) -> None:
        secondWindow = tk.Toplevel(self.__window, bg = self.__bg)
        secondWindow.title("User Suggestions")
        secondWindow.geometry(RESOLUTION_SECOND)

        secondWindow.minsize(MIN_SIZE_X2, MIN_SIZE_Y2)
        secondWindow.maxsize(MAX_SIZE_X, MAX_SIZE_Y)

        suggestionFrame = tk.Frame(secondWindow, bg=self.__bg)
        suggestionFrame.pack(padx=20, pady=20, fill="both", expand=True)
        chats = getChats()
        receivers = [chat["Recipient"] for chat in chats]
        for username, displayName in getUserSuggestions():
            if username in receivers:
                continue
            userFrame = tk.Frame(
                suggestionFrame,
                bg=self.__bg,
                bd=2,
                relief="solid",
                padx=10,
                pady=5
            )
            userFrame.pack(anchor="w", fill="x", pady=5)

            def send(username: str) -> None:
                sendMessage("Hallo!", username)
                secondWindow.destroy()

            userFrame.bind("<Button-1>", lambda event, u=username: send(u))


            iconLabel = tk.Label(
            userFrame,
            text="🖼️",
            font=TITLE_FONT,
            bg=self.__bg,
            fg=self.__fg
            )
            iconLabel.pack(side="left")
            iconLabel.bind("<Button-1>", lambda event, u=username: send(u))

            nameLabel = tk.Label(
                userFrame,
                text=displayName,
                font=FONT,
                bg=self.__bg,
                fg=self.__fg
            )
            nameLabel.pack(side="left", padx=10)
            nameLabel.bind("<Button-1>", lambda event, u=username: send(u))

        # Schließen-Knopf
        tk.Button(
            secondWindow, 
            text="Schließen", 
            command=secondWindow.destroy,
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            font=FONT
        ).pack(pady=15)

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
    
    def toggleNewPassword(self) -> None:
        if self.showPasswordVar.get():
            self.__newPasswordInput1.config(show="")
            self.__newPasswordInput2.config(show="")
        else:
            self.__newPasswordInput1.config(show="*")
            self.__newPasswordInput2.config(show="*")

#==================
#= Knopf-Funktionen
#==================

    def login(self) -> None:
        username:str = self.__userNameInput.get().strip()
        password:str = self.__loginPasswordInput.get().strip()

        if not username or not password:
            self.__errorMessage.config(text = "Bitte gib einen Nutzernamen und ein Passwort ein.")
            return

        success, message = tryLogin(username=username, password=password)
        if success:
            self.__currentName: str = message
            self.showMainScreen()
        else:
            self.__errorMessage.config(text=message)
        
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
        
        success, message = trySignup(username=username, displayName=displayName, password=password1)
        print(success, message)
        if success:
            self.__currentName: str = displayName
            self.showMainScreen()
        else:
            self.__errorMessage.config(text=message)

    def finalConfirm(self) -> None:
        self.finalConfirmPwVAR.set(True)

        if self.finalConfirmPwVAR.get() and not self.confirmPwVAR.get():
            self.__errorMessage.config(text="Passwort muss erst bestätig werden!")
            return

        if not self.__newPasswordInput1.get() or not self.__newPasswordInput2.get() or not self.__newDisplayName.get():
            self.__errorMessage.config(text="Kein Passwort eingegeben!")
            return
        
        successPw, errorMessage = validatePassword(self.__newPasswordInput1.get(), self.__newPasswordInput2.get())
        if not successPw:
           self.__errorMessage.config(text = errorMessage)
           return
        
        successUser, errorMessage2 = validateUser(self.__newDisplayName.get(), self.__newDisplayName.get())
        if not successUser:
            self.__errorMessage.config(text = errorMessage2)
            return
        
        if self.confirmPwVAR.get() and self.finalConfirmPwVAR.get():
            updateUser(self.__newDisplayName.get(), self.__newPasswordInput1.get())
            self.showSettingsScreen()
            self.__successMessage.config(text="Profil wurde erfolgreich aktualisiert!")

#==================
#= Basis-Funktionen
#==================

    def run(self) -> None:
        self.__window.mainloop()
    
    def quit(self) -> None:
        exit(0)

#========
#= CODE
#========
interface: InterfaceHandler = InterfaceHandler()