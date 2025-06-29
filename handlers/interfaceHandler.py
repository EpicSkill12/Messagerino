import tkinter as tk
from tkinter import ttk
from sys import exit
from typing import Literal

from config.constants import RESOLUTION, FONT, BIG_FONT, THEMES, TITLE_FONT, MIN_SIZE_X, MIN_SIZE_Y, NAME, ICON_PATH, LOGO_PATH, MAX_SIZE_X, MAX_SIZE_Y
from helpers.validationHelper import validatePassword, validateUser
from helpers.formattingHelper import getPossessive
from handlers.loginHandler import tryLogin, trySignup
from PIL import Image, ImageTk
from handlers.loginHandler import getOwnUsername


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
        chat_frame_width = 330
        separator_x = chat_frame_width + ((window_width - chat_frame_width) * 0.01)  # kleine Einrückung

        #Hauptcontainer
        mainContainer = tk.Frame(self.__window, bg=self.__bg)
        mainContainer.pack(fill="both", expand=True)

        # Vertikale Trennlinie
        separator = tk.Frame(self.__window, bg=self.__entryBG, width=2)
        separator.place(x=separator_x, y=0, relheight=1.0)

        #Linke Spalte
        chatListFrame = tk.Frame(mainContainer, width=330, bg=self.__bg)
        chatListFrame.pack(side="left", fill="y")

        #Rechte Spalte
        contentFrame = tk.Frame(mainContainer, bg=self.__bg)
        contentFrame.pack(side="right", fill="both", expand=True)

        settingsImg = Image.open("assets/settings_m.png").resize((30, 30)) # type: ignore
        self.__settingsPhoto = ImageTk.PhotoImage(settingsImg)

        settingsButton = tk.Button(
            chatListFrame,
            image = self.__settingsPhoto,
            command = self.showSettingsScreen,
            bd = 0,
            highlightthickness = 0,
            relief = "flat",
            bg = "white",
            activebackground = "white"
        )
        settingsButton.place(x=10, y=10)

        #Chat-Übersicht
        tk.Label(
            chatListFrame, 
            text=f"{getPossessive(self.__currentName)} Chats",
            font=BIG_FONT,
            bg=self.__bg,
            fg = self.__fg
        ).place(x=165, y=30, anchor="n") 

        # for chat in getChats():
        #     chatFrame = tk.Frame(
        #         chatListFrame, 
        #         bd=1, 
        #         relief="solid", 
        #         padx=5, 
        #         pady=5
        #     )
        #     chatFrame.pack(fill="x", pady=2, padx=5)

        #     tk.Label(
        #         chatFrame, 
        #         text=chat.getRecipient().getDisplayName(), 
        #         font=BIG_FONT, 
        #         anchor="w"
        #     ).pack(fill="x")
        #     tk.Label(
        #         chatFrame, 
        #         text=chat.getLastMessage().getContent(), 
        #         font=FONT, 
        #         anchor="w"
        #     ).pack(fill="x")

        #Inhalt-Übersicht
        tk.Label(
            contentFrame, 
            text="Willkommen bei Messagerino! 👋", 
            font=BIG_FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady=30)
        tk.Label(
            contentFrame, 
            text="Wähle links einen Chat aus, um die Unterhaltung zu starten.", 
            font=FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack()
        
    
    def showSettingsScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        self.applyTheme()

        mainContainer = tk.Frame(self.__window, bg=self.__bg)
        mainContainer.pack(fill="both", expand=True)

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
        )

        #neues PW
        # Passwört-Überschrift 1
        tk.Label(
            mainContainer, 
            text = "Neues Passwort", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__newPasswordInput1 = tk.Entry(self.__register_frame, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__newPasswordInput1.pack()

        # Passwört-Überschrift 2
        tk.Label(
            mainContainer, 
            text = "Passwort wiederholen", 
            font = FONT,
            bg=self.__bg,
            fg = self.__fg
        ).pack(pady = 10)
        self.__newPasswordInput2 = tk.Entry(self.__register_frame, font = FONT, show = "*", bg=self.__entryBG, fg=self.__fg)
        self.__newPasswordInput2.pack()

        # Checkbox zum Anzeigen des Passworts
        self.showPasswordVar = tk.BooleanVar()
        ttk.Checkbutton(
            self.__register_frame,
            text = "Passwort anzeigen",
            variable = self.showPasswordVar,
            command = self.toggleNewPassword,
            style="Custom.TCheckbutton"
        ).pack(pady = 15)
        

        #Abmelden-Button
        tk.Button(
            mainContainer,
            text="Abmelden",
            font=FONT,
            bg="#E74C3C",
            fg="white",  # weißer Text hebt sich besser ab
            activebackground="#C0392B",
            command=self.showLoginScreen
        ).pack(pady=200)

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