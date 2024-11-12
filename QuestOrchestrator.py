import os

import autogen

config_list = [{'model': 'gpt-4o', 'api_key': os.environ['OPENAI_API_KEY']}]

# Define the agents
llm_config = {"config_list": config_list, "seed": 42}

quest_master = autogen.AssistantAgent(
    name='QuestMaster',
    llm_config=llm_config,
    system_message=(
        'You are the main QuestMaster and coordinator. '
        'Synthesize input from specialized agents to create a complete, cohesive quest. '
        'Ensure all elements work together harmoniously. Direct the conversation, make final decisions, '
        'and maintain the overall vision of the quest. '
        'Coordinate with the NarrativeDesigner for a compelling storyline. '
        'Work with ChallengeCreator to design interesting obstacles. '
        'Ask RewardAllocator to design fitting rewards. '
        'Incorporate characters from CharacterDeveloper and ensure they fit the storyline. '
        'Consult SettingAdvisor for an immersive setting design. '
        'Terminate the process when you believe the quest is complete.'
    ),
    description='The main QuestMaster and coordinator, responsible for merging input from specialized agents to create a complete, cohesive quest.'
)

narrative_designer = autogen.AssistantAgent(
    name='NarrativeDesigner',
    llm_config=llm_config,
    system_message=(
        'Develop a compelling storyline and plot for the quest. '
        'Incorporate plot twists, themes, and a clear narrative arc. '
        'Align the narrative with the characters and settings. '
        'Coordinate with the QuestMaster to ensure cohesion.'
    ),
    description='Craft the storyline, plot twists, and themes of the quest.'
)

challenge_creator = autogen.AssistantAgent(
    name='ChallengeCreator',
    llm_config=llm_config,
    system_message=(
        'Design challenges and obstacles for the quest, including puzzles, traps, and skill tests. '
        'Ensure they are engaging, balanced, and fit the quest theme. '
        'Coordinate with the QuestMaster and other relevant agents.'
    ),
    description='Design engaging challenges and obstacles for the quest.'
)

reward_allocator = autogen.AssistantAgent(
    name='RewardAllocator',
    llm_config=llm_config,
    system_message=(
        'Outline rewards and incentives for completing the quest. '
        'Consider in-game currency, items, or character advancement. '
        'Ensure rewards are balanced with the difficulty and importance of the quest.'
    ),
    description='Specify rewards and incentives for completing the quest.'
)

character_developer = autogen.AssistantAgent(
    name='CharacterDeveloper',
    llm_config=llm_config,
    system_message=(
        'Develop NPCs for the quest, including allies, antagonists, and neutral parties. '
        'Provide detailed descriptions, motivations, and backgrounds. '
        'Ensure characters align with the narrative and setting.'
    ),
    description='Design and describe NPCs, including allies and antagonists.'
)

setting_advisor = autogen.AssistantAgent(
    name='SettingAdvisor',
    llm_config=llm_config,
    system_message=(
        'Describe the environment and setting where the quest takes place. '
        'Include details about geography, atmosphere, and special features. '
        'Ensure the setting supports the quest\'s narrative and activities.'
    ),
    description='Craft the environment and setting details where the quest takes place.'
)

summarizer = autogen.AssistantAgent(
    name='Summarizer',
    llm_config=llm_config,
    system_message=(
        'Summarize the conversation and provide a concise overview of the quest design process. '
        'Include details about the storyline, challenges, rewards, characters, and setting.'
    ),
    description='Summarize the conversation, providing an exhaustive overview of the quest design process.'
)

human_proxy = autogen.UserProxyAgent(
    name='Human',
    human_input_mode='ALWAYS',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda message: '[QUEST COMPLETE]' in message.get('content', ''),
    system_message='A human providing feedback on quest creation.'
)

groupchat = autogen.GroupChat(
    agents=[
        quest_master,
        narrative_designer,
        challenge_creator,
        reward_allocator,
        character_developer,
        setting_advisor,
        summarizer,
        human_proxy
    ],
    messages=[],
    max_round=50,
    send_introductions=True
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


class QuestOrchestrator:
    def __init__(self):
        self.final_response = None
        self.manager = manager
        self.human_proxy = human_proxy

    def create_quest(self, initial_message):
        self.final_response = self.human_proxy.initiate_chat(
            self.manager,
            message=initial_message,
            summary_method='last_msg'
        ).chat_history
        self.save_quest_plan('final_quest_plan.md', self.final_response)
        print('Quest creation complete. Final response saved to final_quest_plan.md')
        return self.final_response

    def save_quest_plan(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Quest saved to {filename}")