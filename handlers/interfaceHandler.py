import tkinter as tk

AUFLOESUNG:str = "300x200"

class Benutzeroberflaeche():
    def __init__(self):
        self.__fenster = tk.Tk()
        self.__fenster.title("Massagerino")
        self.__fenster.geometry(AUFLOESUNG)
    
#öffne...Menu - Methoden

benutzeroberfläche:Benutzeroberfläche = Benutzeroberfläche()