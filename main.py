import asyncio
import sys
import argparse
from typing import List

# Import configuration
import config

# Import agents configuration
from agents import (
    get_orchestrator_config,
    get_scout_config,
    get_review_config,
    get_vet_config,
    get_nutritionist_config,
    get_safety_config,
)

try:
    from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable
    QUOTA_ERRORS = (ResourceExhausted, ServiceUnavailable)
except ImportError:
    QUOTA_ERRORS = (Exception,)

# Import Antigravity SDK elements from sdk_loader
from agents.sdk_loader import Agent, SDK_AVAILABLE
if not SDK_AVAILABLE:
    print("[WARNING] google-antigravity package is not installed. Running in simulation-only mode.")


async def run_live_pipeline(user_prompt: str):
    """
    Runs the actual multi-agent pipeline using Google Antigravity SDK.
    """
    user_prompt = user_prompt.strip()
    if not user_prompt:
        print("[ERROR] Input prompt cannot be empty.")
        sys.exit(1)
    if len(user_prompt) > 1000:
        print("[ERROR] Input prompt is too long. Please limit to 1000 characters.")
        sys.exit(1)

    if not config.GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY is not set. Please add it to your .env file or environment variables.")
        sys.exit(1)
        
    api_key = config.GEMINI_API_KEY
    model = config.AGENT_MODEL
    
    print("\n[Initializing] Setting up subagent configurations...")
    scout_cfg = get_scout_config(api_key, model)
    review_cfg = get_review_config(api_key, model)
    vet_cfg = get_vet_config(api_key, model)
    nutritionist_cfg = get_nutritionist_config(api_key, model)
    safety_cfg = get_safety_config(api_key, model)
    
    print("[Starting] Spawning child agents inside context managers...")
    # Initialize all child agents concurrently
    async with Agent(scout_cfg) as scout_agent, \
               Agent(review_cfg) as review_agent, \
               Agent(vet_cfg) as vet_agent, \
               Agent(nutritionist_cfg) as nutritionist_agent, \
               Agent(safety_cfg) as safety_agent:
               
        print("[Ready] Subagents are online and listening.")

        # Code-level tracking of delegation calls. This does NOT rely on the model's
        # own narration of what it did -- it increments regardless of what the
        # Orchestrator's final report text claims.
        delegation_counts = {"scout": 0, "vet": 0, "review": 0, "nutritionist": 0, "safety": 0}

        # Define A2A delegation tools.
        # These closures capture the spawned subagent instances.
        async def query_scout_agent(query: str) -> str:
            """
            Query the Scout Agent to search online and discover pet food brands/products based on pet requirements.
            """
            print(f"\n[A2A -> Scout Agent] Query: '{query}'")
            delegation_counts["scout"] += 1
            for attempt in range(3):
                try:
                    resp = await scout_agent.chat(query)
                    text = await resp.text()
                    chunks = await resp.resolve()
                    for chunk in chunks:
                        if type(chunk).__name__ == "ToolCall":
                            print(f"  [Tool Call] {chunk.name}(**{chunk.args})")
                        elif type(chunk).__name__ == "ToolResult":
                            res_str = str(chunk.result)
                            print(f"  [Tool Result] {chunk.name} -> {res_str[:200]}...")
                    print(f"[A2A <- Scout Agent] Received suggestions.")
                    return text
                except QUOTA_ERRORS as e:
                    print(f"[Warning] Scout Agent connection issue (attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        await asyncio.sleep(5 * (2 ** attempt))
            return "Scout Agent is currently unavailable (quota or connection issue). Product suggestions could not be retrieved at this time."
            
        async def query_review_agent(brand_name: str) -> str:
            """
            Query the Review Agent to gather Reddit discussions and scraped reviews/sentiments about a brand.
            """
            print(f"\n[A2A -> Review Agent] Checking reviews for: '{brand_name}'")
            delegation_counts["review"] += 1
            for attempt in range(3):
                try:
                    resp = await review_agent.chat(f"Gather public reviews and platform sentiment for: {brand_name}")
                    text = await resp.text()
                    chunks = await resp.resolve()
                    for chunk in chunks:
                        if type(chunk).__name__ == "ToolCall":
                            print(f"  [Tool Call] {chunk.name}(**{chunk.args})")
                        elif type(chunk).__name__ == "ToolResult":
                            res_str = str(chunk.result)
                            print(f"  [Tool Result] {chunk.name} -> {res_str[:200]}...")
                    print(f"[A2A <- Review Agent] Gathered reviews.")
                    return text
                except QUOTA_ERRORS as e:
                    print(f"[Warning] Review Agent connection issue (attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        await asyncio.sleep(5 * (2 ** attempt))
            return "Review Agent is currently unavailable (quota or connection issue). Review sentiment data could not be retrieved for this brand."
            
        async def query_vet_agent(topic: str) -> str:
            """
            Query the Vet Agent to check Google Scholar or academic articles for nutritional/health guidelines.
            """
            print(f"\n[A2A -> Vet Agent] Query: '{topic}'")
            delegation_counts["vet"] += 1
            for attempt in range(3):
                try:
                    resp = await vet_agent.chat(topic)
                    text = await resp.text()
                    chunks = await resp.resolve()
                    for chunk in chunks:
                        if type(chunk).__name__ == "ToolCall":
                            print(f"  [Tool Call] {chunk.name}(**{chunk.args})")
                        elif type(chunk).__name__ == "ToolResult":
                            res_str = str(chunk.result)
                            print(f"  [Tool Result] {chunk.name} -> {res_str[:200]}...")
                    print(f"[A2A <- Vet Agent] Gathered vet recommendations.")
                    return text
                except QUOTA_ERRORS as e:
                    print(f"[Warning] Vet Agent connection issue (attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        await asyncio.sleep(5 * (2 ** attempt))
            return "Vet Agent is currently unavailable (quota or connection issue). Veterinary guidelines could not be retrieved for this topic."
            
        async def query_nutritionist_agent(pet_profile: str, ingredient_list: str) -> str:
            """
            Query the Nutritionist Agent to analyze ingredients and design a tailored diet plan.
            """
            print(f"\n[A2A -> Nutritionist Agent] Analyzing ingredient profile for: {pet_profile}")
            delegation_counts["nutritionist"] += 1
            for attempt in range(3):
                try:
                    resp = await nutritionist_agent.chat(f"Pet Profile: {pet_profile}. Analyze ingredients: {ingredient_list}")
                    text = await resp.text()
                    chunks = await resp.resolve()
                    for chunk in chunks:
                        if type(chunk).__name__ == "ToolCall":
                            print(f"  [Tool Call] {chunk.name}(**{chunk.args})")
                        elif type(chunk).__name__ == "ToolResult":
                            res_str = str(chunk.result)
                            print(f"  [Tool Result] {chunk.name} -> {res_str[:200]}...")
                    print(f"[A2A <- Nutritionist Agent] Analysis report ready.")
                    return text
                except QUOTA_ERRORS as e:
                    print(f"[Warning] Nutritionist Agent connection issue (attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        await asyncio.sleep(5 * (2 ** attempt))
            return "Nutritionist Agent is currently unavailable (quota or connection issue). Ingredient analysis could not be completed for this profile."
            
        async def query_safety_agent(brand_name: str) -> str:
            """
            Query the Safety Agent to search for active or historical FDA recalls and hazard reports.
            """
            print(f"\n[A2A -> Safety Agent] Checking safety recall history for: '{brand_name}'")
            delegation_counts["safety"] += 1
            for attempt in range(3):
                try:
                    resp = await safety_agent.chat(f"Check recalls for brand: {brand_name}")
                    text = await resp.text()
                    chunks = await resp.resolve()
                    for chunk in chunks:
                        if type(chunk).__name__ == "ToolCall":
                            print(f"  [Tool Call] {chunk.name}(**{chunk.args})")
                        elif type(chunk).__name__ == "ToolResult":
                            res_str = str(chunk.result)
                            print(f"  [Tool Result] {chunk.name} -> {res_str[:200]}...")
                    print(f"[A2A <- Safety Agent] Safety report ready.")
                    return text
                except QUOTA_ERRORS as e:
                    print(f"[Warning] Safety Agent connection issue (attempt {attempt+1}/3): {e}")
                    if attempt < 2:
                        await asyncio.sleep(5 * (2 ** attempt))
            return "Safety Agent is currently unavailable (quota or connection issue). Safety recall history could not be retrieved for this brand."
            
        # Register delegation tools with the Orchestrator config
        orchestrator_tools = [
            query_scout_agent,
            query_review_agent,
            query_vet_agent,
            query_nutritionist_agent,
            query_safety_agent
        ]
        
        orchestrator_cfg = get_orchestrator_config(api_key, model, orchestrator_tools)
        
        print("[Starting] Spawning Orchestrator Agent...")
        async with Agent(orchestrator_cfg) as orchestrator:
            print("\n[Orchestrator Online] How can I help you today?")
            print(f"User Request: '{user_prompt}'\n")
            
            # Send prompt to the orchestrator
            response = await orchestrator.chat(user_prompt)
            
            # Stream the response tokens as they arrive
            print("--- Recommendation Report ---")
            async for token in response:
                sys.stdout.write(token)
                sys.stdout.flush()
            print("\n-----------------------------")

            # Code-level verification of delegation, independent of the report text.
            print("\n[Delegation Summary] Tool call counts per agent:")
            zero_call_agents = []
            for agent_name, count in delegation_counts.items():
                print(f"  - {agent_name}: {count} call(s)")
                if count == 0:
                    zero_call_agents.append(agent_name)
            if zero_call_agents:
                print(f"[WARNING] The following agents were NEVER called: {', '.join(zero_call_agents)}. "
                      "The report above may not be grounded in real tool output.")


def run_dry_run_simulation(user_prompt: str):
    """
    Simulates the agent A2A flow for dry-run verification.
    This runs offline without making real API requests.
    """
    print("\n" + "="*50)
    print("      PET PARENT ADVISOR SYSTEM SIMULATION      ")
    print("="*50)
    print(f"User Request: '{user_prompt}'")
    print("\n[Step 1] Orchestrator parses request and identifies pet profile.")
    
    print("\n[Step 2] Orchestrator queries Scout Agent to find products.")
    print(" >> [A2A -> Scout Agent] 'Find brands and products matching senior dog stomach issues'")
    print(" << [A2A <- Scout Agent] Suggested: 'Hill's Science Diet (Sensitive Stomach)' and 'Orijen (Fit & Trim)'")
    
    print("\n[Step 3] Orchestrator queries Vet Agent for health guidelines.")
    print(" >> [A2A -> Vet Agent] 'Veterinary advice for dogs with sensitive stomachs'")
    print(" << [A2A <- Vet Agent] Guideline: 'Highly digestible ingredients, prebiotic fibers, and low-fat are recommended.'")
    
    print("\n[Step 4] Orchestrator queries Review Agent to search online forums.")
    print(" >> [A2A -> Review Agent] 'Check Reddit reviews for Hill's Science Diet Sensitive Stomach'")
    print(" << [A2A <- Review Agent] Reddit sentiment: 'Many owners reported positive results for skin/coat, but some noted kibble size was too large.'")
    
    print("\n[Step 5] Orchestrator queries Nutritionist Agent to evaluate ingredients.")
    print(" >> [A2A -> Nutritionist Agent] 'Evaluate ingredient: Brewers Rice, Chicken Meal, Whole Grain Oats'")
    print(" << [A2A <- Nutritionist Agent] Ingredients analyzed. First ingredient is whole chicken meal (meat source). Prebiotics identified. Overall suitability score: 9/10.")
    
    print("\n[Step 6] Orchestrator queries Safety Agent to check active food recalls.")
    print(" >> [A2A -> Safety Agent] 'Check active FDA recalls for Hill's Science Diet'")
    print(" << [A2A <- Safety Agent] Safety check: 'No active recalls found in database for Hill's Science Diet.'")
    
    print("\n[Step 7] Orchestrator compiles findings and outputs the final report.")
    print("\n--- Recommendation Report (Simulated) ---")
    print("### Vet Guidelines for Stomach Sensitivity")
    print("A highly digestible diet with prebiotic fiber is essential. Avoid artificial additives.")
    print("\n### Top Recommendation: Hill's Science Diet (Sensitive Stomach & Skin)")
    print("- **Ingredient Assessment**: Oatmeal and prebiotic beet pulp present. Balanced formula.")
    print("- **Online Sentiment**: High satisfaction on r/dogfood for allergy relief.")
    print("- **Safety Status**: Safe (No active recalls).")
    print("------------------------------------------")
    print("\nDry-run simulation completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pet Parent Advisor Agentic System CLI")
    parser.add_argument(
        "--prompt", 
        type=str, 
        default="I need recommendations for my 7-year-old dog who has a sensitive stomach.",
        help="The query description of the pet parent."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Run an offline, dry-run simulation of the multi-agent system."
    )
    args = parser.parse_args()
    
    # If python packages or SDK are missing or --dry-run is specified, run the simulation
    if args.dry_run or not SDK_AVAILABLE:
        run_dry_run_simulation(args.prompt)
    else:
        try:
            asyncio.run(run_live_pipeline(args.prompt))
        except KeyboardInterrupt:
            print("\nExecution cancelled by user.")
