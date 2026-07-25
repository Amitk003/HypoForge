FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'

CUSTOM_CSS = """
/* === Base === */
.stApp { font-family: 'Inter', sans-serif; }

/* === Header === */
.hf-header {
    display: flex; flex-direction: column;
    margin-bottom: 8px;
}
.hf-header-title {
    font-family: 'Inter', sans-serif;
    font-weight: 600; font-size: 20px;
    color: #0F172A; margin: 0;
}
.hf-header-subtitle {
    font-family: 'Inter', sans-serif;
    font-weight: 400; font-size: 12px;
    color: #94A3B8; margin: 0;
}
.hf-header-goal {
    font-family: 'Inter', sans-serif;
    font-size: 13px; color: #475569;
    margin-top: 4px;
    white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
    max-width: 600px;
}

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
    padding: 3px 8px;
    font-size: 11px;
    font-family: 'Inter', sans-serif;
    color: #475569;
    margin-right: 4px;
    margin-bottom: 2px;
    white-space: nowrap;
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
    max-width: 80px;
    line-height: 1.2;
}
.hf-step-label--error { color: #DC2626; font-weight: 500; }

/* === Simulation Result Inline === */
.hf-sim-result {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 13px;
}
.hf-sim-result strong { color: #0F172A; }
.hf-sim-delta-pos { color: #0D9488; font-weight: 600; }
.hf-sim-delta-neg { color: #DC2626; font-weight: 600; }

/* === Protocol Inline === */
.hf-protocol {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 16px;
    margin: 8px 0;
}
.hf-protocol-header {
    font-weight: 600; font-size: 13px; color: #0F172A;
    margin-bottom: 8px;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 6px;
}
.hf-protocol-meta {
    font-size: 12px; color: #475569;
    margin-bottom: 8px;
}
.hf-protocol-steps {
    font-size: 13px; color: #0F172A;
    line-height: 1.6;
}
.hf-protocol-steps ol {
    margin: 4px 0;
    padding-left: 20px;
}
.hf-protocol-steps li {
    margin-bottom: 4px;
}

/* === Section Dividers === */
.hf-divider {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 16px 0;
}

/* === Print Styles === */
@media print {
    .stTabs, header, .stDeployButton { display: none !important; }
    .block-container { max-width: 100% !important; padding: 0 !important; }
}
"""
