from tkinter import *
import tkinter as tk
from tkinter import font
import cv2
from PIL import Image, ImageTk
import numpy as np
import os
from DFINE import *




class App :
    def __init__(self) :
        #Name app
        self.appName = 'Detected face'
        #SetUp Window
        self.window = Tk ()
        self.window.title(self.appName)
        self.window.geometry("{}x{}+{}+{}".format(WINDOW_WIDHT, WINDOW_HEIGHT, WINDOW_POSITION_RIGHT, WINDOW_POSITION_DOWN))
        self.window.resizable(False, False)
        #Icon
        self.window.iconbitmap(os.path.join(IMAGE_PATH,'AnimeVoDien.ico'))
       
        #font
        self.font_primary = font.Font(family='Arial', size= 15)
        
        # Button
        self.ButtonHorizon = Button(self.window, width=10, height=1, text='horizontal', font=self.font_primary, command=lambda: self.BtnHorizontal()).grid(row=6, column=3, padx=10, pady=10)
        self.ButtonVertical = Button(self.window, width=10, height=1, text='vertical', font=self.font_primary, command=lambda: self.BtnVertical()).grid(row=6, column=4, padx=10, pady=10)
        self.ButtonHori_Verti = Button(self.window, width=10, height=1, text='hori+verti', font=self.font_primary, command=lambda: self.BtnVertical_Horizontal()).grid(row=6, column=5, padx=10, pady=10)
        self.ButtonRotate = Button(self.window, width=10, height=1, text='rotate', font=self.font_primary, command=lambda: self.BtnRotate()).grid(row=7, column=3, padx=10, pady=10)
        self.ButtonOpen = Button(self.window, width=10, height=1, text='Open', font=self.font_primary, command=lambda: self.BtnOpen()).grid(row=8, column=3, padx=10, pady=10)
        
        # Entry
        self.DegInput = Entry(self.window, width=30)
        self.DegInput.grid(row=7, column=4, padx=10, pady=10)
      
        self.PathImg = Entry(self.window,width=40)
        self.PathImg.grid(row=8, column=4, padx=10, pady=10) 
        
        
        #Open ảnh mặc định
        
        self.imgLabel = ImageZoomApp(self.window, os.path.join(IMAGE_PATH,'Diep.jpg'))
        self.imgLabel.load_image(self.imgLabel.image_tk)
        
        
        self.window.mainloop()
    def BtnOpen(self):
        self.getPath = self.PathImg.get()
        self.imgLabel = ImageZoomApp(self.window, self.getPath)
        self.imgLabel.load_image(self.imgLabel.image_tk)
    def BtnHorizontal(self):
        self.imgLabel.image = self.imgLabel.horizontal()
        self.imgLabel.image_tk = ImageTk.PhotoImage(self.imgLabel.image)
        self.imgLabel.load_image(self.imgLabel.image_tk)
    def BtnVertical(self):
        self.imgLabel.image = self.imgLabel.vertical()
        self.imgLabel.image_tk = ImageTk.PhotoImage(self.imgLabel.image)
        self.imgLabel.load_image(self.imgLabel.image_tk)
    def BtnVertical_Horizontal(self):
        self.imgLabel.image = self.imgLabel.vertical_Horizoltal()
        self.imgLabel.image_tk = ImageTk.PhotoImage(self.imgLabel.image)
        self.imgLabel.load_image(self.imgLabel.image_tk)
    def BtnRotate(self):
        self.getDeg = self.DegInput.get()
        self.imgLabel.image = self.imgLabel.rotate(int(self.getDeg))
        self.imgLabel.image_tk = ImageTk.PhotoImage(self.imgLabel.image)
        self.imgLabel.load_image(self.imgLabel.image_tk)
        
        
        
    
 
        
class ImageZoomApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Zoom App")

        # Tạo khung để chứa thanh cuộn ngang và thanh cuộn dọc
        self.frame = tk.Frame(root)
        self.frame.grid(row=0, column=3, sticky=(tk.N, tk.W, tk.E, tk.S), rowspan=6, columnspan=6)

        # Tạo thanh cuộn ngang và thanh cuộn dọc
        self.h_scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.v_scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.canvas = tk.Canvas(self.frame, width=1000, height=500,
                                xscrollcommand=self.h_scrollbar.set,
                                yscrollcommand=self.v_scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)
        self.zoom_factor = 1.0  # Zoom factor, 1.0 là kích thước ban đầu
        
        
        #img 
        
        self.image = Image.open(image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        
        

        # Bind mouse events for tracking cursor position
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def load_image(self, image_tk):
        self.canvas.create_image(0, 0, anchor="nw", image=image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def horizontal(self):
        image_horizontal = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        return image_horizontal
    
    def vertical(self):
        image_vertical = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        return image_vertical
    
    def vertical_Horizoltal(self):
        image_vertical_Horizoltal = self.image.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
        return image_vertical_Horizoltal
                
    def on_mouse_click(self, event):
        # Xác định điểm gốc cho việc zoom
        self.zoom_x, self.zoom_y = event.x, event.y

    def on_mouse_drag(self, event):
        # Tính toán sự thay đổi trong vị trí chuột và thực hiện zoom
        dx = event.x - self.zoom_x
        dy = event.y - self.zoom_y
        self.zoom_x, self.zoom_y = event.x, event.y

        # Tính toán zoom factor dựa trên khoảng cách di chuyển chuột
        zoom_delta = 1.0 + dx / 100.0
        self.zoom_factor *= zoom_delta

        # Đảm bảo zoom factor không vượt quá giới hạn
        self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))

        # Thay đổi kích thước ảnh trên canvas
        new_width = int(self.image.width * self.zoom_factor)
        new_height = int(self.image.height * self.zoom_factor)
        zoomed_image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
        self.image_tk = ImageTk.PhotoImage(zoomed_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def rotate(self, angle):
        # Đọc hình ảnh
        open_cv_image = np.array(self.image)  
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        image = open_cv_image

        # Góc xoay (độ)
        angle = (-1) * angle

        # Tính toán kích thước mới của hình ảnh sau khi xoay
        height, width = image.shape[:2]
        new_height = int(width * np.abs(np.sin(np.radians(angle))) + height * np.abs(np.cos(np.radians(angle))))
        new_width = int(height * np.abs(np.sin(np.radians(angle))) + width * np.abs(np.cos(np.radians(angle))))

        # Tính toán ma trận biến đổi xoay
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Điều chỉnh ma trận biến đổi để đảm bảo không cắt góc
        rotation_matrix[0, 2] += (new_width - width) / 2
        rotation_matrix[1, 2] += (new_height - height) / 2

        # Áp dụng ma trận biến đổi để xoay hình ảnh
        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
        
        color_coverted = cv2.cvtColor(rotated_image , cv2.COLOR_BGR2RGB)
        image_Rotate = Image.fromarray(color_coverted)
        
        return image_Rotate
        
                
#Run
if __name__ == '__main__':
    App()
         
         
