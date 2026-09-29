from database import (
    get_incident,
    get_logs,
    get_metrics,
    get_deployments,
    get_code_changes,
    get_resolution
)

from hindsight_memory import Memory


# ============================================================
# RCA PATTERN RULES
# ============================================================

PATTERN_RULES = {
    "db_pool": {
        "keywords": [
            "connection pool",
            "max_connections",
            "db connection",
            "database timeout",
            "100%"
        ],
        "root_cause":
            "Database connection pool exhaustion caused by a deployment configuration change",
        "fix":
            "Restore max_connections to 50 and redeploy"
    },

    "cache": {
        "keywords": [
            "cache",
            "eviction",
            "hit ratio",
            "cache_max_entries"
        ],
        "root_cause":
            "Cache eviction spike caused by an undersized cache configuration",
        "fix":
            "Restore cache capacity and redeploy"
    },

    "auth_timeout": {
        "keywords": [
            "identity provider",
            "idp_timeout",
            "authentication",
            "login timeout"
        ],
        "root_cause":
            "Authentication service timeout caused by an upstream identity-provider timeout configuration",
        "fix":
            "Restore idp_timeout to 5s and redeploy"
    },

    "queue": {
        "keywords": [
            "consumer",
            "concurrency",
            "queue",
            "lag",
            "backlog"
        ],
        "root_cause":
            "Order processing backlog caused by a consumer concurrency reduction",
        "fix":
            "Restore consumer concurrency to 20 and redeploy"
    },
}


# ============================================================
# INVESTIGATION
# ============================================================

def investigate(iid, use_hindsight=True):

    incident = get_incident(iid)

    if not incident:
        raise ValueError(f"Unknown incident: {iid}")

    logs = get_logs(iid)
    metrics = get_metrics(iid)
    deployments = get_deployments(iid)
    changes = get_code_changes(iid)
    resolution = get_resolution(iid)

    # --------------------------------------------------------
    # CURRENT INCIDENT EVIDENCE
    # --------------------------------------------------------

    evidence_text = " ".join([
        str(incident),
        str(logs),
        str(metrics),
        str(deployments),
        str(changes)
    ]).lower()

    # --------------------------------------------------------
    # GENERATE RCA CANDIDATES
    # --------------------------------------------------------

    candidates = []

    for pkey, rule in PATTERN_RULES.items():

        hits = [
            keyword
            for keyword in rule["keywords"]
            if keyword.lower() in evidence_text
        ]

        evidence_ratio = (
            len(hits) /
            max(1, len(rule["keywords"]))
        )

        score = round(evidence_ratio * 70)

        # Deployment evidence gives additional support.
        if deployments and "change" in str(deployments).lower():
            score += 20

        score = min(99, score)

        candidates.append({
            "pattern": pkey,
            "score": score,
            "hits": hits,
            "root_cause": rule["root_cause"],
            "fix": rule["fix"]
        })

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    top = candidates[0]

    # Save the score BEFORE Hindsight.
    base_score = top["score"]

    # ========================================================
    # HINDSIGHT
    # ========================================================

    memories = []

    hindsight_used = False
    hindsight_boost = 0

    if use_hindsight:

        memory = Memory()

        query = (
            f"{incident['service']} "
            f"{incident['symptom']} "
            f"deployment configuration "
            f"{top['pattern']}"
        )

        memories = memory.recall(query)

        # ----------------------------------------------------
        # Check whether recalled experience is actually
        # relevant to the current RCA pattern.
        # ----------------------------------------------------

        memory_text = " ".join(
            str(m.get("text", ""))
            for m in memories
        ).lower()

        relevant = False

        for keyword in PATTERN_RULES[top["pattern"]]["keywords"]:

            if keyword.lower() in memory_text:
                relevant = True
                break

        if relevant:

            hindsight_used = True

            # Hindsight supports existing evidence.
            # It does NOT create a root cause by itself.
            hindsight_boost = min(
                15,
                max(5, len(memories) * 5)
            )

            top["score"] = min(
                99,
                base_score + hindsight_boost
            )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    if top["score"] >= 85:
        confidence = "HIGH"

    elif top["score"] >= 65:
        confidence = "MEDIUM"

    else:
        confidence = "LOW"

    # ========================================================
    # CURRENT EVIDENCE
    # ========================================================

    evidence = [

        {
            "label": "Incident symptom",
            "value": incident["symptom"],
            "strength": True
        },

        {
            "label": "Error logs",
            "value":
                logs[0]["message"]
                if logs
                else "No logs",
            "strength": bool(logs)
        },

        {
            "label": "Metrics",
            "value":
                metrics[0]["value"]
                if metrics
                else "No metrics",
            "strength": bool(metrics)
        },

        {
            "label": "Deployment",
            "value":
                deployments[0]["change_summary"]
                if deployments
                else "No deployment",
            "strength": bool(deployments)
        },

        {
            "label": "Code change",
            "value":
                changes[0]["change"]
                if changes
                else "No code change",
            "strength": bool(changes)
        }
    ]

    # ========================================================
    # STRUCTURED HINDSIGHT EXPERIENCE
    # ========================================================

    hindsight_experience = None

    if hindsight_used:

        rule = PATTERN_RULES[top["pattern"]]

        hindsight_experience = {
            "pattern": top["pattern"],
            "title": "Relevant learned experience",
            "signals": rule["keywords"],
            "learning": (
                f"Previous validated experience indicates that "
                f"this failure pattern is associated with: "
                f"{rule['root_cause']}."
            ),
            "action": rule["fix"],
            "relevance": f"+{hindsight_boost} confidence points"
        }

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "incident": incident,

        "logs": logs,

        "metrics": metrics,

        "deployments": deployments,

        "code_changes": changes,

        "resolution": resolution,

        "candidates": candidates,

        "rca": top,

        "confidence": confidence,

        # Raw memory is retained internally,
        # but the UI can use hindsight_experience
        # instead of displaying old incident text.
        "memories": memories,

        "hindsight_experience":
            hindsight_experience,

        "hindsight_used":
            hindsight_used,

        "hindsight_boost":
            hindsight_boost,

        "base_score":
            base_score,

        "evidence":
            evidence,

        "memory_mode":
            Memory().mode
    }


# ============================================================
# LEARN FROM ENGINEER FEEDBACK
# ============================================================

def learn_from_incident(iid, feedback):

    # Use current evidence to establish the validated RCA.
    result = investigate(
        iid,
        use_hindsight=False
    )

    content = (

        f"Validated incident learning. "

        f"Service={result['incident']['service']}. "

        f"Symptom={result['incident']['symptom']}. "

        f"Failure pattern={result['rca']['pattern']}. "

        f"Validated root cause="
        f"{result['rca']['root_cause']}. "

        f"Recommended remediation="
        f"{result['rca']['fix']}. "

        f"Engineer feedback={feedback}. "

        f"This represents validated operational experience "
        f"that can support future investigations of similar "
        f"failure patterns."
    )

    Memory().retain(
        content,
        context="validated incident post-mortem and engineer feedback"
    )

    return content