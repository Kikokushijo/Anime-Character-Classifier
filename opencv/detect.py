import cv2
import sys
import os.path

MAX_IMAGE_PER_FOLDER = 50

def detect(target_path, cascade_file = "lbpcascade_animeface.xml"):

    cur_path = os.getcwd()
    if not os.path.isfile(os.path.join(cur_path, "opencv", cascade_file)):
        raise RuntimeError("%s: not found" % cascade_file)
    cascade = cv2.CascadeClassifier(cascade_file)

    frame_num = 0
    count = 0
    while True:
        pass

"""
def detect(anime_name, chapter, cascade_file = "lbpcascade_animeface.xml"):
    script_dir = os.path.dirname(__file__)
    cascade_file = os.path.join(script_dir, cascade_file)

    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    cascade = cv2.CascadeClassifier(cascade_file)

    frame_num = 0
    count = 0
    while True:
        if frame_num % 5 == 0:
            print("detect frame %d" % frame_num)
        frame_dir = "%s/frame/%s-%d-frame%d.jpg" % (anime_name, anime_name, chapter, frame_num)
        frame_file = os.path.join(script_dir, frame_dir)
        if not os.path.isfile(frame_file):
            print(frame_file)
            break

        image = cv2.imread(frame_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor = 1.1,
                                         minNeighbors = 5,
                                         minSize = (24, 24))
        for index, (x, y, w, h) in enumerate(faces, count):
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            crop_img = image[y:(y + h), x:(x + w)]
            # cv2.imshow("Crop", crop_img)
            # cv2.waitKey(0)
            cv2.imwrite("opencv/%s/crop/out%d.png" % (anime_name, index), crop_img)

        frame_num += 1
        count += len(faces)
"""