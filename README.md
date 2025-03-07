---
title: Journi - Your Multi-Agent AI Travel Companion
emoji: 🧳
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.15.0
app_file: app.py
pinned: false
tags:
  - smolagents
  - travel-agent
  - AI-companion
  - travel-assistant
  - agent-course
---

# Journi: Your Multi-Agent AI Travel Companion

Journi is an intelligent multi-agent travel assistant that helps you plan and navigate your journeys with ease. Get vivid destination descriptions, accommodation recommendations, local time information, weather forecasts, currency conversions, language translations, and visa requirement details—all in one place.

## Features

- **Destination Descriptions**: Experience rich textual portrayals of travel destinations that bring locations to life
- **Real Accommodation Search**: Search for available accommodations with filters for budget, style, and location
- **Web Search**: Find up-to-date travel information from across the internet
- **Local Time Checker**: Know the current time at any destination around the world
- **Weather Forecasts**: Get detailed weather information with smart packing tips
- **Currency Converter**: Plan your budget with accurate currency conversions
- **Language Assistant**: Learn essential phrases with pronunciation guides in local languages
- **Visa Requirements**: Check entry requirements for international travel

## Usage

Simply ask Journi questions about your travel plans like:
- "Describe what Bali looks like and tell me the best time to visit"
- "Find me mid-range hotels in Tokyo near Shinjuku"
- "What's the local time in Paris right now?"
- "What should I pack for Tokyo next week based on the weather?"
- "How much is 500 USD worth in Japanese Yen?"
- "What essential phrases should I know for my trip to Italy?"
- "Do I need a visa to visit Thailand as a US citizen?"
- "Search for the top attractions in Barcelona"

## How It Works

Journi uses a multi-agent architecture powered by SmolaAgents:

1. **Coordinator Agent**: Orchestrates the workflow and delegates specialized tasks
   - Tools: `final_answer_tool` (Compiles and formats the final response)

2. **Information Retrieval Agent**: Searches and extracts relevant travel information
   - Tools: `web_search` (DuckDuckGo search), `visit_webpage` (Extracts content from websites)

3. **Language & Culture Agent**: Provides translations and cultural context
   - Tools: `translate_phrase` (Translates common travel phrases with pronunciation guides)

4. **Logistics Agent**: Manages practical travel information 
   - Tools: `get_local_time` (Checks current time at destinations), `get_weather_forecast` (Provides weather information with packing tips), `get_visa_requirements` (Checks entry requirements), `convert_currency` (Performs currency conversions)

5. **Recommendation Agent**: Creates destination descriptions, searches real accommodations, and suggests activities
   - Tools: `generate_destination_preview` (Creates vivid textual descriptions of destinations), `search_accommodations` (Searches for real accommodation options with filters)

Each specialized agent contributes its expertise to create comprehensive travel guidance. The multi-agent approach allows for specialized handling of different travel planning aspects, resulting in more detailed and helpful recommendations.

## Built With

- [SmolaAgents](https://github.com/smol-ai/agent) - Small, efficient agent framework for building multi-agent systems
- [Hugging Face](https://huggingface.co) - For language model capabilities
- [Gradio](https://gradio.app) - For the user interface
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) - For web search capabilities
- [PyTZ](https://pypi.org/project/pytz/) - For timezone handling

## About

Journi was created to enhance the travel planning experience by providing accurate, comprehensive travel information in a conversational format. The multi-agent architecture allows for specialized expertise in different aspects of travel planning, resulting in more detailed and helpful recommendations.

By delegating tasks to specialized agents, Journi can handle complex travel queries that span multiple domains (logistics, language, recommendations, etc.) in a more efficient and structured way than a single-agent approach.
