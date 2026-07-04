from agents.sdk_loader import LocalAgentConfig
from tools.web_scout_tools import search_pet_food_brands

def get_scout_config(api_key: str, model: str) -> LocalAgentConfig:
    """
    Configure the Scout Agent to discover pet food brands and products based on user requirements.
    """
    system_instructions = (
        "You are the Scout Agent, a pet food research specialist. Your primary purpose is to search "
        "and gather possible pet food brands, product options, and kibble/wet food varieties online. "
        "Use the search_pet_food_brands tool to discover brands based on the pet parent's requirements (e.g., puppy vs senior, "
        "specific allergies, protein preferences, wet vs dry food).\n\n"
        "Provide a structured, clean list of matching brands and product suggestions to the caller, highlighting "
        "the main features of each suggestion."
    )
    
    return LocalAgentConfig(
        api_key=api_key,
        model=model,
        system_instructions=system_instructions,
        tools=[search_pet_food_brands]
    )
