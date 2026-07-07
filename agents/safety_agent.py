"""
The Safety Agent's job is to check if a food brand has ever been recalled
or flagged for safety problems.
"""
from agents.sdk_loader import LocalAgentConfig
from tools.web_scout_tools import check_pet_food_recalls

def get_safety_config(api_key: str, model: str) -> LocalAgentConfig:
    """
    Configure the Safety Agent to perform FDA recall checks and monitor pet food hazard alerts.
    """
    system_instructions = (
        "You are the Safety Agent (sometimes referred to as the Security Agent). Your primary purpose is to search "
        "for active or historical safety food recalls, FDA warning letters, contamination reports (e.g. Salmonella, Listeria, Aflatoxin), "
        "and general pet food safety issues.\n\n"
        "Use the check_pet_food_recalls tool to search safety recalls for specific brands. "
        "Alert the caller immediately if there are high-risk issues or active recalls associated with a recommended product."
    )
    
    return LocalAgentConfig(
        api_key=api_key,
        model=model,
        system_instructions=system_instructions,
        tools=[check_pet_food_recalls]
    )
