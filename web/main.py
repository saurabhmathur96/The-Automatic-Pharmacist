import os
from flask import Flask, render_template, flash, redirect, url_for, Markup, request


from subprocess import TimeoutExpired, CalledProcessError
from subprocess import check_output
import subprocess

from yaml import parse


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

def parse_output(output, query='?- should_take(user,X).'):
    output = output.replace('NOTE: DCC activates the use of the --prev_forall implementation\n%% QUERY:%s' % query, '')
    
    chunks = output.strip().split('\n\n\n')
    for chunk in chunks:
        #print (repr(chunk))
        parts = chunk.split('\n\n')
        #print (parts[0].strip())
        assert parts[0].strip().startswith('ANSWER')
        _, model = parts[1].split('\n')
        _, *bindings = parts[2].split('\n')

        yield dict(model=model, bindings='\n'.join(bindings))
        

asp_rules = open('asp_rules.lp').read()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=["POST"])
def result():

    symptoms = ['has_symptom(user, %s).' % s for s in request.form.getlist('symptom')]
    factors = ['existing(user, %s).' % f for f in request.form.getlist('factor')]
    query = '?- has_ailment(user,Ailment).'

    asp = asp_rules + '\n' + '\n'.join(symptoms + factors + ['person(user).']) + '\n' + query
    open('user.lp', 'w').write(asp)
    output = get_output('user.lp', ['-s0', '--dcc'], 100)
    
    if 'BINDINGS:' not in output:
        ailment = 'unable to diagnose AILMENT.'
    else:
        bindings = list(set([row['bindings'] for row in parse_output(output, query)]))
        lines = ['\nAnswer %s:\n%s' % (i, b) for i, b in enumerate(bindings, start=1)]
        ailment = 'AILMENT(S) diagnosed:\n' + '\n'.join(lines)
    
    query = '?- has_symptom(user,Symptom),treats(Medicine,Symptom),existing(user,Existing),adverse_interaction(Medicine,Existing).'
    asp = asp_rules + '\n' + '\n'.join(symptoms + factors + ['person(user).']) + '\n' + query
    open('user.lp', 'w').write(asp)
    output = get_output('user.lp', ['-s0', '--dcc'], 500)
    if 'BINDINGS:' not in output:
        conflicts = '\n\nno CONFLICT(S) found'
    else:
        bindings = list(set([row['bindings'] for row in parse_output(output, query)]))
        lines = ['\nAnswer %s:\n%s' % (i, b) for i, b in enumerate(bindings, start=1)]
        conflicts = '\n\nCONFLICT(S):' + '\n'.join(lines)


    symptoms = ['has_symptom(user, %s).' % s for s in request.form.getlist('symptom')]
    factors = ['existing(user, %s).' % f for f in request.form.getlist('factor')]
    query = '?- should_take(user,Medicine).'

    asp = asp_rules + '\n' + '\n'.join(symptoms + factors + ['person(user).']) + '\n' + query
    open('user.lp', 'w').write(asp)

    output = get_output('user.lp', ['-s0', '--dcc'], 100)
    if 'BINDINGS:' not in output:
        #query = '?- has_symptom(user,Symptom),treats(Medicine,Symptom),existing(user,Existing),adverse_interaction(Medicine,Existing).'
        #asp = asp_rules + '\n' + '\n'.join(symptoms + factors + ['person(user).']) + '\n' + query
        #open('user.lp', 'w').write(asp)
        #output = get_output('user.lp', ['-s0', '--dcc'], 500)
        #bindings = list(set([row['bindings'] for row in parse_output(output, query)]))
        #lines = ['\nANSWER %s:\n%s' % (i, b) for i, b in enumerate(bindings, start=1)]
        
        return render_template('result.html', solution=ailment + '\n\nno MEDICINE(S) found.\n' + conflicts)
    
    #lines = [l.strip() for l in output.splitlines() if l.strip()]
    #i = lines.index('BINDINGS:')

    


    bindings = list(set([row['bindings'] for row in parse_output(output, query)]))
    lines = ['\nAnswer %s:\n%s' % (i, b) for i, b in enumerate(bindings, start=1)]
    medicine = '\n\nMEDICINE(S) found:\n' + '\n'.join(lines)
    line = '\n' + '-'*15 + '\n'
    return render_template('result.html', solution=line.join([ailment, medicine, conflicts]))


app.run()