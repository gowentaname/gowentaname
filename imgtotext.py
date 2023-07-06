from cgitb import grey
import cv2
import pytesseract
import matplotlib.pyplot as plt
import easyocr
import os
from gtts import gTTS
import pygame

from tkinter import *   
from tkinter import filedialog
from PIL import ImageTk, Image

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'

root = Tk()
root.title('TechVidvan Text from image project')

newline = Label(root)
uploaded_img = Label(root)
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

def open_camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            cv2.imwrite('captured_image.jpg', frame)  # บันทึกภาพที่ถ่ายเป็นไฟล์ 'captured_image.jpg'
            cv2.imshow('Captured Image', frame)  # แสดงภาพที่ถ่ายได้
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            extract_tesseract('captured_image.jpg')  # ประมวลผลภาพที่ถ่ายและแสดงผลเป็นข้อความ
            break
    cap.release()
    cv2.destroyAllWindows()


def extract_tesseract(path):
    Actual_image = cv2.imread(path)
    Sample_img = cv2.resize(Actual_image, (400, 350))
    Image_ht, Image_wd, Image_thickness = Sample_img.shape
    Sample_img = cv2.cvtColor(Sample_img, cv2.COLOR_BGR2RGB)
    texts = pytesseract.image_to_data(Sample_img)
    mytext = ""
    prevy = 0
    for cnt, text in enumerate(texts.splitlines()):
        if cnt == 0:
            continue
        text = text.split()
        if len(text) == 12:
            x, y, w, h = int(text[6]), int(text[7]), int(text[8]), int(text[9])
            if len(mytext) == 0:
                prey = y
            if prevy - y >= 10 or y - prevy >= 10:
                print(mytext)
                Label(root, text=mytext, font=('Times', 15, 'bold')).pack()
                mytext = ""
            mytext = mytext + text[11] + " "
            prevy = y
    Label(root, text=mytext, font=('Times', 15, 'bold')).pack()
    tts = gTTS(text=mytext, lang='th')
    tts.save('output.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()

def extract_easyocr(path):
    reader = easyocr.Reader(['en', 'th'])
    result = reader.readtext(path)
    for detection in result:
        text = detection[1]
        print(text)
        Label(root, text=text, font=('Times', 15, 'bold')).pack()
        tts = gTTS(text=text, lang='th')
        tts.save('output.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()

def extract_tesseract_and_easyocr(path):
    extract_tesseract(path)
    extract_easyocr(path)

def clear_results():
    for widget in root.winfo_children():
        if isinstance(widget, Label):
            widget.configure(text="")
            
extractBtn3 = None

def show_extract_button(path):
    global extractBtn3
    extractBtn2 = Button(root, text="Extract text with EasyOCR", command=lambda: extract_easyocr(path),
                         bg="#2f2f77", fg="gray", pady=15, padx=15, font=('Times', 15, 'bold'))
    extractBtn2.pack()
    if not extractBtn3:
        extractBtn3 = Button(root, text="Clear Results", command=clear_results,
                             bg="#2f2f77", fg="gray", pady=15, padx=15, font=('Times', 15, 'bold'))
        extractBtn3.pack()

def upload():
    try:
        path = filedialog.askopenfilename()
        image = Image.open(path)
        img = ImageTk.PhotoImage(image)
        uploaded_img.configure(image=img)
        uploaded_img.image = img
        show_extract_button(path)
    except:
        pass

uploadbtn = Button(root, text="Upload an image", command=upload, bg="#2f2f77", fg="gray", height=2, width=20,
                   font=('Times', 15)).pack()

newline.configure(text='\n')
newline.pack()
uploaded_img.pack()

open_camera_btn = Button(root, text="Open Camera", command=open_camera, bg="#2f2f77", fg="gray", pady=15, padx=15, font=('Times', 15, 'bold'))
open_camera_btn.pack()

root.mainloop()