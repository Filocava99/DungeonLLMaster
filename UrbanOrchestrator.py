import os

import autogen

config_list = [{'model': 'gpt-4o', 'api_key': os.environ['OPENAI_API_KEY']}]

# Define the agents
llm_config = {"config_list": config_list, "seed": 42}
urban_planner = autogen.AssistantAgent(
    name='UrbanPlanner',
    llm_config=llm_config,
    system_message=(
        'You are the main Urban Planner and coordinator. '
        'Synthesize input from specialized agents to create a complete, cohesive urban agglomeration. '
        'Ensure all elements work together harmoniously. Direct the conversation, make final decisions, '
        'and maintain the overall vision of the urban area. Coordinate with the LayoutDesigner for detailed city maps. '
        'Ask the InfrastructureSpecialist to detail the city infrastructure. '
        'Ask the PublicSpaceDesigner, ResidentialArchitect, CommercialArchitect, and CulturalAdvisor for their respective inputs. '
        'Ensure regulations are checked by the RegulationExpert. '
        'Always add content to the last message received, do not summarize. '
        'Terminate the process when you believe the agglomeration is complete.'
    ),
    description='The main Urban Planner and coordinator, responsible for merging input from specialized agents to create a complete, cohesive urban agglomeration.'
)

layout_designer = autogen.AssistantAgent(
    name='LayoutDesigner',
    llm_config=llm_config,
    system_message=(
        'Design the overall layout of the urban area, focusing on creating efficient and aesthetic plans. '
        'Include zoning for residential, commercial, and industrial areas. '
        'Design transportation routes, consider geographical features, and ensure accessibility. '
        'Use diagrams or maps for visual support. '
        'Coordinate with the UrbanPlanner for alignment with the overall vision.'
    ),
    description='Design the overall layout of the urban area, focusing on creating efficient and aesthetic plans.'
)

infrastructure_specialist = autogen.AssistantAgent(
    name='InfrastructureSpecialist',
    llm_config=llm_config,
    system_message=(
        'Outline the infrastructure of the city, detailing transportation systems, utilities, and communication networks. '
        'Considers roads, railways, public transit, and airports. Discuss water, power, and waste management systems. '
        'Ensure the design supports the city\'s needs efficiently.'
    ),
    description='Detail the city\'s infrastructure, ensuring it supports its needs efficiently.'
)

public_space_designer = autogen.AssistantAgent(
    name='PublicSpaceDesigner',
    llm_config=llm_config,
    system_message=(
        'Design public spaces such as parks, squares, and public buildings. '
        'Consider accessibility, aesthetics, and community needs. Describe materials, features, and intended uses.'
    ),
    description='Create and describe public spaces, ensuring accessibility and aesthetic appeal.'
)

residential_architect = autogen.AssistantAgent(
    name='ResidentialArchitect',
    llm_config=llm_config,
    system_message=(
        'Design residential areas with various housing types. '
        'Consider demographics, density, amenities, and community integration. Describe style and materials.'
    ),
    description='Design residential areas, considering demographics and community integration.'
)

commercial_architect = autogen.AssistantAgent(
    name='CommercialArchitect',
    llm_config=llm_config,
    system_message=(
        'Plan commercial zones, including shops, markets, and business centers.'
        'Consider foot traffic, accessibility, and economic potential. Describe architecture and style.'
    ),
    description='Plan commercial zones, ensuring economic potential and accessibility.'
)

cultural_advisor = autogen.AssistantAgent(
    name='CulturalAdvisor',
    llm_config=llm_config,
    system_message=(
        'Integrate cultural elements into the city, including historical landmarks, museums, and community centers. '
        'Respect heritage while fostering community and cultural exchange.'
    ),
    description='Integrate cultural elements, respecting heritage and fostering community and cultural exchange.'
)

regulation_expert = autogen.AssistantAgent(
    name='RegulationExpert',
    llm_config=llm_config,
    system_message=(
        'Ensure the urban area complies with zoning laws, building codes, and environmental regulations. '
        'Advise on legal considerations and suggest improvements for compliance.'
    ),
    description='Ensure urban design complies with regulations and advise on legal considerations.'
)

summarizer = autogen.AssistantAgent(
    name='Summarizer',
    llm_config=llm_config,
    system_message=(
        'Summarize the conversation and provide a concise overview of the urban creation process. '
        'Include details on layout, infrastructure, public spaces, residential and commercial areas, cultural elements, and regulations.'
    ),
    description='Summarize the conversation, providing an exhaustive overview of the urban creation process.'
)

human_proxy = autogen.UserProxyAgent(
    name='Human',
    human_input_mode='ALWAYS',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda message: '[URBAN COMPLETE]' in message.get('content', ''),
    system_message='A human providing feedback on urban creation.'
)

groupchat = autogen.GroupChat(
    agents=[
        urban_planner,
        layout_designer,
        infrastructure_specialist,
        public_space_designer,
        residential_architect,
        commercial_architect,
        cultural_advisor,
        regulation_expert,
        summarizer,
        human_proxy
    ],
    messages=[],
    max_round=50,
    send_introductions=True
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)


class UrbanOrchestrator:
    def __init__(self):
        self.final_response = None
        self.manager = manager
        self.human_proxy = human_proxy

    def create_urban_area(self, initial_message):
        self.final_response = self.human_proxy.initiate_chat(
            self.manager,
            message=initial_message,
            summary_method='last_msg'
        ).chat_history
        self.save_urban_plan('final_urban_plan.md', self.final_response)
        print('Urban creation complete. Final response saved to final_urban_plan.md')
        return self.final_response

    def save_urban_plan(self, filename, content):
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Urban conglomerate saved to {filename}")