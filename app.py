import streamlit as st
import pandas as pd

from database import list_incidents
from rca_engine import investigate, learn_from_incident


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="IncidentMind",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
    radial-gradient(circle at 10% 10%, rgba(77, 91, 255, .18), transparent 28%),
    radial-gradient(circle at 90% 20%, rgba(0, 220, 180, .13), transparent 25%),
    linear-gradient(135deg,#070b18 0%,#0d1326 50%,#10152b 100%);
    color:#eef2ff;
}

.block-container {
    padding-top:1.8rem;
    max-width:1450px;
}

h1,h2,h3,h4 {
    color:#f8fafc;
}

.hero {
    padding:28px;
    border:1px solid rgba(255,255,255,.10);
    border-radius:22px;
    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,.25),
            rgba(16,185,129,.10)
        );
    box-shadow:0 18px 60px rgba(0,0,0,.25);
    margin-bottom:20px;
}

.card {
    padding:20px;
    border-radius:18px;
    background:rgba(255,255,255,.055);
    border:1px solid rgba(255,255,255,.09);
    margin-bottom:14px;
}

.memory-card {
    padding:22px;
    border-radius:18px;
    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,.18),
            rgba(16,185,129,.10)
        );
    border:1px solid rgba(129,140,248,.35);
    margin-bottom:14px;
}

.rca {
    padding:26px;
    border-radius:22px;
    background:
        linear-gradient(
            135deg,
            rgba(16,185,129,.20),
            rgba(59,130,246,.12)
        );
    border:1px solid rgba(52,211,153,.35);
    margin-bottom:18px;
}

.problem-box {
    padding:24px;
    border-radius:20px;
    background:rgba(239,68,68,.09);
    border:1px solid rgba(248,113,113,.30);
}

.success-box {
    padding:24px;
    border-radius:20px;
    background:rgba(16,185,129,.10);
    border:1px solid rgba(52,211,153,.35);
}

.off-box {
    padding:22px;
    border-radius:20px;
    background:rgba(239,68,68,.08);
    border:1px solid rgba(248,113,113,.25);
}

.small {
    color:#94a3b8;
    font-size:.9rem;
}

.metric {
    font-size:1.7rem;
    font-weight:800;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

<h1>🧠 IncidentMind</h1>

<p style="font-size:1.25rem">
Hindsight-powered Incident Response Agent
</p>

<p class="small">
Current evidence → Hindsight → RCA → Engineer validation → RETAIN → Future learning
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD INCIDENTS
# ============================================================

try:

    incidents = list_incidents()

except Exception as e:

    st.error(
        f"Could not load incidents: {e}"
    )

    st.stop()


ids = incidents.incident_id.tolist()

if not ids:

    st.error("No incidents found.")

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🚨 Incident Control")

    default_index = (
        ids.index("INC-1012")
        if "INC-1012" in ids
        else 0
    )

    iid = st.selectbox(
        "Incident ID",
        ids,
        index=default_index
    )

    st.divider()

    st.subheader("🧠 Hindsight")

    hindsight_on = st.toggle(
        "Enable Hindsight",
        value=False
    )

    if hindsight_on:

        st.success(
            "Hindsight ON\n\n"
            "Relevant learned experience will be used."
        )

    else:

        st.warning(
            "Hindsight OFF\n\n"
            "RCA uses current incident evidence only."
        )

    st.divider()

    st.caption(
        "Hindsight ON adds relevant validated experience "
        "to the current investigation."
    )


# ============================================================
# INVESTIGATION
# ============================================================

investigation_key = (
    f"{iid}_{hindsight_on}"
)

if (
    "result" not in st.session_state
    or st.session_state.get("investigation_key")
    != investigation_key
):

    with st.spinner(
        "Investigating incident..."
    ):

        st.session_state.result = investigate(
            iid,
            use_hindsight=hindsight_on
        )

    st.session_state.investigation_key = (
        investigation_key
    )

    st.session_state.learning_saved = False


r = st.session_state.result

inc = r["incident"]


# ============================================================
# TOP METRICS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.markdown(
    f"""
    <div class="card">
        <div class="small">INCIDENT</div>
        <div class="metric">{iid}</div>
    </div>
    """,
    unsafe_allow_html=True
)


c2.markdown(
    f"""
    <div class="card">
        <div class="small">SERVICE</div>
        <div class="metric">{inc["service"]}</div>
    </div>
    """,
    unsafe_allow_html=True
)


c3.markdown(
    f"""
    <div class="card">
        <div class="small">HINDSIGHT</div>
        <div class="metric">
            {"ON" if hindsight_on else "OFF"}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


c4.markdown(
    f"""
    <div class="card">
        <div class="small">RCA SCORE</div>
        <div class="metric">
            {r["rca"]["score"]}%
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🎬 RCA Demo",
        "🔎 Investigation",
        "🧠 Hindsight",
        "📊 Evaluation"
    ]
)


# ============================================================
# TAB 1 — RCA DEMO
# ============================================================

with tab1:

    st.header(
        "🎯 Incident Root Cause Analysis"
    )

    st.caption(
        "Toggle Hindsight from the left sidebar to compare "
        "current-evidence reasoning with learned operational experience."
    )


    # --------------------------------------------------------
    # CURRENT INCIDENT
    # --------------------------------------------------------

    st.subheader("🚨 Current Incident")

    st.markdown(
        f"""
        <div class="problem-box">

        <b>INCIDENT</b>

        <h2>{iid}</h2>

        <p>
        <b>Service:</b>
        {inc["service"]}
        </p>

        <p>
        <b>Symptom:</b>
        {inc["symptom"]}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # CURRENT EVIDENCE
    # --------------------------------------------------------

    st.subheader(
        "🔎 Current Incident Evidence"
    )

    evidence_cols = st.columns(4)

    evidence_items = [

        (
            "📜 Logs",
            r["logs"][0]["message"]
            if r.get("logs")
            else "No log available"
        ),

        (
            "📈 Metrics",
            r["metrics"][0]["value"]
            if r.get("metrics")
            else "No metric available"
        ),

        (
            "🚀 Deployment",
            r["deployments"][0]["change_summary"]
            if r.get("deployments")
            else "No deployment available"
        ),

        (
            "💻 Code",
            r["code_changes"][0]["change"]
            if r.get("code_changes")
            else "No code change available"
        )
    ]

    for col, (title, value) in zip(
        evidence_cols,
        evidence_items
    ):

        col.markdown(
            f"""
            <div class="card">

            <b>{title}</b>

            <br><br>

            <span class="small">
            {value}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # HINDSIGHT OFF
    # ========================================================

    if not hindsight_on:

        st.subheader(
            "🧠 Hindsight OFF"
        )

        st.markdown(
            """
            <div class="off-box">

            <h3>Current evidence only</h3>

            <p>
            The agent is investigating this incident without
            retrieving previous operational experience.
            </p>

            <p>
            The RCA is based on the logs, metrics,
            deployment information and code changes
            available in the current incident.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.subheader(
            "🎯 Current-Evidence RCA"
        )

        st.markdown(
            f"""
            <div class="rca">

            <h2>
            {r["rca"]["root_cause"]}
            </h2>

            <p>
            <b>RCA confidence:</b>
            {r["rca"]["score"]}%
            </p>

            <p>
            <b>Confidence level:</b>
            {r["confidence"]}
            </p>

            <p>
            <b>Recommended remediation:</b>
            {r["rca"]["fix"]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        if r.get("candidates"):

            st.subheader(
                "Possible RCA Patterns"
            )

            candidate_df = pd.DataFrame(
                r["candidates"]
            )

            display_columns = [
                x
                for x in [
                    "pattern",
                    "score",
                    "hits"
                ]
                if x in candidate_df.columns
            ]

            if display_columns:

                st.dataframe(
                    candidate_df[
                        display_columns
                    ],
                    use_container_width=True,
                    hide_index=True
                )


        st.info(
            "Turn Hindsight ON from the sidebar to add "
            "relevant validated experience."
        )


    # ========================================================
    # HINDSIGHT ON
    # ========================================================

    else:

        st.subheader(
            "🧠 Hindsight ON"
        )

        st.markdown(
            """
            <div class="success-box">

            <h3>Relevant operational experience recalled</h3>

            <p>
            Hindsight is now available to support the current
            investigation with previously validated learning.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # STRUCTURED EXPERIENCE
        # ----------------------------------------------------

        experience = r.get(
            "hindsight_experience"
        )

        if experience:

            st.subheader(
                "💡 Recalled Experience"
            )

            st.markdown(
                f"""
                <div class="memory-card">

                <h3>
                {experience["title"]}
                </h3>

                <p>
                <b>Failure pattern:</b>
                {experience["pattern"]}
                </p>

                <p>
                <b>Learned relationship:</b>
                {experience["learning"]}
                </p>

                <p>
                <b>Recommended action from experience:</b>
                {experience["action"]}
                </p>

                <p>
                <b>Impact on RCA:</b>
                {experience["relevance"]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No sufficiently relevant Hindsight experience "
                "was found for this incident."
            )


        # ----------------------------------------------------
        # HINDSIGHT RCA
        # ----------------------------------------------------

        st.subheader(
            "🎯 Hindsight-Assisted RCA"
        )

        st.markdown(
            f"""
            <div class="rca">

            <h2>
            {r["rca"]["root_cause"]}
            </h2>

            <p>
            <b>Current evidence score:</b>
            {r["base_score"]}%
            </p>

            <p>
            <b>Hindsight-assisted score:</b>
            {r["rca"]["score"]}%
            </p>

            <p>
            <b>Confidence level:</b>
            {r["confidence"]}
            </p>

            <p>
            <b>Recommended remediation:</b>
            {r["rca"]["fix"]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # WHY THIS RCA?
        # ----------------------------------------------------

        if r.get("rca", {}).get("hits"):

            st.subheader(
                "🔍 Why did the agent choose this RCA?"
            )

            for hit in r["rca"]["hits"]:

                st.success(
                    f"Current evidence: {hit}"
                )

        if r.get("hindsight_used"):

            st.info(
                f"Hindsight contributed "
                f"+{r['hindsight_boost']} confidence points "
                f"because relevant validated experience matched "
                f"the current failure pattern."
            )


        # ----------------------------------------------------
        # ENGINEER VALIDATION
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "👨‍💻 Engineer Validation"
        )

        feedback = st.text_area(
            "Validate or correct this RCA",
            placeholder=(
                "Example: Confirmed. The deployment reduced "
                "the connection pool limit and caused exhaustion."
            ),
            key="demo_feedback"
        )


        if st.button(
            "💾 RETAIN LEARNING",
            type="primary",
            use_container_width=True
        ):

            if not feedback.strip():

                st.warning(
                    "Enter engineer feedback first."
                )

            else:

                with st.spinner(
                    "Retaining validated learning..."
                ):

                    msg = learn_from_incident(
                        iid,
                        feedback.strip()
                    )

                st.session_state.learning_saved = True

                st.success(
                    "Engineer-validated learning retained."
                )

                st.markdown(
                    """
                    <div class="success-box">

                    <h3>
                    🧠 Hindsight RETAIN
                    </h3>

                    <p>
                    ✓ Engineer feedback stored
                    </p>

                    <p>
                    ✓ Validated RCA stored
                    </p>

                    <p>
                    ✓ Failure pattern stored
                    </p>

                    <p>
                    ✓ Future investigations can use this experience
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # LEARNING LOOP
    # ========================================================

    if st.session_state.get(
        "learning_saved",
        False
    ):

        st.divider()

        st.subheader(
            "🔄 Continuous Learning Loop"
        )

        cols = st.columns(6)

        steps = [
            "🚨 Incident",
            "🔎 Evidence",
            "🧠 Recall",
            "🎯 RCA",
            "👨‍💻 Validate",
            "💾 RETAIN"
        ]

        for col, step in zip(
            cols,
            steps
        ):

            col.markdown(
                f"""
                <div class="card"
                     style="text-align:center">

                <b>{step}</b>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# TAB 2 — INVESTIGATION
# ============================================================

with tab2:

    st.header(
        f"🔎 Investigation · {iid}"
    )

    cols = st.columns(5)

    labels = [
        "Incident",
        "Logs",
        "Metrics",
        "Deployment",
        "Code"
    ]

    vals = [

        inc["symptom"],

        r["logs"][0]["message"]
        if r.get("logs")
        else "N/A",

        r["metrics"][0]["value"]
        if r.get("metrics")
        else "N/A",

        r["deployments"][0]["change_summary"]
        if r.get("deployments")
        else "N/A",

        r["code_changes"][0]["change"]
        if r.get("code_changes")
        else "N/A"
    ]

    for col, label, val in zip(
        cols,
        labels,
        vals
    ):

        col.markdown(
            f"""
            <div class="card">

            <b>{label}</b>

            <br><br>

            <span class="small">
            {val}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.subheader(
        "Evidence"
    )

    if r.get("evidence"):

        st.dataframe(
            pd.DataFrame(
                r["evidence"]
            ),
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# TAB 3 — HINDSIGHT
# ============================================================

with tab3:

    st.header(
        "🧠 Hindsight"
    )

    if hindsight_on:

        st.success(
            "Hindsight is currently ON."
        )

        experience = r.get(
            "hindsight_experience"
        )

        if experience:

            st.subheader(
                "Recalled Operational Experience"
            )

            st.markdown(
                f"""
                <div class="memory-card">

                <h3>
                {experience["title"]}
                </h3>

                <p>
                <b>Failure pattern:</b>
                {experience["pattern"]}
                </p>

                <p>
                <b>Learned relationship:</b>
                {experience["learning"]}
                </p>

                <p>
                <b>Recommended action:</b>
                {experience["action"]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "No relevant experience found."
            )

    else:

        st.warning(
            "Hindsight is currently OFF."
        )

        st.info(
            "Turn Hindsight ON from the left sidebar "
            "to retrieve relevant learned experience."
        )


    st.divider()

    st.subheader(
        "RETAIN"
    )

    if st.session_state.get(
        "learning_saved",
        False
    ):

        st.success(
            "✓ Engineer-validated learning was retained."
        )

    else:

        st.info(
            "No new learning has been retained during this session."
        )


    st.divider()

    st.subheader(
        "Learning Architecture"
    )

    st.markdown(
        """
```text
                 INCIDENT
                     │
                     ▼
             CURRENT EVIDENCE
                     │
                     ▼
              HINDSIGHT ON?
                /        \\
              NO          YES
              │             │
              ▼             ▼
        Evidence-only    RECALL
              │             │
              │             ▼
              │      Learned Experience
              │             │
              └──────┬──────┘
                     ▼
                    RCA
                     │
                     ▼
             Engineer validates
                     │
                     ▼
                  RETAIN
                     │
                     ▼
             Future investigations
    """
)

