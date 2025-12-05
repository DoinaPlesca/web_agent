## Web Scraping Agent using AutoGen

This project implements a Web Scraping AI Agent System using the AutoGen framework.
It retrieves real-time stock prices from Yahoo Finance using a registered tool and validates the output through a second agent.


The solution contain:

1. Researcher Agent performs the task
3. Evaluator Agent validates the result
5. UserProxyAgent executes tool calls

---

### System Overview

#### Researcher Agent
* Receives the user's stock URL
* Automatically calls the tool get_stock_price (via AutoGen’s register_function)
* Returns strict JSON after tool execution
* No explanations, no markdown
---

#### Tool: `get_stock_price`
Web scraping with requests + BeautifulSoup
- Uses **TTL caching**, **global rate limiting**, **retry with exponential backoff**, and **fallback**
- Returns structured JSON to the Researcher agent
- The tool is executed automatically by AutoGen when the Researcher invokes it
---

#### Evaluator Agent
The Evaluator checks whether the Researcher output is correct.
* JSON must contain stock_price (numeric) and source (valid URL)
* No additional fields allowed
* Output itself must be strict JSON


````
User → Researcher → Evaluator → Final Output
````

### Project Structure
````
web_agent/
│
├── main.py                 # Runs the sequential Researcher → Evaluator pipeline
├── README.md
├── use_cases.md            # Automatically generated: includes 5 real use cases
│
├── src/
│   ├── agents/
│   │   ├── researcher_agent.py
│   │   ├── evaluator_agent.py
│   │   └── user_proxy.py
│   │
│   └── tools/
│       └── web_scraper.py   # Scraper with caching, retries, rate limiting
│
└── requirements.txt

````
### Dependencies

These are required to run the project:

````
autogen==0.3.1
autogen-agentchat @ git+https://github.com/patrickstolc/autogen.git@0.2#egg=autogen-agentchat
mistralai==1.2.3
ollama==0.3.3
fix-busted-json==0.0.18
python-dotenv
requests
beautifulsoup4
````
Install with:

````bash
pip install -r requirements.txt

````

### Setup Instructions

##### 1. Create and activate a virtual environment

````bash
python -m venv .venv
.\.venv\Scripts\activate
````

##### 2. Add API key
Create a .env file:
````
MISTRAL_API_KEY=api_key
````

##### 3. Run the Web Scraping Agent
````bash
python main.py

````

##### 4. Output
````aiignore
Suggested tool call: get_stock_price
Tool response: {"success": true, "price": 184.55, ...}

Researcher Output:
{"stock_price": 668.57, "source": "https://finance.yahoo.com/quote/META"}

Evaluator Output:
{"evaluation": "SUCCESS", "reason": "...", "is_valid_price": true}

````
#### Use Case File

The project supports generating use cases using the optional utilities in src/utils/.

````
src/utils/run_single_test.py
src/utils/run_all_tests.py
src/utils/markdown_export.py
````
use_cases.md - generated manually using the utilities in src/utils/

1. [ ] META
2. [ ] AAPL
3. [ ] GOOG
4. [ ] INVALID ticker
5. [ ] Non-stock homepage

Each test case includes:

* Input URL
* Researcher Output (JSON)
* Evaluator Output (JSON)

To generate the use_cases.md file, run:
````bash
python src/utils/run_all_tests.py

````
!!! Note: main.py does not generate use cases automatically.

