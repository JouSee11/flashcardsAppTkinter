import customtkinter as ctk
import customtkinter as ctk
from settings import *
import pygame
from os import walk
from PIL import Image, ImageTk


# menu
class MenuButton(ctk.CTkButton):
    def __init__(self, parent, text, command, state):
        super().__init__(
            parent,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            border_color=BORDER_COLOR,
            border_width=BORDER_WIDTH,
            corner_radius=BUTTON_CORNER,
            font=FONT_BUTTON,
            text=text,
            text_color=TEXT_COLOR,
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH,
            command=command,
            state=state,
        )


# play frame
class NextButton(ctk.CTkButton):
    def __init__(self, parent, command):
        super().__init__(
            parent,
            text="NEXT",
            width=266,
            height=66,
            corner_radius=21,
            fg_color=ADD_FRAME_BLUE,
            font=(FONT_FAMILY, 38, "bold"),
            command=command,
        )


class MenuLabel(ctk.CTkLabel):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            font=(FONT_FAMILY, 20, "bold"),
            text_color="white",
            text=text,
            width=900
        )


# cards frame
class AddInput(ctk.CTkEntry):
    def __init__(self, parent, textvariable):
        super().__init__(
            parent,
            height= 53,
            width= 288,
            fg_color="white",
            font=FONT_ADD,
            text_color=TEXT_COLOR,
            border_width= BORDER_ADD,
            border_color=ADD_FRAME_BLUE,
            corner_radius=26,
            textvariable=textvariable,
            placeholder_text_color="#cbcbcb",

        )


class BoxFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            width=612,
            height=609,
            fg_color="white",
            border_color=ADD_FRAME_BLUE,
            border_width=BORDER_ADD,
            corner_radius=26,
        )


class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="white",
        )


class DeleteButton(ctk.CTkButton):
    def __init__(self, parent, textvariable, command):
        super().__init__(
            parent,
            height=43,
            corner_radius=25,
            border_color="#b23914",
            border_width=5,
            fg_color="#f24d1b",
            font=(FONT_FAMILY, 38, "bold"),
            text_color="white",
            textvariable=textvariable,
            hover_color="#f29c81",
            bg_color="white",
            text_color_disabled="#f2a68f",
            command=command,
        )


class TableLabel(ctk.CTkLabel):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            text_color=ADD_FRAME_BLUE,
            font=(FONT_FAMILY, 40, "bold"),
        )


class TableNameFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="#c9e0f4",
            bg_color="transparent",
            corner_radius=10,
        )

        # add text
        key_label = TableLabel(self, "TERM")
        value_label = TableLabel(self, "DEFINITION")

        key_label.place(relx=0.2, rely=0.5, anchor="center")
        value_label.place(relx=0.8, rely=0.5, anchor="center")


class TableItem(ctk.CTkLabel):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            font=(FONT_FAMILY, 30, "bold"),
            text_color=ADD_FRAME_BLUE,
            text=text,
        )


class AddCardsToFrame:
    def __init__(self, key, value, row, cards_display, cards_selected_int, cards_selected, delete_var, hard_items):
        cards_display.rowconfigure(row, weight=1)

        self.table_row = ctk.CTkFrame(cards_display, fg_color="transparent", width=800, height=38)

        self.key_display = key
        if len(self.key_display) > 14:
            key_display = f"{self.key_display[0:12]}..."

        self.value_display = value
        if len(self.value_display) > 14:
            self.value_display = f"{self.value_display[0:12]}..."

        self.table_row.grid(row=row, column=0, columnspan=3, pady=5)
        TableItem(self.table_row, self.key_display).place(relx=0.05, rely=0.5, anchor="w")
        TableItem(self.table_row, self.value_display).place(relx=0.5, rely=0.5, anchor="w")
        if key in hard_items:
            image_display = ctk.CTkImage(Image.open("images/star-gold.png"), size=(30,30))
            ctk.CTkLabel(self.table_row, image=image_display, text="").place(relx=0.9, rely=0.5, anchor="w")

        # event - hover effect
        self.is_selected = ctk.BooleanVar(value=False)
        self.table_row.bind("<Enter>", lambda _: self.enter(_))
        self.table_row.bind("<Leave>", lambda _: self.leave(_))
        self.table_row.bind("<Button-1>", lambda _: self.selected(_, key, cards_selected_int, cards_selected, delete_var))

    # selecting and hovering functions
    def selected(self, event, key, cards_selected_int, cards_selected, delete_var):

        # sounds selected
        pygame.mixer.Sound(CLICK_SOUND_PATH).play()

        # if the row isnt already selected
        if self.is_selected.get() == False:
            self.is_selected.set(True)
            self.table_row.configure(fg_color="#f27550")
            cards_selected_int = cards_selected_int + 1
            print(cards_selected_int)
            cards_selected.append(key)
            delete_var.set(f"Delete ({len(cards_selected)})")
        else:
            self.is_selected.set(False)
            self.table_row.configure(fg_color="transparent")
            cards_selected.remove(key)
            cards_selected_int -= 1
            print(cards_selected_int)
            delete_var.set(f"Delete ({len(cards_selected)})")

    def enter(self, _):
        print(self.is_selected.get())
        if self.is_selected.get():
            pass
        else:
            self.table_row.configure(fg_color="#c8e0f4")

    def leave(self, _):
        print(self.is_selected)
        if self.is_selected.get():
            pass
        else:
            self.table_row.configure(fg_color="transparent")


# settings
class AnimationStart(ctk.CTkButton):
    def __init__(self, parent, path_images):

        # animation logic setup
        self.frames = self.import_folders(path_images)
        self.frame_index = 0
        self.animation_length = len(self.frames) - 1

        super().__init__(
            master=parent,
            text="",
            image=self.frames[self.frame_index],
            fg_color="transparent",
            hover_color=SETTINGS_FG,
        )
        self.animation_speed = 10

    def import_folders(self, path_images):
        image_paths = []
        for folder_name, sub_folder, image_name in walk(path_images):
            sorted_data = image_name

            full_path_data = [path_images + '/' + item for item in sorted_data]
            image_paths = full_path_data

        print(image_paths)
        ctk_images = []
        for image_path in image_paths:
            ctk_image = ctk.CTkImage(Image.open(image_path), size=(800, 1000))
            ctk_images.append(ctk_image)

        return ctk_images

    def animate(self):
        self.frame_index += 1
        self.configure(image=self.frames[self.frame_index])


# save/load
class TableHeaderSave(ctk.CTkFrame):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            fg_color="#c9e0f4",
            bg_color="transparent",
            corner_radius=15,
        )

        # add text
        column_name = TableLabel(self, text)

        column_name.place(relx=0.5, rely=0.5, anchor="center")


# def load_selected_assign(item):
#     return item


class AddCardsToLoad(ctk.CTkFrame):
    def __init__(self, name, parent, selected_item, all_instances):
        super().__init__(parent, fg_color="transparent")

        self.name = name

        if len(self.name) > 23:
            name_display = f"{self.name[0:20]}..."
        else:
            name_display = self.name

        self.text = TableItem(self, text=name_display)
        self.text.pack(pady=5)

        # event - hover effect
        self.is_selected = ctk.BooleanVar(value=False)
        self.bind("<Enter>", lambda _: self.enter(_))
        self.bind("<Leave>", lambda _: self.leave(_))
        self.bind("<Button-1>", lambda _: self.selected(_, selected_item, all_instances))
        self.text.bind("<Button-1>", lambda _: self.selected(_, selected_item, all_instances))
        self.text.bind("<Enter>", lambda _: self.enter(_))
        self.text.bind("<Leave>", lambda _: self.leave(_))

    # selecting and hovering functions
    def selected(self, _, selected_item, all_instances):

        # sounds selected
        pygame.mixer.Sound(CLICK_SOUND_PATH).play()

        # if the row isnt already selected
        if not self.is_selected.get():
            selected_item.set(value=self.name)
            for obj in all_instances:
                obj.configure(fg_color="transparent")
            self.is_selected.set(True)
            self.configure(fg_color=GREEN_LOAD)
        else:
            self.is_selected.set(False)
            self.configure(fg_color="transparent")
            selected_item.set(value="")

    def enter(self, _):
        print(self.is_selected.get())
        if self.is_selected.get():
            pass
        else:
            self.configure(fg_color="#c8e0f4")

    def leave(self, _):
        print(self.is_selected)
        if self.is_selected.get():
            pass
        else:
            self.configure(fg_color="transparent")


# settings version2
class SettingsContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=MID_BLUE,
            width=510,
            height=730,
            border_width=5,
            border_color=LIGHT_BLUE,
            corner_radius=30,
        )


class SettingSection(ctk.CTkFrame):
    def __init__(self, parent, text):
        super().__init__(parent, corner_radius=30, fg_color=ADD_FRAME_BLUE)

        # general info
        self.switch_var = ctk.IntVar(value=0)
        self.rotation_state = 0


        # frame for title
        self.title_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=50)
        self.title_frame.pack(fill="x", expand=1, padx=15, pady=15)

        # main title
        self.title_label = ctk.CTkLabel(self.title_frame, text=text, font=(FONT_FAMILY, 25, "bold"))
        self.title_label.pack(side="left", fill="x", expand=1)

        #button
        #ctk.CTkImage(Image.open(image_path), size=(100, 100))
        self.dropdown_image = Image.open("images\\dropdown.png")
        self.expand_button = ctk.CTkButton(
            self.title_frame,
            image=ctk.CTkImage(self.dropdown_image, size=(20, 20)),
            text="",
            command=self.dropdown,
            fg_color="transparent",
            width=20
        )
        #self.expand_button.pack(side="right", expand=1, padx=10)
        self.expand_button.place(relx=0.9)
        self.title_frame.bind("<Button-1>", lambda _: self.dropdown())

        self.subframe = ctk.CTkFrame(self, fg_color=LIGHT_BLUE, corner_radius=0)

    def rotate_icon(self):
        if self.rotation_state == 0:
            self.expand_button.configure(image=ctk.CTkImage(self.dropdown_image.rotate(180), size=(20, 20)))
            self.rotation_state = 180
        else:
            self.expand_button.configure(image=ctk.CTkImage(self.dropdown_image.rotate(0), size=(20, 20)))
            self.rotation_state = 0

    def dropdown(self):
        if self.switch_var.get() == 0:
            self.switch_var.set(value=1)
            self.subframe.pack(fill="x", expand=1)
            self.rotate_icon()
        else:
            self.rotate_icon()
            self.switch_var.set(value=0)
            self.subframe.forget()


class SettingsSwitch(ctk.CTkSwitch):
    def __init__(self, parent, variable, text):
        super().__init__(
            parent,
            text=text,
            switch_width=60,
            switch_height=30,
            font=(FONT_FAMILY, 25, "bold"),
            progress_color=ADD_FRAME_BLUE,
            text_color=ADD_FRAME_BLUE,
            button_color="#e3e3e3",
            onvalue="on",
            offvalue="off",
            variable=variable
        )


class SettingsCheck(ctk.CTkCheckBox):
    def __init__(self, parent, variable, text, command):
        super().__init__(
            parent,
            checkbox_width=30,
            checkbox_height=30,
            onvalue="on",
            offvalue="off",
            variable=variable,
            text=text,
            font=(FONT_FAMILY, 25, "bold"),
            text_color=ADD_FRAME_BLUE,
            corner_radius=10,
            command=command
        )


class SettingsRowSwitch(ctk.CTkFrame):
    def __init__(self, parent, variable, text):
        super().__init__(parent, fg_color="transparent")

        switch = SettingsSwitch(self, variable, text)
        switch.pack(side="left")

        self.pack(fill="x", expand=1, padx=15, pady=15)


class SettingsRowCheck(ctk.CTkFrame):
    def __init__(self, parent, variable, text, command):
        super().__init__(parent, fg_color="transparent")

        check = SettingsCheck(self, variable, text, command)
        check.pack(side="left")

        self.pack(fill="x", expand=1, padx=15, pady=15)


class SettingButton(ctk.CTkButton):
    def __init__(self, parent, command, text):
        super().__init__(
            parent,
            width=250,
            height=40,
            fg_color="#f24d1b",
            command=command,
            text=text,
            font=(FONT_FAMILY, 25, "bold"),
            corner_radius=25,
            hover_color="#f29c81",
            text_color_disabled="#f29c81"
        )


class SettingsOptionMenu(ctk.CTkOptionMenu):
    def __init__(self, parent, values, variable, command):
        super().__init__(
            parent,
            width=250,
            height=40,
            fg_color="#deeefc",
            corner_radius=10,
            button_color=ADD_FRAME_BLUE,
            button_hover_color="#7992a8",
            font=(FONT_FAMILY, 18, "bold"),
            text_color="black",
            dropdown_fg_color="#deeefc",
            dropdown_font=(FONT_FAMILY, 18, "bold"),
            dropdown_text_color="black",
            values=values,
            variable=variable,
            command=command
        )


class ChoiceButton(ctk.CTkButton):
    def __init__(self, parent, text, command):
        super().__init__(
            parent,
            fg_color=ADD_FRAME_BLUE,
            border_color=MID_BLUE,
            border_width=3,
            corner_radius=30,
            font=(FONT_FAMILY, 35, "bold"),
            text=text,
            text_color="white",
            height=80,
            width=400,
            command=command,
        )







