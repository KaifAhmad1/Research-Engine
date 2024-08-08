## Research-Engine



```
Research-Engine/
├── data/
| ├── datafetching.py     # Contains data scraping, social media scraping and initializing external sources of knowledge engines like exa.ai, duckduckgo
│ └── dataloading.py   # Contains logic to call these functions and get relevant data 
|
├── model/
│ ├── agents.py    # Contains all agent's logic and initialization
│ ├── model.py     # Contains LLM, Embedding Model Initialization and Storing in Vector DB
│ └── prompts.py   # Contains agent's responsibilities and prompts 
│
├── app.py    # Contains Streamlit Scripts and basic interface
│
├── README.md 
└── requirements.txt  # Contains Package and dependencies to run this application
```
