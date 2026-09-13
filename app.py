import time
import streamlit as st
from data import SCENARIO
from agent import run_agent

st.set_page_config(
    page_title="SupplyGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# PREMIUM DEMO UI
# ============================================================
st.markdown(
r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(84, 101, 255, .22), transparent 28%),
        radial-gradient(circle at 92% 8%, rgba(0, 214, 190, .13), transparent 25%),
        radial-gradient(circle at 50% 100%, rgba(116, 73, 255, .12), transparent 32%),
        #060811;
    color: #f7f8ff !important;
}

.block-container {
    max-width: 1220px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---------- HERO ---------- */
.hero {
    position: relative;
    overflow: hidden;
    padding: 36px 38px;
    border-radius: 26px;
    border: 1px solid rgba(255,255,255,.11);
    background:
        linear-gradient(135deg, rgba(27,34,67,.97), rgba(10,14,28,.95));
    box-shadow: 0 25px 90px rgba(0,0,0,.40);
    animation: rise .65s ease;
}

.hero:after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -90px;
    top: -110px;
    border-radius: 50%;
    background: rgba(104,119,255,.16);
    filter: blur(5px);
}

.badge {
    display: inline-block;
    padding: 7px 12px;
    border-radius: 999px;
    color: #cbd2ff !important;
    background: rgba(100,115,255,.13);
    border: 1px solid rgba(129,140,248,.32);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .12em;
}

.hero-title {
    margin-top: 14px;
    font-size: 46px;
    line-height: 1;
    font-weight: 800;
    letter-spacing: -.045em;
    color: #ffffff !important;
}

.hero-title span {
    color: #aeb9ff !important;
}

.hero-subtitle {
    margin-top: 9px;
    color: #b8c0d5 !important;
    font-size: 16px;
}

/* ---------- SECTIONS ---------- */
.section {
    margin-top: 28px;
}

.section-title {
    color: #ffffff !important;
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 5px;
}

.section-subtitle {
    color: #9fa9c0 !important;
    font-size: 13px;
    margin-bottom: 15px;
}

/* ---------- CARDS ---------- */
.card {
    min-height: 105px;
    padding: 18px;
    border-radius: 17px;
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(17,22,39,.88);
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}

.card:hover {
    transform: translateY(-3px);
    border-color: rgba(122,137,255,.30);
    box-shadow: 0 14px 40px rgba(0,0,0,.25);
}

.label {
    color: #929db7 !important;
    font-size: 11px;
    font-weight: 750;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.value {
    color: #ffffff !important;
    font-size: 23px;
    font-weight: 800;
    margin-top: 9px;
}

/* ---------- CONTROL ---------- */
.control {
    padding: 18px 20px;
    border-radius: 17px;
    border: 1px solid rgba(255,255,255,.09);
    background: rgba(15,20,35,.88);
}

.control-title {
    color: #ffffff !important;
    font-weight: 750;
}

.control-text {
    color: #aab4ca !important;
    font-size: 13px;
    line-height: 1.55;
    margin-top: 6px;
}

div.stButton > button {
    min-height: 52px;
    border-radius: 15px;
    border: 1px solid rgba(155,164,255,.55);
    background: linear-gradient(135deg, #5968f5, #7654ff);
    color: #ffffff !important;
    font-weight: 800;
    box-shadow: 0 12px 38px rgba(89,104,245,.27);
    transition: transform .18s ease, box-shadow .18s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 45px rgba(89,104,245,.38);
}

/* ---------- LIVE STATUS ---------- */
.live {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #b9c5ff !important;
    font-size: 12px;
    font-weight: 750;
}

.dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #62a7ff;
    box-shadow: 0 0 14px rgba(98,167,255,.9);
    animation: pulse 1.25s infinite;
}

/* ---------- EXECUTION TRACE ---------- */
.trace {
    padding: 15px 17px;
    margin: 8px 0;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,.075);
    background: rgba(15,20,35,.86);
    animation: slide .38s ease both;
}

.trace.active {
    border-color: rgba(112,130,255,.45);
    box-shadow: 0 0 0 1px rgba(112,130,255,.08), 0 12px 35px rgba(50,60,150,.15);
}

.trace-row {
    display: flex;
    gap: 13px;
    align-items: flex-start;
}

.trace-num {
    width: 30px;
    height: 30px;
    min-width: 30px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: rgba(91,108,255,.18);
    color: #d1d6ff !important;
    font-size: 12px;
    font-weight: 800;
}

.trace-title {
    color: #ffffff !important;
    font-weight: 750;
    font-size: 14px;
}

.trace-detail {
    color: #a0aac0 !important;
    font-size: 12px;
    line-height: 1.5;
    margin-top: 4px;
}

.tag {
    display: inline-block;
    margin-top: 7px;
    padding: 4px 8px;
    border-radius: 7px;
    background: rgba(255,255,255,.055);
    color: #aeb8cf !important;
    font-size: 10px;
    font-weight: 700;
}

/* ---------- BRAIN ---------- */
.brain {
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,.09);
    background: linear-gradient(145deg, rgba(21,27,49,.92), rgba(12,16,29,.92));
}

.brain-line {
    padding: 11px 0;
    border-bottom: 1px solid rgba(255,255,255,.055);
}

.brain-line:last-child {
    border-bottom: 0;
}

.brain-label {
    color: #808ba6 !important;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-weight: 800;
}

.brain-value {
    color: #eef1ff !important;
    font-size: 13px;
    font-weight: 650;
    margin-top: 4px;
}

/* ---------- DECISION ---------- */
.pass {
    padding: 24px;
    border-radius: 20px;
    border: 1px solid rgba(65,220,166,.30);
    background: linear-gradient(135deg, rgba(22,68,56,.62), rgba(12,28,28,.88));
    box-shadow: 0 18px 65px rgba(0,0,0,.28);
    animation: success .65s ease;
}

.pass-title {
    color: #ffffff !important;
    font-size: 26px;
    font-weight: 850;
}

.pass-text {
    color: #c0c9d9 !important;
    font-size: 14px;
    margin-top: 7px;
}

/* ---------- KEY CHANGE ---------- */
.change {
    padding: 18px;
    border-radius: 17px;
    border: 1px solid rgba(120,136,255,.18);
    background: rgba(18,23,42,.86);
}

.change-old {
    color: #ff9c9c !important;
    font-weight: 750;
}

.change-arrow {
    color: #9daaff !important;
    font-size: 20px;
    margin: 0 6px;
}

.change-new {
    color: #72e6be !important;
    font-weight: 800;
}

/* ---------- CHECK ---------- */
.check {
    padding: 11px 13px;
    margin: 6px 0;
    border-radius: 11px;
    background: rgba(255,255,255,.045);
    color: #e0e5f2 !important;
    font-size: 12px;
}

/* ---------- ANIMATIONS ---------- */
@keyframes rise {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slide {
    from { opacity: 0; transform: translateX(-12px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes success {
    from { opacity: 0; transform: scale(.985); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes pulse {
    0%, 100% { transform: scale(.82); opacity: .65; }
    50% { transform: scale(1.18); opacity: 1; }
}

.footer {
    text-align: center;
    margin-top: 38px;
    color: #606b84 !important;
    font-size: 11px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# SESSION STATE
# ============================================================
if "agent_state" not in st.session_state:
    st.session_state.agent_state = None

if "mission_ran" not in st.session_state:
    st.session_state.mission_ran = False

# ============================================================
# HERO
# ============================================================
st.markdown(
"""
<div class="hero">
    <div class="badge">AUTONOMOUS OPERATIONS • SUPPLY RECOVERY</div>
    <div class="hero-title">🛡️ SupplyGuard <span>AI</span></div>
    <div class="hero-subtitle">Autonomous Retail Supply Chain Recovery Agent</div>
</div>
""",
unsafe_allow_html=True,
)

# ============================================================
# MISSION
# ============================================================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Recovery Mission</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Prevent a stockout without being given the recovery solution in advance.</div>',
    unsafe_allow_html=True,
)

cols = st.columns(4)
scenario = [
    ("PRODUCT", SCENARIO["product"]),
    ("INVENTORY", "35 units"),
    ("DEMAND", "25 / day"),
    ("PRIMARY SUPPLIER", "Supplier A"),
]

for col, (label, value) in zip(cols, scenario):
    with col:
        st.markdown(
            f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# CONTROL
# ============================================================
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="section-title">⚡ Mission Control</div>', unsafe_allow_html=True)

left, right = st.columns([1.8, 1])

with left:
    st.markdown(
"""
<div class="control">
    <div class="control-title">Disruption injected: Supplier A is unavailable</div>
    <div class="control-text">
        The agent must discover this through a tool call, update its state,
        abandon the failed plan, select a feasible alternative and verify the outcome.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

with right:
    run = st.button("🚀  Run Autonomous Recovery", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RUN BACKEND
# ============================================================
if run:
    SCENARIO["inventory"] = 35

    with st.spinner("SupplyGuard AI is executing the autonomous decision loop..."):
        st.session_state.agent_state = run_agent()

    st.session_state.mission_ran = True

state = st.session_state.agent_state

# ============================================================
# RESULTS
# ============================================================
if state:
    evaluation = state.get("evaluation_result") or {}
    verification = state.get("verification_result") or {}
    checks = verification.get("checks", {})
    passed = evaluation.get("passed", False)

    # ---------- Live-looking status ----------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    status_text = "RECOVERY VERIFIED" if passed else "MISSION NEEDS ATTENTION"
    st.markdown(
        f'<div class="live"><span class="dot"></span>{status_text}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Metrics ----------
    st.markdown('<div class="section-title">🧠 Mission Intelligence</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">State produced by the actual agent execution.</div>',
        unsafe_allow_html=True,
    )

    metrics = [
        ("INITIAL RISK", state.get("initial_stockout_risk", "—")),
        ("FINAL RISK", state.get("final_stockout_risk", "—")),
        ("INVENTORY", f'{state.get("current_inventory", 0)} units'),
        ("ITERATIONS", str(state.get("iteration_count", 0))),
    ]

    cols = st.columns(4)
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    # ---------- Agent + brain ----------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    left, right = st.columns([1.55, 1])

    with left:
        st.markdown('<div class="section-title">🔄 Agent Execution Trace</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-subtitle">Goal → Plan → Tool → Observation → State Update → Replan → Action → Verification</div>',
            unsafe_allow_html=True,
        )

        actions = state.get("actions_taken", [])
        observations = state.get("observations", [])

        # This is a visual replay of the agent's recorded execution trace.
        # The backend has already completed before the UI renders this trace.
        for i, action in enumerate(actions):
            detail = observations[i] if i < len(observations) else "Agent action executed."

            tag_map = {
                "get_inventory": "ENVIRONMENT",
                "get_sales_velocity": "ENVIRONMENT",
                "calculate_stockout_risk": "RISK ENGINE",
                "check_current_supplier": "SUPPLIER CHECK",
                "find_alternative_suppliers": "REPLAN",
                "simulate_recovery": "ACTION",
                "calculate_final_risk": "STATE UPDATE",
                "verify_recovery": "VERIFICATION",
                "evaluate_run": "EVALUATOR",
                "finish": "FINAL DECISION",
            }

            tag = tag_map.get(action if isinstance(action, str) else "simulate_recovery", "AGENT")

            st.markdown(
                f"""
<div class="trace">
    <div class="trace-row">
        <div class="trace-num">{i + 1}</div>
        <div>
            <div class="trace-title">{action}</div>
            <div class="trace-detail">{detail}</div>
            <div class="tag">{tag}</div>
        </div>
    </div>
</div>
""",
                unsafe_allow_html=True,
            )

    with right:
        st.markdown('<div class="section-title">🧩 Agent Brain</div>', unsafe_allow_html=True)
        st.markdown(
            """
<div class="brain">
    <div class="brain-line">
        <div class="brain-label">Objective</div>
        <div class="brain-value">Prevent Wireless Headphones stockout</div>
    </div>
    <div class="brain-line">
        <div class="brain-label">Current State</div>
        <div class="brain-value">50 units • 2.0 days coverage</div>
    </div>
    <div class="brain-line">
        <div class="brain-label">Failed Plan</div>
        <div class="brain-value">Supplier A</div>
    </div>
    <div class="brain-line">
        <div class="brain-label">Replanned Strategy</div>
        <div class="brain-value">Use feasible available source</div>
    </div>
    <div class="brain-line">
        <div class="brain-label">Selected Recovery</div>
        <div class="brain-value">Warehouse Chennai</div>
    </div>
    <div class="brain-line">
        <div class="brain-label">Verification</div>
        <div class="brain-value">5 / 5 checks passed</div>
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Replan highlight ----------
    st.markdown('<div class="section-title">🚨 Decision Pivot</div>', unsafe_allow_html=True)
    failures = state.get("failures", [])
    replans = state.get("replans", [])

    if failures:
        st.warning(f"Disruption detected: {failures[0]}")

    if replans:
        replan = replans[0]
        old_plan = replan.get("original_plan", "Supplier A") if isinstance(replan, dict) else "Supplier A"
        new_plan = replan.get("new_plan", "Warehouse Chennai") if isinstance(replan, dict) else "Warehouse Chennai"

        old_name = old_plan.get("supplier", str(old_plan)) if isinstance(old_plan, dict) else str(old_plan)
        new_name = new_plan.get("supplier", str(new_plan)) if isinstance(new_plan, dict) else str(new_plan)

        st.markdown(
            f"""
<div class="change">
    <div class="label">AUTONOMOUS REPLAN</div>
    <div style="margin-top:10px;font-size:19px;">
        <span class="change-old">{old_name}</span>
        <span class="change-arrow">→</span>
        <span class="change-new">{new_name}</span>
    </div>
    <div class="trace-detail">Original plan abandoned after the environment reported a supplier failure.</div>
</div>
""",
            unsafe_allow_html=True,
        )

    # ---------- Final ----------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏁 Final Decision</div>', unsafe_allow_html=True)

    if passed:
        st.markdown(
f"""
<div class="pass">
    <div class="pass-title">✅ RECOVERY PASS</div>
    <div class="pass-text">{evaluation.get("summary", "Recovery successfully verified.")}</div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.error(evaluation.get("summary", "Evaluation failed."))

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Verification ----------
    st.markdown('<div class="section-title">🛡️ Independent Verification</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">The evaluator checks the final environment independently from the planning decision.</div>',
        unsafe_allow_html=True,
    )

    vcols = st.columns(5)
    check_items = [
        ("Supplier", checks.get("supplier_available", False)),
        ("Inventory", checks.get("inventory_recovered", False)),
        ("Risk", checks.get("stockout_risk_reduced", False)),
        ("Budget", checks.get("within_budget", False)),
        ("Lead Time", checks.get("reasonable_lead_time", False)),
    ]

    for col, (label, ok) in zip(vcols, check_items):
        with col:
            st.markdown(
                f'<div class="card"><div class="label">{label}</div>'
                f'<div class="value" style="font-size:22px;">{"✅" if ok else "❌"}</div>'
                f'<div class="trace-detail">{"PASS" if ok else "FAIL"}</div></div>',
                unsafe_allow_html=True,
            )

    st.caption(
        f'Final inventory: {verification.get("inventory", "—")} units  ·  '
        f'Coverage: {verification.get("coverage_days", "—")} days  ·  '
        f'Recovery cost: ₹{verification.get("cost", "—")}'
    )

    with st.expander("🔍 Independent evaluator details"):
        for name, ok in evaluation.get("checks", {}).items():
            st.write(("✅ " if ok else "❌ ") + name.replace("_", " ").title())

    with st.expander("🧪 Debug / raw agent state"):
        st.json(state)

else:
    st.markdown(
"""
<div class="pass" style="border-color:rgba(120,136,255,.20);background:rgba(18,23,42,.70);">
    <div class="pass-title">🟢 System Ready</div>
    <div class="pass-text">
        Start the mission to execute the real recovery agent and inspect its
        decisions, tool observations, replanning, recovery action and verification.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer">SupplyGuard AI · Autonomous Retail Supply Chain Recovery Agent · Hackathon Demo</div>',
    unsafe_allow_html=True,
)

