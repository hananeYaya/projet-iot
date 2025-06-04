# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask
import datetime
#from flask import Flask, render_template

from flask import Flask, render_template, jsonify
#from moteur import avancer, reculer, tourner_gauche, tourner_droite, arreter

from pidog import Pidog
from time import sleep
from preset_actions import pant
from preset_actions import body_twisting

from flask import Flask, render_template, jsonify
from threading import Thread

my_dog = Pidog(head_init_angles=[0, 0, -30])
sleep(1)


def wake_up():
    # stretch
    my_dog.rgb_strip.set_mode('listen', color='yellow', bps=0.6, brightness=0.8)
    my_dog.do_action('stretch', speed=50)
    my_dog.head_move([[0, 0, 30]]*2, immediately=True)
    my_dog.wait_all_done()
    sleep(0.2)
    body_twisting(my_dog)
    my_dog.wait_all_done()
    sleep(0.5)
    my_dog.head_move([[0, 0, -30]], immediately=True, speed=90)
    # sit and wag_tail
    my_dog.do_action('sit', speed=25)
    my_dog.wait_legs_done()
    my_dog.do_action('wag_tail', step_count=10, speed=100)
    my_dog.rgb_strip.set_mode('breath', color=[245, 10, 10], bps=2.5, brightness=0.8)
    pant(my_dog, pitch_comp=-30, volume=80)
    my_dog.wait_all_done()
    # hold
    my_dog.do_action('wag_tail', step_count=10, speed=30)
    my_dog.rgb_strip.set_mode('breath', 'pink', bps=0.5)
#    while True:
#        sleep(1)
# Define actions
actions = [
    ['stand', 0, 50],
    ['sit', -30, 50],
    ['lie', 0, 20],
    ['lie_with_hands_out', 0, 20],
    ['trot', 0, 95],
    ['forward', 0, 98],
    ['backward', 0, 98],
    ['turn_left', 0, 98],
    ['turn_right', 0, 98],
    ['doze_off', -30, 90],
    ['stretch', 20, 20],
    ['push_up', -30, 50],
    ['shake_head', -1, 90],
    ['tilting_head', -1, 60],
    ['wag_tail', -1, 100],
]

actions_len = len(actions)
STANDUP_ACTIONS = ['trot', 'forward', 'backward', 'turn_left', 'turn_right']

# Load sound effects
sound_effects = []
sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './sounds'))
os.chdir(sound_path)
for name in os.listdir(sound_path):
    sound_effects.append(name.split('.')[0])
sound_effects.sort()

sound_len = min(len(sound_effects), actions_len)
sound_effects = sound_effects[:sound_len]

# Globals
last_index = 0
last_head_pitch = 0


def do_function(index):
    global last_index, last_head_pitch
    my_dog.body_stop()

    if index < 0:
        return "Invalid action index", 400

    if index < actions_len:
        name, head_pitch_adjust, speed = actions[index]

        if last_index < len(actions) and actions[last_index][0] == 'push_up':
            last_head_pitch = 0
            my_dog.do_action('lie', speed=60)

        if name in STANDUP_ACTIONS and (last_index >= len(actions) or actions[last_index][0] not in STANDUP_ACTIONS):
            last_head_pitch = 0
            my_dog.do_action('stand', speed=60)

        if head_pitch_adjust != -1:
            last_head_pitch = head_pitch_adjust

        my_dog.head_move_raw([[0, 0, last_head_pitch]], immediately=False, speed=60)
        my_dog.do_action(name, step_count=10, speed=speed, pitch_comp=last_head_pitch)
        last_index = index
        return f"Action '{name}' executed.", 200

    elif index < actions_len + sound_len:
        sound_name = sound_effects[index - actions_len]
        my_dog.speak(sound_name, volume=80)
        last_index = index
        return f"Sound '{sound_name}' played.", 200
    else:
        return "Index out of range", 400




app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reveiller')
def route_reveiller():
    #wake_up()
    thread = Thread(target=wake_up)
    thread.start()
    return jsonify({'status': 'Robot éveillé'})

@app.route('/avancer')
def route_avancer():
    do_function(index)
    #avancer()
    thread = Thread(target=move_forward)
    thread.start()
    return jsonify({'status': 'Robot avance'})

@app.route('/reculer')
def route_reculer():
    #reculer()
    thread = Thread(target=move_backward)
    thread.start()
    return jsonify({'status': 'Robot recule'})

@app.route('/gauche')
def route_gauche():
    #tourner_gauche()
    thread = Thread(target=tourner_gauche)
    thread.start()
    return jsonify({'status': 'Robot tourne à gauche'})

@app.route('/droite')
def route_droite():
    thread = Thread(target=tourner_droite)
    thread.start()
    #tourner_droite()
    return jsonify({'status': 'Robot tourne à droite'})

@app.route('/stop')
def route_stop():
    #arreter()
    return jsonify({'status': 'Robot arrêté'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
