import warnings
# Suppress autogen and other deprecation/user warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings('ignore', category=UserWarning)

from autogen import ConversableAgent, GroupChat, GroupChatManager
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Sample LLM Configuration (Replace with actual API keys/config if needed)
llm_config = {"config_list": [{"model": "gpt-4", "api_key": api_key}]}  # Replace with real API key

# Step 1: Create AI Agents with Defined Roles
patient_agent = ConversableAgent(
    name="patient", 
    system_message="You describe symptoms and ask for medical help.", 
    llm_config=llm_config
)

diagnosis_agent = ConversableAgent(
    name="diagnosis", 
    system_message="You analyze symptoms and provide a possible diagnosis. Summarize key points in one response.", 
    llm_config=llm_config
)

pharmacy_agent = ConversableAgent(
    name="pharmacy", 
    system_message="You recommend medications based on diagnosis. Only respond once.", 
    llm_config=llm_config
)

consultation_agent = ConversableAgent(
    name="consultation", 
    system_message="You determine if a doctor's visit is required. Provide a final summary with clear next steps. IMPORTANT: End your response with 'CONSULTATION_COMPLETE' to signal the end of the conversation.", 
    llm_config=llm_config
)

# Step 2: Create GroupChat for Structured Interaction
groupchat = GroupChat(
    agents=[diagnosis_agent, pharmacy_agent, consultation_agent],  # Patient only initiates
    messages=[], 
    max_round=5,  # Limits conversation to 5 rounds
    speaker_selection_method="round_robin"  # Ensures structured conversation flow
)

# Step 3: Create GroupChatManager to Handle Conversation
manager = GroupChatManager(name="manager", groupchat=groupchat)

# Step 4: Get Patient Input and Start Consultation
print("\n🤖 Welcome to the AI Healthcare Consultation System!")
symptoms = input("🩺 Please describe your symptoms: ")

print("\n🩺 Diagnosing symptoms...")
response = patient_agent.initiate_chat(
    manager, 
    message=f"I am feeling {symptoms}. Can you help?",
)
print(response)
