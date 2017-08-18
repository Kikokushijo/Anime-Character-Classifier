import cv2
import sys
import os.path

MAX_IMAGE_PER_FOLDER = 50

def detect(target_path, cascade_file = "lbpcascade_animeface.xml"):

    cur_path = os.getcwd()
    cascade_path = os.path.join(cur_path, "opencv", cascade_file)
    if not os.path.isfile(cascade_path):
        raise RuntimeError("%s: not found" % cascade_file)
    cascade = cv2.CascadeClassifier(cascade_path)

    frame_path = os.path.join(target_path, "frame")
    crop_path = os.path.join(target_path, "crop")

    frame_num = 0
    crop_count = 0
    sub_curr_crop_path = None
    for folder in os.listdir(frame_path):
        folder_path = os.path.join(frame_path, folder)
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)
            for frame in os.listdir(subfolder_path):
                
                if frame_num % 100 == 0:
                    print("Cropping Frame %d" % frame_num)

                frame_path = os.path.join(subfolder_path, frame)
                # image = cv2.read(frame)
                image = cv2.imread(frame_path)
                # cv2.imshow("test", image)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)

                # cv2.imshow("test", gray)
                # cv2.waitKey(0)
                faces = cascade.detectMultiScale(gray,
                                        # detector options
                                                scaleFactor = 1.1,
                                                minNeighbors = 5,
                                                minSize = (48, 48))

                # cv2.imshow(gray)
                for index, (x, y, w, h) in enumerate(faces, crop_count):
                    # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    crop_img = image[y:(y + h), x:(x + w)]
                    # cv2.imshow("Crop", crop_img)
                    # cv2.waitKey(0)
                    if crop_count % MAX_IMAGE_PER_FOLDER == 0:
                        sub_crop_path = os.path.join(crop_path, str(crop_count // MAX_IMAGE_PER_FOLDER))
                        os.makedirs(sub_crop_path, exist_ok = True)
                    cv2.imwrite(os.path.join(sub_crop_path, "%d.jpg" % crop_count), crop_img)
                    print("Successfully Crop Out Image %d" % crop_count)
                    crop_count += 1

                frame_num += 1    