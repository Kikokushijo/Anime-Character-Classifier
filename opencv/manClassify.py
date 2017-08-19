import tkinter as tk
import os

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

def manClassify(target_path):

    training_path = os.path.join(target_path, "training_data")
    dict_path = os.path.join(training_path, "dict.txt")
    classifyDict = ClassifyDict(dict_path)
    print(classifyDict.class_name)

    window = tk.Tk()
    window.title("Man Classifier")
    labels = [tk.Label(window, text = "%d %s" % (index, classes)) \
            for index, classes in enumerate(classifyDict.class_name)]
    for label in labels:
        label.pack()

    button = tk.Button(window, text = "OK")
    button.pack()

    window.mainloop()