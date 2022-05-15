import os
from flask import Flask, render_template, flash, redirect, url_for, Markup, request


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

asp_rules = open('asp_rules.lp').read()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result():
    symptoms = ['has_symptom(user, %s).' % s for s in request.form.getlist('symptom')]
    factors = ['existing(user, %s).' % f for f in request.form.getlist('factor')]
    query = '?-should_take(user, X).'

    asp = asp_rules + '\n' + '\n'.join(symptoms + factors + ['person(user).']) + '\n' + query
    open('user.lp', 'w').write(asp)

    output = get_output('user.lp', ['-s1', '--dcc'], 100)
    print (output)
    if 'BINDINGS:' not in output:
        return render_template('result.html', solution='no medicine found')
    
    lines = [l.strip() for l in output.splitlines() if l.strip()]
    i = lines.index('BINDINGS:')
    
    return render_template('result.html', solution='\n'.join(lines[i:]))


app.run()