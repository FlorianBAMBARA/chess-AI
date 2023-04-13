import pygame as p
import os

width,height=760,760
dimension=8 # this game is a 8x8 game 

square_size=height//8

FPS=60
Images={}


'''
initialize a global dictionary of images wich will called exactly once in the main file
'''
Path = os.path.join(os.getcwd(), "Chess/Images/")

def load_images():
    pieces=['wKN','wQ','wR','wK','wP','wB','bP','bKN','bK','bQ','bR','bB']
    for piece in pieces: 
        dir = os.path.join(Path, piece + ".png")
        Images[piece]=p.transform.scale(p.image.load(dir),(square_size,square_size))
    return Images