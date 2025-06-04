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

def move_forward():
    pass

def move_backward():
    pass

def tourner_gauche():
    pass

def tourner_droite():
    pass

def arreter():
    """Fonction pour arrêter le robot en le laissant debout"""
    try:
        my_dog.do_action('stand', speed=80)
        my_dog.head_move([[0, 0, -30]], speed=80)
        my_dog.rgb_strip.set_mode('breath', color=[255, 192, 203], bps=0.5)
        my_dog.wait_all_done()
    except Exception as e:
        print(f"Erreur lors de l'arrêt: {e}")

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
    """Route pour arrêter le robot"""
    try:
        thread = Thread(target=arreter)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'success', 'message': 'Robot arrêté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
