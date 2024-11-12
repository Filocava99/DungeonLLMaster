# DungeonLLMaster

![](dungeonllmaster_logo.jpeg)

## Introduction
Are you a Dungeon Master (DM) of a tabletop RPG game? You wanted some inspiration for your next session? Or maybe you are tired of improvising everything because your players are going off the rails?
Or maybe you are a new DM and you don't know how to properly plan a session? Or maybe you hadn't the time to plan the session and you need to improvise everything?
This is the solution for you! DungeonLLMaster is a tool that helps you to create a session plan for your RPG game.
You can create dungeons, quests, cities, villages, NPCs, monsters, and much more!

## Features

### Dungeon creation
| Feature              | Description                                              |
|----------------------|----------------------------------------------------------|
| Lore                 | Detailed description of the lore of the dungeon          |
| Rooms                | Detailed description of each room                        |
| Monsters             | Monsters placement and boss creation                     |
| Traps                | Traps placement                                          |
| Loot                 | Loot placement                                           |
| Puzzles              | Puzzle creation                                          |
| NPCs                 | NPC placement                                            |
| Layout               | Advanced spatial layout of the dungeon                   |
| Map Generation       | Dungeon map generation (using ASCII art)                 |
| 3D Map Visualization | 3D dungeon map visualization (coming soon)               |

### Quest creation
| Feature    | Description                                              |
|------------|----------------------------------------------------------|
| Lore       | Detailed description of the lore of the quest            |
| Objectives | Quest objectives                                         |
| Rewards    | Quest rewards                                            |
| NPCs       | Quest NPCs                                               |
| Monsters   | Quest monsters                                           |
| Locations  | Quest locations                                          |

### Urban agglomerate creation
| Feature              | Description                                              |
|----------------------|----------------------------------------------------------|
| Lore                 | Detailed description of the lore of the city/village     |
| Locations            | Detailed description of each location                    |
| NPCs                 | NPCs placement                                           |
| Quests               | Quests placement                                         |
| Shops                | Shops placement                                          |
| Taverns              | Taverns placement                                        |
| Inns                 | Inns placement                                           |
| Temples              | Temples placement                                        |
| Guilds               | Guilds placement                                         |
| Map Generation       | Urban map generation (using ASCII art)                   |
| 3D Map Visualization | 3D urban map visualization (coming soon)                 |

### General usage
| Feature       | Description                                              |
|---------------|----------------------------------------------------------|
| Generative AI | Support for tasks not covered by the main submodules, like generating new lore, names, etc. |

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
