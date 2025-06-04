# Interface Flask pour contrôler le robot PiDog

from flask import Flask, render_template, jsonify
from threading import Thread
from time import sleep
import datetime

from pidog import Pidog
from preset_actions import pant, body_twisting

# Initialisation du robot PiDog
my_dog = Pidog(head_init_angles=[0, 0, -30])
sleep(1)

def wake_up():
    """Fonction pour réveiller le robot avec une séquence d'animations"""
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

def move_forward():
    """Fonction pour faire avancer le robot"""
    try:
        my_dog.rgb_strip.set_mode('solid', color=[0, 255, 0], brightness=0.6)
        my_dog.do_action('forward', step_count=3, speed=60)
        my_dog.wait_all_done()
        my_dog.do_action('sit', speed=50)
        my_dog.rgb_strip.set_mode('breath', color=[255, 192, 203], bps=0.5)
    except Exception as e:
        print(f"Erreur lors de l'avancement: {e}")

def move_backward():
    """Fonction pour faire reculer le robot"""
    try:
        my_dog.rgb_strip.set_mode('solid', color=[255, 0, 0], brightness=0.6)
        my_dog.do_action('backward', step_count=3, speed=60)
        my_dog.wait_all_done()
        my_dog.do_action('sit', speed=50)
        my_dog.rgb_strip.set_mode('breath', color=[255, 192, 203], bps=0.5)
    except Exception as e:
        print(f"Erreur lors du recul: {e}")

def tourner_gauche():
    """Fonction pour faire tourner le robot à gauche"""
    try:
        my_dog.rgb_strip.set_mode('solid', color=[0, 0, 255], brightness=0.6)
        my_dog.do_action('turn_left', step_count=2, speed=60)
        my_dog.wait_all_done()
        my_dog.do_action('sit', speed=50)
        my_dog.rgb_strip.set_mode('breath', color=[255, 192, 203], bps=0.5)
    except Exception as e:
        print(f"Erreur lors du virage à gauche: {e}")

def tourner_droite():
    """Fonction pour faire tourner le robot à droite"""
    try:
        my_dog.rgb_strip.set_mode('solid', color=[255, 165, 0], brightness=0.6)
        my_dog.do_action('turn_right', step_count=2, speed=60)
        my_dog.wait_all_done()
        my_dog.do_action('sit', speed=50)
        my_dog.rgb_strip.set_mode('breath', color=[255, 192, 203], bps=0.5)
    except Exception as e:
        print(f"Erreur lors du virage à droite: {e}")

def arreter():
    """Fonction pour arrêter le robot en le laissant debout"""
    try:
        my_dog.do_action('stand', speed=80)
        my_dog.head_move([[0, 0, -30]], speed=80)
        my_dog.rgb_strip.set_mode('breath', color=[255, 192, 203], bps=0.5)
        my_dog.wait_all_done()
    except Exception as e:
        print(f"Erreur lors de l'arrêt: {e}")

# Initialisation de l'application Flask
app = Flask(__name__)

@app.route('/')
def index():
    """Page d'accueil avec l'interface de contrôle"""
    return render_template('index.html')

@app.route('/reveiller')
def route_reveiller():
    """Route pour réveiller le robot"""
    try:
        thread = Thread(target=wake_up)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'success', 'message': 'Robot éveillé'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

@app.route('/avancer')
def route_avancer():
    """Route pour faire avancer le robot"""
    try:
        thread = Thread(target=move_forward)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'success', 'message': 'Robot avance'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

@app.route('/reculer')
def route_reculer():
    """Route pour faire reculer le robot"""
    try:
        thread = Thread(target=move_backward)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'success', 'message': 'Robot recule'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

@app.route('/gauche')
def route_gauche():
    """Route pour faire tourner le robot à gauche"""
    try:
        thread = Thread(target=tourner_gauche)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'success', 'message': 'Robot tourne à gauche'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

@app.route('/droite')
def route_droite():
    """Route pour faire tourner le robot à droite"""
    try:
        thread = Thread(target=tourner_droite)
        thread.daemon = True
        thread.start()
        return jsonify({'status': 'success', 'message': 'Robot tourne à droite'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erreur: {str(e)}'})

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

# Routes supplémentaires pour compatibilité avec différentes interfaces
@app.route('/forward')
def route_forward():
    """Route alternative pour avancer (compatibilité)"""
    return route_avancer()

@app.route('/backward')
def route_backward():
    """Route alternative pour reculer (compatibilité)"""
    return route_reculer()

@app.route('/left')
def route_left():
    """Route alternative pour tourner à gauche (compatibilité)"""
    return route_gauche()

@app.route('/right')
def route_right():
    """Route alternative pour tourner à droite (compatibilité)"""
    return route_droite()
    """Route pour obtenir le statut du robot"""
    try:
        return jsonify({
            'status': 'success',
            'robot_connected': True,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'robot_connected': False,
            'message': f'Erreur: {str(e)}'
        })

# Fonction de nettoyage à la fermeture
def cleanup():
    """Ferme proprement la connexion avec le robot"""
    try:
        my_dog.close()
        print("Connexion PiDog fermée proprement")
    except Exception as e:
        print(f"Erreur lors de la fermeture: {e}")

if __name__ == '__main__':
    try:
        print("Démarrage du serveur Flask pour PiDog...")
        print("Interface accessible sur http://localhost:8080")
        app.run(host='0.0.0.0', port=8080, debug=False)
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    finally:
        cleanup()