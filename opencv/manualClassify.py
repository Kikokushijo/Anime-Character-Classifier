from PIL import Image, ImageTk, ImageDraw
from collections import OrderedDict, deque
from copy import copy
import tkinter as tk
import numpy as np
import cv2
import os

CLS_SIZE = 35
SEL_SIZE = 60
ORI_SIZE = 96
IMAGE_PER_ROW = 10

class ClassifyDict(object):
    def __init__(self, dict_path):
        self.dict_path = dict_path
        if not os.path.exists(self.dict_path):
            wants_create = self.askCreateDict()
            if wants_create:
                os.makedirs(dict_path, exist_ok=True)

        if os.path.exists(self.dict_path):
            self.dict_file = open(dict_path, "r+")
            self.class_name = list(OrderedDict.fromkeys([name.strip('\n') for name in self.dict_file]))
            wants_rewrite = self.askRewriteDict()
            if wants_rewrite:
                self.rewrite()
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
            if cmd[0] == "add":
                if len(cmd) == 2:
                    if cmd[1] in self.class_name:
                        print("Class %s already exists." % cmd[1])
                    elif len(self.class_name) >= 9:
                        print("Class Numbers Exceeded.")
                    else:
                        self.class_name.append(cmd[1])
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
                    self.class_name = []
                else:
                    self.rewriteHelp()
            elif cmd[0] == "quit":
                if len(cmd) == 1:
                    if len(self.class_name) == 0:
                        print("You Must Have At Least One Class.")
                    else:
                        return
                else:
                    self.rewriteHelp()
            else:
                self.rewriteHelp()

    def rewriteHelp(self):
        print("")
        print("---------------------------------------")
        print("To Create A New Class (Up to 9 Classes), use \"add %s\" % class_name")
        print("To Delete A Existed Class, use \"del %s\" % class_name")
        print("To Clean All The Dict File, use \"reset\"")
        print("To Quit Rewrite Mode, use \"quit\"")
        print("---------------------------------------")
        print("")

class TextFrame(tk.Frame):
    def __init__(self, parent, sets):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.key_pairs = [(str(index), name) for index, name in enumerate(sets, 1)] + \
                         [('0', 'None of Above'),
                          ('X', 'Not Face'),
                          ('N', 'Unclassify'),
                          (' ', ' '),
                          ('C', 'Convert between Click/Focus Mode'),
                          ('Ctrl-S', 'Save Current Classified Status'),
                          ('Ctrl-Z', 'Back to Last Saved Status'),
                          ('Ctrl-R', 'Reset All'),
                          ('Ctrl-A', 'Select Unclassified All'),
                          ('Ctrl-T', 'Toggle Unclassified All'),
                          ('Enter' , 'Complete Classifying and'),
                          ('      ', 'Switch to Next Folder')]
        self.key_labels = [tk.Label(self, text=key) for key, _ in self.key_pairs]
        self.name_labels = [tk.Label(self, text=class_name) for _, class_name in self.key_pairs]
        for index, label in enumerate(self.key_labels):
            label.grid(row=index, column=0, sticky="W")
        for index, label in enumerate(self.name_labels):
            label.grid(row=index, column=1, sticky="W")
        self.grid(row=0, column=0, sticky="NW")

class PhotoButtonFrame(tk.Frame):

    class PhotoButton(tk.Button):
        def __init__(self, parent, image_path, index):
            tk.Button.__init__(self, parent, command=lambda i=index:parent.toggle(i))
            self.parent = parent
            self.is_selected = False
            self.is_focused = False
            self.initializeImg(Image.open(image_path))
            self.grid(row=index//IMAGE_PER_ROW, column=index%IMAGE_PER_ROW)
            self.setClass(None)
            self.update()

        def initializeImg(self, img):
            ori_image = np.array(img.resize((ORI_SIZE, ORI_SIZE)))
            tk_ori_image = ImageTk.PhotoImage(Image.fromarray(ori_image))

            sel_image = np.array(img.resize((ORI_SIZE, ORI_SIZE)))
            cv2.rectangle(sel_image, (0,0), (ORI_SIZE, ORI_SIZE), color=(255,255,255), thickness=10)
            tk_sel_image = ImageTk.PhotoImage(Image.fromarray(sel_image))

            foc_image = np.array(img.resize((ORI_SIZE, ORI_SIZE)))
            cv2.rectangle(foc_image, (0,0), (ORI_SIZE, ORI_SIZE), color=(255,0,0), thickness=10)
            tk_foc_image = ImageTk.PhotoImage(Image.fromarray(foc_image))

            self.img_dict = {"ori_image":tk_ori_image,
                             "sel_image":tk_sel_image,
                             "foc_image":tk_foc_image}

            self.tmp_img_dict = {"ori_image":ori_image,
                                 "sel_image":sel_image,
                                 "foc_image":foc_image}

            self.cls_img_dict = {"ori_image":tk_ori_image,
                                 "sel_image":tk_sel_image,
                                 "foc_image":tk_foc_image}

        def setClass(self, target_class):
            self.cls_img_dict = {}
            self.cls = target_class
            for key, img in self.tmp_img_dict.items():
                tmp = copy(img)
                if not None:
                    cv2.rectangle(img=tmp, pt1=(0,60), pt2=(ORI_SIZE-60, ORI_SIZE), \
                                  color=(255,255,255), thickness=-1)
                    cv2.putText(img=tmp, text=self.cls, org=(0,90), fontFace=cv2.FONT_HERSHEY_SIMPLEX, \
                                fontScale=1.5, color=(0,0,0), thickness=2)
                self.cls_img_dict[key] = ImageTk.PhotoImage(Image.fromarray(tmp))

        def update(self):
            if self.is_selected:
                self.config(relief="sunken", image=self.cls_img_dict["sel_image"])
            elif self.is_focused:
                self.config(relief="raised", image=self.cls_img_dict["foc_image"])
            else:
                self.config(relief="raised", image=self.cls_img_dict["ori_image"])

    def __init__(self, parent, crop_path, class_num, folder_index=385):

        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.crop_path = crop_path
        self.folder_index = folder_index
        self.class_num = class_num

        self.select_mode = "Click Mode"
        self.is_multi_selecting = False
        self.on_which_button = None
        self.saved_classify_result = [None] * 50
        self.saved_unclassified = deque([])

        sub_crop_path = os.path.join(self.crop_path, str(self.folder_index))
        if os.path.exists(sub_crop_path):
            self.photoButtons = []
            for index, image_name in enumerate(os.listdir(sub_crop_path)):
                image_path = os.path.join(sub_crop_path, image_name)
                button = self.PhotoButton(self, image_path, index)
                self.photoButtons.append(button)

        self.grid(row=0, column=1, sticky="NW")
        self.focus_set()
        self.setBindKey()

    def toggle(self, index):
        if self.select_mode == "Click Mode":
            button = self.photoButtons[index]
            button.is_selected = not button.is_selected
            button.update()

    def setBindKey(self):

        def focusModeInit():
            self.saved_unclassified = deque([])
            for index, button in enumerate(self.photoButtons):
                button.is_selected = False
                button.is_focused = False
                if button.cls is None:
                    self.saved_unclassified.append(button)
            if self.saved_unclassified:
                button = self.saved_unclassified[0]
                button.is_focused = True
            for button in self.photoButtons:
                button.update()

        def clickModeInit():
            if self.saved_unclassified:
                button = self.saved_unclassified[0]
                button.is_focused = False
                button.update()
            self.saved_unclassified = deque([])

        def classify(event):
            if self.select_mode == "Click Mode":
                for index, button in enumerate(self.photoButtons):
                    if button.is_selected:
                        if event.char == 'n':
                            button.setClass(None)
                        else:
                            button.setClass(event.char)
                        self.toggle(index)
            else:
                if self.saved_unclassified:
                    button = self.saved_unclassified[0]
                    if event.char == 'n':
                        pass
                    else:
                        button.is_focused = False
                        button.setClass(event.char)
                        button.update()
                        _ = self.saved_unclassified.popleft()

                        if self.saved_unclassified:
                            button = self.saved_unclassified[0]
                            button.is_focused = True
                            button.update()

        def convertSelectMode(event):
            if self.select_mode == "Click Mode":
                self.select_mode = "Focus Mode"
                focusModeInit()
            else:
                self.select_mode = "Click Mode"
                clickModeInit()

            for button in self.photoButtons:
                button.update()

        def saveClassifiedStatus(event):
            self.saved_classify_result = []
            for button in self.photoButtons:
                self.saved_classify_result.append(button.cls)

        def backToLastSavedStatus(event):
            for target_class, button in zip(self.saved_classify_result, self.photoButtons):
                button.setClass(target_class)
                button.update()

            if self.select_mode == "Click Mode":
                clickModeInit()
            else:
                focusModeInit()

        def resetClassifiedAll(event):
            for button in self.photoButtons:
                button.setClass(None)
                button.update()

            if self.select_mode == "Click Mode":
                clickModeInit()
            else:
                focusModeInit()

        def selectUnclassifiedAll(event):
            if self.select_mode == "Click Mode":
                for index, button in enumerate(self.photoButtons):
                    if button.cls is None:
                        button.is_selected = True
                        button.update()

        def toggleUnclassifiedAll(event):
            if self.select_mode == "Click Mode":
                for index, button in enumerate(self.photoButtons):
                    if button.cls is None:
                        self.toggle(index)

        def enterButton(event, index):
            self.on_which_button = index

        def leaveButton(event, index):
            self.on_which_button = None

        self.bind_pairs = [(str(i), classify) for i in range(self.class_num+1)] + \
                          [("x", classify),
                           ("n", classify),
                           ("c", convertSelectMode),
                           ("<Control-s>", saveClassifiedStatus),
                           ("<Control-z>", backToLastSavedStatus),
                           ("<Control-r>", resetClassifiedAll),
                           ("<Control-a>", selectUnclassifiedAll),
                           ("<Control-t>", toggleUnclassifiedAll)]

        for key, func in self.bind_pairs:
            self.bind(key, func)

        for index, button in enumerate(self.photoButtons):
            button.bind("<Enter>", lambda event, i=index: enterButton(event=event, index=i))
            button.bind("<Leave>", lambda event, i=index: leaveButton(event=event, index=i))

def manualClassify(target_path):

    training_path = os.path.join(target_path, "training_data")
    crop_path = os.path.join(target_path, "crop")
    dict_path = os.path.join(training_path, "dict.txt")
    classify_dict = ClassifyDict(dict_path)
    print(classify_dict.class_name)

    window = tk.Tk()
    window.minsize(width=1300, height=600)
    window.maxsize(width=1300, height=600)
    window.title("Manual Classifier")
    text_frame = TextFrame(window, classify_dict.class_name)
    photo_button = PhotoButtonFrame(parent=window, crop_path=crop_path, \
                                    class_num=len(classify_dict.class_name))
    window.mainloop()