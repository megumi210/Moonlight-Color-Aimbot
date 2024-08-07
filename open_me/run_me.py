import warnings
import threading
import sys
import os
import platform
import datetime
import hashlib
import configparser
import time
import json as jsond
import psutil
import traceback
from urllib.parse import urlencode
from keyauth import api
from modules import *
from widgets import *

auth_event = threading.Event()
auth_event.clear()



def create_config1():
    config_path = 'C:\\MoonLightAI\\MoonLightAI-Config.ini'
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.optionxform = str
        config['DEFAULT'] = {
            'radius_hip': 35, 'always_on_aimbot_FOV': 35, 'min_radius_hip': 50, 'max_radius_hip': 50,
            'BaseSpeed_aimbot1': 50, 'ramp_up_speed': 150, 'moonlink_aim': 'False', 'moonlink_aim_smooth': 5.0,
            'moonlink_aim_smooth_2': 5.0, 'moonlink_aim_smooth_y': 5.0, 'moonlink_aim_smooth_y_2': 5.0,
            'max_speed_aimbot': 120, 'some_reference_size': 50, 'fov_reduction_step': 50, 'fov_reset_step': 50,
            'spring_constant': 30, 'dampening_constant': 10, 'max_dist_thresh': 50, 'close_dist_thresh': 10,
            'far_factor': 200, 'close_factor': 100, 'default_factor': 'Legacy', 'aimbot_type': 'Nearest Bone (SIMPLE)',
            'aiming_point_checkbox': 'Debug', 'visual_type': 'UNKNOWN', 'select_monitor_fuser': 20,
            'visual_update_rate': 1, 'lead_correction': 'False', 'aimbot_switch': 'False', 'dynamic_fov_switch': 'False'
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
create_config1()

def create_config2():
    config_path = 'C:\\MoonLightAI\\master-config.ini'
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'config_filename': 'MoonLightAI-Config.ini', 'model_filename': 'Universal_v4_quantized.onnx'}
        with open(config_path, 'w') as configfile:
            config.write(configfile)
create_config2()

os.environ['QT_FONT_DPI'] = '96'
warnings.filterwarnings('ignore', category=DeprecationWarning)
widgets = None

def exit_program():
    auth_thread.join()
    os._exit(0)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global widgets
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        widgets = self.ui
        Settings.ENABLE_CUSTOM_TITLE_BAR = True
        self.setWindowTitle('Moonlight AI')
        self.ui.titleRightInfo.setText(' Universal Object Detector ')
        self.ui.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
        UIFunctions.uiDefinitions(self)
        self.ui.btn_aimbot.clicked.connect(self.buttonClick)
        self.ui.btn_Flickbot.clicked.connect(self.buttonClick)
        self.ui.btn_RCS.clicked.connect(self.buttonClick)
        self.ui.btn_Misc.clicked.connect(self.buttonClick)
        self.show()
        useCustomTheme = False
        themeFile = 'themes\\py_dracula_light.qss'
        if useCustomTheme:
            UIFunctions.theme(self, themeFile, True)
            AppFunctions.setThemeHack(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)
        self.ui.btn_aimbot.setStyleSheet(UIFunctions.selectMenu(self.ui.btn_aimbot.styleSheet()))

    def buttonClick(self):
        btn = self.sender()
        btnName = btn.objectName()
        try:
            if btnName == 'btn_aimbot':
                self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            elif btnName == 'btn_Flickbot':
                self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            elif btnName == 'btn_RCS':
                self.ui.stackedWidget.setCurrentWidget(self.ui.RCS_page)
            elif btnName == 'btn_Misc':
                self.ui.stackedWidget.setCurrentWidget(self.ui.Misc_page)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
        except Exception as e:
            print(e)

    def resizeEvent(self, event):
        UIFunctions.resize_grips(self)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

blacklisted_programs = [
    'Fiddler', 'Wireshark', 'wireshark', 'dumpcap', 'dnSpy', 'dnSpy-x86', 'cheatengine-x86_64', 'HTTPDebuggerUI',
    'Procmon', 'Procmon64', 'Procmon64a', 'ProcessHacker', 'x32dbg', 'x64dbg', 'DotNetDataCollector32', 
    'DotNetDataCollector64', 'Everything', 'Filergabber', 'FileGrab', 'Brocesshacker', 'nigga', 'white', 'm46asp', 
    'CFF Explorer', 'ollydbg', 'ida', 'ida64', 'idag', 'idag64', 'idaw', 'idaw64', 'idaq', 'idaq64', 'idau', 'idau64', 
    'scylla', 'scylla_x64', 'scylla_x86', 'protection_id', 'x64dbg', 'x32dbg', 'windbg', 'reshacker', 'ImportREC', 
    'IMMUNITYDEBUGGER', 'MegaDumper', 'dotPeek32', 'dotPeek64', 'dnSpy', 'dnSpy.Console', 'ILSpy'
]

def get_all_running_processes():
    try:
        processes = [proc.info['name'].lower() for proc in psutil.process_iter(attrs=['name'])]
        return processes
    except Exception as e:
        print(f'Error in get_all_running_processes: {e}')
        return []

class KeyAuthApp:
    def __init__(self, name, ownerid, secret, version):
        self.name = name
        self.ownerid = ownerid
        self.secret = secret
        self.version = version
        self.hash_to_check = self.getchecksum()
        self.api_instance = self.create_api_instance()

    def getchecksum(self):
        md5_hash = hashlib.md5()
        with open(''.join(sys.argv), 'rb') as file:
            md5_hash.update(file.read())
        return md5_hash.hexdigest()

    def create_api_instance(self):
        return api(name=self.name, ownerid=self.ownerid, secret=self.secret, version=self.version, hash_to_check=self.hash_to_check)

    def log(self, message):
        self.api_instance.log(message)



if __name__ == '__main__':
    try:
        lock = threading.Lock()
       
       
       
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('C:/MoonLightAI/icons/images/images/moon.ico'))
        window = MainWindow()
        sys.exit(app.exec())
    except Exception as e:
        print(f'Error: {e}')
        traceback.print_exc()
