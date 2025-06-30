import tkinter as tk
from tkinter import ttk
from sys import exit
from typing import Callable, Literal
from config.constants import (CHAT_HEIGHT, CHATS_WIDTH, ICON_PATH, LOGO_PATH,
    MAX_SIZE_X, MAX_SIZE_Y, MESSAGE_HEIGHT, MESSAGE_WIDTH, MIN_SIZE_X, MIN_SIZE_X2, MIN_SIZE_Y, MIN_SIZE_Y2, NAME,
    RESOLUTION, SIDEBAR_WIDTH, THEMES, TOTAL_CHATS_WIDTH, RESOLUTION_SECOND, MIN_FONT_SIZE, MAX_FONT_SIZE)
from helpers.validationHelper import validatePassword, validateUser
from helpers.formattingHelper import formatTime, getPossessive
from handlers.loginHandler import (getChats, getDisplayName, getMessages, getOwnUsername,
    getUserSuggestions, sendMessage, tryLogin, trySignup, updateUser)
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

        self.__currentChat: str | None = None
        self.__lastMessageTimes: dict[str, float] = {}
        self.__lastPreviewMessageTimes: dict[str, float] = {}
        

        self.__fontSize: int = 12
        self.setFont("")
        

        self.showLoginScreen()

        

    def applyTheme(self) -> None:
        """
        Vor.: self.__theme enthält einen gültigen Schlüssel aus THEMES
        Eff.: Aktualisiert Farben und Styles des Fensters
        Erg.: -
        """
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
        """
        Vor.: theme_name ist "light" oder "dark"
        Eff.: Ändert das aktuelle Farbschema
        Erg.: -
        """
        self.__theme = theme_name
        self.applyTheme()
        self.showSettingsScreen()

    def setFont(self, plusMinus:str) -> None:
        if plusMinus == "down" :
            self.__fontSize -= 1
        elif plusMinus == "up":   
            self.__fontSize += 1
        self.__font:tuple[str, int] = ("Arial", self.__fontSize) 
        self.__bigFont:tuple[str, int] = ("Arial", self.__fontSize + 4)
        self.__titleFont:tuple[str, int, str] = ("Arial", self.__fontSize + 8, "bold")
        return
    
        

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
            font = self.__titleFont,
            bg=self.__bg,
            fg = self.__fg
        ).pack()

        self.__loginFrame: tk.Frame = tk.Frame(self.__window, bg=self.__bg)
        self.__loginFrame.pack(expand = True, anchor="n", pady=50)
        
        # Nutzernamen Zeile
        tk.Label(
            self.__loginFrame, 
            text = "Nutzername", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__userNameInput = tk.Entry(self.__loginFrame, font = self.__font, bg=self.__entryBG, fg=self.__fg,highlightthickness=2, highlightbackground=THEMES[self.__theme]["buttonBG"], highlightcolor=self.__highlight)
        self.__userNameInput.pack()

        # Passwort Zeile:
        tk.Label(
            self.__loginFrame, text = "Passwort",
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__loginPasswordInput = tk.Entry(self.__loginFrame, font = self.__font, show = "*", bg=self.__entryBG, fg=self.__fg)
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
            font = self.__font,
            bg=self.__entryBG,
            fg=self.__entryFG,
            command = self.login
        ).pack(pady=15)

        # Registrieren-Knopf
        tk.Button(
            self.__loginFrame,
            text = "Registrieren",
            font = self.__font,
            bg=self.__entryBG,
            fg=self.__entryFG,
            command = self.showRegisterScreen
        ).pack(pady=15)

        self.__errorMessage: tk.Label = tk.Label(self.__loginFrame, text = "", font = self.__font, fg = "red", bg=self.__bg)
        self.__errorMessage.pack()

        self.__errorMessage: tk.Label = tk.Label(self.__loginFrame, text = "", font = self.__font, fg = "red", bg=self.__bg)
        self.__errorMessage.pack()

    def showRegisterScreen(self) -> None:
        """
        Vor.: -
        Eff.: Zeigt das Registrierungsformular an
        Erg.: -
        """
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        # Registrieren-Überschrift
        tk.Label(
            self.__window,
            text = "Registrieren",
            font = self.__titleFont,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 20)

        self.__register_frame:tk.Frame = tk.Frame(self.__window, bg=self.__bg)
        self.__register_frame.pack(expand = True)
        
        # Nutzername-Eingabe
        tk.Label(
            self.__register_frame, 
            text = "Nutzername", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        
        self.__registerUsernameInput = tk.Entry(self.__register_frame, font = self.__font, bg=self.__entryBG, fg=self.__fg)
        self.__registerUsernameInput.pack()
        
        # Anzeigename-Eingabe
        tk.Label(
            self.__register_frame, 
            text = "Anzeigename", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__registerDisplayNameInput = tk.Entry(self.__register_frame, font = self.__font, bg=self.__entryBG, fg=self.__fg)
        self.__registerDisplayNameInput.pack()

        # Passwört-Überschrift 1
        tk.Label(
            self.__register_frame, 
            text = "Passwort", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__registerPasswordInput1 = tk.Entry(self.__register_frame, font = self.__font, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__registerPasswordInput1.pack()

        # Passwört-Überschrift 2
        tk.Label(
            self.__register_frame, 
            text = "Passwort wiederholen", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__registerPasswordInput2 = tk.Entry(self.__register_frame, font = self.__font, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__registerPasswordInput2.pack()
        
        self.__errorMessage:tk.Label = tk.Label(self.__register_frame, text = "", font = self.__font, fg = "red", bg=self.__bg)
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
            font = self.__font,
            command = self.register,
            bg=self.__entryBG,
            fg=self.__entryFG
        ).pack(pady=15)

    def showMainScreen(self) -> None:
        """
        Vor.: Ein Benutzer ist eingeloggt
        Eff.: Zeigt die Hauptansicht mit Chats
        Erg.: -
        """
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


        def refreshPreview(frame: tk.Frame, scrollMethod: Callable[[tk.Event], None]) -> None:
            """
            Vor.: Die Hauptansicht ist aktiv
            Eff.: Aktualisiert die Chatvorschau, wenn neue Nachrichten eingegangen sind
            Erg.: Die Chatliste wird bei neuen Nachrichten neu geladen
            """
            try: 
                if not frame.winfo_exists():
                    return
                updated = False
                for chat in getChats():
                    recipient = chat["Recipient"]
                    last_time = self.__lastPreviewMessageTimes.get(recipient, 0)
                    if chat["LastMessage"]["SendTime"] > last_time:
                        updated = True
                        self.__lastPreviewMessageTimes[recipient] = chat["LastMessage"]["SendTime"]
                self.__window.after(5000, refreshPreview, frame, scrollMethod)
                if updated:
                    self.createChats(frame, scrollMethod)
            except tk.TclError:
                return

        settingsButton = tk.Button(
            sideBarFrame,
            text = "⚙️",
            command = self.showSettingsScreen,
            bd = 0,
            highlightthickness = 0,
            relief = "flat",
            bg = self.__bg,
            fg = self.__fg,
            font = self.__bigFont,
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
            font = self.__bigFont,
            activebackground = self.__bg
        )
        moreButton.place(x=10, y=60)

        #Chat-Übersicht
        tk.Label(
            chatListFrame, 
            text=f"{getPossessive(self.__currentName)} Chats",
            font=self.__bigFont,
            bg=self.__bg,
            fg = self.__fg
        ).pack(anchor="n",pady=15) 
        
        chatsScrollFrame = tk.Frame(chatListFrame, bg=self.__bg)
        chatsScrollFrame.pack(fill="both", expand=True, padx=5)
        
        chatsCanvas = tk.Canvas(chatsScrollFrame, bg=self.__bg, highlightthickness=0, width=CHATS_WIDTH)
        chatsScrollbar = tk.Scrollbar(chatsScrollFrame, orient="vertical", command=chatsCanvas.yview) # type: ignore
        chatsCanvas.configure(yscrollcommand=chatsScrollbar.set)
        
        # ? Scrollbar-Anzeige
        # chatsScrollbar.pack(side="right", fill="y")
        chatsCanvas.pack(side="left", fill="both", expand=True)
        
        chatsFrame = tk.Frame(chatsCanvas, bg=self.__bg)
        chats_container_id = chatsCanvas.create_window((0, 0), window=chatsFrame, anchor="nw")
        
        def scrollInChatsList(event: tk.Event) -> None:
            if event.delta:
                chatsCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                chatsCanvas.yview_scroll(1 if event.num == 5 else -1, "units")
        
        chatsCanvas.bind("<MouseWheel>", scrollInChatsList)
        chatsCanvas.bind("<Button-4>", scrollInChatsList)
        chatsCanvas.bind("<Button-5>", scrollInChatsList)
        chatsFrame.bind("<MouseWheel>", scrollInChatsList)
        chatsFrame.bind("<Button-4>", scrollInChatsList)
        chatsFrame.bind("<Button-5>", scrollInChatsList)
        
        def chatsFrameConfig(event: tk.Event) -> None:
            chatsCanvas.configure(scrollregion=chatsCanvas.bbox("all"))
        
        chatsFrame.bind("<Configure>", chatsFrameConfig)
        chatsCanvas.bind(
            "<Configure>",
            lambda e: chatsCanvas.itemconfig(chats_container_id, width=e.width)
        )
        self.createChats(chatsFrame, scrollInChatsList)
        self.__window.after(5000, refreshPreview, chatsFrame, scrollInChatsList)
        chatsFrame.update_idletasks()
        chatsCanvas.configure(scrollregion=chatsCanvas.bbox("all"))

        #Inhalt-Übersicht
        tk.Label(
            self.contentFrame, 
            text="Willkommen bei Messagerino! 👋", 
            font=self.__bigFont,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady=30)
        tk.Label(
            self.contentFrame, 
            text="Wähle links einen Chat aus, um die Unterhaltung zu starten.", 
            font=self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(expand=True, fill="y")


    def createChats(self, frame: tk.Frame, scrollMethod: Callable[[tk.Event], None]) -> None:
        for child in frame.winfo_children():
            child.destroy()
        for chat in getChats():
            if (name := getDisplayName(chat["Recipient"])):
                displayName = name[1]
            else:
                print(name[1])
                displayName = chat["Recipient"]
            _currentChat = tk.Frame(
                frame,
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
            def _currentOpenFunc(event: tk.Event, recipient: str = chat["Recipient"], displayName: str = displayName) -> None:
                """
                Vor.: recipient ist ein Nutzername
                Eff.: Öffnet den entsprechenden Chat
                Erg.: -
                """
                self.openChat(recipient)
            _currentChat.bind("<Button-1>", _currentOpenFunc)
            _currentChat.bind("<MouseWheel>", scrollMethod)
            _currentChat.bind("<Button-4>", scrollMethod)
            _currentChat.bind("<Button-5>", scrollMethod)

            pfpPlaceholder = tk.Label(_currentChat, text="🖼️", font=self.__titleFont, bg=self.__bg, fg=self.__fg)
            pfpPlaceholder.pack(side="left")
            pfpPlaceholder.bind("<Button-1>", _currentOpenFunc)
            pfpPlaceholder.bind("<MouseWheel>", scrollMethod)
            pfpPlaceholder.bind("<Button-4>", scrollMethod)
            pfpPlaceholder.bind("<Button-5>", scrollMethod)

            (_chatTextFrame := tk.Frame(_currentChat, bg=self.__bg)).pack(side="left")
            _chatTextFrame.bind("<Button-1>", _currentOpenFunc)
            _chatTextFrame.bind("<MouseWheel>", scrollMethod)
            _chatTextFrame.bind("<Button-4>", scrollMethod)
            _chatTextFrame.bind("<Button-5>", scrollMethod)
            (_nameDateFrame := tk.Frame(_chatTextFrame, bg=self.__bg)).pack(side="top", fill="x")
            _nameDateFrame.bind("<Button-1>", _currentOpenFunc)
            _nameDateFrame.bind("<MouseWheel>", scrollMethod)
            _nameDateFrame.bind("<Button-4>", scrollMethod)
            _nameDateFrame.bind("<Button-5>", scrollMethod)
            (_messageFrame := tk.Frame(_chatTextFrame, bg=self.__bg)).pack(side="top", fill="x")
            _messageFrame.bind("<Button-1>", _currentOpenFunc)
            _messageFrame.bind("<MouseWheel>", scrollMethod)
            _messageFrame.bind("<Button-4>", scrollMethod)
            _messageFrame.bind("<Button-5>", scrollMethod)

            recipientName = tk.Label(_nameDateFrame, text=displayName, font = self.__bigFont, bg=self.__bg, fg=self.__fg)
            recipientName.pack(side="left", anchor="w")
            recipientName.bind("<Button-1>", _currentOpenFunc)
            recipientName.bind("<MouseWheel>", scrollMethod)
            recipientName.bind("<Button-4>", scrollMethod)
            recipientName.bind("<Button-5>", scrollMethod)

            lastMessageTime = tk.Label(_nameDateFrame, text=formatTime(chat["LastMessage"]["SendTime"]), font=self.__font, bg=self.__bg, fg=self.__fg)
            lastMessageTime.pack(side="right", anchor="e")
            lastMessageTime.bind("<Button-1>", _currentOpenFunc)
            lastMessageTime.bind("<MouseWheel>", scrollMethod)
            lastMessageTime.bind("<Button-4>", scrollMethod)
            lastMessageTime.bind("<Button-5>", scrollMethod)
            # message
            messageAndStatusFrame = tk.Frame(_messageFrame, bg=self.__bg)
            messageAndStatusFrame.pack(fill="x", anchor="w", padx=2)
            messageAndStatusFrame.bind("<MouseWheel>", scrollMethod)
            messageAndStatusFrame.bind("<Button-4>", scrollMethod)
            messageAndStatusFrame.bind("<Button-5>", scrollMethod)

            message = tk.Label(
                messageAndStatusFrame,
                text=chat["LastMessage"]["Content"],
                font=self.__font,
                bg=self.__bg,
                fg=self.__fg,
                anchor="w",
                justify="left",
                wraplength=CHATS_WIDTH - 60 
            )
            message.pack(side="left")
            message.bind("<Button-1>", _currentOpenFunc)
            message.bind("<MouseWheel>", scrollMethod)
            message.bind("<Button-4>", scrollMethod)
            message.bind("<Button-5>", scrollMethod)

            isMine = chat["LastMessage"]["Sender"] == self.__currentName
            read_indicator = "✔️✔️" if chat["LastMessage"]["Read"] else "✔️"
            readLabel = tk.Label(
                messageAndStatusFrame,
                text=read_indicator if isMine else "",
                font=self.__font,
                bg=self.__bg,
                fg=self.__fg
            )
            readLabel.pack(side="right", padx=5)
            readLabel.bind("<Button-1>", _currentOpenFunc)
            readLabel.bind("<MouseWheel>", scrollMethod)
            readLabel.bind("<Button-4>", scrollMethod)
            readLabel.bind("<Button-5>", scrollMethod)
        
    def openChat(self, recipient: str) -> None:
        """
        Vor.: recipient ist der Nutzername eines Chatpartners
        Eff.: Zeigt den Chatverlauf an und ermöglicht Nachrichtenversand
        Erg.: -
        """
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        self.__currentChat = recipient

        messages = getMessages(recipient)
        if messages:
            self.__lastMessageTimes[recipient] = messages[-1]["SendTime"]
        else:
            self.__lastMessageTimes[recipient] = 0

        typingBox = tk.Frame(self.contentFrame, bg=self.__bg)
        typingBox.pack(side="bottom", fill="x")

        messagesFrame = tk.Frame(self.contentFrame, bg=self.__bg)
        messagesFrame.pack(fill="both", expand=True)

        canvas = tk.Canvas(messagesFrame, bg=self.__bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(messagesFrame, orient="vertical", command=canvas.yview) # type: ignore
        canvas.configure(yscrollcommand=scrollbar.set)

        # ? Scrollbar-Anzeige
        # scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        messagesContainer = tk.Frame(canvas, bg=self.__bg)
        container_id = canvas.create_window((0, 0), window=messagesContainer, anchor="nw")

        def scrollInChat(event: tk.Event) -> None:
            if event.delta:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                canvas.yview_scroll(1 if event.num == 5 else -1, "units")

        canvas.bind("<MouseWheel>", scrollInChat)
        canvas.bind("<Button-4>", scrollInChat)
        canvas.bind("<Button-5>", scrollInChat)
        messagesContainer.bind("<MouseWheel>", scrollInChat)
        messagesContainer.bind("<Button-4>", scrollInChat)
        messagesContainer.bind("<Button-5>", scrollInChat)
        
        canvas.focus_set()

        def frameConfig(event: tk.Event) -> None:
            canvas.configure(scrollregion=canvas.bbox("all"))

        messagesContainer.bind("<Configure>", frameConfig)
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(container_id, width=e.width)
        )

        self.__messageEntry = tk.Entry(
            typingBox,
            font=self.__font,
            bg=self.__entryBG,
            fg=self.__fg,
            highlightthickness=2,
            highlightbackground=self.__entryBG,
            highlightcolor=self.__highlight
        )
        self.__messageEntry.pack(side="left", fill="x", expand=True, padx=20, pady=5)
        
        def sendCurrentMessage() -> None:
            """
            Vor.: Eine Nachricht wurde in das Eingabefeld geschrieben
            Eff.: Sendet die Nachricht und läd den Chat neu
            Erg.: -
            """
            content = self.__messageEntry.get().strip()
            if content:
                sendMessage(content, recipient)
                self.openChat(recipient)
                self.__messageEntry.delete(0, tk.END)

        self.__messageEntry.bind("<Return>", lambda event: sendCurrentMessage())

        sendButton = tk.Button(
            typingBox,
            text="Senden",
            command=sendCurrentMessage,
            font=self.__font,
            bg=self.__entryBG,
            fg=self.__entryFG,
            activebackground=self.__highlight
        )
        sendButton.pack(side="right", padx=5, pady=5)

        
        if (name := getDisplayName(recipient)):
            displayName = name[1]
        else:
            print(name[1])
            displayName = recipient
        tk.Label(
            messagesContainer, 
            text=displayName,
            font=self.__titleFont,
            bg=self.__bg,
            fg=self.__fg
        ).pack()

        for message in messages:
            mine = message["Receiver"] == recipient

            _currentMessage = tk.Frame(
                messagesContainer,
                width=MESSAGE_WIDTH,
                height=MESSAGE_HEIGHT,
                bg=self.__bg,
                bd=2,
                relief="solid"
            )
            _currentMessage.pack(anchor="ne" if mine else "nw", padx=20, pady=10)
            _currentMessage.bind("<MouseWheel>", scrollInChat)
            _currentMessage.bind("<Button-4>", scrollInChat)
            _currentMessage.bind("<Button-5>", scrollInChat)
            
            _info = tk.Frame(_currentMessage, background=self.__bg)
            _info.pack(side="right" if mine else "left", anchor="e" if mine else "w")
            _info.bind("<MouseWheel>", scrollInChat)
            _info.bind("<Button-4>", scrollInChat)
            _info.bind("<Button-5>", scrollInChat)
            
            _time = tk.Label(_info, text=formatTime(message["SendTime"]), font=self.__font, bg=self.__bg, fg=self.__fg)
            _time.grid(row=0)
            _time.bind("<MouseWheel>", scrollInChat)
            _time.bind("<Button-4>", scrollInChat)
            _time.bind("<Button-5>", scrollInChat)
            
            _read = tk.Label(_info, text="✔️✔️" if message["Read"] == 1 else "✔️", font=self.__bigFont, bg=self.__bg, fg=self.__fg)
            _read.grid(row=1)
            _read.bind("<MouseWheel>", scrollInChat)
            _read.bind("<Button-4>", scrollInChat)
            _read.bind("<Button-5>", scrollInChat)

            _content = tk.Label(
                _currentMessage,
                text=message["Content"],
                font=self.__bigFont,
                bg=self.__bg,
                fg=self.__fg,
                anchor="w",
                justify="left",
                wraplength=400
            )
            _content.pack(fill="x", side="left" if not mine else "right")
            _content.bind("<MouseWheel>", scrollInChat)
            _content.bind("<Button-4>", scrollInChat)
            _content.bind("<Button-5>", scrollInChat)

        messagesContainer.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(1.0)  

        def refreshChat() -> None:
            """
            Vor.: Der Chat ist geöffnet
            Eff.: Prüft regelmäßig auf neue Nachrichten
            Erg.: Aktualisiert die Anzeige bei neuen Nachrichten
            """
            if self.__currentChat != recipient:
                return
            new_messages = getMessages(recipient)
            last_seen = self.__lastMessageTimes.get(recipient, 0)
            if new_messages and new_messages[-1]["SendTime"] > last_seen:
                self.openChat(recipient)
            else:
                self.__window.after(5000, refreshChat)

        self.__window.after(5000, refreshChat)
            
            
    
    def showSettingsScreen(self) -> None:
        """
        Vor.: -
        Eff.: Zeigt die Einstellungen inklusive Theme- und Profiloptionen
        Erg.: -
        """
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
            font = self.__bigFont
        )
        settingsButton.place(x=10, y=10)

        #Inhalt-Übersicht
        tk.Label(
            mainContainer, 
            text="Einstellungen", 
            font=self.__titleFont,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=30)

        # Theme-Auswahl
        tk.Label(
            mainContainer,
            text="Design auswählen:",
            font=self.__bigFont,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=5)

        tk.Button(
            mainContainer,
            text="Light Theme",
            font=self.__font,
            bg=THEMES["light"]["buttonBG"],
            fg=THEMES["light"]["buttonFG"],
            command=lambda: self.setTheme("light")
        ).pack(pady=5)

        tk.Button(
            mainContainer,
            text="Dark Theme",
            font=self.__font,
            bg=THEMES["dark"]["buttonBG"],
            fg=THEMES["dark"]["buttonFG"],
            command=lambda: self.setTheme("dark")
        ).pack(pady=5)

        #Schriftgröße
        
        tk.Label(
            mainContainer,
            text="Schriftgröße anpassen:",
            font=self.__bigFont,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=5)

        def upFont() -> None:
            if self.__fontSize >= MAX_FONT_SIZE:
                self.showFontWarning("Maximale Schriftgröße erreicht.")
                return 
            self.setFont("up")
            self.showSettingsScreen()
        tk.Button(
            mainContainer,
            text="➕",
            font=self.__font,
            bg=self.__bg,
            fg=self.__fg,
            command=lambda: upFont()
        ).pack(pady=5)

        def downFont() -> None:
            if self.__fontSize <= MIN_FONT_SIZE:
                self.showFontWarning("Minimale Schriftgröße erreicht.")
                return 
            self.setFont("down")
            self.showSettingsScreen()
        tk.Button(
            mainContainer,
            text="➖",
            font=self.__font,
            bg=self.__bg,
            fg=self.__fg,
            command=lambda: downFont()
        ).pack()

        self.__fontWarningLabel = tk.Label(
            mainContainer,
            text="",
            font=self.__font,
            fg="orange",
            bg=self.__bg
        )
        self.__fontWarningLabel.pack()

        #Profilbearbeitung
        tk.Label(
            mainContainer,
            text="Profilbearbeitung:",
            font=self.__bigFont,
            bg=self.__bg,
            fg=self.__fg
        ).pack(pady=5)

        #aktueller Nutzer
        tk.Label(
            mainContainer,
            text = f"Aktueller Nutzer: {getOwnUsername()}",
            font=self.__font,
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
            font=self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady=10)
        displayNameVAR = tk.StringVar()
        self.__newDisplayName = tk.Entry(mainContainer, font = self.__font, show = "", bg=self.__entryBG, fg=self.__fg, textvariable=displayNameVAR)
        displayNameVAR.set(self.__currentName)
        self.__newDisplayName.pack()
        

        #neues PW
        # Passwört-Überschrift 1
        tk.Label(
            mainContainer, 
            text = "Neues Passwort", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__newPasswordInput1 = tk.Entry(mainContainer, font = self.__font, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__newPasswordInput1.pack()

        # Passwört-Überschrift 2
        tk.Label(
            mainContainer, 
            text = "Passwort wiederholen", 
            font = self.__font,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__newPasswordInput2 = tk.Entry(mainContainer, font = self.__font, show = "*", bg=self.__entryBG, fg=self.__fg)
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
            font = self.__font,
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

        self.__errorMessage:tk.Label = tk.Label(mainContainer, text = "", font = self.__font, fg = "red", bg=self.__bg)
        self.__errorMessage.pack(pady=10)

        #Abmelden-Button
        tk.Button(
            mainContainer,
            text="Abmelden",
            font=self.__font,
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            command=self.showLoginScreen
        ).pack(pady=15)

    def showUserSuggestions(self) -> None:
        """
        Vor.: -
        Eff.: Öffnet ein zweites Fenster mit Kontaktvorschlägen
        Erg.: -
        """
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
                """
                Vor.: username ist ein gültiger Nutzername
                Eff.: Sendet eine Begrüßungsnachricht und schließt das Fenster
                Erg.: -
                """
                sendMessage("Hallo!", username)
                secondWindow.destroy()
                self.showMainScreen()

                

            userFrame.bind("<Button-1>", lambda event, u=username: send(u))


            iconLabel = tk.Label(
            userFrame,
            text="🖼️",
            font=self.__titleFont,
            bg=self.__bg,
            fg=self.__fg
            )
            iconLabel.pack(side="left")
            iconLabel.bind("<Button-1>", lambda event, u=username: send(u))

            nameLabel = tk.Label(
                userFrame,
                text=displayName,
                font=self.__font,
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
            font=self.__font
        ).pack(pady=15)

# === Passwörter zeigen/verstecken ===

    def togglePassword(self) -> None:
        """
        Vor.: -
        Eff.: Zeigt oder versteckt das Login-Passwort
        Erg.: -
        """
        if self.showPasswordVar.get():
            self.__loginPasswordInput.config(show="")
        else:
            self.__loginPasswordInput.config(show="*")
    
    def toggleRegisterPassword(self) -> None:
        """
        Vor.: -
        Eff.: Zeigt oder versteckt das Registrierungs-Passwort
        Erg.: -
        """
        if self.showPasswordVar.get():
            self.__registerPasswordInput1.config(show="")
            self.__registerPasswordInput2.config(show="")
        else:
            self.__registerPasswordInput1.config(show="*")
            self.__registerPasswordInput2.config(show="*")
    
    def toggleNewPassword(self) -> None:
        """
        Vor.: -
        Eff.: Zeigt oder versteckt das neue Passwort im Einstellungsmenü
        Erg.: -
        """
        if self.showPasswordVar.get():
            self.__newPasswordInput1.config(show="")
            self.__newPasswordInput2.config(show="")
        else:
            self.__newPasswordInput1.config(show="*")
            self.__newPasswordInput2.config(show="*")
    
    def showFontWarning(self, message: str) -> None:
            self.__fontWarningLabel.config(text=message)
            self.__window.after(2000, lambda: self.__fontWarningLabel.config(text=""))

#==================
#= Knopf-Funktionen
#==================

    def login(self) -> None:
        """
        Vor.: Nutzerdaten wurden in die Eingabefelder eingetragen
        Eff.: Versucht eine Anmeldung über das Netzwerk
        Erg.: Öffnet das Hauptfenster bei Erfolg oder zeigt eine Fehlermeldung
        """
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
        """
        Vor.: Alle Registrierungsfelder wurden ausgefüllt
        Eff.: Versucht einen neuen Account anzulegen
        Erg.: Öffnet das Hauptfenster bei Erfolg oder zeigt eine Fehlermeldung
        """

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
        """
        Vor.: Neue Profilinformationen wurden eingegeben und bestätigt
        Eff.: Sendet die Änderungen an den Server
        Erg.: Zeigt eine Erfolgs- oder Fehlermeldung an
        """
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
            self.__errorMessage.config(text="Profil wurde erfolgreich aktualisiert!", fg="green")

#==================
#= Basis-Funktionen
#==================

    def run(self) -> None:
        """
        Vor.: -
        Eff.: Startet die Hauptschleife des GUI
        Erg.: -
        """
        self.__window.mainloop()

    def quit(self) -> None:
        """
        Vor.: -
        Eff.: Beendet die Anwendung sofort
        Erg.: -
        """
        exit(0)

#========
#= CODE
#========
interface: InterfaceHandler = InterfaceHandler()