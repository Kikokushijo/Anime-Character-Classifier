import tkinter as tk
from PIL import Image, ImageTk
# from tkinter import ttk
import os
import cv2

MAX_SIZE = 96, 96

class ClassifyDict(object):
    def __init__(self, dict_path):
        self.dict_path = dict_path
        if not os.path.exists(self.dict_path):
            wants_create = self.askCreateDict()
            if wants_create:
                os.makedirs(dict_path, exist_ok=True)

        if os.path.exists(self.dict_path):
            self.dict_file = open(dict_path, "r+")
            self.class_name = set([name.strip('\n') for name in self.dict_file])
            wants_rewrite = self.askRewriteDict()
            if wants_rewrite:
                self.rewrite()
            # self.class_name.add("None")
        else:
            pass

    def askCreateDict(self):
        print("No Classify Dictionary.")
        while True:
            ans = input("Create A New Classify Dict? (Y/N)")
            if ans in ["Y", "y"]:
                return True
            elif ans in ["N", "n"]:
                return False
            else:
                print("Please Enter Y or N Only.")

    def askRewriteDict(self):
        while True:
            ans = input("Rewrite The Classify Dict? (Y/N) ")
            if ans in ["Y", "y"]:
                return True
            elif ans in ["N", "n"]:
                return False
            else:
                print("Please Enter Y or N Only.")

    def rewrite(self):
        self.rewriteHelp()
        while True:
            print("")
            print("Current classes:", self.class_name if len(self.class_name) else "No class exists.")
            print("")

            cmd = input().split()
            if cmd[0] == "new":
                if len(cmd) == 2:
                    if cmd[1] in self.class_name:
                        print("Class %s already exists." % cmd[1])
                    elif len(self.class_name) >= 9:
                        print("Class Numbers Exceeded.")
                    else:
                        self.class_name.add(cmd[1])
                else:
                    self.rewriteHelp()
            elif cmd[0] == "del":
                if len(cmd) == 2:
                    if cmd[1] in self.class_name:
                        self.class_name.remove(cmd[1])
                    else:
                        print("Class %s doesn't exist." % cmd[1])
                else:
                    self.rewriteHelp()
            elif cmd[0] == "reset":
                if len(cmd) == 1:
                    self.class_name = set([])
                else:
                    self.rewriteHelp()
            elif cmd[0] == "quit":
                if len(cmd) == 1:
                    return
                else:
                    self.rewriteHelp()
            else:
                self.rewriteHelp()

    def rewriteHelp(self):
        print("")
        print("---------------------------------------")
        print("To Create A New Class (Up to 9 Classes), use \"new %s\" % class_name")
        print("To Delete A Existed Class, use \"del %s\" % class_name")
        print("To Clean All The Dict File, use \"reset\"")
        print("To Quit Rewrite Mode, use \"quit\"")
        print("---------------------------------------")
        print("")

class Interface(tk.Tk):
    def __init__(self, class_set, crop_path):
        super(Interface, self).__init__()

        self.sub_crop_folder_index = 0
        self.crop_path = crop_path

        self.title("Test")
        labels_index = [tk.Label(self, text = str(index)) \
                for index in range(1, len(class_set)+1)]
        labels_class = [tk.Label(self, text = classes) \
                for classes in class_set]

        for index, (lindex, lclass) in enumerate(zip(labels_index, labels_class)):
            lindex.grid(row=index, column=0)
            lclass.grid(row=index, column=1)

        self.setImage()

        self.mainloop()

        print("test")

    def setImage(self):
        sub_crop_path = os.path.join(self.crop_path, str(self.sub_crop_folder_index))
        if os.path.exists(sub_crop_path):

            images = []
            # photos = []
            for image in os.listdir(sub_crop_path):
                image_path = os.path.join(sub_crop_path, image)
                # print(image_path)
                # tmp = cv2.imread(image_path)
                # cv2.imshow("test", tmp)
                # cv2.waitKey(0)
                image = Image.open(image_path)
                image.thumbnail(MAX_SIZE, Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(image=photo)
                label.image = photo
                images.append(label)

            for index, image in enumerate(images):
                image.grid(row=index//10, column=index%10+2)
            # images[0].grid(row=0, column=3)


def manClassify(target_path):

    training_path = os.path.join(target_path, "training_data")
    crop_path = os.path.join(target_path, "crop")
    dict_path = os.path.join(training_path, "dict.txt")
    classify_dict = ClassifyDict(dict_path)
    
    print(classify_dict.class_name)

    interface = Interface(classify_dict.class_name, crop_path)
    """
    master = tk.Tk()
    master.title("Test")
    tk.Label(master, text="First").grid(row=0)
    tk.Label(master, text="Second").grid(row=1)
    tk.Entry(master).grid(row=0, column=1)
    tk.Entry(master).grid(row=1, column=1)
    master.mainloop()

    window = tk.Tk()
    window.title("Man Classifier")

    frame = tk.Frame(window)
    frame.pack()

    labels = [tk.Label(frame, text = "%d %s" % (index, classes)) \
            for index, classes in enumerate(classifyDict.class_name)]
    for label in labels:
        label.pack()

    button = tk.Button(frame, text = "OK")
    button.pack()

    window.mainloop()
    """