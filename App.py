from tkinter import *
from tkinter import messagebox
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
        #background
        bg = PhotoImage(file = os.path.join(IMAGE_PATH,'background.png'))
        self.label1 = Label(self.window, image = bg)
        self.label1.place(x = 0, y = 0)
        
        #font
        self.font_primary = font.Font(family='Arial', size= 15)
        
        # Button
        self.imgLabel = Canvas(self.window, width=1000, height=500)
        self.imgLabel.grid(row=0,column=0,columnspan=5, rowspan=6, padx=150, pady=10)
        self.ButtonHorizon = Button(self.window, width=10, height=1, text='horizontal', font=self.font_primary, command= lambda : self.HorizontalImg()).grid(row=6, column=1, padx=10, pady=10)
        self.ButtonVertical = Button(self.window, width=10, height=1, text='vertical', font=self.font_primary, command= lambda :self.VerticalImg()).grid(row=6, column=2, padx=10, pady=10)
        self.ButtonHori_Verti = Button(self.window, width=10, height=1, text='hori+verti', font=self.font_primary, command=lambda:self.Horizol_VertiImg()).grid(row=6, column=3, padx=10, pady=10)
        self.ButtonRotate = Button(self.window, width=10, height=1, text='rotate', font=self.font_primary, command= lambda : self.RotateImg(self.getDeg())).grid(row=7, column=1, padx=10, pady=10)
        self.ButtonOpen = Button(self.window, width=10, height=1, text='Open', font=self.font_primary, command=lambda :self.OpenImg() ).grid(row=8, column=1, padx=10, pady=10)
        
        # Entry
        self.DegInput = Entry(self.window, width=30)
        self.DegInput.grid(row=7, column=2, padx=10, pady=10)
      
        self.PathImg = Entry(self.window,width=40)
        self.PathImg.grid(row=8, column=2, padx=10, pady=10)
        
        self.window.mainloop()
        
        
        
        
    #Function to work with image   
    def CovertCV2toPil(self, img) :
        color_coverted = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image= Image.fromarray(color_coverted))
        return photo
    def getDeg(self):
        self.deg = self.DegInput.get()
        if  self.deg == '':
            messagebox.showinfo('Infor', 'nhap so')
            self.deg =0
            return self.deg 
        try :
            self.deg = int(self.deg)
        except :
            messagebox.showinfo('Infor', 'Khong dc nhap chu')
        return self.deg
    
    def GetImg(self):
        path = self.PathImg.get()
        if path == '':
            messagebox.showinfo('Info', 'Nhap link anh vao')
        Image = Images(path)
        return Image
    
    def OpenImg(self):
        #Open
        self.Image = self.GetImg().img
        #Convert to PIL
        self.photo = self.CovertCV2toPil(self.Image)
        self.Show(self.Image,self.photo)
        
    def Show(self,Image, photo):
        # Show Img 
        heightImg = int(Image.shape[0])
        widthImg = int(Image.shape[1])
        self.imgLabel = Canvas(self.window, width=widthImg, height=heightImg)
        self.imgLabel.grid(row=0,column=0,columnspan=5, rowspan=6, padx=150, pady=10)
        self.imgLabel.create_image(0, 0, image= photo, anchor=NW)
        
    def HorizontalImg(self):
        self.imghorizontal = self.GetImg()
        self.photohrizontal = self.CovertCV2toPil(self.imghorizontal.Horizontal())
        self.Show(self.imghorizontal.Horizontal(), self.photohrizontal )
    def VerticalImg(self):
        self.imgVertical = self.GetImg()
        self.photoVertical = self.CovertCV2toPil(self.imgVertical.Vertical())
        self.Show(self.imgVertical.Vertical(), self.photoVertical )
    def Horizol_VertiImg(self):
        self.imgHorizol_VertiImg = self.GetImg()
        self.photoHorizol_VertiImg = self.CovertCV2toPil(self.imgHorizol_VertiImg.Hori_Verti())
        self.Show(self.imgHorizol_VertiImg.Hori_Verti(), self.photoHorizol_VertiImg )
    def RotateImg(self, deg) :
        self.imgRotate = self.GetImg()
        self.photoRotate= self.CovertCV2toPil(self.imgRotate.Rotate(deg))
        self.Show(self.imgRotate.Rotate(deg), self.photoRotate )
        
    
 
        

#Imgae and Function  
class Images :
    def __init__(self, path_img):
        self.path_img = path_img
        self.img = cv2.imread(path_img)
        self.ImagePi = Image.open(path_img)
    def Horizontal(self):
        self.img = cv2.flip(self.img,1) 
        return self.img
    def Vertical(self):
        self.img = cv2.flip(self.img,0) 
        return self.img
    def Hori_Verti(self):
        self.img = cv2.flip(self.img,-1) 
        return self.img
    def Rotate(self, deg) :
        image = self.ImagePi
        # Specify the rotation angle in radians (positive values for clockwise)
        angle = np.radians(-deg)

        # Get the image dimensions
        width, height= image.size

        # Create an empty NumPy array for the rotated image
        rotated_image = np.zeros((height, width, 3), dtype=np.uint8)

        # Calculate the rotation matrix
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        center_x = width // 2
        center_y = height // 2

        # Perform the rotation manually using the rotation matrix
        for y in range(height):
            for x in range(width):
                # Translate coordinates to center
                translated_x = x - center_x
                translated_y = y - center_y

                # Apply rotation
                new_x = int(translated_x * cos_theta - translated_y * sin_theta + center_x)
                new_y = int(translated_x * sin_theta + translated_y * cos_theta + center_y)

                # Check if the new coordinates are within bounds
                if 0 <= new_x < width and 0 <= new_y < height:
                    rotated_image[y, x] = image.getpixel((new_x, new_y))

        # Create a Pillow image from the rotated NumPy array
        rotated_image = Image.fromarray(rotated_image)
        open_cv_image = np.array(rotated_image)  
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        self.img = open_cv_image
        return self.img 
            
                
#Run
if __name__ == '__main__':
    App()
         
         
