import subprocess
from subprocess import PIPE


def curl_stream(url):
    try:
        return subprocess.Popen("curl {url}".format(url=url), shell=True, stdout=PIPE)
    except subprocess.CalledProcessError, e:
        print "failed to curl {url}".format(url=url), e.output

def stream_run(url):
    run_from_stream(curl_stream(url))


def run_from_stream(script_stream):
    try:
        install_process = subprocess.Popen("python", shell=True, stdin=script_stream.stdout)
    except subprocess.CalledProcessError, e:
        print "failed to execute stream", e.output

