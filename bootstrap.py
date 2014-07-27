#!/usr/bin/env python

import sys
import platform
import subprocess
from subprocess import STDOUT
import processes

class InstallationManager():

    def install_easy_install(self):
        processes.stream_run('https://bootstrap.pypa.io/ez_setup.py')


    def match_action_from_description(self, actions):
        for key in actions.keys():
            if key in platform.platform().lower():
                return actions[key]

    def install_curl(self):
        actions = {
              'cygwin': "echo Run cygwin setup.exe (in you downloads directory?) and search for 'curl' in packages."
            , 'darwin': 'brew install curl'
            , 'centos': 'yum install curl'
            , 'redhat': 'yum install curl'
            , 'fedora': 'yum install curl'
            , 'ubuntu': 'apt-get install curl'
        }

        plat_key = sys.platform

        if plat_key in actions.keys():
            action = actions[plat_key]
        else:
            action = self.match_action_from_description(actions)

        if action:
            processes.shell_run(action)
        else:
            print "Couldn't find {key}".format(key=plat_key)

    def execute_install(self, util, script):
        if hasattr(InstallationManager, script):
            exec "self.{fxn}()".format(fxn=script)
        else:
            processes.shell_run(script)
    def pip_install(self, module):
        processes.shell_run("pip install {module}".format(module=module))

    def installed(self, util):
        return processes.shell_run("command -v {util}".format(util=util), suppress=True) == 0

    def install_dependencies(self, util):
        deps = {
              "virtualenv": "pip"
            , "pip": "easy_install"
            , "easy_install": "curl"
        }

        if util in deps.keys():
            self.install(deps[util])

    def install(self, util):
        install_scripts = {
              "pip": "easy_install pip"
            , "virtualenv": "pip install virtualenv"
            , "easy_install": "install_easy_install"
            , "curl": "install_curl"
        }

        if not self.installed(util) and util in install_scripts:
            self.install_dependencies(util)
            self.execute_install(util, install_scripts[util])
        else:
            print util, "is already installed!"

if hasattr(sys, 'real_prefix'):
    print "has venv"
else:
    installer = InstallationManager()
    installer.install("virtualenv")
