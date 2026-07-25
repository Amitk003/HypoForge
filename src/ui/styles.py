FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

CUSTOM_CSS = """
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
    margin-right: 6px;
    margin-bottom: 4px;
}
.score-pill--high { border-color: #0D9488; }
.score-pill--low { border-color: #D97706; }
.score-value {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}

/* === Info Pills (confounders/mediators) === */
.pill {
    display: inline-block;
    border-radius: 9999px;
    padding: 4px 12px;
    font-size: 12px;
    margin-right: 8px;
    margin-bottom: 4px;
}
.pill--info {
    background: #EFF6FF;
    color: #1E40AF;
    border: 1px solid #BFDBFE;
}

/* === Pipeline Stepper === */
.hf-stepper { display: flex; align-items: center; gap: 0; margin: 24px 0; flex-wrap: nowrap; overflow-x: auto; }
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
    min-width: 16px;
}
.hf-step-line--complete { background: #0D9488; }
.hf-step-label {
    font-size: 10px; color: #475569;
    text-align: center; margin-top: 4px;
    max-width: 100px;
    line-height: 1.2;
}

/* === Print Styles === */
@media print {
    .stTabs, header, .stDeployButton { display: none !important; }
    .block-container { max-width: 100% !important; padding: 0 !important; }
}
"""
