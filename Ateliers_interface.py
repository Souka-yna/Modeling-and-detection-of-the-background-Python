# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 16:08:52 2022

@author: Lenovo
"""
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
import cv2
import tkinter as tk
import time
import numpy as np
class videoGUI:

    def __init__(self, window, window_title):

        self.window = window
        self.window.title(window_title)

        top_frame = Frame(self.window)
        top_frame.grid(row=0, column=0)

        bottom_frame =Frame(self.window)
        bottom_frame.grid(row=0, column=1)
        top_frame1 = Frame(self.window)
        top_frame1.grid(row=1, column=0)

        bottom_frame1 =Frame(self.window)
        bottom_frame1.grid(row=1, column=1)
        self.pause = False   # Parameter that controls pause button
        self.canvas = tk.Canvas(top_frame,width = 450, height = 350, background="silver")
        self.canvas.pack(pady=10,padx=10)
        self.canvas1 = tk.Canvas(top_frame1,width = 450, height = 350, background="silver")
        self.canvas1.pack(pady=10,padx=10)
        # Select Button
        self.btn_select=tk.Button(bottom_frame, text="Select video file", width=15, background="papayawhip", command=self.open_file)
        self.btn_select.grid(row=0, column=0,pady=5,padx=5)
        self.btn_camera=tk.Button(bottom_frame, text="Open WebCam", width=15, background="papayawhip", command=self.open_camera)
        self.btn_camera.grid(row=0, column=1,pady=5,padx=5)
        # Play Button
        self.btn_play=tk.Button(bottom_frame, text="Play", width=15, background="papayawhip", command=self.play_video)
        self.btn_play.grid(row=1, column=0,pady=5,padx=5)

        # Pause Button
        self.btn_pause=tk.Button(bottom_frame, text="Pause", width=15, background="papayawhip", command=self.pause_video)
        self.btn_pause.grid(row=1, column=1,pady=5,padx=5)
        self.btn_simple=tk.Button(bottom_frame1, text="Simple approach", width=15, background="papayawhip", command=self.proche_simple)
        self.btn_simple.grid(row=0, column=0,pady=5,padx=5)
        self.btn_different=tk.Button(bottom_frame1, text="Frame differencing", width=15, background="papayawhip", command=self.proche_differant)
        self.btn_different.grid(row=0, column=1,pady=5,padx=5)
        self.btn_moyenne=tk.Button(bottom_frame1, text="Mean filter", width=15, background="papayawhip", command=self.proche_moyenne)
        self.btn_moyenne.grid(row=2, column=0,pady=5,padx=5)
        self.btn_mediane=tk.Button(bottom_frame1, text="Median filter", width=15, background="papayawhip", command=self.proche_mediane)
        self.btn_mediane.grid(row=1, column=0,pady=5,padx=5)
        self.btn_mog=tk.Button(bottom_frame1, text="MOG2", width=15, background="papayawhip", command=self.proche_MOG)
        self.btn_mog.grid(row=1, column=1,pady=5,padx=5)
        self.btn_flot_Optique_Diff=tk.Button(bottom_frame1, text="RUNNING AVERAGE", width=15, background="papayawhip", command=self.proche_Folt_O_Dif)
        self.btn_flot_Optique_Diff.grid(row=2, column=1,pady=5,padx=5)
        self.delay = 15   # ms
        self.simple=False
        self.different=False
        self.moyene=False
        self.mediane=False
        self.ferst_frame=np.zeros(shape=(360,640))
        self.n=25
        self.nFrame=np.zeros((self.n,360,640))
        self.Mog=False
        self.Flot_Dif=False
        self.framesMedian=[]
        
        self.window.mainloop()
    def open_camera(self):
        self.pause = False
        self.cap = cv2.VideoCapture(0)
        _,first_fr=self.cap.read()
        self.ferst_frame=cv2.cvtColor(first_fr,cv2.COLOR_BGR2GRAY)
        self.ferst_frame=cv2.GaussianBlur(self.ferst_frame,(5,5),0)
    def open_file(self):

        self.pause = False

        self.filename = filedialog.askopenfilename(title="Select file", filetypes=(("MP4 files", "*.mp4"),
                                                                                         ("WMV files", "*.wmv"), ("AVI files", "*.avi")))
        print(self.filename)

        # Open the video file
        self.cap = cv2.VideoCapture(self.filename)
        _,first_fr=self.cap.read()
        self.ferst_frame=cv2.cvtColor(first_fr,cv2.COLOR_BGR2GRAY)
        self.ferst_frame=cv2.GaussianBlur(self.ferst_frame,(5,5),0)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        #self.canvas.config(width = self.width, height = self.height)


    def get_frame(self):   # get only one frame

        try:

            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        except:
            messagebox.showerror(title='Video file not found', message='Please select a video file.')


    def play_video(self):
        
        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor =NW)
            if self.simple:
                frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                frame_gray=cv2.GaussianBlur(frame_gray,(5,5),0)
                difference=cv2.absdiff(self.ferst_frame,frame_gray)
                _,difference= cv2.threshold(difference,25,255,cv2.THRESH_BINARY)
                self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(difference))
                self.canvas1.create_image(0, 0, image = self.photo1, anchor =NW)
            elif self.different:
                frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                frame_gray=cv2.GaussianBlur(frame_gray,(5,5),0)
                difference=cv2.absdiff(self.ferst_frame,frame_gray)
                _,difference= cv2.threshold(difference,25,255,cv2.THRESH_BINARY)
                self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(difference))
                self.canvas1.create_image(0, 0, image = self.photo1, anchor =NW)
                self.ferst_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                self.ferst_frame=cv2.GaussianBlur(self.ferst_frame,(5,5),0)
            elif self.moyene:
                frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                frame_gray=cv2.GaussianBlur(frame_gray,(5,5),0)
                difference=cv2.absdiff(self.ferst_frame,frame_gray)
                _,difference= cv2.threshold(difference,25,255,cv2.THRESH_BINARY)
                self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(difference))
                self.canvas1.create_image(0, 0, image = self.photo1, anchor =NW)
            elif self.mediane:
                frame_gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                frame_gray=cv2.GaussianBlur(frame_gray,(5,5),0)
                difference=cv2.absdiff(self.ferst_frame,frame_gray)
                _,difference= cv2.threshold(difference,25,255,cv2.THRESH_BINARY)
                self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(difference))
                self.canvas1.create_image(0, 0, image = self.photo1, anchor =NW)
            elif self.Mog:
                difference=self.substractor.apply(frame)
                self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(difference))
                self.canvas1.create_image(0, 0, image = self.photo1, anchor =NW)
            elif self.Flot_Dif:
               frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
               model = cv2.addWeighted(self.ferst_frame,(1-0.7),frame,0.7,0)
               foreground = cv2.absdiff(model,frame)
               th , foreground = cv2.threshold(foreground, 25, 255, cv2.THRESH_BINARY)
               self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(foreground))
               self.canvas1.create_image(0, 0, image = self.photo1, anchor =NW)
               self.ferst_frame = model
    # draw the tracks
            #self.pause = False
        if not self.pause:
            self.window.after(self.delay, self.play_video)
    def somme(self):
        S = np.zeros((360,640))
        for i in range(self.n):
            S += self.nFrame[i,:,:]
        return S
    def Nframe(self):
        
        for i in range(self.n):
            ret, frame = self.cap.read()
            if ret == True:
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.GaussianBlur(frame, (5, 5), 0)
                #frame=cv2.resize(frame, (round(360), round(640)), interpolation=cv2.INTER_AREA)
                self.nFrame[i,:,:] = frame
        return ((1/self.n)*self.somme()).astype(int)
   
    def pause_video(self):
        self.pause = True
    def proche_simple(self):
        self.Flot_Dif=False
        self.simple=True
        self.different=False
        self.moyene=False
        self.mediane=False
        self.Mog=False
    def proche_differant(self):
        self.simple=False
        self.Flot_Dif=False
        self.different=True
        self.moyene=False
        self.mediane=False
        self.Mog=False
    def proche_moyenne(self):
        self.simple=False
        self.Mog=False
        self.Flot_Dif=False
        self.different=False
        self.ferst_frame=self.Nframe()
        self.ferst_frame= self.ferst_frame.astype('uint8')
        self.ferst_frame=cv2.GaussianBlur(self.ferst_frame,(5,5),0)
        self.moyene=True
        self.mediane=False
    def proche_mediane(self):
        self.simple=False
        self.Mog=False
        self.Flot_Dif=False
        self.different=False
        self.moyene=False
        for i in range(self.n):    
            ret, frame = self.cap.read()
            if ret == True:
                frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.GaussianBlur(frame, (5, 5), 0)
                #frame=cv2.resize(frame, (round(450), round(450)), interpolation=cv2.INTER_AREA)
                self.framesMedian.append(frame)
        self.ferst_frame=np.median(self.framesMedian, axis=0).astype(dtype=np.uint8)
        #cv2.imshow('frame', self.ferst_frame)
        self.mediane=True
    def proche_MOG(self):
        self.simple=False
        self.different=False
        self.moyene=False
        self.mediane=False
        self.Flot_Dif=False
        self.substractor = cv2.createBackgroundSubtractorMOG2()
        self.Mog=True
    def proche_Folt_O_Dif(self):
        self.simple=False
        self.different=False
        self.moyene=False
        self.mediane=False
        self.Mog=False
 
        self.Flot_Dif=True
    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

##### End Class #####


# Create a window and pass it to videoGUI Class
videoGUI(tk.Tk(), "Analyse Video")