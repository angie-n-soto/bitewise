---
name: nutritionist_agent_skill
description: Guidelines for parsing ingredient lists, guaranteed analyses, and designing diet plans.
---
# Nutritionist Agent Skill

Use this skill when analyzing ingredient lists, guaranteed analyses, and macro splits.

## Ingredient Parsing Guidelines
- Parse the ingredient statement to identify the primary protein source (first ingredient) and quality.
- Identify and flag cheap fillers (e.g., corn/wheat gluten, soy hulls) and controversial synthetic preservatives (e.g., BHA, BHT, ethoxyquin).
- Detect and flag potential allergens based on the pet's profile.
- Evaluate the guaranteed analysis (minimum protein/fat, maximum fiber/moisture) and compare against dietary guidelines.
- Highlight the biological value of ingredients and provide a nutrition adequacy assessment.
- Always note that recommendations are informational and do not replace consultation with the pet's own veterinarian, especially for pets with diagnosed medical conditions.
