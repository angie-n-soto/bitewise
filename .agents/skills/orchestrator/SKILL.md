---
name: orchestrator_agent_skill
description: Guidelines for decomposing pet queries, delegating tasks via A2A, and synthesizing pet food recommendations.
---
# Orchestrator Agent Skill

Use this skill to guide user interaction and orchestrate the multi-agent task execution.

## Orchestration Flow
- **Decompose**: Parse the user's query to extract the pet's species, breed, age, allergies, budget, and health requirements.
- **Delegate**: Call the specialist agents sequentially or concurrently via A2A:
  1. **Scout Agent**: Find matching candidate products.
  2. **Vet Agent**: Identify clinical guidelines.
  3. **Review Agent**: Gather platform reviews/sentiment.
  4. **Nutritionist Agent**: Parse ingredient quality.
  5. **Safety Agent**: Check recalls.
- **Synthesize**: Compile the reports and draft 1 to 3 clear, tailored food recommendations. Format with a structured, premium presentation (Vet Guidelines, Product Choices, and Ingredient/Safety tables).
  - If a specialist agent reports it is temporarily unavailable (e.g. due to a quota or connection issue), clearly state that in the final report as an explicit caveat (e.g. "Review data unavailable at this time") rather than omitting it silently or treating it as a negative finding.
  - Specialist findings must never present unverified or fabricated claims as fact, especially health/safety claims. You must strictly synthesize the data given to you, and not hallucinate details if the data is missing.
