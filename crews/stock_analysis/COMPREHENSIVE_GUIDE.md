# Stock Analysis CrewAI Example - Comprehensive Guide

## 🎯 Overview & Purpose

The **stock_analysis** example is a **multi-agent AI system** that automates comprehensive stock analysis and investment recommendations. It orchestrates 3 specialized AI agents that collaborate sequentially to:

1. Analyze financial health and market performance
2. Research news, sentiment, and SEC filings
3. Generate actionable investment recommendations

Think of it as a **virtual investment research team** where each agent has a specific expertise and they work together to produce a complete analysis report.

---

## 🏗️ Architecture

### High-Level Flow:
```
User Input (Stock Ticker: e.g., "AMZN")
    ↓
Financial Analyst Agent → Financial Analysis Task
    ↓
Research Analyst Agent → Research Task + SEC Filings Analysis Task
    ↓
Investment Advisor Agent → Investment Recommendation Task
    ↓
Final Comprehensive Report
```

**Execution Model**: `Process.sequential` - agents work one after another, with each building on previous results.

---

## 👥 The Three Agents

### 1. Financial Analyst Agent
**Role**: "The Best Financial Analyst"  
**Goal**: Impress customers with financial data and market trends analysis  
**Expertise**: Stock market analysis, investment strategies, financial metrics

**Tools Available**:
- `CalculatorTool()` - Mathematical calculations (P/E ratios, growth rates, etc.)
- `ScrapeWebsiteTool()` - Extract data from financial websites
- `WebsiteSearchTool()` - Search within websites for specific information
- `SEC10QTool()` - Search quarterly SEC filings (10-Q)
- `SEC10KTool()` - Search annual SEC filings (10-K)

**Tasks Assigned**:
- **Financial Analysis** - Analyze key metrics (P/E ratio, EPS growth, revenue trends, debt-to-equity)
- **Filings Analysis** - Deep dive into 10-K/10-Q SEC filings

### 2. Research Analyst Agent
**Role**: "Staff Research Analyst"  
**Goal**: Gather and interpret data to amaze customers  
**Expertise**: News analysis, company announcements, market sentiment

**Tools Available**:
- `ScrapeWebsiteTool()` - Extract news articles and press releases
- `SEC10QTool()` - Quarterly filings research
- `SEC10KTool()` - Annual filings research

**Tasks Assigned**:
- **Research** - Collect recent news, press releases, market sentiment, analyst opinions, upcoming events (earnings)

### 3. Investment Advisor Agent
**Role**: "Private Investment Advisor"  
**Goal**: Deliver full analyses and complete investment recommendations  
**Expertise**: Synthesizing analytical insights into strategic investment advice

**Tools Available**:
- `CalculatorTool()` - Financial calculations for recommendations
- `ScrapeWebsiteTool()` - Additional market data
- `WebsiteSearchTool()` - Verify information

**Tasks Assigned**:
- **Recommend** - Synthesize all previous analyses into a comprehensive investment recommendation with clear stance (BUY/HOLD/SELL)

---

## 📋 The Four Tasks

### Task 1: Financial Analysis
**Agent**: Financial Analyst  
**What it does**:
- Examines key financial metrics (P/E ratio, EPS growth, revenue trends, debt-to-equity ratio)
- Compares stock performance against industry peers
- Analyzes overall market trends
- Uses most recent data available

**Output**: Comprehensive report on financial standing, strengths/weaknesses, competitive position

### Task 2: Research
**Agent**: Research Analyst  
**What it does**:
- Collects recent news articles and press releases
- Summarizes market analyses related to the stock
- Identifies significant events and market sentiment shifts
- Captures analyst opinions
- Notes upcoming events (earnings calls, product launches)

**Output**: Summary of latest news, market sentiment shifts, potential impacts, stock ticker confirmation

### Task 3: Filings Analysis
**Agent**: Financial Analyst (reused)  
**What it does**:
- Analyzes latest 10-Q (quarterly) and 10-K (annual) SEC filings
- Reviews Management's Discussion and Analysis (MD&A)
- Examines financial statements
- Checks insider trading activity
- Identifies disclosed risks

**Output**: Expanded report highlighting significant findings, red flags, or positive indicators

### Task 4: Recommend
**Agent**: Investment Advisor  
**What it does**:
- Synthesizes all previous analyses (Financial + Research + Filings)
- Considers financial health, market sentiment, qualitative EDGAR data
- Includes insider trading activity section
- Notes upcoming events (earnings)

**Output**: **Final comprehensive investment recommendation** with clear stance (BUY/HOLD/SELL), strategy, and supporting evidence - formatted for presentation to customer

---

## 🛠️ The Custom Tools

### 1. CalculatorTool (Most Recently Improved)
**File**: `src/stock_analysis/tools/calculator_tool.py`

**Purpose**: Safe mathematical expression evaluator for financial calculations

**How it works**:
1. **Input validation** - Only allows numbers and operators: `0-9`, `+`, `-`, `*`, `/`, `(`, `)`, `.`, `%`, spaces
2. **AST parsing** - Converts string to Abstract Syntax Tree (prevents code injection)
3. **Safe evaluation** - Only allows specific operators (Add, Sub, Mult, Div, Pow, Mod, USub, UAdd)
4. **Error handling** - Catches syntax errors, division by zero, invalid expressions

**Example uses**:
```python
calculator._run("200*7")           # → 1400.0
calculator._run("5000/2*10")       # → 25000.0
calculator._run("100 * (1 + 0.15)") # → 115.0 (P/E ratio calculations)
```

**Security**: Uses Python's AST (Abstract Syntax Tree) instead of `eval()` to prevent arbitrary code execution.

**Recent improvements**:
- Added comprehensive test suite (31 tests, 85% coverage)
- Achieved 82.6% mutation score (validates tests actually catch bugs)
- Documented testing methodology

### 2. SEC10KTool (Annual Reports)
**File**: `src/stock_analysis/tools/sec_tools.py`

**Purpose**: Semantic search within company's latest 10-K SEC filing

**How it works**:
1. **Initialization with stock ticker** (e.g., "AMZN")
2. **Fetches filing** from SEC EDGAR using sec-api:
   - Queries SEC API for latest 10-K for the ticker
   - Downloads the filing HTML
3. **Converts to text** using html2text library
4. **Cleans text** - Removes non-English characters, keeps letters, numbers, dollar signs
5. **Indexes content** using RAG (Retrieval-Augmented Generation) via embedchain
6. **Enables semantic search** - Can answer questions about the 10-K content

**Example queries**:
- "What was the total revenue last year?"
- "What are the main risk factors?"
- "What does management say about future growth?"

**Why 10-K matters**: Annual reports contain comprehensive financial statements, business descriptions, risk factors, and management's perspective.

### 3. SEC10QTool (Quarterly Reports)
**Purpose**: Semantic search within company's latest 10-Q SEC filing

**How it works**: Same as SEC10KTool but for quarterly filings (10-Q)

**Why 10-Q matters**: More frequent updates (quarterly vs annual), shows recent performance trends and changes.

---

## 🔧 Configuration & Setup

### Dependencies (pyproject.toml):
```toml
crewai[tools]>=0.152.0  # Core framework + built-in tools
python-dotenv>=1.0.1     # Environment variable management
html2text>=2024.2.26     # Convert SEC HTML filings to text
sec-api>=1.0.20          # SEC EDGAR API access
```

### Environment Variables Required (.env):
```bash
SERPER_API_KEY       # Web search (serper.dev) - free tier
BROWSERLESS_API_KEY  # Headless browser (browserless.io) - free tier
SEC_API_API_KEY      # SEC filings access (sec-api.io) - free tier
OPENAI_API_KEY       # LLM provider (OpenAI)
```

### LLM Configuration:
**Current**: Uses Ollama with llama3.1 (local model)
```python
from langchain.llms import Ollama
llm = Ollama(model="llama3.1")
```

**Can switch to GPT-4**:
```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)
```

---

## 🔄 How It All Works Together

### Execution Flow:

1. **User starts the crew**:
```python
StockAnalysisCrew().crew().kickoff(inputs={
    'query': 'What is the company you want to analyze?',
    'company_stock': 'AMZN'
})
```

2. **Financial Analyst** executes first:
   - Uses CalculatorTool for financial ratios
   - Scrapes financial websites for current data
   - Searches SEC filings for specific metrics
   - **Output**: Financial health assessment

3. **Research Analyst** takes over:
   - Scrapes news sites and financial media
   - Searches SEC filings for management commentary
   - Analyzes market sentiment and analyst opinions
   - **Output**: Market sentiment report + SEC insights

4. **Investment Advisor** synthesizes:
   - Reviews all previous outputs
   - Combines quantitative (financial metrics) and qualitative (sentiment, risks) data
   - Uses CalculatorTool for final valuation calculations
   - **Output**: **Investment recommendation with BUY/HOLD/SELL stance**

5. **Final report** returned to user:
   - Comprehensive analysis covering all aspects
   - Clear investment recommendation
   - Supporting evidence from multiple sources
   - Formatted for presentation

---

## 🎨 CrewAI Framework Patterns Used

### 1. @CrewBase Decorator
Marks the class as a Crew project with auto-discovery of agents and tasks:
```python
@CrewBase
class StockAnalysisCrew:
    agents_config = 'config/agents.yaml'  # Agent definitions
    tasks_config = 'config/tasks.yaml'    # Task definitions
```

### 2. YAML Configuration
**Agents** defined in `config/agents.yaml`:
- `role`: What the agent does
- `goal`: What they aim to achieve
- `backstory`: Their expertise and context

**Tasks** defined in `config/tasks.yaml`:
- `description`: Detailed instructions
- `expected_output`: What format/content is required

This separates **configuration** (YAML) from **implementation** (Python).

### 3. Auto-Population
```python
@agent and @task decorators automatically populate:
self.agents = [financial_agent(), research_analyst_agent(),
               financial_analyst_agent(), investment_advisor_agent()]
self.tasks = [financial_analysis(), research(),
              filings_analysis(), recommend()]
```

### 4. Sequential Process
```python
process=Process.sequential  # Agents work one after another
```
Each agent completes their task before the next begins. Output from one task is available to subsequent tasks.

---

## 🧪 Testing & Quality Assurance

### Test Suite:
- **Location**: `tests/tools/test_calculator_tool.py`
- **Coverage**: 31 comprehensive tests covering:
  - Basic operations (addition, subtraction, multiplication, division)
  - Complex expressions with parentheses and order of operations
  - Unary operators (negative, positive)
  - Error handling (invalid input, division by zero)
  - Edge cases (zero, large numbers, decimals)
  - Real-world financial calculations

### Mutation Testing:
- **Tool**: mutmut v2.4.5
- **Score**: 82.6% (Good rating - exceeds 75% production standard)
- **What it validates**: Tests actually catch bugs (not just execute code)
- **Configuration**: `.mutmut.ini` and `pyproject.toml`

### Code Coverage:
- **Tool**: pytest-cov
- **Score**: 85% line coverage
- **Gaps**: 4 unreachable defensive error handlers (intentional)

**Run tests**:
```bash
python3 -m pytest tests/ -v
python3 -m pytest tests/ --cov=src/stock_analysis/tools
python3 -m mutmut run  # Mutation testing
```

---

## 📊 Use Cases

**Who should use this**:
- Individual investors researching stocks
- Financial analysts needing quick comprehensive reports
- Portfolio managers evaluating new positions
- Students learning financial analysis

**What it produces**:
- **Quantitative analysis**: Financial ratios, growth rates, valuation metrics
- **Qualitative analysis**: Management quality, competitive position, industry trends
- **Risk assessment**: From SEC filings and news analysis
- **Actionable recommendation**: Clear BUY/HOLD/SELL with reasoning

---

## 🚀 Running the Example

### Quick Start:
```bash
cd crews/stock_analysis

# Setup
cp .env.example .env
# Edit .env and add your API keys

# Install dependencies
uv sync

# Run analysis
uv run stock_analysis
# or: python src/stock_analysis/main.py

# Train the crew (optional)
uv run train 5  # 5 training iterations
```

### What happens when you run it:
1. Prompts: "What is the company you want to analyze?" (default: AMZN)
2. Three agents execute sequentially (verbose logs show their thinking)
3. Final comprehensive report printed to console
4. Can take 5-15 minutes depending on LLM speed

---

## 💡 Key Innovations

1. **Multi-agent collaboration**: Different expertise areas working together
2. **SEC filing integration**: Real regulatory data, not just news/opinions
3. **Safe calculation tool**: Prevents code injection while enabling math
4. **RAG-powered SEC search**: Semantic search over long documents
5. **Comprehensive testing**: 82.6% mutation score validates quality
6. **Flexible LLM**: Works with both cloud (GPT-4) and local (Ollama) models

---

## 🔍 Code Structure

```
stock_analysis/
├── src/stock_analysis/
│   ├── main.py                      # Entry point (run, train functions)
│   ├── crew.py                      # Main crew definition (@CrewBase)
│   ├── config/
│   │   ├── agents.yaml              # Agent definitions (role, goal, backstory)
│   │   └── tasks.yaml               # Task definitions (description, expected_output)
│   └── tools/
│       ├── calculator_tool.py       # Safe math evaluator (AST-based)
│       └── sec_tools.py             # SEC10KTool, SEC10QTool (RAG search)
├── tests/
│   └── tools/
│       └── test_calculator_tool.py  # 31 comprehensive tests
├── docs/
│   ├── blog-post-mutation-testing.md      # Technical blog post (4,500+ words)
│   ├── TESTING_TUTORIAL.md                # 15-minute quick start guide
│   ├── LESSONS_LEARNED.md                 # One-page summary
│   └── SOCIAL_MEDIA_SNIPPETS.md           # 25+ content variants
├── pyproject.toml                   # Dependencies and scripts
├── pytest.ini                       # Test configuration
├── .mutmut.ini                      # Mutation testing config
├── .env.example                     # Example environment variables
├── MUTATION_RESULTS_FINAL.md        # Final mutation testing report
└── README.md                        # Quick start guide
```

---

## 📈 Potential Enhancements

- Add technical analysis (chart patterns, moving averages)
- Include competitor comparison matrix
- Integrate real-time price data
- Add sentiment analysis on social media
- Generate visualizations (charts, graphs)
- Support multiple stocks for portfolio analysis
- Add backtesting capabilities
- Export reports to PDF/Word
- Dashboard interface with Streamlit
- Historical trend analysis

---

## 🎓 Learning Resources

### Understanding the Codebase:
1. **Start with**: `README.md` - Quick overview
2. **Then read**: `src/stock_analysis/main.py` - Entry point
3. **Study**: `src/stock_analysis/crew.py` - Core orchestration
4. **Examine**: `config/agents.yaml` and `config/tasks.yaml` - Agent/task definitions
5. **Deep dive**: `tools/` directory - Custom tool implementations

### Testing Documentation:
1. **Start with**: `docs/LESSONS_LEARNED.md` - One-page summary
2. **Then read**: `docs/TESTING_TUTORIAL.md` - Quick start guide
3. **Deep dive**: `docs/blog-post-mutation-testing.md` - Full journey
4. **Results**: `MUTATION_RESULTS_FINAL.md` - Final analysis

### CrewAI Framework:
- Official docs: https://docs.crewai.com/
- Examples repo: https://github.com/crewAIInc/crewAI-examples
- Community: CrewAI Discord server

---

## ⚙️ Technical Details

### Agent Communication:
- Agents don't communicate directly
- Each task's output becomes input context for subsequent tasks
- The crew manages this context passing automatically
- Agents can see results from previous tasks but not future ones

### Tool Execution:
- Tools are called by agents when they determine it's needed
- LLM decides which tool to use based on the tool's description
- Tool results are fed back to the agent for further processing
- Failed tool calls are retried or handled by the agent

### Memory & Learning:
- Crew can be trained using `train()` function
- Training stores learned patterns in `trained_agents_data.pkl`
- Each training iteration provides feedback on agent performance
- Training improves agent decision-making over iterations

### Error Handling:
- Each tool has comprehensive error handling
- Invalid inputs are caught and meaningful errors returned
- Agents can recover from tool failures
- Verbose logging helps debug issues

---

## 🔐 Security Considerations

### CalculatorTool Security:
- **AST-based evaluation**: Never uses `eval()` or `exec()`
- **Input validation**: Regex checks before parsing
- **Operator whitelist**: Only safe mathematical operators allowed
- **No variable access**: Cannot reference Python variables or modules

### API Keys:
- Stored in `.env` file (never committed to git)
- Loaded via python-dotenv at runtime
- Each service has its own dedicated key
- Keys should use principle of least privilege

### SEC Data:
- Read-only access to public SEC filings
- No sensitive data stored locally
- Proper User-Agent headers for SEC compliance
- Rate limiting respected

---

## 📚 Related Documentation

- **CLAUDE.md** - Project-wide documentation for AI assistants
- **README.md** - Quick start guide
- **MUTATION_TESTING.md** - Complete mutation testing guide
- **MUTATION_TESTING_SUMMARY.md** - Initial setup documentation
- **docs/blog-post-mutation-testing.md** - Journey from 60.87% to 82.6%
- **docs/TESTING_TUTORIAL.md** - 15-minute mutation testing guide
- **docs/LESSONS_LEARNED.md** - Key findings summary
- **docs/SOCIAL_MEDIA_SNIPPETS.md** - 25+ content variants

---

## 🤝 Contributing

This is part of the CrewAI examples repository. To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure mutation score stays above 75%
6. Submit a pull request

---

## 📝 License

This project is released under the MIT License.

---

## 📞 Support

- CrewAI Documentation: https://docs.crewai.com/
- CrewAI GitHub: https://github.com/crewAIInc/crewAI
- CrewAI Examples: https://github.com/crewAIInc/crewAI-examples

---

**This is a production-ready example** demonstrating professional software engineering practices: clean architecture, comprehensive testing, mutation testing validation, proper error handling, and extensive documentation.

**Created by**: [@joaomdmoura](https://x.com/joaomdmoura)  
**Enhanced with**: Comprehensive testing suite, mutation testing (82.6% score), and extensive documentation
