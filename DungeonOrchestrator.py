import os
import autogen

config_list = [{'model': 'gpt-4o', 'api_key': os.environ['OPENAI_API_KEY']}]

# Define the agents
llm_config = {"config_list": config_list, "seed": 42}


# Define specialized agents
dungeon_creator = autogen.AssistantAgent(
    name='DungeonCreator',
    llm_config=llm_config,
    system_message=(
        'You are the main Dungeon Creator and coordinator. '
        'Synthesize input from specialized agents to create a complete, cohesive dungeon. '
        'Ensure all elements work together harmoniously. Direct the conversation, make final decisions, '
        'and maintain the overall vision of the dungeon. Coordinate with the LayoutDesigner to ensure a detailed map is drawn.'
        'Ask the TrapDesigner to include traps in the dungeon.'
        'Ask the RoomDetail to provide detailed descriptions for each room.'
        'Ask the MonsterPlacement to populate the dungeon with monsters.'
        'Ask the TreasureGenerator to create and place treasures throughout the dungeon.'
        'Always add content to the last message received, do not summarize.'
        'Use the Summarizer to provide a concise overview of the dungeon creation process once all the other agents have contributed to the creation process.'
        'When you believe the dungeon is complete, end your message with [DUNGEON COMPLETE] to terminate the process.'
    ),
    description='The main Dungeon Creator and coordinator, responsible for merging input from specialized agents to create a complete, cohesive dungeon.'
)

layout_designer = autogen.AssistantAgent(
    name='LayoutDesigner',
    llm_config=llm_config,
    description='Design the overall layout of the dungeon, focusing on creating organic, non-linear structures unless specifically instructed otherwise.',
    system_message=(
        'Design the overall layout of the dungeon, focusing on creating organic, non-linear structures unless specifically instructed otherwise. '
        'Create complex, interconnected layouts with multiple paths, secret passages, and varied elevations. '
        'Consider the natural formation of the environment and how it would influence the dungeon\'s shape. '
        'Provide accurate details, including room sizes, positions, and how they relate to each other in 3D space. '
        'Draw a detailed map of the dungeon, including all rooms, corridors, and notable features. Use ASCII art or other visual aids to enhance clarity. '
        'Coordinate with the TrapDesigner for optimal trap placement.'
        'Always add content to the last message received, do not summarize.'
    )
)

room_detail = autogen.AssistantAgent(
    name='RoomDetail',
    llm_config=llm_config,
    description='Define extremely detailed descriptions for each room, appealing to all five senses and reflecting the room\'s purpose and history.',
    system_message=(
        'Define extremely detailed descriptions for each room, as if describing them to a person who cannot see. '
        'Make the descriptions vivid and engaging, appealing to all five senses. Include information on textures, smells, sounds, temperature, and even taste where relevant. '
        'Describe the materials, architecture, lighting, and atmosphere. '
        'Detail any notable features, furnishings, or objects. '
        'Consider how the room\'s purpose and history might be reflected in its appearance. '
        'Report your ideas to the Dungeon Creator, ensuring each room feels unique and memorable.'
        'Always add content to the last message received, do not summarize.'
    )
)

monster_placement = autogen.AssistantAgent(
    name='MonsterPlacement',
    llm_config=llm_config,
    description='Populate the dungeon with monsters, carefully considering the party\'s level to ensure appropriate difficulty.',
    system_message=(
        'Populate the dungeon with monsters, carefully considering the party\'s level to ensure appropriate difficulty. '
        'For each monster, provide exhaustive details including: skill points, health, armor class, abilities, special characteristics, attacks (with damage dice), armor and playstile. '
        'Always use the metric system'
        'Create a challenging boss for the final room, again tailored to the party\'s level. '
        'Consider the ecology of the dungeon and how monsters interact with each other and their environment. '
        'Suggest monster placements, encounter dynamics, and potential strategies to the Dungeon Creator. '
        'Include any relevant lore or background for the monsters that might enhance the story.'
        'Always add content to the last message received, do not summarize.'
    )
)

treasure_generator = autogen.AssistantAgent(
    name='TreasureGenerator',
    description='Create and place treasures throughout the dungeon, including a significant reward for the final room. Balance the treasure distribution to match the dungeon\'s difficulty and the party\'s level.',
    llm_config=llm_config,
    system_message=(
        'Create and place treasures throughout the dungeon, including a significant reward for the final room. '
        'Balance the treasure distribution to match the dungeon\'s difficulty and the party\'s level. '
        'For each treasure, provide detailed descriptions including appearance, value, and any magical properties. '
        'Consider the history and theme of the dungeon when creating unique, thematic treasures. '
        'Suggest clever hiding spots or protection methods for valuable items. '
        'You can also create cursed or dangerous treasures to add variety and challenge. '
        'Use the metric system for all measurements. '
        'Propose treasure locations and descriptions to the Dungeon Creator, ensuring they enhance the overall dungeon experience.'
        'Always add content to the last message received, do not summarize.'
    )
)

trap_designer = autogen.AssistantAgent(
    name='TrapDesigner',
    description='Design and place a variety of traps throughout the dungeon, considering the dungeon\'s theme, the party\'s level, and the overall difficulty.',
    llm_config=llm_config,
    system_message=(
        'Design and place a variety of traps throughout the dungeon. '
        'Consider the dungeon\'s theme, the party\'s level, and the overall difficulty when creating traps. '
        'Provide detailed descriptions of each trap, including its trigger mechanism, effects, difficulty to detect and disarm, and potential damage or consequences. '
        'Coordinate with the LayoutDesigner for optimal placement of traps within the dungeon\'s layout. '
        'Suggest trap locations and descriptions to the Dungeon Creator, ensuring they enhance the overall challenge and theme of the dungeon.'
        'Always add content to the last message received, do not summarize.'
    )
)

summarizer = autogen.AssistantAgent(
    name = "Summarizer",
    llm_config=llm_config,
    description="Summarize the conversation and provide a concise overview of the dungeon creation process.",
    system_message=(
        "Use the information provided by each agent to create an exhaustive description of the dungeon. "
        "Report every detail and decision made during the conversation. "
        "The result should a description of the dungeon, its layout, rooms, monsters, traps, treasures, and any other relevant details like the ones you can find in the official D&D manuals. "
    )
)

human_proxy = autogen.UserProxyAgent(
    name='Human',
    human_input_mode='ALWAYS',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: '[DUNGEON COMPLETE]' in x.get('content', ''),
    system_message='A human giving instructions for dungeon creation and providing feedback.'
)

groupchat = autogen.GroupChat(
    agents=[
        dungeon_creator,
        layout_designer,
        room_detail,
        monster_placement,
        treasure_generator,
        trap_designer,
        summarizer,
        human_proxy
    ],
    messages=[],
    max_round=50,
    send_introductions=True
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

class DungeonOrchestrator:
    def __init__(self):
        self.final_response = None
        self.manager = manager
        self.human_proxy = human_proxy
        self.feedback = None

    def create_dungeon_initial(self, initial_message=None):
        if initial_message is None:
            initial_message = (
                'Create a dungeon in the misty mountains of Middle-earth. '
                'The dungeon is the nest of the great eagles. '
                'It should be both a temple carved inside the mountain and on the surface where eagles can fly. '
                'At least 20 rooms, difficulty for a party of five level 8 players. '
                'DungeonCreator, please coordinate the creation process and synthesize the input from other agents. '
                'Ensure a detailed map is drawn and traps are included. '
                'Terminate the process when you believe the dungeon is complete.'
                'Always add content to the last message received, do not summarize.'
        )
        self.final_response = self.human_proxy.initiate_chat(
            self.manager,
            message=initial_message,
            summary_method='last_msg'
        ).chat_history
        self.save_dungeon('final_dungeon.md', self.final_response)
        print('Dungeon creation complete. Final response saved to final_dungeon.md')
        return self.final_response

    def save_dungeon(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Dungeon saved to {filename}")