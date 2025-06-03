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
    while True:
        sleep(1)

def move_forward():
    # Étape 1 : le robot se lève (se met debout)
    stand_angles = [40, 15, -40, -15, 60, 5, -60, -5]
    my_dog.legs_move([stand_angles], speed=80)
    my_dog.wait_all_done()

    # Étape 2 : faire un pas en avant (alternance de jambes)
    step_1 = [-30, 60, -20, -60, 80, -45, -80, 45]
    step_2 = [-40, 50, -30, -50, 70, -40, -70, 40]

    my_dog.legs_move([step_1], speed=85)
    my_dog.wait_all_done()

    my_dog.legs_move([step_2], speed=85)
    my_dog.wait_all_done()

    # Étape 3 : revenir en position debout
    stand_angles = [40, 15, -40, -15, 60, 5, -60, -5]
    my_dog.legs_move([stand_angles], speed=80)
    my_dog.wait_all_done()

def move_backward():
    # Étape 1 : se mettre debout
    stand_angles = [40, 15, -40, -15, 60, 5, -60, -5]
    my_dog.legs_move([stand_angles], speed=80)
    my_dog.wait_all_done()

    # Étape 2 : faire un pas en arrière
    step_1 = [-50, 40, -50, -30, 60, -30, -60, 30]
    step_2 = [-40, 60, -30, -60, 80, -45, -80, 45]

    my_dog.legs_move([step_1], speed=85)
    my_dog.wait_all_done()

    my_dog.legs_move([step_2], speed=85)
    my_dog.wait_all_done()

    # Étape 3 : revenir en position debout
    my_dog.legs_move([stand_angles], speed=80)
    my_dog.wait_all_done()

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reveiller')
def route_reveiller():
    wake_up()
    return jsonify({'status': 'Robot avance'})

@app.route('/avancer')
def route_avancer():
    move_forward()
    return jsonify({'status': 'Robot avance'})

@app.route('/reculer')
def route_reculer():
    move_backward()
    return jsonify({'status': 'Robot recule'})

@app.route('/gauche')
def route_gauche():
    #tourner_gauche()
    return jsonify({'status': 'Robot tourne à gauche'})

@app.route('/droite')
def route_droite():
    #tourner_droite()
    return jsonify({'status': 'Robot tourne à droite'})

@app.route('/stop')
def route_stop():
    #arreter()
    return jsonify({'status': 'Robot arrêté'})

#@app.route('/')
#def index():
#    return render_template('index.html')
    #return 'Web App with Python Flask!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
