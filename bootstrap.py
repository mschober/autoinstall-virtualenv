#!/usr/bin/env python

import sys
import subprocess
from subprocess import STDOUT
import processes

class InstallationManager():

    def install_easy_install(self):
        processes.stream_run('https://bootstrap.pypa.io/ez_setup.py')

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
        }

        if util in deps.keys():
            self.install(deps[util])

    def install(self, util):
        install_scripts = {
              "pip": "easy_install pip"
            , "virtualenv": "pip install virtualenv"
            , "easy_install": "install_easy_install"
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
