Owner is a dickhead + rude as fuck

Official guide you get after wasting $150:


DO these steps on your 2nd PC running the Chair! 

Disable Virus Protection on Script PC. It can mess with the OpenCV install.

Download the opencv simple build from
https://drive.google.com/file/d/1jDDhIitfYsqWsuaSnRKMi9gdBUxRtspt/view?usp=share_link

For opencv install, place "opencv_build" folder in this location - C:\
run Installer (GPU).bat as admin (which is located in the opencv_build folder).

Once you get to the end of  Installer(GPU).bat, It auto starts build.bat....
Pick the GPU series that is in your 2nd pc. (If you have 40 series pick the 30 series option not auto)
Once this completes, screenshot the output and post in your ticket!

Next, download the MoonlightCV or MoonlightAI folder and place that in C:\
The folder needs placed in this directory in order to properly run.

Continue with your arduino/KmBox/moonlink setup and your NDI/capture card setup
Cap in game FPS


Install NDI Tools from https://ndi.video/tools/download/ , after installing, open screen capture.



After doing this, copy the MoonlightAI folder to C:/

use avrdude to flash whichever mouse firmware if using arduino.

arduino needs to be on COM3, kmbox B has to be on COM41

Open a cmd in the folder and do python.exe main.pyc

Do python.exe run_me.py

Make sure main pc and second pc are connected to same network.


PLEASE DM ME MORE STUFF FROM MOONLIGHT
