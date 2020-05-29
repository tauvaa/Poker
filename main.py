#!/usr/bin/env python3

from Source.game import play

def main():
    play()
if __name__ == '__main__':
    winner = play()
    print(winner)