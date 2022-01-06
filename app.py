import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
import PIL.Image, PIL.ImageTk
from tkinter import font
import time

from camera_model import CameraModel

class Application(tk.Frame):
    def __init__(self,master, video_source=0):
        super().__init__(master)

        self.flip=False
        
        # モデル
        self.model = CameraModel()
        
        # フィルター
        self.filter_names = [
            'None',
            'LightSepia',
            'Sepia',
            'ColorShift',
            'Postarization',
        ]
        # デコレーション
        self.decoration_names = [
            'Face MediaPipe',
            'Fruits Lottery',
            'Finger Drawing',
        ]
        
        # 現在有効なデコレーション
        self.activated_decorations = []
        
        self.master.geometry("700x700")
        self.master.title("MediaPipe Camera")

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font( family="Meiryo UI", size=15, weight="normal" )
        self.font_btn_big = font.Font( family="Meiryo UI", size=20, weight="bold" )
        self.font_btn_normal = font.Font( family="Meiryo UI", size=10, weight="normal" )
        self.font_btn_small = font.Font( family="Meiryo UI", size=10, weight="normal" )

        self.font_lbl_bigger = font.Font( family="Meiryo UI", size=45, weight="bold" )
        self.font_lbl_big = font.Font( family="Meiryo UI", size=30, weight="bold" )
        self.font_lbl_middle = font.Font( family="Meiryo UI", size=15, weight="bold" )
        self.font_lbl_small = font.Font( family="Meiryo UI", size=12, weight="normal" )

        # ---------------------------------------------------------
        # Open the video source
        # ---------------------------------------------------------

        self.vcap = cv2.VideoCapture( video_source )
        self.width = self.vcap.get( cv2.CAP_PROP_FRAME_WIDTH )
        self.height = self.vcap.get( cv2.CAP_PROP_FRAME_HEIGHT )

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------

        self.create_widgets()
        
        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------

        self.delay = 15 #[mili seconds]
        self.update()

    def create_widgets(self):        
        #Frame_Camera
        self.frame_cam = tk.LabelFrame(self.master, text = 'Camera', font=self.font_frame)
        self.frame_cam.place(x = 10, y = 10)
        self.frame_cam.configure(width = self.width+30, height = self.height+50)
        self.frame_cam.grid_propagate(0)

        #Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure( width= self.width, height=self.height)
        self.canvas1.grid(column= 0, row=0,padx = 10, pady=10)

        # Frame_Control
        self.frame_control = tk.LabelFrame( self.master, text='Control', font=self.font_frame )
        self.frame_control.place( x=10, y=550 )
        self.frame_control.configure( width=self.width + 30, height=180 )
        self.frame_control.grid_propagate( 0 )

        # Frame_CameraControl
        self.frame_cameraControl = tk.Frame(self.frame_control, )

        #Snapshot Button
        global camera_img
        camera_img = tk.PhotoImage(file="images/gui/camera.png").subsample(5, 5)
        self.btn_snapshot = ttk.Button( self.frame_cameraControl, text='Snapshot')
        self.btn_snapshot.configure(
            command=self.press_snapshot_button,
            image=camera_img, compound='top'
        )
        #Flip Button
        global flip_img
        flip_img = tk.PhotoImage(file="images/gui/flip.png").subsample(5, 5)
        self.btn_flip = ttk.Button( self.frame_cameraControl, text='Flip')
        self.btn_flip.configure(
            command=self.press_flip_button,
            image=flip_img, compound='top'
        )

        # Frame_FilterControl
        self.frame_filter = ttk.LabelFrame(self.frame_control, text='Filter')
        
        # Combobox_Filter
        val = tk.StringVar()
        val.set('None')
        self.combobox_filter = ttk.Combobox(
            self.frame_filter, state='readonly',
            textvariable=val, values=tuple(self.filter_names),
        )
        self.combobox_filter.bind('<<ComboboxSelected>>', self.select_combobox)
        
        # Frame_DecorationControl
        self.frame_decoration = ttk.LabelFrame(self.frame_control, text='Decorations')
        
        # デコレーション選択ボタン ttk.Buttonを使う
        global deco_imgs
        # デコレーション選択ボタン画像 リスト
        deco_imgs = [
            tk.PhotoImage(file="images/gui/face_mp.png").subsample(5, 5),
            tk.PhotoImage(file="images/gui/fruit_lottery.png").subsample(5, 5),
            tk.PhotoImage(file="images/gui/finger_drawing.png").subsample(5, 5),
        ]
        self.btn_deco_list = []
        for i, decoration_name in enumerate(self.decoration_names):
            self.btn_deco_list.append(
                    ttk.Button(
                            self.frame_decoration, text=decoration_name,
                            image=deco_imgs[i], compound='top',
                    )
            )
            self.btn_deco_list[i].bind("<ButtonPress>", self.callback_decoration_btn)
        
        # 現在有効なデコレーションラベル
        self.label_to_show = tk.StringVar()
        self.label_to_show.set("")
        self.label_decorations = ttk.Label(self.frame_decoration, textvariable=self.label_to_show)
        
        # Layout
        self.frame_control.grid_columnconfigure(0, weight=2)
        self.frame_control.grid_columnconfigure(1, weight=1)
        self.frame_control.grid_columnconfigure(2, weight=2)
        
        self.frame_filter.grid(row=0, column=0, padx=10)
        self.combobox_filter.pack(anchor='center', expand=1)
        
        self.frame_cameraControl.grid(row=0, column=1, padx=10, sticky='NESW')
        self.btn_snapshot.pack(side=tk.LEFT, padx=5)
        self.btn_flip.pack(side=tk.LEFT, padx=5)
        
        self.frame_decoration.grid(row=0, column=2, padx=10, sticky='W')
        self.label_decorations.pack(side=tk.BOTTOM)
        for btn in self.btn_deco_list:
            btn.pack(side=tk.LEFT)

        # Close
        # self.btn_close = tk.Button( self.frame_control, text='Close', font=self.font_btn_big )
        # self.btn_close.configure( width=15, height=1, command=self.press_close_button )
        # self.btn_close.grid( column=1, row=0, padx=20, pady=10 )

    def update(self):
        #Get a frame from the video source
        _, frame = self.vcap.read()

        input_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # モデル部分を作りやすいよう、RGB形式に変換
        if self.flip:  # 左右反転
            input_image = cv2.flip(input_image, 1)
        
        # input_imageをモデルにかける
        self.processed_image = self.model.process(input_image)
        
        self.img2show = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.processed_image))
        
        #self.img2show -> Canvas
        self.canvas1.create_image(0,0, image= self.img2show, anchor = tk.NW)

        self.master.after(self.delay, self.update)

    def press_snapshot_button(self):
        cv2.imwrite( "frame-" + time.strftime( "%Y-%d-%m-%H-%M-%S" ) + ".png",
                     cv2.cvtColor( self.processed_image, cv2.COLOR_BGR2RGB ) )
    
    def press_flip_button(self):
        self.flip = not self.flip
    
    def select_combobox(self, event):
        self.model.change_filter(event.widget.get())
    
    def callback_decoration_btn(self, event):
        name = event.widget['text']
        self.model.change_decorations(name)
        if name in self.activated_decorations:
            self.activated_decorations.remove(name)
        else:
            self.activated_decorations.append(name)
        self.label_to_show.set(', '.join(self.activated_decorations))
        
    def press_close_button(self):
        self.master.destroy()
        self.vcap.release()

def main():
    root = tk.Tk()
    app = Application(master=root)#Inherit
    app.mainloop()

if __name__ == "__main__":
    main()
