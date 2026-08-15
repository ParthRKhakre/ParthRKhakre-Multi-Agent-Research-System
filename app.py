import streamlit as st
import time
from datetime import datetime
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Field Research System",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:ital,wght@0,300;0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --paper:      #F5F1E7;
    --paper-alt:  #EDE7D8;
    --paper-line: rgba(26,25,20,0.10);
    --ink:        #1C1A15;
    --ink-soft:   #6B6455;
    --navy:       #223755;
    --navy-soft:  rgba(34,55,85,0.08);
    --navy-line:  rgba(34,55,85,0.28);
    --rust:       #B8441F;
    --rust-soft:  rgba(184,68,31,0.10);
    --sage:       #55694A;
    --sage-soft:  rgba(85,105,74,0.10);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--ink);
}

.stApp {
    background-color: var(--paper);
    background-image:
        repeating-linear-gradient(180deg, rgba(34,55,85,0.035) 0px, rgba(34,55,85,0.035) 1px, transparent 1px, transparent 34px),
        radial-gradient(ellipse 70% 40% at 15% 0%, rgba(184,68,31,0.05) 0%, transparent 60%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.2rem 3rem 4rem; max-width: 1180px; }

/* ── Cover / hero ── */
.cover {
    position: relative;
    padding: 2.4rem 0 2rem;
    border-bottom: 1px solid var(--paper-line);
    margin-bottom: 2.4rem;
}
.cover-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.6rem;
}
.case-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--navy);
    border: 1px solid var(--navy-line);
    padding: 0.35rem 0.7rem;
    border-radius: 3px;
    background: var(--navy-soft);
}
.case-date {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--ink-soft);
    letter-spacing: 0.05em;
    text-align: right;
    line-height: 1.5;
}
.cover h1 {
    font-family: 'Fraunces', serif;
    font-optical-sizing: auto;
    font-size: clamp(2.6rem, 5.4vw, 4.3rem);
    font-weight: 600;
    line-height: 0.98;
    letter-spacing: -0.01em;
    color: var(--ink);
    margin: 0 0 0.9rem;
}
.cover h1 em {
    font-style: italic;
    font-weight: 500;
    color: var(--navy);
}
.cover-sub {
    font-size: 1.02rem;
    font-weight: 300;
    color: var(--ink-soft);
    max-width: 560px;
    line-height: 1.7;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.74rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--navy);
    margin: 0 0 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--paper-line);
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.35);
    border: 1px solid var(--paper-line);
    border-left: 3px solid var(--navy);
    border-radius: 4px;
    padding: 1.8rem 2rem 1.5rem;
    margin-bottom: 1.2rem;
}

.stTextInput input,
.stTextInput > div > div > input,
[data-baseweb="input"] input,
[data-baseweb="base-input"] input {
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid var(--navy-line) !important;
    border-radius: 3px !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    caret-color: var(--navy) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input::placeholder {
    color: #A39C8C !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #A39C8C !important;
}
.stTextInput input:focus {
    border-color: var(--navy) !important;
    box-shadow: 0 0 0 3px var(--navy-soft) !important;
}
.stTextInput > label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: var(--ink-soft) !important;
    font-weight: 500 !important;
}
[data-baseweb="base-input"] { background: transparent !important; }

/* ── Button ── */
.stButton > button {
    background: var(--ink) !important;
    color: var(--paper) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.75rem 1.6rem !important;
    cursor: pointer !important;
    transition: background 0.15s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover {
    background: var(--navy) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── download button ── */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--navy) !important;
    border: 1px solid var(--navy-line) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-radius: 3px !important;
    padding: 0.55rem 1.2rem !important;
}
.stDownloadButton > button:hover {
    background: var(--navy-soft) !important;
    border-color: var(--navy) !important;
}

/* ── Example chips ── */
.chip-row { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; margin: 0.9rem 0 1.8rem; }
.chip-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: var(--ink-soft);
    letter-spacing: 0.14em;
    text-transform: uppercase;
}
.chip {
    background: rgba(255,255,255,0.4);
    border: 1px solid var(--paper-line);
    border-radius: 3px;
    padding: 0.28rem 0.75rem;
    font-size: 0.78rem;
    color: var(--ink-soft);
    font-family: 'Inter', sans-serif;
}

/* ── Case log / pipeline entries ── */
.entry {
    position: relative;
    background: rgba(255,255,255,0.3);
    border: 1px solid var(--paper-line);
    border-radius: 3px;
    padding: 1.1rem 1.4rem 1.1rem 1.6rem;
    margin-bottom: 0.9rem;
    overflow: hidden;
}
.entry.active { border-color: var(--rust); background: var(--rust-soft); }
.entry.done   { border-color: var(--sage); background: var(--sage-soft); }
.entry::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--paper-line);
}
.entry.active::before {
    background: var(--rust);
    animation: scan 1.6s ease-in-out infinite;
}
.entry.done::before { background: var(--sage); }
@keyframes scan {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
.entry-row {
    display: flex;
    align-items: baseline;
    gap: 0.7rem;
}
.entry-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: var(--ink-soft);
}
.entry-title {
    font-family: 'Fraunces', serif;
    font-size: 1.02rem;
    font-weight: 600;
    color: var(--ink);
}
.entry-status {
    margin-left: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    white-space: nowrap;
}
.status-waiting { color: #A39C8C; }
.status-running { color: var(--rust); }
.status-done    { color: var(--sage); }
.entry-desc {
    font-size: 0.8rem;
    color: var(--ink-soft);
    margin-top: 0.3rem;
    padding-left: 1.35rem;
    font-weight: 300;
}

/* ── Result / raw panels ── */
.result-panel {
    background: rgba(255,255,255,0.3);
    border: 1px solid var(--paper-line);
    border-radius: 4px;
    padding: 1.5rem 1.8rem;
    margin-top: 0.6rem;
}
.result-panel-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--paper-line);
}
.result-content {
    font-size: 0.88rem;
    line-height: 1.75;
    color: var(--ink);
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
    font-weight: 300;
}

/* ── Dossier report panel ── */
.report-panel {
    position: relative;
    background: rgba(255,255,255,0.5);
    border: 1px solid var(--paper-line);
    border-radius: 4px;
    padding: 2.2rem 2.6rem;
    margin-top: 0.6rem;
    box-shadow: 0 1px 0 var(--paper-line), 0 12px 30px -20px rgba(28,26,21,0.35);
}
.stamp {
    position: absolute;
    top: 1.6rem;
    right: 2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    color: var(--navy);
    border: 1.5px solid var(--navy);
    border-radius: 3px;
    padding: 0.3rem 0.6rem;
    transform: rotate(3deg);
    opacity: 0.75;
}
.feedback-panel {
    background: rgba(255,255,255,0.4);
    border: 1px solid var(--paper-line);
    border-left: 3px solid var(--sage);
    border-radius: 4px;
    padding: 2rem 2.4rem;
    margin-top: 0.6rem;
}
.panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid var(--paper-line);
    color: var(--ink-soft);
}
.report-panel .stMarkdown, .report-panel p { font-family: 'Inter', sans-serif; }

/* ── Expander ── */
[data-testid="stExpander"] {
    border: 1px solid var(--paper-line) !important;
    border-radius: 4px !important;
    background: rgba(255,255,255,0.2) !important;
}
details summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.74rem !important;
    color: var(--ink-soft) !important;
    letter-spacing: 0.08em !important;
    cursor: pointer;
}

/* ── Spinner ── */
.stSpinner > div { color: var(--rust) !important; }
.stSpinner p { font-family: 'IBM Plex Mono', monospace !important; font-size: 0.8rem !important; }

/* ── Divider ── */
.hr {
    height: 1px;
    background: var(--paper-line);
    margin: 2.4rem 0 2rem;
}

/* ── Footer ── */
.footer {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #A39C8C;
    text-align: center;
    margin-top: 3.5rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a case-log entry ───────────────────────────────────────────
def entry_card(tag: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("PENDING", "status-waiting"),
        "running": ("● IN PROGRESS", "status-running"),
        "done":    ("✓ COMPLETE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="entry {card_cls}">
        <div class="entry-row">
            <span class="entry-tag">{tag}</span>
            <span class="entry-title">{title}</span>
            <span class="entry-status {cls}">{label}</span>
        </div>
        {"<div class='entry-desc'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Cover ─────────────────────────────────────────────────────────────────────
today = datetime.now().strftime("%d.%m.%Y")
st.markdown(f"""
<div class="cover">
    <div class="cover-top">
        <span class="case-tag">Multi-Agent Research System</span>
        <span class="case-date">FILE OPENED<br>{today}</span>
    </div>
    <h1>Research<em>Mind</em></h1>
    <p class="cover-sub">
        Four specialized agents work a single case in sequence — searching, reading,
        drafting, and reviewing — to produce a sourced research report on any topic you assign.
    </p>
</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="section-heading">Assign a Topic</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("Open Case & Run Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    chips_html = '<div class="chip-row"><span class="chip-label">Try →</span>'
    for ex in examples:
        chips_html += f'<span class="chip">{ex}</span>'
    chips_html += '</div>'
    st.markdown(chips_html, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Case Log</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    entry_card("ENTRY 01", "Search Agent", s("search"), "Gathers recent, reliable sources from the open web")
    entry_card("ENTRY 02", "Reader Agent", s("reader"), "Scrapes and extracts deep content from the lead source")
    entry_card("ENTRY 03", "Writer Chain", s("writer"), "Drafts the full structured research report")
    entry_card("ENTRY 04", "Critic Chain", s("critic"), "Scores the report and flags weaknesses")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Findings</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("Search Results — raw", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("Scraped Content — raw", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <span class="stamp">FILED</span>
            <div class="panel-label">Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label">Critic's Notes</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">ResearchMind — LangChain Multi-Agent Pipeline — Built on Streamlit</div>
""", unsafe_allow_html=True)