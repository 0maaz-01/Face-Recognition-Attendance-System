from tkinter import *
from D import Attendance
import os
import cv2
from PIL import Image 
from numpy import * 
from tkinter import messagebox 
import mysql.connector
from datetime import datetime  
 

class Face_Recognition_System:

    def __init__(self, window):
        self.window = window
        self.window.title("Face Recognition System")

        def student():
            from B import Student
            Student(self.window)
        def attendance():
            Attendance(self.window)


        self.boy = PhotoImage(file = "Images\\12.png")
        student_details = Button(self.window, font=("aerial", 20, "bold"), text="Student Details", image =  self.boy,
                         background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, border=0, command= student,
                         borderwidth=6, activebackground="#fa8072")
        student_details.place(x=220, y=100)

        self.face = PhotoImage(file = "Images\\Face2.png")
        face_recog = Button(self.window, font=("aerial", 20, "bold"), text="Face Recognition", image=self.face,
                         background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, border=0,
                         borderwidth=6, activebackground="#fa8072", command = self.face_recog)
        face_recog.place(x=1060, y=100)

        self.atten = PhotoImage(file = "Images\\Attendance.png")
        attend = Button(self.window, font=("aerial", 20, "bold"), text="Attendance", image=self.atten,
                         background="#ffdab9", compound=TOP, height=250, width=240, relief=RAISED, border=0,
                         borderwidth=6, activebackground="#fa8072", command = attendance)
        attend.place(x=640, y=100)

        self.group = PhotoImage(file = "Images\\Group.png")
        face_samples = Button(self.window, command = self.open_img, font=("aerial", 20, "bold"), text="Face Samples", image=self.group, background="#ffdab9",
                         compound=TOP, height=250, width=240, relief=RAISED, border=0, borderwidth=6,
                         activebackground="#fa8072")
        face_samples.place(x=640, y=440)


        self.exi = PhotoImage(file = "Images\\EXIT.png")
        close = Button(self.window, font=("aerial", 20, "bold"), text="Exit",background="#ffdab9",image=self.exi,
                         compound=TOP, height=250, width=240, relief=RAISED, border=0, borderwidth=6, command = self.close,
                         activebackground="#fa8072")
        close.place(x=1060, y=440)


        self.trai = PhotoImage(file = "Images\\5.png")
        train = Button(self.window, font=("aerial", 20, "bold"), text="Train Data",background="#ffdab9", image=self.trai,
                         compound=TOP, height=250, width=240, relief=RAISED, border=0, borderwidth=6, command = self.train,
                         activebackground="#fa8072")
        train.place(x=220, y=440)

    def close(self):
        self.window.destroy()

    def open_img(self):
        os.startfile("Faces")

    def train(self):
        faces_dir = ("Faces")
        path = [os.path.join(faces_dir, file) for file in os.listdir(faces_dir)]
        faces = []
        ids = []

        for image in path:
            img = Image.open(image).convert('L')
            image_np = array(img, "uint8")
            id = int(os.path.split(image)[1].split('.')[1])
            faces.append(image_np)
            ids.append(id)
            cv2.imshow("Training", image_np)
            cv2.waitKey(1) == 27

        ids = array(ids)

        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifire.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Result", "Training images completed!!")

    def mark_attendance(self, i, n):
        with open("Attendance\\Attendance.csv", "r+", newline="\n") as f:
            myDatalist = f.readlines()
            name_list = []
            for line in myDatalist:
                entry = line.split((","))
                name_list.append(entry[0])

            if ((i not in name_list)) and ((n not in name_list)):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i}, {n}, {d1},{dtString}, Present")


    def face_recog(self):

        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, (255, 25, 255), "Face", clf)
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifire.xml")

        videoCap = cv2.VideoCapture(0)

        while True:
            ret, img = videoCap.read()
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Face Detector", img)

            if cv2.waitKey(1) == 27:
                break
        videoCap.release()
        cv2.destroyAllWindows()

     
        def draw_boundray(img, classifier, scaleFactor, minNeighbors, color, text, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            featuers = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []

            for (x, y, w, h) in featuers:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h, x:x + w])

                confidence = int((100 * (1 - predict / 300)))

                conn = mysql.connector.connect(host="localhost", username="root", password="5moha@8234mo!#Ham",
                                               database="frs")
                cursor = conn.cursor()

                cursor.execute("select Name from student where StudentID=" + str(id))
                n = cursor.fetchone()
                n = "+".join(n)

                cursor.execute("select StudentID from student where StudentID=" + str(id))
                i = cursor.fetchone()
                i = "+".join(i)

                if confidence > 77:
                    cv2.putText(img, f"StudentID:{i}", (x, y - 80), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,0), 2)
                    cv2.putText(img, f"Name:{n}", (x, y - 55), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0,0), 2)
                    self.mark_attendance(i, n)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,0, 0), 3)

                coord = [x, y, w, y]
            return coord



if __name__ == "__main__":
    window = Tk()
    s = Face_Recognition_System(window)
    icon = PhotoImage(file = "Images\\M.png")
    window.iconphoto(True, icon)
    window.geometry("1540x800+-10+0")
    window.configure(background="#008080")
    window.mainloop()
