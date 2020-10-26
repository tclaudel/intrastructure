#!/usr/bin/env python3

import os
import sys
import subprocess

stage = 0
DEBUG = False
DEVNULL = subprocess.DEVNULL = open(os.devnull, 'wb')
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
VAGRANT_JENKINS_IP = "192.168.5.2"


def sys_exec(command, opt=1):
    command = command.split(' ')
    if DEBUG:
        print(command)
    if opt == 2:
        p = subprocess.run(command, stdout=DEVNULL)
    else:
        p = subprocess.run(command)
    if DEBUG:
        print(p.returncode)
    if p.returncode != 0:
        print("An Error Occured, Exiting ...")
        exit(1)
    return p


def display_stage(fct):
    """This will log the script"""

    def logging_function():
        global stage
        print("[{}] {}".format(stage, fct.__name__.translate(str.maketrans('_', ' '))))
        stage += 1
        return fct()

    return logging_function


def check_and_install(check, install):
    global stage
    check_command = check.split(' ')
    if subprocess.run(check_command, stdout=DEVNULL).returncode != 0:
        install_command = install.split(' ')
        print("[{}] install {}".format(stage, check_command[0]))
        stage += 1
        subprocess.run(install_command)
    print("{:20} [OK]".format(check_command[0]))


@display_stage
def lunch_vagrant_jenkins():
    os.chdir(BASE_FOLDER + "/Vagrant")
    input = open("./Vagrantfile_template")
    output = open("./Vagrantfile", 'w')
    subprocess.run(["sed", "s/VAGRANT_JENKINS_IP/"+VAGRANT_JENKINS_IP+"/g"], stdin=input, stdout=output)
    sys_exec("sudo vagrant up p1jenkins-pipeline")


def reset():
    os.chdir(BASE_FOLDER + "/Vagrant")
    sys_exec("sudo vagrant destroy -f")
    print("CLUSTER RESETED")
    exit(0)

def main():
    if "-r" in sys.argv:
        reset()
    DEBUG = "-d" in sys.argv
    if DEBUG:
        sys.argv.remove("-d")
    check_and_install("virtualbox -h", "sudo apt-get install virtualbox")
    check_and_install("vagrant -h", "sudo apt-get install vagrant")
    lunch_vagrant_jenkins()
    jenkins_pwd = subprocess.run(["sudo", "vagrant", "ssh", "p1jenkins-pipeline", "-c sudo cat /var/lib/jenkins/secrets/initialAdminPassword"], capture_output=True)
    if jenkins_pwd.returncode != 0:
        print("An Error Occured, Exiting ...")
        exit(1)
    jenkins_pwd = jenkins_pwd.stdout.decode("utf-8").rstrip()
    print(jenkins_pwd)

if __name__ == "__main__":
    main()
