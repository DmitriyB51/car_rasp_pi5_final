
from flask import Flask, render_template, request, redirect
from motor_control import forward, backward, left, right, stop
import threading
from line_follower import line_follower, stop as line_stop
import time

app = Flask(__name__)


current_mode = 'remote'
line_thread = None
line_active = False


@app.route('/')
def index():
    return render_template('index.html', mode=current_mode)

@app.route('/mode', methods=['POST'])
def switch_mode():
    global current_mode, line_thread, line_active

    if current_mode == 'remote':
        current_mode = 'line'
        line_active = True
        line_thread = threading.Thread(target=start_line_follower)
        line_thread.start()
    else:
        current_mode = 'remote'
        line_active = False
        line_stop()

    return redirect('/')


def is_active():
    return line_active

def start_line_follower():
    line_follower(is_active)

@app.route('/move', methods=['POST'])
def move():
    if current_mode != 'remote':
        return '', 204

    direction = request.form['direction']
    if direction == 'forward':
        forward()
    elif direction == 'backward':
        backward()
    elif direction == 'left':
        left()
    elif direction == 'right':
        right()
    elif direction == 'stop':
        stop()
    return '', 204




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
from flask import Flask, render_template, request, redirect
from motor_control import forward, backward, left, right, stop

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    direction = request.form['direction']
    if direction == 'forward':
        forward()
    elif direction == 'backward':
        backward()
    elif direction == 'left':
        left()
    elif direction == 'right':
        right()
    elif direction == 'stop':
        stop()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
"""
