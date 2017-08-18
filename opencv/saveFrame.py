import cv2
import os

MAX_IMAGE_PER_FOLDER = 50

def saveFrame(target_path, interval = 24):
    video_path = os.path.join(target_path, "video")
    frame_path = os.path.join(target_path, "frame")

    print("Saving Frame...")

    for index, video in enumerate(os.listdir(video_path)):

        curr_frame_path = os.path.join(frame_path, str(index))

        vidcap = cv2.VideoCapture(os.path.join(video_path, video))
        frame_count = 0
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_count * interval)
        success, image = vidcap.read()

        if success:
            print("Successfully Opening Video %d:%s" %(index, video))
            os.makedirs(curr_frame_path, exist_ok=True)
        else:
            print("Fail to Open Video %d:%s" %(index, video))

        sub_curr_frame_path = None
        while success:
            if frame_count % MAX_IMAGE_PER_FOLDER == 0:
                sub_curr_frame_path = os.path.join(curr_frame_path, str(frame_count // MAX_IMAGE_PER_FOLDER))
                os.makedirs(sub_curr_frame_path, exist_ok=True)
            
            frame_name = os.path.join(sub_curr_frame_path, "output%d.jpg" % frame_count)
            cv2.imwrite(frame_name, image)
            print("Saving Frame %d-%d..." % (index, frame_count))

            frame_count += 1
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_count * interval)
            success, image = vidcap.read()

    print("All Video's Frame Saved.")