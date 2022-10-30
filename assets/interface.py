from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import subprocess, time, os, multiprocessing, subprocess, pexpect
from rich.console import Console
console = Console()

def dependencies():
    global user_distro
    distroinfo = subprocess.check_output(["lsb_release", "-a"]).decode('utf-8').lower()
    arch_based = ["manjaro", "arch", "garuda", "endeavour", "arco"]
    debian_based = ["debian", "ubuntu", "kubuntu", "xubuntu", "lubuntu", "pop!", "zorin", "kali", "deepin"]
    
    for elem in arch_based:
        if elem in distroinfo:
            user_distro = "arch"
            console.print("[cyan bold]User distro is arch based.[/]")
    for elem in debian_based:
        if elem in distroinfo:
            user_distro = "debian"
            console.print("[cyan bold]User distro is debian based.[/]")
    if user_distro is None:
        QMessageBox.about(MainWindow, "Warning", "Your system is not arch or debian based. Please install ffmpeg, gphoto2, v4l2loopback-utils, v4l2loopback-dkms")
    def arch_operations():
        dependencies = ["ffmpeg", "v4l2loopback-dkms", "gphoto2"]
        for dependency in dependencies:
            try: 
                subprocess.check_output(["pacman", "-Q", f"{dependency}"]).decode('utf-8')
            except subprocess.CalledProcessError:
                console.print(f"Dependency:[red] {dependency}[/] is not installed.")  
                os.system(f"sudo pacman -S {dependency}")
    def debian_operations():
        dependencies = ["ffmpeg", "v4l2loopback-dkms", "gphoto2"]
        for dependency in dependencies:
            if "not installed." in subprocess.check_output(["dpkg", "-i", f"{dependency}"]).decode('utf-8'):   
                os.system(f"sudo apt-get {dependency}")
            else:
                pass    

    if user_distro == 'arch':
        arch_operations()
    elif user_distro == 'debian':
        debian_operations
    console.print("[red italic]Dependency Checks completed.[/]")
    QMessageBox.about(MainWindow, "Info", "Dependency Checks completed.")

def help():
    QMessageBox.about(MainWindow, "Help", """
-Start Frame Capture: Starts the webcam with frames from your camera.

-Abort Frame Capture: Stops frame capture.

-Install Dependencies: Checks and installs for certain packages required by the program. [Debian / Arch] based only.   

-Please enter your sudo password in the field above the buttons.
---------------------------------------------------------------------------------------------------------------
Made by Kaiser. github.com/kaiserwastaken | kaiserwastaken.org   
    """)

def camera_status():
    if "canon" in str(subprocess.check_output("lsusb")).lower():
        return True
    else:
        return False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(502, 254)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.framecapturebutton = QtWidgets.QPushButton(self.centralwidget)
        self.framecapturebutton.setGeometry(QtCore.QRect(0, 40, 181, 61))
        self.framecapturebutton.setObjectName("framecapturebutton")
        self.abortbutton = QtWidgets.QPushButton(self.centralwidget)
        self.abortbutton.setGeometry(QtCore.QRect(0, 100, 181, 61))
        self.abortbutton.setObjectName("abortbutton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(200, 0, 16, 281))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.helpbutton = QtWidgets.QPushButton(self.centralwidget)
        self.helpbutton.setGeometry(QtCore.QRect(470, 200, 31, 38))
        self.helpbutton.setObjectName("helpbutton")
        self.sudopassword = QtWidgets.QLineEdit(self.centralwidget)
        self.sudopassword.setGeometry(QtCore.QRect(0, 0, 181, 41))
        self.sudopassword.setObjectName("sudopassword")
        self.dependencies = QtWidgets.QPushButton(self.centralwidget)
        self.dependencies.setGeometry(QtCore.QRect(0, 160, 181, 61))
        self.dependencies.setObjectName("dependencies")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.sudopassword.setEchoMode(QtWidgets.QLineEdit.Password)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        def framecapture():
            global captureprocess
            if camera_status() == True:
                def start_capture():
                    global captureprocess
                    if camera_status() == True:

                        sudopass = self.sudopassword.text()
                        print(f"sudopass: {sudopass}")
                        child = pexpect.spawn('sudo modprobe v4l2loopback exclusive_caps=1 max_buffer=2')
                        child.logfile = sys.stdout.buffer
                        child.expect("password")
                        child.sendline(sudopass)

                        os.system('gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec  rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video0')
                captureprocess = multiprocessing.Process(target=start_capture, args=())
                captureprocess.start()
            else:
                QMessageBox.warning(MainWindow, "Warning", "Please make sure your camera is connected and turned on.")
        
        def end_capture():
            global captureprocess
            try:
                os.system("pkill ffmpeg")
                captureprocess.terminate()
            except NameError:
                pass
                
        
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.framecapturebutton.setText(_translate("MainWindow", "Start Frame Capture"))
        self.abortbutton.setText(_translate("MainWindow", "Abort Frame Capture"))
        self.helpbutton.setText(_translate("MainWindow", "?"))
        self.sudopassword.setText(_translate("MainWindow", "pass"))
        self.dependencies.setText(_translate("MainWindow", "Install Dependencies"))
        self.framecapturebutton.clicked.connect(framecapture)
        self.abortbutton.clicked.connect(end_capture)
        self.dependencies.clicked.connect(dependencies)
        self.helpbutton.clicked.connect(help)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setWindowTitle('Canon Driver Utility')
    MainWindow.show()
    sys.exit(app.exec_())
