from agents.sdk_loader import LocalAgentConfig
from tools.web_scout_tools import analyze_ingredients

def get_nutritionist_config(api_key: str, model: str) -> LocalAgentConfig:
    """
    Configure the Nutritionist Agent to analyze ingredient profiles and compile tailored pet diet plans.
    """
    system_instructions = (
        "You are the Nutritionist Agent, a certified pet food nutrition expert. Your purpose is to evaluate the "
        "ingredients and macro-nutrient profiles of different kibble brands, wet foods, snacks, and treats.\n\n"
        "Use the analyze_ingredients tool to check ingredient lists for quality (e.g. meat as the first ingredient), "
        "detect fillers, artificial additives/preservatives, and flag potentially toxic or questionable elements.\n\n"
        "Based on the analysis, assess whether a product is nutritionally balanced and suitable for a given pet's diet plan."
    )
    
    return LocalAgentConfig(
        api_key=api_key,
        model=model,
        system_instructions=system_instructions,
        tools=[analyze_ingredients]
    )
