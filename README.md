# Smart Traffic Management System using Socket Programming

A real-time traffic signal simulation developed using Python, Tkinter, and TCP socket programming. The project demonstrates how intelligent traffic management systems can dynamically control traffic signals based on vehicle density while prioritizing emergency vehicles such as ambulances.

## Overview

This project simulates a traffic control environment where vehicle information is transmitted from a sensor-side client to a traffic control server through socket communication. Based on the received traffic conditions, the server determines the optimal signal state and sends instructions back to the simulation.

The system also implements emergency vehicle prioritization, ensuring ambulances receive immediate right-of-way by automatically switching the signal to green.

## Features

* Real-time vehicle movement simulation
* Dynamic traffic signal control
* Vehicle density monitoring
* Ambulance detection and signal override
* TCP socket-based client-server communication
* Pedestrian crossing simulation
* Collision avoidance logic
* Interactive GUI built with Tkinter

## Technologies Used

* Python
* Tkinter
* Socket Programming (TCP)
* Multithreading
* Object-Oriented Programming

## System Architecture

```text
Client (Traffic Sensor Simulation)
              │
              ▼
TCP Socket Communication
              │
              ▼
Server (Traffic Control Logic)
              │
              ▼
Traffic Signal Decision
              │
              ▼
GUI Traffic Simulation
```

## How It Works

1. Vehicles are generated continuously on the road.
2. The client monitors traffic density near the signal.
3. Vehicle count and ambulance presence are transmitted to the server.
4. The server evaluates traffic conditions and determines whether the signal should be red or green.
5. Ambulances receive immediate signal priority.
6. The GUI updates in real time to reflect traffic flow and signal changes.

## How to Run

### Start the Server
```bash
python server.py
```
### Start the Client
Open a second terminal and run:

```bash
python client.py
```
