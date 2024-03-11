import os
import tempfile
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from googletrans import Translator
import customtkinter as ctk
import random
from settings import *
from widgets import *
import pygame
import sqlite3
from gtts import gTTS
from io import BytesIO

# menu choices frames
# sounds
pygame.init()

# open app
pygame.mixer.Sound("audio/open_app.wav").play()

# app soundtrack
soundtrack = pygame.mixer.Sound(SOUNDTRACK_PATH)
soundtrack.set_volume(0.08)
soundtrack.play(loops=-1)

# connect to databse
conn = sqlite3.connect("cards.db")
cur = conn.cursor()


def start_screen(canvas, label):
    global CURRENT_FRAME

    label.place_forget()

    #canvas.animate()
    while True:
        if canvas.frame_index < canvas.animation_length:
            print(canvas.frame_index, canvas.animation_length)
            app.after(canvas.animation_speed, canvas.animate())
            app.update()
        else: break

    CURRENT_FRAME = "menu"
    app.frame_choice()



def change_soundtrack():
    global soundtrack
    soundtrack.stop()
    name = soundtrack_style.get()
    soundtrack = pygame.mixer.Sound(f"audio/soundtracks/{name}.mp3")
    soundtrack.set_volume(0.08)
    if music_sound == "on":
        soundtrack.play(loops=-1)


def back_home():
    global CURRENT_FRAME
    global cards_selected
    global cards_selected_int

    # sounds
    sound_click.play().set_volume(volume)

    CURRENT_FRAME = "menu"
    app.frame_choice()
    app.cards_info()

    cards_selected = []
    cards_selected_int = 0
    delete_var.set(f"Delete ({cards_selected_int})")


def play_frame():
    global CURRENT_FRAME
    global app
    global current_card
    global dictionary_list
    global current_side

    # sounds
    sound_click.play().set_volume(volume)

    current_card = 0
    dictionary_list = []
    current_side = "key"

    # check if there are some cards marked as starred
    # if play_mode.get() == "star" and len(hard_list) == 0:
    #     messagebox.showerror(title="Error", message="No starred cards")
    #     CURRENT_FRAME = "menu"
    #     app.frame_choice()
    #     return

    if len(dictionary) > 0:
        if play_mode.get() == "star":
            for key in hard_list:
                dictionary_list.append((key, dictionary[key]))
        else:
            for key, value in dictionary.items():
                dictionary_list.append((key, value))

        # shuffle the cards
        random.shuffle(dictionary_list)
        # make sure that the word fits
        word = dictionary_list[current_card][0]
        if 15 < len(word) < 30:
            word = f"{word[0:15]}-\n{word[15:30]}"
        elif len(word) > 30:
            word = f"{word[0:15]}-\n{word[15:30]}-\n{word[30:]}"

        play_word.set(word)
        play_number.set(f"{current_card + 1}/{len(dictionary_list)}")

        #read the card
        if tts_var.get() == "on":
            play_tts(word, 1)

    else:
        # sound
        pygame.mixer.Sound(DELETE_SOUND_PATH).play().set_volume(volume * 0.2)

        messagebox.showerror(title="Error", message="You don't have any cards")
        play_word.set("")
        play_number.set("No cards")
        CURRENT_FRAME = "menu"
        app.frame_choice()
        return

    CURRENT_FRAME = "play_flashcards"
    app.frame_choice()


def play_guess_frame():
    global CURRENT_FRAME
    CURRENT_FRAME = "play_guess"
    app.frame_choice()


def play_tts(text, number):
    if (number == 1 and tts_first_v.get() == "None") or (number == 2 and tts_second_v.get() == "None"):
        return

    lang_variable = tts_first_v.get() if number == 1 else tts_second_v.get()
    tts = gTTS(text=text, lang=shortcut_translator[lang_variable], slow=False)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.write_to_fp(temp_audio)
    pygame.mixer.Sound(temp_audio.name).play()
    os.remove(temp_audio.name)


def change_play_mode(card_frame, checkbox):
    print(play_mode.get())
    if play_mode.get() == "star" and len(hard_list) == 0:
        messagebox.showerror(title="Error", message="No starred cards")
        play_mode.set("normal")
        return
    play_frame()
    if play_mode.get() == "star":
        print("here")
        card_frame.configure(border_color=HARD_COLOR_GOLD)
    else:
        card_frame.configure(border_color="#add1f0")


def flip_card(_, self):
    global current_side
    global CURRENT_FRAME

    pygame.mixer.Sound(FLIP_SOUND_PATH).play().set_volume(volume)

    if current_side == "key":
        print(dictionary_list)
        word = dictionary_list[current_card][1]
        if 15 < len(word) < 30:
            word = f"{word[0:15]}-\n{word[15:30]}"
        elif len(word) > 30:
            word = f"{word[0:15]}-\n{word[15:30]}-\n{word[30:]}"

        self.configure(fg_color="#28b790")

        play_word.set(word)
        current_side = "value"

        # read the card
        if tts_var.get() == "on":
            play_tts(word, 2)

    elif current_side == "value":
        word = dictionary_list[current_card][0]
        if 15 < len(word) < 30:
            word = f"{word[0:15]}-\n{word[15:30]}"
        elif len(word) > 30:
            word = f"{word[0:15]}-\n{word[15:30]}-\n{word[30:]}"

        self.configure(fg_color="#2876b7")

        play_word.set(word)
        current_side = "key"

        # read the card
        if tts_var.get() == "on":
            play_tts(word, 1)

    elif current_side == "end":
        CURRENT_FRAME = "menu"
        app.frame_choice()


def flip_color(event, self):
    if current_side == "value":
        self.configure(fg_color="#28b790")
    else:
        self.configure(fg_color="#2876b7")


def next_card(card, button_hard, button_next):
    global current_card
    global CURRENT_FRAME
    global current_side

    # sounds
    sound_click.play().set_volume(volume)

    if play_mode.get() == "star" and current_card < len(hard_list) - 1:
        current_card += 1

        word = dictionary_list[current_card][0]
        if 15 < len(word) < 30:
            word = f"{word[0:15]}-\n{word[15:30]}"
        elif len(word) > 30:
            word = f"{word[0:15]}-\n{word[15:30]}-\n{word[30:]}"

        play_word.set(word)
        play_number.set(f"{current_card + 1}/{len(dictionary_list)}")

        app.frame_choice()
        current_side = "key"

        # read the card
        if tts_var.get() == "on":
            play_tts(word, 1)
    elif play_mode.get() == "normal" and current_card < len(dictionary) - 1:
        current_card += 1

        word = dictionary_list[current_card][0]
        if 15 < len(word) < 30:
            word = f"{word[0:15]}-\n{word[15:30]}"
        elif len(word) > 30:
            word = f"{word[0:15]}-\n{word[15:30]}-\n{word[30:]}"

        play_word.set(word)
        play_number.set(f"{current_card + 1}/{len(dictionary)}")

        app.frame_choice()
        current_side = "key"

        # read the card
        if tts_var.get() == "on":
            play_tts(word, 1)
    else:
        # sound
        pygame.mixer.Sound(FINISHED_SOUND_PATH).play().set_volume(volume)
        play_word.set("FINISHED\nclick to exit")
        button_next.configure(state="disabled")
        button_hard.configure(state="disabled")
        # messagebox.showinfo(title="Finished", message="All cards exercised")
        current_side = "end"
        card.configure(fg_color="#31a229")


def next_card_guess(guess_var, button_next, score_var, entry, result_show):
    global current_card
    global CURRENT_FRAME
    global current_side

    # sounds
    sound_click.play().set_volume(volume)

    # check if the previous guess is correct
    if guess_var.get().lower() == dictionary[play_word.get()].lower():
        score_var.set(score_var.get() + 1)
        # show the result in the label
        result_show.configure(text="Correct", text_color=GREEN_LOAD)
        entry.configure(fg_color=GREEN_LOAD)
        app.update()
        app.after(500, result_show.configure(text=""), entry.configure(fg_color="white"))

    else:
        result_show.configure(text=f"False, correct was \"{dictionary[play_word.get()]}\"", text_color="red")
        entry.configure(fg_color="red")
        app.update()
        app.after(1000, result_show.configure(text=""), entry.configure(fg_color="white"))

    if current_card < len(dictionary) - 1:
        guess_var.set(value="")
        current_card += 1

        word = dictionary_list[current_card][0]
        if 15 < len(word) < 30:
            word = f"{word[0:15]}-\n{word[15:30]}"
        elif len(word) > 30:
            word = f"{word[0:15]}-\n{word[15:30]}-\n{word[30:]}"

        play_word.set(word)
        play_number.set(f"{current_card + 1}/{len(dictionary_list)}")

        app.update()
        current_side = "key"

        # read the card
        if tts_var.get() == "on":
            play_tts(word, 1)
    else:
        # sound
        pygame.mixer.Sound(FINISHED_SOUND_PATH).play().set_volume(volume)
        play_word.set("FINISHED\nclick to exit")
        button_next.configure(state="disabled")
        # messagebox.showinfo(title="Finished", message="All cards exercised")
        current_side = "end"
        messagebox.showinfo(title="Finished", message=f"You finished with {score_var.get()} points")
        CURRENT_FRAME = "menu"
        app.frame_choice()



def cards_frame():
    global CURRENT_FRAME
    global cards_display
    global CARDS_ROWS

    # sounds
    sound_click.play().set_volume(volume)

    # change interface
    CURRENT_FRAME = "cards"
    app.frame_choice()

    # add current cards to grid
    CARDS_ROWS = 0
    for key, value in dictionary.items():
        AddCardsToFrame(key, value, CARDS_ROWS, cards_display, cards_selected_int, cards_selected, delete_var, hard_list)
        CARDS_ROWS += 1

    key_var.set("")
    value_var.set("")


def load_cards():
    # sounds
    sound_click.play().set_volume(volume)

    file_path = filedialog.askopenfile(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    try:
        with open(file_path.name, "r", encoding='utf-8') as file:
            for line in file:
                text = line.strip()
                text_cor = text.split("-")
                print(text_cor)
                dictionary[text_cor[0]] = text_cor[1]
                print(dictionary)

            # load sound
            pygame.mixer.Sound(SUCCESS_SOUND_PATH).play().set_volume(volume)
    except AttributeError:
        pass
    app.cards_info()


def save_frame():
    global CURRENT_FRAME
    # sounds
    sound_click.play().set_volume(volume)

    CURRENT_FRAME = "save"
    app.frame_choice()
    # file_path = filedialog.asksaveasfilename(
    #     filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    #     defaultextension=".txt")
    # with open(file_path, "w", encoding='utf-8') as file:
    #     for key, value in dictionary.items():
    #         file.write(f"{key}-{value}\n")

    # get all tables name from database


def save_to_db(name_var):
    global CURRENT_FRAME
    try:
        # create table and inset values if the table doesnt exist
        cur.execute(f"CREATE TABLE \'{name_var.get()}\' (key TEXT, value TEXT);")
        for key, value in dictionary.items():
            cur.execute(f"INSERT INTO \'{name_var.get()}\' (key, value) VALUES (\'{key}\', \'{value}\');")
            conn.commit()
        conn.commit()
        saved_bool.set(value=True)
        CURRENT_FRAME = "menu"
        app.frame_choice()
        # sounds
        pygame.mixer.Sound(SAVE_SOUND_PATH).play().set_volume(volume)
        # create table and inset values if the table exists
    except sqlite3.OperationalError as e:
        print(e)
        override_bool = messagebox.askyesno("Override", f"Override save - {name_var.get()} ")
        # if user wants to override the old databse (delete old and create new)
        if override_bool:
            cur.execute(f"DROP TABLE \'{name_var.get()}\'")
            cur.execute(f"CREATE TABLE \'{name_var.get()}\' (key TEXT, value TEXT);")
            for key, value in dictionary.items():
                cur.execute(f"INSERT INTO \'{name_var.get()}\' (key, value) VALUES (\'{key}\', \'{value}\');")
                conn.commit()
            # load items
            saved_bool.set(value=True)
            CURRENT_FRAME = "menu"
            app.frame_choice()
            # sounds
            pygame.mixer.Sound(SAVE_SOUND_PATH).play().set_volume(volume)

    # except sqlite3.OperationalError as e:
    #     print(e)
    #     name_var.set(value="Name already exists")
    #     app.after(500, lambda:name_var.set(value=""))


def delete_from_db(variable):
    #check if the table exists
    try:
        cur.execute(f"SELECT * FROM {variable.get()}")

        delete_bool = messagebox.askyesno("Delete", f"Delete save - {variable.get()}")
        if delete_bool:
            cur.execute(f"DROP TABLE \'{variable.get()}\'")
            conn.commit()
            variable.set("")
            pygame.mixer.Sound(DELETE_SOUND_PATH).play().set_volume(volume * 0.2)
    except sqlite3.OperationalError:
        messagebox.showerror("Error ", f"No save named - {variable.get()}")


def translate_input(_):
    translator = Translator()
    text_to_translate = key_var.get()
    translated_text = translator.translate(text_to_translate, dest=shortcut_translator[language_var.get()])
    value_var.set(translated_text.text)
    # add_card()


def add_card():
    global CARDS_ROWS
    # add to grid

    # sounds
    sound_click.play().set_volume(volume)

    def selected(_):
        global cards_selected_int
        global cards_selected

        # sound on click
        sound_click.play().set_volume(volume)

        # if the row isnt already selected
        if is_selected.get() == False:
            is_selected.set(True)
            table_row.configure(fg_color="#f27550")
            cards_selected_int += 1
            delete_var.set(f"Delete ({cards_selected_int})")
            cards_selected.append(key)
        else:
            is_selected.set(False)
            table_row.configure(fg_color="transparent")
            cards_selected.remove(key)
            cards_selected_int -= 1
            delete_var.set(f"Delete ({cards_selected_int})")

    def enter(_):
        print(is_selected.get())
        if is_selected.get():
            pass
        else:
            table_row.configure(fg_color="#c8e0f4")

    def leave(_):
        print(is_selected)
        if is_selected.get():
            pass
        else:
            table_row.configure(fg_color="transparent")

    # check if the value already exist or insnt empty
    if key_var.get() not in dictionary.keys() and key_var.get() != "" and value_var.get() != "":
        cards_display.rowconfigure(CARDS_ROWS, weight=1)

        table_row = ctk.CTkFrame(cards_display, fg_color="transparent", width=800, height=38)
        # table_row.rowconfigure(0, weight=1)
        # table_row.columnconfigure((0,1), weight=1)

        # get the key form input and make it maximum 15 characters
        key = key_var.get()
        if len(key) > 14:
            key = f"{key[0:12]}..."

        value = value_var.get()
        if len(value) > 14:
            value = f"{value[0:12]}..."

        # layout
        table_row.grid(row=CARDS_ROWS, column=0, columnspan=3, pady=5)
        # TableItem(table_row, key).grid(row=0, column=0, sticky="w", pady=5)
        # TableItem(table_row, value).grid(row=0, column=1, sticky="w", pady=5)
        key_display = TableItem(table_row, key)
        key_display.place(relx=0.05, rely=0.5, anchor="w")
        TableItem(table_row, value).place(relx=0.5, rely=0.5, anchor="w")

        # event - hover effect
        is_selected = ctk.BooleanVar(value=False)
        table_row.bind("<Enter>", enter)
        table_row.bind("<Leave>", leave)
        table_row.bind("<Button-1>", selected)

        # load card to dictionary
        dictionary[key_var.get()] = value_var.get()

        app.cards_info()
        key_var.set("")
        value_var.set("")
        CARDS_ROWS += 1
        saved_bool.set(value=False)
    else:
        if key_var.get() == "":
            messagebox.showerror(title="Empty", message="Key can't be empty")
        elif value_var.get() == "":
            messagebox.showerror(title="Error", message="Value can't be empty")
        else:
            messagebox.showerror(title="Error", message="Key already exists")


def delete_cards():
    global cards_selected_int
    global cards_selected
    global CURRENT_FRAME

    # sounds
    pygame.mixer.Sound(DELETE_SOUND_PATH).play().set_volume(volume * 0.2)

    # deleting cards from dictionary
    if len(cards_selected) > 0:
        for key in cards_selected:
            dictionary.pop(key)

        # set values to zero in gui
        cards_selected = []
        cards_selected_int = 0
        delete_var.set(f"Delete ({cards_selected_int})")

        if len(dictionary) == 0:
            saved_bool.set(value=True)
        else:
            saved_bool.set(value=False)
        CURRENT_FRAME = "menu"
        app.frame_choice()
        app.cards_info()


def load_frame():
    global CURRENT_FRAME

    sound_click.play().set_volume(volume)

    CURRENT_FRAME = "load"
    app.frame_choice()


def load_db_file(text_var):
    global CURRENT_FRAME

    # check if I am not trying to select empty table
    try:
        result_list = cur.execute(f"SELECT * FROM '{load_selected.get()}'").fetchall()
    except sqlite3.OperationalError:
        return
    # if it is empty do not return back to menu
    if not result_list:
        text_var.set(value="Empty save")
        app.update()
        app.after(1000, text_var.set(value=""))
    else:
        for card in result_list:
            dictionary[card[0]] = card[1]

        app.cards_info()
        # load sound
        saved_bool.set(value=False)
        pygame.mixer.Sound(SUCCESS_SOUND_PATH).play().set_volume(volume)
        CURRENT_FRAME = "menu"
        app.frame_choice()


def settings_frame():
    global CURRENT_FRAME
    CURRENT_FRAME = "settings"
    app.frame_choice()


def mark_hard(word_key, button):
    if word_key in hard_list:
        hard_list.remove(word_key)
        image = "star-empty"
    else:
        hard_list.add(word_key)
        image = "star-full"
        pygame.mixer.Sound(STAR_CLICK_PATH).play().set_volume(volume * 0.6)
    image_ctk = ctk.CTkImage(Image.open(f"images/{image}.png"), size=(40,40))
    button.configure(image=image_ctk)


def mode_choice(mode):
    global CURRENT_FRAME
    if mode == "flashcards":
        CURRENT_FRAME = "play_flashcards"
    else:
        CURRENT_FRAME = "play_guess"

    app.frame_choice()


# app
class Flashcards(ctk.CTk):
    def __init__(self):
        super().__init__()

        # size
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.title("Flashcards")
        self.configure(fg_color=APP_COLOR)

        # place initial frame (without animation)
        # self.frame_display = MenuFrame(self)
        # self.frame_display.place(relx=0, rely=0.15, relwidth=1, relheight=0.7)

        # add settings
        self.setting = self.settings()
        self.setting.place(relx=0.99, rely=0.01, anchor="ne")

        # add frame / widgets
        self.cards_info()
        self.home_button()

        # place initial frame (animation)
        self.frame_display = StartScreen(self)
        self.frame_display.place(relx=0, rely=0, relwidth=1, relheight=1)

    def frame_choice(self):
        self.frame_display.place_forget()
        if CURRENT_FRAME == "menu":
            self.frame_display = MenuFrame(self)
            self.setting.place(relx=0.99, rely=0.01, anchor="ne")
            self.frame_display.place(relx=0, rely=0.15, relwidth=1, relheight=0.7)
        elif CURRENT_FRAME == "cards":
            self.frame_display = CardsFrame(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)
        elif CURRENT_FRAME == "play":
            self.frame_display = PlayChoice(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        elif CURRENT_FRAME == "play_flashcards":
            self.frame_display = PlayFrame(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        elif CURRENT_FRAME == "play_guess":
            self.frame_display = PlayGuessFrame(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        elif CURRENT_FRAME == "save":
            self.frame_display = SaveFrame(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        elif CURRENT_FRAME == "load":
            self.frame_display = LoadFrame(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
        elif CURRENT_FRAME == "settings":
            self.frame_display = SettingsFrame(self)
            self.setting.place_forget()
            self.frame_display.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def cards_info(self):
        label = MenuLabel(self, f"NUMBER OF CARDS: {len(dictionary)}")
        label.place(relx=0.5, rely=0.97, anchor="center")

    def home_button(self):
        home_icon = ctk.CTkImage(Image.open("images\\home.png"), size=(71, 71))
        home_button = ctk.CTkButton(
            self,
            image=home_icon,
            text="",
            width=71,
            height=71,
            fg_color="transparent",
            command=back_home,
        )
        home_button.place(relx=0.01, rely=0.01)

    def settings(self):
        settings_icon = ctk.CTkImage(Image.open("images\\settings_icon.png"), size=(71, 71))
        settings_button = ctk.CTkButton(
            self,
            image=settings_icon,
            text="",
            width=71,
            height=71,
            fg_color="transparent",
            command=settings_frame,
        )
        return settings_button
        # settings_button.place(relx=0.99, rely=0.01, anchor="ne")


class StartScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.animation()

    def animation(self):
        canvas = AnimationStart(self, "animation/start-3")
        canvas.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")
        label = ctk.CTkLabel(self, text="Hover to start", font=(FONT_FAMILY, 40, "italic"), fg_color="#87c5f7", text_color="#22366b")
        label.place(relx=0.5, rely=0.5, anchor="center")

        canvas.bind("<Enter>", lambda _:start_screen(canvas, label))


#menu frame
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


# cards frame
class PlayChoice(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.widgets()

    def widgets(self):
        info_label = ctk.CTkLabel(self, text="Choose play mode:", font=(FONT_FAMILY, 60, "bold"))

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")

        mode_one_button = ChoiceButton(buttons_frame, "Flashcards", lambda :mode_choice("flashcards"))
        mode_two_button = ChoiceButton(buttons_frame, "Guess", lambda : mode_choice("guess"))

        # layout
        info_label.pack(pady=100)
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        mode_one_button.pack(pady=80)
        mode_two_button.pack()



class CardsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

        # add frames
        self.InputFrame(self)
        self.AllCardsFrame(self)

    # top part with inputs
    class InputFrame(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="transparent")

            # self layout
            self.columnconfigure((0, 1), weight=1, uniform="both")
            self.rowconfigure((0, 1), weight=1, uniform="both")

            self.pack()

            # add widgets
            self.widgets_add()

        def widgets_add(self):
            add_button = ctk.CTkButton(
                self,
                width=614,
                height=52,
                corner_radius=19,
                fg_color=ADD_FRAME_BLUE,
                font=(FONT_FAMILY, 38, "bold"),
                text="ADD CARD",
                text_color="white",
                command=add_card,
            )
            key_input = AddInput(self, key_var)
            value_input = AddInput(self, value_var)

            # layout
            key_input.grid(row=0, column=0, pady=15)
            value_input.grid(row=0, column=1, pady=15)
            add_button.grid(row=1, column=0, columnspan=2)

            # events
            # if auto translate is on
            if auto_trans_var.get() == "on":
                key_input.bind("<Return>", translate_input)
                value_input.configure(state="disabled", fg_color="#999999")
            else:
                key_input.bind("<Return>", lambda _: value_input.focus_set())
                value_input.configure(state="normal", fg_color="white")
                value_input.bind("<Return>", lambda _: (add_card(), key_input.focus_set()))

    # bottom part
    class AllCardsFrame(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="transparent")

            self.widgets_all()

            self.pack()

        def widgets_all(self):
            global cards_display
            box = BoxFrame(self)
            column_name = TableNameFrame(box)
            cards_display = ScrollFrame(box)
            delete_button = DeleteButton(self, delete_var, delete_cards)

            cards_display.columnconfigure((0, 1), weight=1)

            # layout
            box.pack()
            column_name.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.1)
            cards_display.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.7)
            delete_button.place(relx=0.1, rely=0.88, relwidth=0.80)


class PlayFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.widgets()

    def widgets(self):
        info_label = ctk.CTkLabel(
            self,
            text="CLICK ON CARD TO REVEAL SOLUTION",
            font=(FONT_FAMILY, 19, "bold", "italic")
        )
        switch_mode = ctk.CTkCheckBox(
            self,
            variable=play_mode,
            offvalue="normal",
            onvalue="star",
            command=lambda: change_play_mode(play_card, switch_mode),
            checkbox_width=30,
            checkbox_height=30,
            font=(FONT_FAMILY, 20, "bold"),
            textvariable=play_mode
        )
        play_card = self.PlayCard(self, "#2876b7")

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        next_button = NextButton(buttons_frame, lambda: next_card(play_card, hard_button, next_button))
        #hard button
        play_word_local = play_word.get()
        if play_word_local in hard_list:
            image = "star-full"
        else: image = "star-empty"
        star_image = ctk.CTkImage(Image.open(f"images/{image}.png"), size=(40,40))
        hard_button = NextButton(buttons_frame, lambda: mark_hard(play_word.get(), hard_button))
        hard_button.configure(
            width=100,
            text="",
            fg_color=HARD_COLOR,
            image=star_image
        )

        status_label = ctk.CTkLabel(
            self,
            font=(FONT_FAMILY, 50, "bold"),
            textvariable=play_number,
        )

        # layout
        switch_mode.pack(pady=5)
        info_label.pack(pady=5)
        play_card.pack(pady=15)
        buttons_frame.pack(pady=15)
        next_button.pack(side="left")
        hard_button.pack(padx=10)
        status_label.pack(pady=15)

        # event
        next_button.bind("<Button-1>", lambda _: self.PlayCard(self, "#28b790"))

        #change theme if the mode is different
        if play_mode.get() == "star":
            play_card.configure(border_color=HARD_COLOR_GOLD)
            next_button.configure(fg_color=HARD_COLOR_GOLD)
            next_button.configure(hover_color="#b0ae1c")
            switch_mode.configure(fg_color=HARD_COLOR_GOLD)

    class PlayCard(ctk.CTkFrame):
        def __init__(self, parent, fg_color):
            super().__init__(
                parent,
                corner_radius=55,
                width=580,
                height=620,
                fg_color=fg_color,
                border_width=8,
                border_color="#add1f0",
            )

            # add text
            self.widget()

            # events (click on card)
            self.bind("<Button-1>", lambda _: flip_card(_, self))
            # self.bind("<Button-1>", flip_color(self))

        def widget(self):
            display_word = ctk.CTkLabel(
                self,
                font=(FONT_FAMILY, 60, "bold"),
                textvariable=play_word,
            )

            # layout
            display_word.place(relx=0.5, rely=0.5, anchor="center")


class PlayGuessFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.widgets()

    def widgets(self):
        score_var = ctk.IntVar()
        guess_var = ctk.StringVar()

        info_label = ctk.CTkLabel(
            self,
            text="\"WRITE THE CORRECT ANSWER AND PRESS NEXT\"",
            font=(FONT_FAMILY, 19, "bold", "italic")
        )

        game_frame = ctk.CTkFrame(
            self,
            fg_color=MID_BLUE,
            corner_radius=30,
            border_width=7,
            border_color="#add1f0",
            height=600,
            width=800
        )

        key_word = ctk.CTkLabel(
                game_frame,
                font=(FONT_FAMILY, 60, "bold"),
                textvariable=play_word,
                text_color="white",
        )
        # guess input box
        guess_entry = AddInput(game_frame, guess_var)
        guess_entry.configure(width=500, justify="center")

        guess_entry.bind("<Return>", lambda _: next_card_guess(guess_var, next_button, score_var, guess_entry, result_show))

        #titles
        score_title = ctk.CTkLabel(game_frame, font=(FONT_FAMILY, 40, "bold"), text="Your score is:", text_color="white")
        score_label = ctk.CTkLabel(game_frame, font=(FONT_FAMILY, 70, "bold"), textvariable=score_var, text_color="white")
        result_show = ctk.CTkLabel(game_frame, font=(FONT_FAMILY, 30, "bold"), text="")

        next_button = NextButton(self, lambda: next_card_guess(guess_var, next_button, score_var, guess_entry, result_show))
        status_label = ctk.CTkLabel(
            self,
            font=(FONT_FAMILY, 50, "bold"),
            textvariable=play_number,
        )


        # layout
        info_label.pack(pady=5)

        game_frame.place(rely=0.4, relx=0.5, anchor="center", relwidth=0.75, relheight=0.6)
        key_word.pack(pady=50)
        guess_entry.pack()
        result_show.pack(pady=10)
        score_title.pack(pady=10)
        score_label.pack()
        next_button.place(relx=0.5, rely=0.85, anchor="center")
        status_label.place(relx=0.5, rely=0.95, anchor="center")


# save frame
class SaveFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.save_name = ctk.StringVar(value="")

        self.display_tables()

    def display_tables(self):
        # box with saved files
        box_display = BoxFrame(self)
        box_display.configure(width=500)

        column_label = TableHeaderSave(box_display, "SAVED FILES")
        name_scroll = ScrollFrame(box_display)
        # name input
        name_input = AddInput(self, textvariable=self.save_name)
        name_input.configure(width=500)
        # save button
        save_button = ctk.CTkButton(
            self,
            width=400,
            height=52,
            corner_radius=19,
            fg_color=ADD_FRAME_BLUE,
            font=(FONT_FAMILY, 38, "bold"),
            text="Save",
            text_color="white",
            command=lambda: save_to_db(self.save_name),
        )

        # layout
        box_display.pack()
        column_label.place(relx=0.5, rely=0.02, anchor="n", relwidth=0.93, relheight=0.1)
        name_scroll.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.8)
        name_input.pack(pady=20)
        save_button.pack(pady=20)

        self.add_decks(name_scroll)

    def add_decks(self, parent):
        decks_db = cur.execute(
            "SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) DESC;").fetchall()
        all_decks = [n[0] for n in decks_db]
        for name in all_decks:
            row_frame = ctk.CTkFrame(parent, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)
            row_frame.columnconfigure(0, weight=1)
            row_frame.rowconfigure(0, weight=1)

            # add values from entry and import to database
            item = (TableItem(row_frame, text=name))
            item.grid(column=0, row=0)


class LoadFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.save_name = ctk.StringVar(value="")

        self.all_objects = []

        self.display_tables()

    def display_tables(self):
        # box with saved files
        box_display = BoxFrame(self)
        box_display.configure(width=500)

        column_label = TableHeaderSave(box_display, "LOAD")
        name_scroll = ScrollFrame(box_display)

        # save button
        load_button = ctk.CTkButton(
            self,
            width=400,
            height=52,
            corner_radius=19,
            fg_color=ADD_FRAME_BLUE,
            font=(FONT_FAMILY, 38, "bold"),
            text="LOAD",
            text_color="white",
            command=lambda: load_db_file(empty_info_var),
        )

        # shows if label is empty
        empty_info_var = ctk.StringVar(value="")
        empty_label = ctk.CTkLabel(
            self,
            font=(FONT_FAMILY, 30, "bold"),
            textvariable=empty_info_var,
        )

        # layout
        box_display.pack()
        column_label.place(relx=0.5, rely=0.02, anchor="n", relwidth=0.93, relheight=0.1)
        name_scroll.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.7)
        load_button.pack(pady=20)
        empty_label.pack(pady=10)

        self.add_decks(name_scroll, empty_info_var)

    def add_decks(self, parent, empty_var):
        decks_db = cur.execute(
            "SELECT name FROM sqlite_master WHERE type=\'table\'  ORDER BY ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) DESC;").fetchall()
        all_decks = [n[0] for n in decks_db]
        for name in all_decks:
            row_frame = AddCardsToLoad(name, parent, load_selected, self.all_objects)
            row_frame.pack(fill="x", pady=5)
            row_frame.bind("<Double-Button-1>", lambda _: load_db_file(empty_var))
            self.all_objects.append(row_frame)


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.widgets()

    class ManageCards(ctk.CTkFrame):
        def __init__(self, parent):
            super().__init__(parent, fg_color="transparent")

            self.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

            self.all_objects = []
            self.search_var = ctk.StringVar()

            self.display_tables()

        def search_callback(self, *args, window, variable):
            for widget in window.winfo_children():
                widget.destroy()

            result_items = cur.execute(
                f"SELECT name FROM sqlite_master WHERE type=\"table\" AND name LIKE  \'%{variable.get()}%\'").fetchall()

            for item in result_items:
                # create new row
                row_frame = ctk.CTkFrame(window, fg_color="transparent")
                row_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(row_frame, font=(FONT_FAMILY, 30, "bold"), text_color=ADD_FRAME_BLUE, text=item[0]).pack()

        def display_tables(self):
            # box with saved files
            box_display = BoxFrame(self)
            box_display.configure(width=500)

            column_label = TableHeaderSave(box_display, "SAVES")
            column_label.configure(height=50)
            name_scroll = ScrollFrame(box_display)

            # save button
            name_input = AddInput(self, textvariable=self.search_var)
            name_input.configure(width=500)
            # save button
            delete_button = ctk.CTkButton(
                self,
                width=200,
                height=50,
                corner_radius=19,
                fg_color="#f24d1b",
                font=(FONT_FAMILY, 30, "bold"),
                text="DELETE",
                text_color="white",
                command=lambda: delete_from_db(self.search_var),
            )
            self.search_var.trace_add("write", lambda *args: self.search_callback(*args, window=name_scroll,
                                                                                  variable=self.search_var))
            self.search_var.set(value="")

            # layout
            box_display.pack()
            column_label.place(relx=0.5, rely=0.02, anchor="n", relwidth=0.93, relheight=0.1)
            name_scroll.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.7)
            name_input.pack(pady=20)
            delete_button.pack(pady=20)

        # def add_decks(self, parent, *args):
        #     decks_db = cur.execute(
        #         "SELECT name FROM sqlite_master WHERE type=\'table\'  ORDER BY ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) DESC;").fetchall()
        #     all_decks = [n[0] for n in decks_db]
        #     for name in all_decks:
        #         row_frame = AddCardsToLoad(name, parent, load_selected, self.all_objects)
        #         row_frame.pack(fill="x", pady=5)
        #         self.all_objects.append(row_frame)

    def widgets(self):
        # create header
        settings_header = ctk.CTkLabel(
            self,
            font=(FONT_FAMILY, 65, "bold"),
            text="SETTINGS",
        )

        # settings box
        all_container = SettingsContainer(self)
        settings_scroll = ctk.CTkScrollableFrame(
            all_container,
            fg_color="transparent"
        )

        # add setting collapse
        def general_fun():
            def soundtrack_control(*args, variable):
                global music_sound
                if variable.get() == "on":
                    soundtrack.play(loops=-1)
                    music_sound = "on"
                else:
                    soundtrack.stop()
                    music_sound = "off"

            def mute_all(*args, variable):
                global volume, buttons_sound
                if variable.get() == "on":
                    volume = 1
                    buttons_sound = "on"
                elif variable.get() == "off":
                    volume = 0
                    buttons_sound = "off"

            general_settings = SettingSection(settings_scroll, "GENERAL")
            general_settings.pack(fill="x", expand=1, pady=7)
            # create two columns

            music_set_var = ctk.StringVar(value=music_sound)
            music_set_var.trace_add("write", lambda *args: soundtrack_control(*args, variable=music_set_var))

            button_sound_var = ctk.StringVar(value=buttons_sound)
            button_sound_var.trace_add("write", lambda *args: mute_all(*args, variable=button_sound_var))
            # music turn off
            music_row = SettingsRowSwitch(general_settings.subframe, music_set_var, "MUSIC")
            music_row.columnconfigure((0, 1), weight=1)
            music_row.rowconfigure(0, weight=1)
            # music choose
            music_choose = SettingsOptionMenu(
                music_row,
                ["CALM", "DEEP FOCUS", "FANTASY", "ACTIVE", "INTERSTELLAR", "CHRISTMAS"],
                variable=soundtrack_style,
                command=lambda _: change_soundtrack()
            )
            music_choose.pack(side="right")

            SettingsRowSwitch(general_settings.subframe, button_sound_var, "BUTTON SOUNDS")

        def cards_fun():
            def switch_values():
                global dictionary
                flipped_dict = {value: key for key, value in dictionary.items()}
                dictionary = flipped_dict

            def delete_all_cards():
                global dictionary
                confirm_delete = messagebox.askquestion(title="Delete",
                                                        message=f"Do you really want do delete all({len(dictionary)}) cards?")
                if confirm_delete:
                    dictionary = {}
                    pygame.mixer.Sound(DELETE_SOUND_PATH).play().set_volume(volume * 0.2)
                    delete_all_button.configure(state="disabled")
                else:
                    pass

            card_setting = SettingSection(settings_scroll, "CARDS")
            card_setting.pack(fill="x", expand=1, pady=7)

            SettingsRowCheck(card_setting.subframe, switch_dict, "SWITCH VALUES", switch_values)
            delete_all_button = SettingButton(card_setting.subframe, delete_all_cards, "DELETE ALL CARDS")
            if not len(dictionary):
                delete_all_button.configure(state="disabled")
            delete_all_button.pack(pady=15, padx=15, side="left", expand=1, fill="x")

        def translate_fun():
            def custom_state_option(*args, var):
                if var.get() == "on":
                    options_widget.configure(state="normal")
                else:
                    options_widget.configure(state="disabled")

            general_settings = SettingSection(settings_scroll, "TRANSLATE")
            general_settings.pack(fill="x", expand=1, pady=7)

            # add check button
            auto_trans_var.trace_add("write", lambda *args: custom_state_option(*args, var=auto_trans_var))
            SettingsRowCheck(general_settings.subframe, auto_trans_var, "AUTO-TRANSLATE", lambda: print(""))
            # language options
            language_options_frame = ctk.CTkFrame(general_settings.subframe, fg_color="transparent")
            options_widget = SettingsOptionMenu(
                language_options_frame,
                ["Czech", "English", "German", "Russian", "Spanish", "Chinese", "Hungarian"],
                variable=language_var,
                command=lambda _: print(""),
            )

            options_widget.configure(state="disabled")
            language_options_frame.pack(fill="x", expand=1, padx=15, pady=15)
            options_widget.pack(side="left")

        def tts_fun():
            general_settings = SettingSection(settings_scroll, "TEXT TO SPEECH")
            general_settings.pack(fill="x", expand=1, pady=7)

            # add check button
            SettingsRowCheck(general_settings.subframe, tts_var, "TEXT TO SPEECH", lambda: print(""))
            # language options
            language_options_frame = ctk.CTkFrame(general_settings.subframe, fg_color="transparent")
            options_one = SettingsOptionMenu(
                language_options_frame,
                ["None", "Czech", "English", "German", "Russian", "Spanish", "Chinese", "Hungarian"],
                variable=tts_first_v,
                command=lambda _: print(""),
            )
            options_two = SettingsOptionMenu(
                language_options_frame,
                ["None", "Czech", "English", "German", "Russian", "Spanish", "Chinese", "Hungarian"],
                variable=tts_second_v,
                command=lambda _: print(""),
            )
            language_options_frame.pack(fill="x", expand=1, padx=15, pady=15)
            options_one.pack(fill="x", expand=1, pady=10)
            options_two.pack(fill="x", expand=1, pady=10)

        def manage_saves():
            manage_button = ctk.CTkButton(
                settings_scroll,
                corner_radius=50,
                fg_color="#f24d1b",
                hover_color="#f29c81",
                text="MANAGE SAVES",
                font=(FONT_FAMILY, 25, "bold"),
                command=lambda: self.ManageCards(self),
            )
            manage_button.pack(fill="x", expand=1, pady=15)

        # layout
        settings_header.pack(pady=15)
        all_container.pack(pady=10)
        settings_scroll.place(relx=0.03, rely=0.03, relheight=0.94, relwidth=0.94)
        # place sections
        general_fun()
        cards_fun()
        translate_fun()
        tts_fun()
        manage_saves()


app = Flashcards()

# global variables
key_var = ctk.StringVar()
value_var = ctk.StringVar()
cards_selected_int = 0
cards_selected = []
delete_var = ctk.StringVar(value=f"Delete ({cards_selected_int})")
cards_display = ""
cards_info_var = ctk.StringVar()
play_word = ctk.StringVar()
dictionary_list = []
play_number = ctk.StringVar()
current_card = 0
current_side = "key"
auto_trans_var = ctk.StringVar(value="off")
language_var = ctk.StringVar(value="English")
music_var = ctk.StringVar(value="on")
saved_bool = ctk.BooleanVar(value=True)
load_selected = ctk.StringVar(value="")
volume = 1
hard_list = set()
play_mode = ctk.StringVar(value="normal")
# settings
music_sound = "on"
buttons_sound = "on"
soundtrack_style = ctk.StringVar(value="CALM")
switch_dict = ctk.StringVar(value="off")
tts_var = ctk.StringVar(value="off")
tts_first_v = ctk.StringVar(value="English")
tts_second_v = ctk.StringVar(value="English")
shortcut_translator = {"Czech": "cs", "English": "en", "German": "de",
                       "Chinese": "zh-CN", "Spanish": "es", "Russian": "ru", "Hungarian": "hu"}

sound_click = pygame.mixer.Sound(CLICK_SOUND_PATH)

app.mainloop()
# disconnect the database
cur.close()
conn.close()
