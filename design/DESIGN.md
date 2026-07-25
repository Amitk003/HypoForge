# HypoForge — UI/UX Design Specification (Option C)

> **Version:** 2.0  
> **Approach:** Hybrid — Custom CSS + Component Extraction (Streamlit)  
> **Status:** Final — Implementation-Ready  
> **Last Updated:** July 2026  
> **Estimated Effort:** ~25hr

---

## 0. Approach Decision

| Option | Verdict | Why |
|--------|---------|-----|
| A: Streamlit + hacks | ❌ Rejected | Every visual detail needs a hack. Long-term maintenance burden. |
| B: React + FastAPI | ⏳ Future | Full design control, but 40-60hr and two codebases. Do this if the product scales. |
| **C: Streamlit + clean extraction** | ✅ **Chosen** | 80% of design value. No backend rewrite. Cleaner code structure. |

**This document defines what Option C delivers, what it skips, and exactly how to build it.**

---

## 1. What We Skip (And Why)

These features from the ideal spec are **not worth fighting Streamlit for** in this phase:

| Skipped Feature | Why |
|-----------------|-----|
| Fixed top bar with editable goal | Streamlit can't do fixed positioning reliably. Use a simple header instead. |
| Activity log sidebar (250px fixed) | Fixed sidebars don't work in Streamlit. Use `st.expander` below the stepper instead. |
| Node-click → hypothesis linking | PyVis renders in an iframe; cross-iframe click events are unreliable. Not worth the complexity. |
| PDF export | `window.print()` in Streamlit's sandbox is unreliable. Browser Ctrl+P is fine. Markdown download is sufficient. |
| Node size proportional to degree | Small visual gain, complex PyVis per-node config. Use uniform node size. |
| Confounder dashed borders on graph nodes | PyVis doesn't easily support per-node border styles. Show confounders as a text list below the graph. |
| Real-time streaming progress | Threading + callbacks + Streamlit reruns = fragile. Show a static stepper after completion instead. |
| Keyboard shortcuts (Ctrl+1–5) | `st.components.v1.html` JS injection is fragile across Streamlit versions. Skip for now. |
| Star/pin hypotheses | Adds state complexity. Sort + filter is sufficient. |
| Mobile-optimized graph | PyVis iframes don't respond to CSS media queries. On mobile, show a static Graphviz image fallback. |

---

## 2. What We Deliver

### 2.1 Visual System (applies to all tabs)

#### Color Palette

Implemented via `.streamlit/config.toml` + CSS injection in `styles.py`.

| Token | Hex | Where Used |
|-------|-----|------------|
| `bg-page` | `#F8FAFC` | Page background |
| `bg-surface` | `#FFFFFF` | Cards, panels |
| `border-default` | `#E2E8F0` | Card borders, dividers |
| `border-subtle` | `#F1F5F9` | Inner separators |
| `text-primary` | `#0F172A` | Headings, body |
| `text-secondary` | `#475569` | Captions, descriptions |
| `text-tertiary` | `#94A3B8` | Placeholders |
| `accent-primary` | `#1E40AF` | Primary buttons, active states (sparingly) |
| `accent-success` | `#0D9488` | Success, complete pipeline stages |
| `accent-warning` | `#D97706` | Warnings, critique notes |
| `accent-danger` | `#DC2626` | Errors, safety flags only |
| `accent-info` | `#38BDF8` | Info badges, graph edges |

**Rules:** No gradients. No glassmorphism. No heavy illustrations. Color means something or it doesn't exist.

#### Typography

| Role | Font | Weight | Size |
|------|------|--------|------|
| Body | Inter | 400 / 500 | 14–16px |
| Heading | Inter | 600 | 18–24px |
| Monospace | JetBrains Mono | 400 | 12–14px |
| Caption | Inter | 400 | 12px |

Loaded via Google Fonts in `styles.py`. Monospace for scores, IDs, and technical values.

#### Spacing

- Base unit: 8px
- Card padding: 24px inner
- Section gap: 32px
- Border radius: 6px (cards), 4px (buttons), 9999px (pills)

---

### 2.2 File Structure

```
src/ui/
  app.py                    # Main Streamlit app — tab layout + routing
  styles.py                 # All CSS as a single string constant + font imports
  components/
    __init__.py
    header.py               # Simple header (logo + subtitle, NOT fixed)
    pipeline_stepper.py     # Horizontal stepper after completion
    hypothesis_card.py      # Collapsible hypothesis card with scores
    score_pill.py           # Reusable score pill HTML component
    causal_graph.py         # PyVis rendering with light theme
    simulator.py            # Counterfactual controls + results
    report.py               # Executive summary + markdown report
    empty_state.py          # Reusable empty state component
    error_card.py           # Reusable error card with message

.streamlit/
  config.toml               # Native Streamlit theme config
```

---

### 2.3 Header (replaces fixed top bar)

Simple `st.container()` at the top of every page. NOT fixed position.

```
┌─────────────────────────────────────────────────────────────┐
│  HypoForge          AI Co-Scientist                         │
│  How does urban green space affect local air temperature... │
└─────────────────────────────────────────────────────────────┘
```

- **Left:** "HypoForge" (Inter 600, 20px) + "AI Co-Scientist" (Inter 400, 12px, tertiary)
- **Below:** Current research goal as read-only `st.caption()` text, truncated to 1 line
- **No export button here** — export lives in the Report tab

---

### 2.4 Tab Layout (5 tabs)

Streamlit's native `st.tabs()`. No custom tab CSS needed — `config.toml` handles theme colors.

| Tab | Label | Purpose |
|-----|-------|---------|
| 1 | **Setup** | Goal input, data upload, advanced settings, run button |
| 2 | **Pipeline** | Visual stepper showing 8 agent stages + output snippets |
| 3 | **Hypotheses** | Ranked cards with scores, evidence, protocols, simulations |
| 4 | **Causal & Simulation** | Interactive graph + counterfactual slider |
| 5 | **Report** | Executive summary + full markdown + download |

---

### 2.5 Tab 1: Setup

```
┌──────────────────────────────────────────────────────────┐
│  col1 (2/3)                        col2 (1/3)            │
│  ┌────────────────────────────┐  ┌──────────────────┐   │
│  │ Research Goal               │  │ Data Preview      │   │
│  │ st.text_area (120px)       │  │ st.dataframe()    │   │
│  │                             │  │ Row/col count     │   │
│  │ File Upload                 │  │ Missing values    │   │
│  │ st.file_uploader            │  │                   │   │
│  │                             │  │                   │   │
│  │ ▶ Advanced Settings         │  │                   │   │
│  │   st.expander:              │  │                   │   │
│  │   - alpha (0.05)            │  │                   │   │
│  │   - max hypotheses (10)     │  │                   │   │
│  │                             │  │                   │   │
│  │ [ ▶ Run Pipeline ]          │  │                   │   │
│  │ st.button (primary)         │  │                   │   │
│  └────────────────────────────┘  └──────────────────┘   │
│                                                          │
│  ┌─ Last Run Summary (if pipeline_run) ────────────────┐ │
│  │ Hypotheses: 8  │  Simulations: 3  │  Protocols: 3   │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**Components:**

| Widget | Implementation |
|--------|---------------|
| Research Goal | `st.text_area(height=120)` with placeholder text |
| File Upload | `st.file_uploader(type=["csv", "parquet"])` |
| Data Preview | `st.dataframe(df.head(10))` + `st.caption(f"{rows} rows × {cols} columns")` |
| Advanced Settings | `st.expander("Advanced Settings")` containing `st.number_input` for alpha, max_hypotheses |
| Run Button | `st.button("Run Pipeline", type="primary", use_container_width=True)` |
| Last Run Summary | `st.columns(4)` with `st.metric()` for each count |

**After pipeline runs:** Show 4 metrics. If errors, show `st.expander("Warnings")` with `st.warning()` for each.

---

### 2.6 Tab 2: Pipeline (replaces "Agent Debate")

**This is the biggest UX improvement.** Replace the scrolling chat thread with a clean stepper.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ① Literature  ──  ② Data Analysis  ──  ③ Generator  ── ...│
│     Scout                                                   │
│                                                          │
│  ┌─ Stage Detail ──────────────────────────────────────┐ │
│  │  Data Analysis — Causal Discovery                   │ │
│  │  ✓ Complete (2.3s)                                  │ │
│  │                                                     │ │
│  │  • Loaded 500 rows × 6 columns                     │ │
│  │  • Discovered causal graph: 6 nodes, 8 edges       │ │
│  │  • Identified 2 confounders, 1 mediator            │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─ Activity Log ──────────────────────────────────────┐ │
│  │  ▸ Literature Scout: Found 8 papers (0.8s)          │ │
│  │  ▸ Data Analysis: Graph built (2.3s)                │ │
│  │  ▸ Generator: 8 hypotheses created (0.1s)          │ │
│  │  ▸ Critic: 3 issues found (0.1s)                   │ │
│  │  ▸ Evolver: Ranked top 5 (0.05s)                   │ │
│  │  ▸ Simulator: 3 counterfactuals run (1.2s)         │ │
│  │  ▸ Experiment Designer: 3 protocols (0.1s)         │ │
│  │  ▸ Meta-Reviewer: Report synthesized (0.05s)       │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**Stepper implementation:**

- Rendered as inline HTML via `st.markdown(unsafe_allow_html=True)` in `pipeline_stepper.py`
- 8 dots connected by lines in a horizontal row
- Each dot is an HTML `<span>` styled as a circle
- States:
  - `pending`: `#E2E8F0` background, gray
  - `complete`: `#0D9488` background with ✓ character
  - `error`: `#DC2626` background with ✗ character
- Lines between dots: `#E2E8F0` (pending) or `#0D9488` (complete)
- Below the stepper: `st.expander` for the stage detail card

**Stage Detail Card (inside expander):**

- Agent name + role (bold)
- Status badge (✓ Complete / ✗ Failed)
- Duration
- 2–3 bullet points of key output
- Error message if failed

**Activity Log (below the stepper):**

- Simple `st.expander("Activity Log")` containing timestamped lines
- Each line: `[timestamp]  Agent: summary (duration)`
- NOT a chat thread. NOT roleplayed. Just facts.

**Empty state:** "Run the pipeline to see agent progress."

**Note on "running" state:** Since we're not doing real-time streaming, the pipeline runs synchronously via `st.spinner`. The stepper appears after completion. During the run, show: "Running multi-agent pipeline…" with `st.spinner`.

---

### 2.7 Tab 3: Hypotheses (Most Important Results View)

```
┌──────────────────────────────────────────────────────────┐
│  Sort: [Composite Score ▾]    Filter: [All ▾]           │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ #1  Urban green space reduces peak temperature     │  │
│  │ Observed strong statistical coupling between       │  │
│  │ green_space_pct and temperature suggests...        │  │
│  │                                                    │  │
│  │ [Novelty 0.82] [Rigor 0.75] [Test 0.80] [Impact 0.70]│
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ #2  Changes in traffic density cause changes...    │  │
│  │ ...                                                │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─ Expanded (when hypothesis clicked) ───────────────┐  │
│  │                                                    │  │
│  │ Statement: "..."                                   │  │
│  │ Proposed Mechanism: "..."                          │  │
│  │                                                    │  │
│  │ Supporting Evidence:                               │  │
│  │ • Correlation detected: green_space <-> temp       │  │
│  │ • Causal path: green_space -> temperature          │  │
│  │                                                    │  │
│  │ Critique Notes:                                    │  │
│  │ ⚠ Causal fallacy: no direct edge in graph         │  │
│  │                                                    │  │
│  │ Safety Flags:                                      │  │
│  │ 🛑 Involves human subjects                         │  │
│  │                                                    │  │
│  │ ── Linked Experiment Protocol ──                   │  │
│  │ Design: t-test | Sample: 64 | Duration: 6 weeks   │  │
│  │ 1. Identify population...                          │  │
│  │ 2. Measure baseline...                             │  │
│  │ [Copy Protocol]                                    │  │
│  │                                                    │  │
│  │ ── Simulation Result ──                            │  │
│  │ Intervention: green_space → 96.0                   │  │
│  │ Predicted temp change: -0.4231 (95% CI: [...])     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**Score Pill Component (`score_pill.py`):**

Reusable HTML snippet rendered via `st.markdown(unsafe_allow_html=True)`.

```html
<span class="score-pill score-pill--high">
  Novelty <span class="score-value">0.82</span>
</span>
```

CSS classes:
- `.score-pill`: inline-flex, border 1px solid `#E2E8F0`, border-radius 9999px, padding 4px 10px, font-size 12px
- `.score-pill--high`: border-color `#0D9488` (score > 0.7)
- `.score-pill--low`: border-color `#D97706` (score < 0.4)
- `.score-value`: JetBrains Mono, font-weight 500

**Expanded Card Implementation:**

Use `st.expander()` for each hypothesis. Inside:
- `st.markdown()` for statement, mechanism, evidence
- `st.warning()` for critique notes
- `st.error()` for safety flags
- Linked protocol as a mini-document (numbered list)
- Linked simulation result as metrics

**Sort & Filter:**

- `st.selectbox("Sort by", ["Composite Score", "Novelty", "Causal Rigor", "Testability", "Impact"])` 
- `st.selectbox("Filter", ["All", "High Impact (>0.7)", "Novel (>0.8)", "With Critiques", "With Safety Flags"])`
- Filter/sort logic applied to `state.hypotheses` before rendering

**Copy Protocol:**

```python
st.code(protocol_text, language=None)  # Shows copy button natively
```

Or use `st.button("Copy Protocol")` + `pyperclip.copy()`.

---

### 2.8 Tab 4: Causal & Simulation

**60/40 column split.** Left: graph. Right: simulator.

```
┌────────────────────────────────────┬────────────────────┐
│  col1 (3)                          │  col2 (2)          │
│                                    │                    │
│  Interactive Causal Graph (DAG)    │  Counterfactual    │
│  ┌──────────────────────────────┐  │  Simulator         │
│  │ PyVis iframe (400px height)  │  │                    │
│  │ Light bg: #FFFFFF            │  │  Target:           │
│  │ Nodes: #1E293B fill          │  │  st.selectbox      │
│  │ Edges: #38BDF8 + weight      │  │                    │
│  │ Directed arrows              │  │  Intervention:     │
│  └──────────────────────────────┘  │  st.selectbox      │
│                                    │                    │
│  Confounders: [pill] [pill]       │  Baseline: 25.3    │
│  Mediators: [pill]                │  st.slider          │
│                                    │                    │
│                                    │  ┌──────────────┐  │
│                                    │  │ Predicted:    │  │
│                                    │  │ 24.9          │  │
│                                    │  │ Delta: -0.4   │  │
│                                    │  │ 95% CI: [...] │  │
│                                    │  └──────────────┘  │
└────────────────────────────────────┴────────────────────┘
```

**Graph (`causal_graph.py`):**

```python
from pyvis.network import Network
net = Network(height="400px", width="100%", bgcolor="#FFFFFF", font_color="#0F172A")
# ... add nodes and edges ...
net.set_options('{"physics": {"enabled": true, "stabilization": {"iterations": 100}}}')
# Save to temp HTML, render via st.components.v1.html
```

- Light background: `#FFFFFF` (matches page)
- Nodes: `#1E293B` fill, `#38BDF8` border, Inter font
- Edges: `#38BDF8` color, weight labels, directed arrows
- **No node-click linking** (skipped per dev)
- **No node size proportional to degree** (skipped per dev)
- **No confounder dashed borders** (skipped per dev)

**Confounders/Mediators:**

Display as pill badges below the graph using `st.markdown(unsafe_allow_html=True)`:

```html
<span class="pill pill--info">Confounder: green_space</span>
<span class="pill pill--info">Mediator: temperature</span>
```

**Simulator (`simulator.py`):**

- `st.selectbox("Target variable", num_cols)`
- `st.selectbox("Intervention variable", [c for c in num_cols if c != target])`
- `st.slider("Set value", min, max, value=baseline, step=σ/10)`
- `st.metric("Baseline", f"{baseline:.2f}")`
- Results via `st.metric()` for predicted outcome, delta, 95% CI

**Fallback:** If no data uploaded, show `st.info("Upload a dataset with numeric variables to enable causal discovery.")`

---

### 2.9 Tab 5: Report

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌─ Executive Summary ─────────────────────────────────┐ │
│  │ Research Goal: How does urban green space...        │ │
│  │ Generated 8 hypotheses, ran 3 simulations,          │ │
│  │ designed 3 experiment protocols.                    │ │
│  │                                                     │ │
│  │ Top hypothesis: "Urban green space reduces..."      │ │
│  │ Score: 0.77                                         │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                          │
│  ── Full Report ────────────────────────────────────────  │
│                                                          │
│  st.markdown(state.meta_review_report)                   │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ [ Download Markdown ]                               │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

**Executive Summary Card:**

White card (`st.container` with CSS class `card`) showing:
- Research goal (bold)
- Stats line: "Generated X hypotheses, ran Y simulations, designed Z protocols."
- Top hypothesis title + score

**Full Report:**

`st.markdown(state.meta_review_report)` — renders the Markdown natively.

**Download:**

`st.download_button("Download Markdown", data=report, file_name="hypoforge_report.md", mime="text/markdown")`

**No PDF export.** Browser Ctrl+P is sufficient.

---

### 2.10 Empty States

All tabs except Setup follow this pattern:

```python
if not st.session_state.pipeline_run:
    st.info("Run the pipeline to see [tab content].")
    st.stop()
```

| Tab | Empty State Message |
|-----|-------------------|
| Pipeline | "Run the pipeline to see agent progress." |
| Hypotheses | "Run the pipeline to generate hypotheses." |
| Causal & Simulation | "Upload a dataset with numeric variables to enable causal discovery." |
| Report | "Run the pipeline to generate a report." |

---

### 2.11 Error Handling

**Per-stage errors** (in Pipeline tab):

```python
if stage_error:
    st.error(f"❌ {stage_name}: {error_message}")
```

**Global errors** (in Setup tab after run):

```python
if state.errors:
    with st.expander(f"⚠ {len(state.errors)} warnings"):
        for err in state.errors:
            st.warning(err.split("\n")[0])
```

**No error = no noise.** Errors only appear when something actually went wrong.

---

## 3. Implementation Steps

### Phase 1: Foundation (~4hr)

| Step | File | What |
|------|------|------|
| 1.1 | `.streamlit/config.toml` | Theme colors, fonts, layout defaults |
| 1.2 | `src/ui/styles.py` | All CSS as a Python string: color tokens, typography, card styles, score pills, pills, stepper dots, print styles |
| 1.3 | `src/ui/components/__init__.py` | Package init |
| 1.4 | `src/ui/components/empty_state.py` | Reusable empty state component |
| 1.5 | `src/ui/components/error_card.py` | Reusable error card component |
| 1.6 | `src/ui/components/header.py` | Simple header with logo + research goal |

### Phase 2: Setup Tab (~3hr)

| Step | File | What |
|------|------|------|
| 2.1 | `src/ui/app.py` | Restructure main app: inject CSS via `styles.py`, add header, create 5 tabs. **Preserve** existing pipeline execution logic (file upload → save to disk → `run_pipeline()` → `session_state` update). Only the rendering layer changes. |
| 2.2 | `src/ui/app.py` | Setup tab: goal textarea, file upload, advanced settings expander, run button, last run summary |

### Phase 3: Pipeline Tab (~5hr)

| Step | File | What |
|------|------|------|
| 3.1 | `src/ui/components/pipeline_stepper.py` | HTML stepper component: 8 dots + connecting lines + states |
| 3.2 | `src/ui/app.py` | Pipeline tab: render stepper, activity log expander, stage detail cards |
| 3.3 | `src/orchestrator.py` + `src/state.py` | Add timing per stage (see Section 5 for state and orchestrator changes) |

### Phase 4: Hypotheses Tab (~5hr)

| Step | File | What |
|------|------|------|
| 4.1 | `src/ui/components/score_pill.py` | Reusable score pill HTML component |
| 4.2 | `src/ui/components/hypothesis_card.py` | Collapsible card with scores, evidence, critique, protocol, simulation |
| 4.3 | `src/ui/app.py` | Hypotheses tab: sort/filter controls, render hypothesis cards, expand/collapse logic |

### Phase 5: Causal & Simulation Tab (~4hr)

| Step | File | What |
|------|------|------|
| 5.1 | `src/ui/components/causal_graph.py` | PyVis rendering with light theme, confounders/mediators pills |
| 5.2 | `src/ui/components/simulator.py` | Target/intervention dropdowns, slider, prediction results |
| 5.3 | `src/ui/app.py` | Causal & Simulation tab: 60/40 column layout, graph + simulator |

### Phase 6: Report Tab (~2hr)

| Step | File | What |
|------|------|------|
| 6.1 | `src/ui/components/report.py` | Executive summary card + markdown render + download button |
| 6.2 | `src/ui/app.py` | Report tab: executive summary, full report, download |

### Phase 7: Polish & Test (~2hr)

| Step | What |
|------|------|
| 7.1 | Verify all tabs render correctly with sample data |
| 7.2 | Test error states (no data, failed pipeline, empty results) |
| 7.3 | Test responsive behavior (resize browser) |
| 7.4 | Verify score pills, stepper, graph all render with correct styles |

---

## 4. Config Files

### `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#1E40AF"
backgroundColor = "#F8FAFC"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#0F172A"
font = "sans serif"

[server]
headless = true
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### `src/ui/styles.py` (structure)

```python
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* === Base === */
.stApp { font-family: 'Inter', sans-serif; }

/* === Cards === */
.hf-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 24px;
    margin-bottom: 16px;
}

/* === Score Pills === */
.score-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    border: 1px solid #E2E8F0;
    border-radius: 9999px;
    padding: 4px 10px;
    font-size: 12px;
    font-family: 'Inter', sans-serif;
    color: #475569;
}
.score-pill--high { border-color: #0D9488; }
.score-pill--low { border-color: #D97706; }
.score-value {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}

/* === Info Pills (confinders/mediators) === */
.pill {
    display: inline-block;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 12px;
    margin-right: 8px;
}
.pill--info {
    background: #EFF6FF;
    color: #1E40AF;
    border: 1px solid #BFDBFE;
}

/* === Pipeline Stepper === */
.hf-stepper { display: flex; align-items: center; gap: 0; margin: 24px 0; }
.hf-step-dot {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; font-weight: 600;
    flex-shrink: 0;
}
.hf-step-dot--pending { background: #E2E8F0; color: #94A3B8; }
.hf-step-dot--complete { background: #0D9488; color: #FFFFFF; }
.hf-step-dot--error { background: #DC2626; color: #FFFFFF; }
.hf-step-line {
    height: 2px; flex: 1;
    background: #E2E8F0;
}
.hf-step-line--complete { background: #0D9488; }
.hf-step-label {
    font-size: 11px; color: #475569;
    text-align: center; margin-top: 4px;
    max-width: 80px;
}

/* === Print Styles === */
@media print {
    .stTabs, header, .stDeployButton { display: none !important; }
    .block-container { max-width: 100% !important; padding: 0 !important; }
}
"""
```

---

## 5. State Additions

Add to `src/state.py` `HypothesisState`:

```python
pipeline_stage_timings: dict = Field(default_factory=dict, description="Stage name -> duration in seconds")
```

Update `src/orchestrator.py` to record timing per stage. Preserve the existing descriptive error prefixes:

```python
import time

STAGE_NAMES = [
    ("literature_scout", "Literature Scout", run_literature_scout),
    ("data_analysis", "Data Analysis", run_data_analysis),
    ("hypothesis_generator", "Hypothesis Generator", generate_hypotheses),
    ("critic", "Critic", critique_hypotheses),
    ("evolver", "Evolver", evolve_and_rank),
    ("simulator", "Simulator", run_simulations),
    ("experiment_designer", "Experiment Designer", design_experiments),
    ("meta_reviewer", "Meta-Reviewer", synthesize_review),
]

def run_pipeline(state: HypothesisState) -> HypothesisState:
    state.errors = []
    for key, label, fn in STAGE_NAMES:
        t0 = time.time()
        try:
            state = fn(state)
        except Exception as e:
            state.errors.append(f"{label} failed: {e}")
        state.pipeline_stage_timings[key] = round(time.time() - t0, 2)
    state.pipeline_stage = "complete"
    return state
```

---

## 6. Summary: What's Different From v1

| v1 Spec | v2 (This Doc) |
|---------|---------------|
| Fixed top bar with edit modal | Simple `st.container()` header |
| Activity log sidebar (250px fixed) | `st.expander` below stepper |
| Node-click → hypothesis linking | Skipped (PyVis iframe limitation) |
| PDF export via weasyprint | Markdown download + browser Ctrl+P |
| Node size proportional to degree | Uniform node size |
| Confounder dashed borders | Text pill list below graph |
| Real-time streaming stepper | Static stepper after completion |
| Keyboard shortcuts | Skipped (not worth the fragile JS injection across Streamlit versions) |
| Star/pin hypotheses | Sort + filter controls |
| Mobile-optimized graph | Static Graphviz fallback on small screens |
| 6 tabs (protocols separate) | 5 tabs (protocols inside hypothesis cards) |
| 10+ component files | 9 component files (leaner) |
| ~40-60hr estimate | ~25hr estimate |

---

*End of design specification.*
