# ResearchMind

**Multi-agent AI research pipeline** — search → scrape → write → critique.

ResearchMind takes any topic and runs it through four specialized AI agents that collaborate in sequence to produce a sourced, structured, self-reviewed research report. Built with LangChain, Mistral, Tavily, and a Streamlit front end styled as a field dossier.

---

## How it works

| # | Agent | Job |
|---|-------|-----|
| 01 | **Search Agent** | Queries the web (via Tavily) for recent, reliable sources on the topic |
| 02 | **Reader Agent** | Picks the most relevant result and scrapes it for deeper content |
| 03 | **Writer Chain** | Drafts a structured report — introduction, key findings, conclusion, sources |
| 04 | **Critic Chain** | Reviews the report, scores it out of 10, and lists strengths and weaknesses |

Each stage feeds the next, so the final output is grounded in real, scraped source material rather than the model's own recall — and it comes with an honest critique attached.

## Features

- 🔍 Live web search grounded in current sources, not model memory
- 📄 Automatic scraping and content extraction from the top result
- ✍️ Structured, sourced report generation
- 🧐 Built-in critic pass with a numeric score and specific feedback
- 🖥️ Clean Streamlit UI with a real-time pipeline status log
- ⬇️ One-click Markdown export of the final report

## Tech stack

- **[LangChain](https://python.langchain.com/)** — agent orchestration
- **[Mistral AI](https://mistral.ai/)** (`mistral-large-latest`) — the underlying LLM
- **[Tavily](https://tavily.com/)** — web search API
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)** — HTML scraping
- **[Streamlit](https://streamlit.io/)** — UI

## Getting started

### Prerequisites

- Python 3.10+
- A [Mistral AI](https://mistral.ai/) API key
- A [Tavily](https://tavily.com/) API key

### Installation

```bash
git clone https://github.com/<your-username>/researchmind.git
cd researchmind
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run it

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`), enter a topic, and run the pipeline.

You can also run the pipeline headlessly from the command line:

```bash
python run_pipeline.py
```

## Project structure

```
.
├── app.py            # Streamlit UI + pipeline orchestration
├── agents.py         # Agent + chain definitions (search, reader, writer, critic)
├── tools.py           # Web search and scraping tools
├── run_pipeline.py   # CLI entry point for running the pipeline without the UI
├── requirements.txt
└── .env               # API keys (not committed)
```

## Example topics

- LLM agents 2025
- CRISPR gene editing
- Fusion energy progress
- Quantum computing breakthroughs in 2025

## Roadmap

- [ ] Multi-source scraping (beyond a single top result)
- [ ] PDF export alongside Markdown
- [ ] Configurable model provider (OpenAI, Anthropic, local models)
- [ ] Persistent history of past research runs

## License

MIT — see [LICENSE](LICENSE) for details.

## Contributing

Issues and pull requests are welcome. If you're adding a new agent or chain, keep it self-contained in `agents.py` and wire it into the pipeline in both `app.py` and `run_pipeline.py`.
