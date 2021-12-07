# ai-battleship-player

# An AI Battleship Player

**AJ Rivera**

## OVERVIEW

I would like to assemble a group of people interested in building an artificially intelligent Battleship player trained using Deep Reinforcement Learning (RL). The motivation comes from a desire to observe how an AI player develops strategies that a human could form on its own. For example, it is common for humants to "fire" shots near previous hits of an floating ship. It would be interesting to see if the AI player can "learn" this. I would like to develop the player from end-to-end, as a team. Check out the tasks section to see what are the things I will be doing.

## GOALS

To create an AI Battleship Player

## NOTIONAL PLAN

The approach will be to use a Deep Neural Network (DNN) and train it using a reinforcement learning. To be able to train the DNN, we first need to identify an existing Battleship game engine or build our own. This will allow us to write scripts that run the game.

Reinforcement learning is all about the agent (the DNN) interacting with the environment (the game) in a way that some reward (hit/miss/win) is maximized. During the first part, the DNN will be trained to devise the best strategy to attack and sink all the ships with the fewest number of shots possible. During the second part, the DNN will be trained to devise the best strategy to defend its ships. The only strategy involved in defending the ships is their placement at the beginning of the game. This defender can be trained using our attacker by playing them against each other, similar to what the Google folks did with AlphaGo.

Some decisions will be made along the way, for example, the reinforcement learning algorithm to use, the NN architecture to use. We anticipate different persons contributing to different areas. If you are a CS, CE, or EE student,  being part of this will definitely be valuable in the future, whether you decide to work for yourself, a startup, a small team, or a big firm.

A timeline has not been established yet, but it would be nice to reach Milestone B1 before Christmas 2017.

## MILESTONES

Board size is 10x10 squares.

A1. An attacking player that can sink a fleet in less than 80 shots on average after playing 1,000 games.

A2. An attacking player that can sink a fleet in less than 60 shots on average after playing 1,000 games.

A3. An attacking player that can sink a fleet in less than 40 shots on average after playing 1,000 games.

B1. A defender that wins against a random-strategy player.

B1. A defender that wins against a search &amp; hunt-strategy player. Search and hunt means that upon a hit, the attacker focused on adjacent squares.

## TOOLS &amp; PROGRAMMING LANGUAGES WE WILL MOST LIKELY USE

- Python (to code the game)
- Google Tensor Flow (for the Neural Network)
- Everything will be hosted on github - public repo (don&#39;t know which license yet)

## TASKS IDENTIFIED SO FAR

1. Identify or build our own Python-based Battleship player.
2. Identify reinforcement training algorithm.
3. Identify DNN architecture.
4. Develop API for Battleship game.
5. Develop interface for the DNN to play using the game&#39;s API.
6. Develop attacker.
7. Develop defender.
8. Develop web application so that people can play against it.

_If you are interested, send me an email at aj.rivera@jhu.edu_
