#!/usr/bin/env python

import sys
import subprocess
from subprocess import STDOUT
import processes

class InstallationManager():

    def pip_install(self, module):
        processes.shell_run("pis install {module}".format(module=module))

    def installed(self, util):
        shell_run("command -v {util}".format(util=util), supress=True)
        try:
            subprocess.check_call("command -v {util}".format(util=util)
                , shell=True
                , stdout=self.devnull
                , stderr=STDOUT
            )
        except subprocess.CalledProcessError, e:
            return False
        return True

    def install_dependencies(self, util):
        deps = {
              "virtualenv": "pip"
            , "pip": "easy_install"
        }

        if util in deps.keys():
            self.install(deps[util])

    def install_easy_install(self):
        processes.stream_run('https://bootstrap.pypa.io/ez_setup.py')

    def install(self, util):
        install_scripts = {
              "pip": "easy_install pip"
            , "virtualenv": "pip install virtualenv"
            , "easy_install": "install_easy_install"
        }

        if self.installed(util):
            print util + " is already installed"
        else:
            print "installing " + util
            self.install_dependencies(util)
            if util in install_scripts:
                if hasattr(InstallationManager, install_scripts[util]):
                    print 'yup'
                    exec "self.{fxn}()".format(fxn=install_scripts[util])
                else:
                    try:
                        subprocess.check_output(install_scripts[util], shell=True)
                    except subprocess.CalledProcessError, e:
                        print "failed to run installer script", e.output
            else:
                print util + " is not currently supported for installing"

if hasattr(sys, 'real_prefix'):
    print "has venv"
else:
    installer = InstallationManager()
    installer.install("virtualenv")
