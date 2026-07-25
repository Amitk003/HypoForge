HypoForge: Open-Source Multi-Agent AI Co-Scientist

Project Overview

HypoForge is an AI system that helps scientists come up with new ideas. You give it a research question and some data. It reads research papers, finds patterns in your data, creates hypotheses, checks them, runs simulations, and writes a full report. All of this runs on your own computer. You do not need any paid API keys.

Problem Being Solved

Coming up with a good scientific hypothesis takes a lot of time. A researcher has to read many papers, look at data, find cause-and-effect relationships, think of new ideas, design experiments, and write everything up. This can take months. HypoForge does most of this work automatically. The researcher can focus on the creative parts and making decisions.

Proposed Solution

HypoForge has 8 agents that work one after another. Each agent has one job:

1. Literature Scout: Searches arXiv for research papers related to your question. It uses AI to find the most relevant papers and remembers them for later use.

2. Data Analyst: Loads your CSV or Parquet file. Makes a summary of the data. Then runs causal discovery to find out how different variables affect each other.

3. Hypothesis Generator: Creates hypotheses from three places: patterns it finds in your data, cause-and-effect paths in the graph, and gaps in the research papers.

4. Critic: Checks every hypothesis for problems. Is there evidence for it? Does it confuse correlation with causation? Can it be tested? Are there ethical issues?

5. Evolver: Scores each hypothesis on four things: how new it is, how strong the cause-and-effect evidence is, how easy it is to test, and how important it would be if proven true. It can also combine two good hypotheses or improve weak parts.

6. Simulator: Trains a machine learning model on your data. It runs simulations to answer "what if" questions. For example: what would happen to temperature if we doubled green space? It gives results with a 95% confidence range.

7. Experiment Designer: Turns the best hypothesis into a real experiment plan. It tells you what to measure, what to control for, which statistical test to use, and how many samples you need.

8. Meta-Reviewer: Takes everything from all the agents and writes a final report. It includes citations from papers, the cause-and-effect graph, simulation results, experiment plans, and safety warnings.

Innovation and Uniqueness

No paid AI services needed. HypoForge uses only free tools like sentence-transformers, scikit-learn, and a custom causal discovery algorithm. You do not need OpenAI, Claude, or any other paid service.

Full hypothesis lifecycle. Most tools only do one thing like generate ideas or search papers. HypoForge does everything from literature search to experiment design in one pipeline.

Custom causal discovery engine. HypoForge has its own implementation of the PC algorithm. It finds cause-and-effect relationships in data, identifies confounders and mediators, and builds a visual graph. No external causal libraries needed.

Eight specialized agents. Instead of one big AI prompt, HypoForge uses 8 agents each with a specific job. This makes the system more reliable and each part can be improved independently.

Technology Stack

Python 3.12, Streamlit (user interface), FastAPI (REST API), scikit-learn (RandomForest for simulations), sentence-transformers (AI for searching papers), networkx (for causal graphs), ChromaDB (for storing paper summaries), pandas, numpy, scipy, arXiv API.

Architecture

Research Question + Data -> Literature Scout -> Data Analyst -> Hypothesis Generator -> Critic -> Evolver -> Simulator -> Experiment Designer -> Meta-Reviewer -> Ranked Hypotheses + Causal Graph + Simulations + Protocols + Report

Domain Examples

1. Urban Microclimate: "How does urban green space affect local air temperature and air quality?" Uses data with variables like temperature, green_space, traffic_density, surface_albedo, and PM2.5.

2. Environmental Health: "How does long-term exposure to air pollution and noise affect sleep quality?" Uses data with variables like sleep_quality, AQI, noise_level, and physical_activity.

3. Biodiversity and Climate: "How do temperature and precipitation changes affect species diversity?" Uses data with variables like species_richness, temperature, precipitation, and habitat_fragmentation.

Results and Validation

26 automated tests pass. All agents, the pipeline, data engine, causal discovery, and simulation are tested.

The pipeline generates 10 or more ranked hypotheses per run. Each hypothesis has scores for novelty, causal rigor, testability, and impact.

Causal graphs automatically find confounders and mediators from your data.

The ML simulator gives counterfactual predictions with 95% confidence intervals.

Experiment protocols include sample size estimates and recommended statistical tests.

How to Run

pip install -r requirements.txt
streamlit run src/ui/app.py

Open your browser, enter a research question, upload data if you have any, and click "Run Pipeline".

Deployment

Deployed on Streamlit Community Cloud. Connected to GitHub for automatic updates.

Repository

https://github.com/Amitk003/HypoForge

License

Open source.
