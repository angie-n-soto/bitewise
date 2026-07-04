---
name: review_agent_skill
description: Guidelines for gathering and analyzing social reviews and public sentiment about pet food brands.
---
# Review Agent Skill

Use this skill when processing social sentiment, forums, reviews, or platform-specific comments about pet food.

## Sentiment Aggregation Guidelines
- Connect to online platforms using MCP tools (Reddit MCP, web-scrape/Firecrawl MCP).
- Filter out spam, generic reviews, and biased marketing posts.
- Focus on extracting real-world outcomes: palatability ("picky eater approved"), digestive responses, and skin/coat improvements.
- Summarize findings into clear sections: Common Praise, Common Criticisms, and Overall Public Sentiment.
- If live Reddit API access is unavailable, treat RSS-feed-sourced posts (e.g. subreddit .rss endpoints) as an acceptable substitute data source for sentiment gathering.
