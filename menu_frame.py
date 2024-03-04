import customtkinter
from flashcards import *


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        # self layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # place buttons
        self.buttons()

        # self.place(relx=0, rely=0.15, relwidth=1, relheight=0.7)

    def buttons(self):
        play_button = MenuButton(self, "PLAY", play_frame, "normal")
        cards_button = MenuButton(self, "CARDS", cards_frame, "normal")
        load_button = MenuButton(self, "LOAD CARDS", load_frame, "normal")
        save_button = MenuButton(self, "SAVE CARDS", save_frame, "disabled")
        try:
            if not saved_bool.get():
                save_button.configure(state="normal")
        except NameError:
            pass

        # layout
        play_button.grid(row=0, column=0)
        cards_button.grid(row=1, column=0)
        load_button.grid(row=2, column=0)
        save_button.grid(row=3, column=0)