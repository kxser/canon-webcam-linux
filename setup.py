import os
import shutil

user = os.getlogin()
print(user)
os.system(f"mkdir /home/{user}/Documents/CannonDriver")
os.system("pip install -r requirements.txt")
shutil.copy2("assets/interface.py", f"/home/{user}/Documents/CannonDriver/interface.py")
shutil.copy2("assets/camera-logo.xpm", f"/home/{user}/Documents/CannonDriver/camera-logo.xpm")

with open (f"/home/{user}/Desktop/CameraDriver.desktop", "w+") as f:
    f.writelines(f"""
[Desktop Entry]
Categories=Application;
Comment=Open Python script (name)
Exec=python /home/{user}/Documents/CannonDriver/interface.py
Icon=/home/{user}/Documents/CannonDriver/camera-logo.xpm
Name[en_US]=CameraDriver
Name=CameraDriver
Terminal=true
Type=Application
Version=1.0""")


print("Check your desktop folder for a CameraDriver.desktop file.")