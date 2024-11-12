import os
from typing import Annotated

from autogen import AssistantAgent, register_function, UserProxyAgent, GroupChat, GroupChatManager

from DungeonOrchestrator import DungeonOrchestrator
from QuestOrchestrator import QuestOrchestrator
from UrbanOrchestrator import UrbanOrchestrator

config_list = [{'model': 'gpt-4o', 'api_key': os.environ['OPENAI_API_KEY']}]
llm_config = {"config_list": config_list, "seed": 42}

def create_dungeon(message: Annotated[str, 'Dungeon creation query']) -> Annotated[str, 'Dungeon creation response']:
    return DungeonOrchestrator().create_dungeon_initial(message)

def create_quest(message: Annotated[str, 'Quest creation query']) -> Annotated[str, 'Quest creation response']:
    return QuestOrchestrator().create_quest(message)

def create_urban_area(message: Annotated[str, 'Urban area creation query']) -> Annotated[str, 'Urban area creation response']:
    return UrbanOrchestrator().create_urban_area(message)

dungeonMaster = AssistantAgent(
    name="dungeon_master",
    llm_config=llm_config,
    system_message="You are a Dungeon Master. You can create dungeons, quests, and urban areas using the appropriate tools."
                   "For tasks not covered by the tools, you can use your creativity. Once you are done, end the conversation with [TERMINATE] ",
    description="A Dungeon Master is a person who creates and oversees an imaginary world, such as a fantasy world, for a role-playing game.",
    is_termination_msg=lambda x: '[TERMINATE]' in x.get('content', ''),
)

human = UserProxyAgent(
    name="human",
    human_input_mode='ALWAYS',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda message: '[TERMINATE]' in message.get('content', ''),
    system_message='A human asking questions to the Dungeon Master.'
)

tool_executor = UserProxyAgent(
    name="tool_executor",
    human_input_mode='NEVER',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda message: '[TERMINATE]' in message.get('content', ''),
    system_message='A tool executing commands.'
)

register_function(
    create_dungeon,
    name='create_dungeon',
    description='Create a dungeon for a role-playing game.',
    caller=dungeonMaster,
    executor=tool_executor
)

register_function(
    create_quest,
    name='create_quest',
    description='Create a quest for a role-playing game.',
    caller=dungeonMaster,
    executor=tool_executor
)

register_function(
    create_urban_area,
    name='create_urban_area',
    description='Create an urban area for a role-playing game.',
    caller=dungeonMaster,
    executor=tool_executor
)

group_chat = GroupChat(
    agents=[
        dungeonMaster,
        human,
        tool_executor
    ],
    messages=[],
    max_round=50,
    send_introductions=True
)

group_chat_manager = GroupChatManager(groupchat=group_chat)

if __name__ == '__main__':
    question = input("What would you like to do? ")
    human.initiate_chat(
        group_chat_manager,
        message=question,
        summary_method='last_msg'
    )