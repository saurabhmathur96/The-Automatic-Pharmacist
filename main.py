from subprocess import TimeoutExpired, CalledProcessError
from subprocess import check_output
import subprocess


def get_output(script_path, args, seconds):
  '''
    executes a python script and returns the contents of STDOUT
    
    Arguments:
      script_path (str)
      args (list)
      seconds (int)
    
    Throws:
      TimeoutExpired
      CalledProcessError
      UnicodeEncodeError
  '''
  output = check_output(['scasp', script_path, *args],  timeout=seconds, stderr=subprocess.STDOUT)
  return output.decode('utf8')
