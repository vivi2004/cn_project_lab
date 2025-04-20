Multiplayer Fighting Game - README
Overview

This is a 2D multiplayer fighting game built using Python's Pygame library with UDP networking for real-time gameplay over a local network. The game follows a client-server architecture where the server manages the game state and synchronizes actions between two players.
Features

    Real-time 2D fighting gameplay

    Local network multiplayer support

    Basic fighting mechanics (movement, jumping, attacking)

    Health tracking and visual health bars

    Client-server architecture with UDP communication

Technologies Used

    Python 3: Core programming language

    Pygame: For game rendering and input handling

    UDP Sockets: For network communication

    Pickle: For data serialization

Architecture

Client 1 (Player 1)  ← UDP →  Server  ← UDP →  Client 2 (Player 2)
       (Rendering)         (Game State Management)       (Rendering)
       (Input Handling)                                 (Input Handling)

Installation

    Ensure you have Python 3.x installed

    Install required dependencies:
    bash

    pip install pygame

How to Run

    Start the Server:
    bash

python server.py

Start Client 1 (Player 1):
bash

python client.py

Start Client 2 (Player 2) on another machine (or same machine with different port):
bash

    python client.py

Controls

    Player 1:

        Move: W, A, S, D

        Attack: Space

        Guard: Shift

    Player 2:

        Move: Arrow Keys

        Attack: Enter

        Guard: Right Shift

Network Configuration

    Default server port: 9999 (UDP)

    Clients should be configured to connect to the server's IP address

    For local testing, use 127.0.0.1 as the server address

Game Mechanics

    Each player starts with 100 health

    Attacks reduce opponent's health

    Guarding reduces damage taken

    The player who reduces opponent's health to 0 first wins

Future Improvements

    Add character selection

    Implement special moves and combos

    Add sound effects and music

    Improve netcode for better synchronization

    Add matchmaking system

Troubleshooting

    If connection fails, check firewall settings

    Ensure all machines are on the same local network

    Verify server IP address configuration in clients
