from agents.sdk_loader import LocalAgentConfig
from tools.web_scout_tools import search_veterinary_articles

def get_vet_config(api_key: str, model: str) -> LocalAgentConfig:
    """
    Configure the Vet Agent to search and analyze veterinary recommendations and literature.
    """
    system_instructions = (
        "You are the Vet Agent, a veterinary research assistant. Your purpose is to find vet-backed recommendations, "
        "academic guidelines, and clinical study data related to pet food ingredients and diet plans for specific conditions "
        "(e.g., allergies, obesity, pancreatitis, age-specific needs).\n\n"
        "Use the search_veterinary_articles tool to look up veterinary advice and citations. "
        "Highlight what clinical trials or professional veterinary associations (like WSAVA or AAHA) recommend for the pet's condition."
    )
    
    return LocalAgentConfig(
        api_key=api_key,
        model=model,
        system_instructions=system_instructions,
        tools=[search_veterinary_articles]
    )
