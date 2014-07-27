import subprocess, os
from subprocess import PIPE, STDOUT

devnull = open(os.devnull, 'w')

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


def shell_run(script_string, err_msg="Failed to execute cmd:", suppress=False):
    args = { 'shell': True }
    supress_args = { 'stdout': devnull, 'stderr': STDOUT }

    if suppress:
        args.update(supress_args)

    try:
        return subprocess.check_call(script_string, **args)
    except subprocess.CalledProcessError, e:
        print """
{err_msg}
{header}
{cmd}
{header}
""".format(err_msg=err_msg, header=50*"#", cmd=script_string)
