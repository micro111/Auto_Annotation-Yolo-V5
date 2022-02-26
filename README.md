I am Japanese, so I use a translation tool.

Are you sick of annotations?   
This tool was created with the intention of helping you.　 :)  

# Auto_Annotation-Yolo-V5
　This is a tool that automatically annotates from videos. Two formats are available: .exe and .Py.  
![image](https://user-images.githubusercontent.com/88880693/155735245-48e246c5-f2b8-46bd-a7b5-a439c7dc7173.png)

# How to Use..?
https://user-images.githubusercontent.com/88880693/155746427-955dc6e3-fe2e-4341-9056-fad5da51be6e.mp4

## 1.Select the video to be annotated
　Please Click on "Open the Video" in the upper left corner.  
Currently this tool supports "mp4" and "mov" format for videos.

(If you want to add it to an existing yaml file instead of generating a new one,  
press the button again to load the yaml file, or drag and drop it.  
(Either the video or the yaml can be done first.) )  

## 2. Enter the name of the object.
 　Write the name of the object appearing in the video next to "Class name:"  
 in the lower left corner.
 
## 3.We're Ready..! Please press the Start button to begin.
　We are ready to go!  
All you have to do is press start and it will be annotated automatically.

## 4.Checking the generated file
 　The path to the save location is written at the bottom right side  
 where it says "---log---".　



# List of folders to be created

+ data
  + /custom   
    + /bbox (Not used for training, but for object detection confirmation)
    + /train (Data for training)
      + /images/*
      + /labels/*
    + /vaild (Data for training)
      + /images/*
      + /labels/* 
    + /yaml(yaml file to be loaded during learning)
      + .data.yaml  
    + /debug (This folder is located in "auto.conf" and will be created if debug is set to 1.)  
      + /frame/* (Output of frames cut out from video.)
      + /gray/*  (A grayscale image of the cutout.)
      + /bin/*  (The result of binarizing the cropped image.)
      + /mask/*  (Image generated for mask)
      + /masked/* (Image with mask applied.)
      
# Caution.
　This tool should be done using a video where the current binarization process is easy to apply.  
(background and object colors are close to opposite colors).  
Also, only one object can be detected per video.  
(We plan to support this later.)   


# Windows(Ano.exe) Download
<img src="https://img.shields.io/badge/-Windows-0078D6.svg?logo=windows&style=flat">

I just compiled it with PyInstaller.  
Note the following.  
 - It is very large (about 300MB).  
 - This app does not have a certificate, so Defender will warn you.

Use it at your own risk and compare it to HASH below.  
Also, I would appreciate it if someone could tell me how to add proof to the exe.

| HASH | KEY |
|:---:|:---:|
|SHA256 |0756ba626e3454ba24cf5dc20ed5eebb6bd95f8f76e0aa7dc5661e4b33758bc5 |
|MD5 |56852fbee7ac72cd6ae881430213b28d |

Windows (Ano.exe) Google-Drive:  
https://drive.google.com/file/d/1bnMnFtN9144rAcvKPudSEISMyqyGtR68/view?usp=sharing


# Other(Ano.py) Download
<img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">  
The operation of this tool has been verified with Python 3.9.5.

```
git clone https://github.com/micro111/Auto_Annotation-Yolo-V5/
cd Auto_Annotation-Yolo-V5
pip install -r requirements.txt
python Ano.py  (or python3 Ano.py)
```
It does not work in WSL and WSL2 environments.
(Because it uses threads).  

# Plans for future improvements
 - Change in the algorithm for determining the threshold of binarization  
(Modifications will be made to place a point on the image and place that position as white)  
 - Support for other kinds of annotations  
(Currently, support for Yolo-V3 and XML is planned (almost complete).
 - Automatically annotate a folder with a large number of images.
 - Extraction of multiple objects in a single image
(This will be solved by dividing the image into regions.)

===========================================================  
Thanks for looking. Hope it will help someone else.
