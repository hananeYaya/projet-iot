import RPi.GPIO as GPIO
import time

# Définir les broches utilisées
BROCHE_G_AV = 17
BROCHE_G_AR = 18
BROCHE_D_AV = 22
BROCHE_D_AR = 23

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BROCHE_G_AV, GPIO.OUT)
GPIO.setup(BROCHE_G_AR, GPIO.OUT)
GPIO.setup(BROCHE_D_AV, GPIO.OUT)
GPIO.setup(BROCHE_D_AR, GPIO.OUT)

def avancer():
    GPIO.output(BROCHE_G_AV, True)
    GPIO.output(BROCHE_G_AR, False)
    GPIO.output(BROCHE_D_AV, True)
    GPIO.output(BROCHE_D_AR, False)

def reculer():
    GPIO.output(BROCHE_G_AV, False)
    GPIO.output(BROCHE_G_AR, True)
    GPIO.output(BROCHE_D_AV, False)
    GPIO.output(BROCHE_D_AR, True)

def tourner_gauche():
    GPIO.output(BROCHE_G_AV, False)
    GPIO.output(BROCHE_G_AR, True)
    GPIO.output(BROCHE_D_AV, True)
    GPIO.output(BROCHE_D_AR, False)

def tourner_droite():
    GPIO.output(BROCHE_G_AV, True)
    GPIO.output(BROCHE_G_AR, False)
    GPIO.output(BROCHE_D_AV, False)
    GPIO.output(BROCHE_D_AR, True)

def arreter():
    GPIO.output(BROCHE_G_AV, False)
    GPIO.output(BROCHE_G_AR, False)
    GPIO.output(BROCHE_D_AV, False)
    GPIO.output(BROCHE_D_AR, False)
