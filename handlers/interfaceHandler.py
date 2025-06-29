import tkinter as tk
from tkinter import ttk
from sys import exit
from config.constants import INTERFACE_COLOR, RESOLUTION, FONT, BIG_FONT, TITLE_FONT, MIN_SIZE_X, MIN_SIZE_Y, NAME, ICON_PATH, LOGO_PATH, MAX_SIZE_X, MAX_SIZE_Y
from helpers.validationHelper import validatePassword, validateUser
from helpers.formattingHelper import getPossessive
from handlers.loginHandler import tryLogin, trySignup
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
            font = TITLE_FONT
        ).pack()

        self.__loginFrame: tk.Frame = tk.Frame(self.__window)
        self.__loginFrame.pack(expand = True, anchor="n", pady=50)
        
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

        self.__window.update_idletasks()

        window_width = self.__window.winfo_width()
        chat_frame_width = 330
        separator_x = chat_frame_width + ((window_width - chat_frame_width) * 0.01)  # kleine Einrückung

        #Hauptcontainer
        mainContainer = tk.Frame(self.__window)
        mainContainer.pack(fill="both", expand=True)

        # Vertikale Trennlinie
        separator = tk.Frame(self.__window, bg="gray", width=2)
        separator.place(x=separator_x, y=0, relheight=1.0)

        #Linke Spalte
        chatListFrame = tk.Frame(mainContainer, width=330, bg=INTERFACE_COLOR)
        chatListFrame.pack(side="left", fill="y")

        #Rechte Spalte
        contentFrame = tk.Frame(mainContainer)
        contentFrame.pack(side="right", fill="both", expand=True)

        settingsImg = Image.open("assets/settings_m.png").resize((30, 30))
        self.__settingsPhoto = ImageTk.PhotoImage(settingsImg)

        settingsButton = tk.Button(
            chatListFrame,
            image = self.__settingsPhoto,
            command = self.showSettingsScreen,
            bd = 0,
            highlightthickness = 0,
            relief = "flat",
            bg = INTERFACE_COLOR,
            activebackground = "white"
        )
        settingsButton.place(x=10, y=10)

        #Chat-Übersicht
        tk.Label(
            chatListFrame, 
            text=f"{getPossessive(self.__currentName)} Chats",
            font=BIG_FONT,
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
            font=BIG_FONT
        ).pack(pady=30)
        tk.Label(
            contentFrame, 
            text="Wähle links einen Chat aus, um die Unterhaltung zu starten.", 
            font=FONT
        ).pack()
        

    def showSettingsScreen(self) -> None:
        for widget in self.__window.winfo_children():
            widget.destroy()
        
        mainContainer = tk.Frame(self.__window)
        mainContainer.pack(fill="both", expand=True)

        #Inhalt-Übersicht
        tk.Label(
            mainContainer, 
            text="Einstellungen", 
            font=TITLE_FONT
        ).pack(pady=30)

        # Abmelden-Button
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