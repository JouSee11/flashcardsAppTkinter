import customtkinter as ctk
from os import walk
from googletrans import Translator

app = ctk.CTk()
app.geometry("800x800")


class AnimatedButton(ctk.CTkButton):
    def __init__(self, parent, path_light):

        # animation logic setup
        self.import_folders(path_light)

        super().__init__(
            master=parent,
            text='A animated button',
            #image=self.frames[self.frame_index],
            #command=self.trigger_animation
        )
        self.pack(expand=True)

    def import_folders(self, path_light):
        for folder_name, sub_folder, image_name in walk(path_light):
            print(image_name)


AnimatedButton(app, "animation")

app.mainloop()