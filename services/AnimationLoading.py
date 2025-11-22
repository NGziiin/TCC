import os, sys
from customtkinter import *
from PIL import Image, ImageTk, ImageSequence

class Start:
    def __init__(self, frameAnimation):

        self.animation = None

        self.frameAnimation = frameAnimation
        self.LoadArchive()
        self.OpenGif()
        self.AnimatedGif()

    def LoadArchive(self):
        self.loadingfile = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        self.loadingpath = os.path.join(os.path.abspath(self.loadingfile), "..", "image", "SucessUpdate.gif")

    def OpenGif(self):
        self.gif = Image.open(self.loadingpath)
        self.frames = [frame.copy().resize((100, 100)) for frame in ImageSequence.Iterator(self.gif)]
        self.delay = self.gif.info.get('duration', 100)

    def AnimatedGif(self, index=0):
        self.frame = self.frames[index]
        self.photo = ImageTk.PhotoImage(self.frame)
        self.frameAnimation.configure(image=self.photo, text='')
        self.frameAnimation.image = self.photo
        var = self.animation = self.frameAnimation.after(self.delay,
                                                          lambda: self.AnimatedGif((index + 1) % len(self.frames)))


    def StopAnimation(self):
        if self.animation is not None:
            self.frameAnimation.after_cancel(self.animation)
            self.frameAnimation.configure(image='', text='')
            self.frameAnimation.image = None
            self.animation = None