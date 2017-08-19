# Anime_Character_Classifier
WARNING: STILL UNDER CONSTRUCT

This project is just an NN experiment about classifying anime characters.

To start with, you have to create folders and put video into it , and the whole structure should be like below:
```
\Anime_Character_Classifier
    \opencv
        \detect.py
        \manClassify.py
        \saveFrame.py
        \lbpcascade_animeface.xml
    \video
        \foldername         // You can name your folder there
            \video
                \video.mp4  // And put your video there
            \crop
            \frame
            \training_data
    \.gitignore
    \main.py
    \README.md
```


Then you can:
* Use ```python main.py saveframe foldername ``` to Save Frame
* Use ```python main.py detectface foldername``` to Detect Character Face
* Use ```python main.py manclassify foldername``` to Classify Training Data

NOTICE:
* The frames capturing from the video will be saved in ```video\foldername\frame``` folder, with some subfolders in it like below:
```
\video
    \foldernmae
        \video
            \video.mp4
        \crop
            \0
            \1
            \...        // Depend on how many images you crop, each subfolder contains 50 frames in default.
        \frame
            \0
            \1
            \...        // Depend on how many frames you capture, each subfolder contains 50 frames in default.
        \training_data
            \0
            \1
            \...        // Depend on how many subclasses you set.
```
* The images cropping from frames will be saved in ```video\foldername\crop``` folder, with some subfolders in it, just like the frame folder.
* The classified cropped images will be saved in ```video\foldername\training_data```, with some subfolders in it.  Each subfolder represent a subclass, and the images belong to this subclass will be compressed and saved in it.




