#!/usr/bin/env python

import sys, os
import subprocess
from subprocess import PIPE, STDOUT

class InstallationManager():
    devnull = open(os.devnull, 'w')
    
        
    def curl_stream(self, url):
        try:
            return subprocess.Popen("curl {url}".format(url=url), shell=True, stdout=PIPE)
        except:
            print "failed to curl {url}".format(url=url)
        
        
    def run_from_stream(self, script_stream):
        try:
            install_process = subprocess.Popen("python", shell=True, stdin=script_stream.stdout)
        except:
            print "failed to execute stream"
            
    def pip_install(self, moduel):
        try:
            subprocess.check_call("pip install {module}".format(module=module), shell=True)
        except:
            print "failed to install {module}".format(module=module)

    def installed(self, util):
        try:
            subprocess.check_call("command -v {util}".format(util=util)
                , shell=True
                , stdout=self.devnull
                , stderr=STDOUT
            )
        except:
            return False
        return True
    
    def install_dependencies(self, util):
        dependencies = {
            "virtualenv": ["pip"]
        }
        
        if util in dependencies.keys():
            for dep in dependencies[util]:
                self.install(dep)
        
    def install_pip(self):
        print "installing pip"
        self.run_from_stream(self.curl_stream("https://bootstrap.pypa.io/get-pip.py"))
        
    def install_virtualenv(self):
        print "installing virtualenv"
        subprocess.check_call("pip install virtualenv", shell=True)
        
    def install(self, util):
        install_scripts = {
              "pip": "self.install_pip()"
            , "virtualenv": "self.install_virtualenv()"
        }
        
        if self.installed(util):
            print util + " is already installed"
        else:
            print "installing " + util
            self.install_dependencies(util)
            if util in install_scripts:
                exec install_scripts[util]  
            else:
                print util + " is not currently supported for installing"

    
def necessary(check_fxn):
    print 
    return True

if hasattr(sys, 'real_prefix'):
    print "has venv"
else:
    installer = InstallationManager()
    #installer.install("virtualenv")
    
