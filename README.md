# DungeonLLMaster

![](dungeonllmaster_logo.jpeg)

## Introduction
Are you a Dungeon Master (DM) of a tabletop RPG game? You wanted some inspiration for your next session? Or maybe you are tired of improvising everything because your players are going off the rails?
Or maybe you are a new DM and you don't know how to properly plan a session? Or maybe you hadn't the time to plan the session and you need to improvise everything?
This is the solution for you! DungeonLLMaster is a tool that helps you to create a session plan for your RPG game.
You can create dungeons, quests, cities, villages, NPCs, monsters, and much more!

## Features

### Dungeon creation
  - Detailed description of the lore of the dungeon
  - Detailed description of each room
  - Monsters placement and boss creation
  - Traps placement
  - Loot placement
  - Puzzle creation
  - NPC placement
  - Advanced spacial layout of the dungeon
  - Dungeon map generation (using ASCII art)
  - 3D dungeon map visualization (coming soon)
### Quest creation
  - Detailed description of the lore of the quest
  - Quest objectives
  - Quest rewards
  - Quest NPCs
  - Quest monsters
  - Quest locations
### Urban agglomerate creation
  - Detailed description of the lore of the city/village
  - Detailed description of each location
  - NPCs placement
  - Quests placement
  - Shops placement
  - Taverns placement
  - Inns placement
  - Temples placement
  - Guilds placement
  - Urban map generation (using ASCII art)
  - 3D urban map visualization (coming soon)

### General usage
- Generative AI support for tasks not covered by the main submodules, like generating new lore, names, etc.

## Installation

### Requirements
- Python 3.9 or higher
- pip
- virtualenv (optional)
- git
- Docker
- OpenAI API key

### Steps
1. Clone the repository
```bash
git clone git@github.com:Filocava99/DungeonLLMaster.git
```
2. Create a virtual environment (optional)
```bash
cd DungeonLLMaster
python -m venv venv
```
3. Activate the virtual environment (optional)
```bash
source venv/bin/activate
```
4. Install the dependencies
```bash
pip install -r requirements.txt
```

5. Run the application
```bash
OPENAI_API_KEY=your_secret_key python main.py
```
