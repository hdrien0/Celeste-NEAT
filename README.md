# Celeste NEAT

An attempt at making an AI learn to play the game [Celeste](https://store.steampowered.com/app/504230/Celeste/) using [Neuroevolution of Augmenting Topologies (NEAT)](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies), specifically [neat-python](https://neat-python.readthedocs.io/en/latest/).
It uses data fetched directly from the game engine at runtime using [this instrumentation framework](https://github.com/hdrien0/Celeste-Instrumentation).

Thanks to @zteboui for the original idea and the help!

## Overview

Video demo :

[![video demo](https://img.youtube.com/vi/SePBjJ5Z0Lo/0.jpg)](https://www.youtube.com/watch?v=SePBjJ5Z0Lo)


The AI agents are neural networks. They are grouped in generations, and the better-performing agents of each generation are combined and mutated to form the next one. 
At every frame of the game, the agents decide what actions to take based on the following information :
- The distance to the nearest object in 8 directions
- The type of the nearest object for those 8 directions
- Their X and Y velocity
- Their ability to dash
- Their amount of stamina remaining
- The angle to their objective
- The distance to their objective  

The calculation of the agents' performance is based on their distance to their objective (usually the exit of the room) and how fast they reach it.

### Performance

> The NEAT algorithm often arrives at effective networks more quickly than other contemporary neuro-evolutionary techniques and reinforcement learning methods (Wikipedia)  

NEAT can evolve agents that clear simple rooms them in very few generations (~10 generations of 150 agents for the first room). They are even able to do it quite swiftly and to use some advanced movement techniques!  

However, the current simplicity of the agents' input data makes it unviable for levels requiring greater anticipation or complex interactions with the surroundings. With that said, there is still a lot of room for improvement, and other learning techniques such as using Inverse Reinforcement Learning on human gameplay could be well-suited to the task. 


## Installation

- Follow the steps to install the instrumentation part of the project [here](https://github.com/hdrien0/Celeste-Instrumentation#installation).
- Clone this repository and navigate to the repo folder

### Linux / MacOS
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Usage

After launching the instrumented game :
```bash
python celeste_neat.py
```
See `celest_neat_config` for the NEAT parameters.
