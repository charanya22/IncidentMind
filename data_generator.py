from pathlib import Path
import duckdb
import pandas as pd
import random

DB_PATH = Path("data/incidentmind.duckdb")
DB_PATH.parent.mkdir(exist_ok=True)

PATTERNS = {
    "db_pool": {
        "service": "payment-service",
        "symptom": "HTTP 500",
        "root_cause": "Database connection pool exhaustion caused by a deployment configuration change",
        "code_change": "max_connections changed from 50 to 10",
        "deployment": "Reduced database connection pool configuration",
        "log_pattern": "database connection pool exhausted",
        "metric_pattern": "db connection utilization reached 100%",
        "fix": "Restore max_connections to 50 and redeploy",
    },
    "cache": {
        "service": "order-service",
        "symptom": "high latency",
        "root_cause": "Cache eviction spike caused by an undersized cache configuration",
        "code_change": "cache_max_entries changed from 100000 to 20000",
        "deployment": "Reduced cache capacity",
        "log_pattern": "cache eviction rate above threshold",
        "metric_pattern": "cache hit ratio dropped below 20%",
        "fix": "Restore cache capacity and redeploy",
    },
    "auth_timeout": {
        "service": "auth-service",
        "symptom": "login timeout",
        "root_cause": "Authentication service timeout caused by an upstream identity-provider timeout configuration",
        "code_change": "idp_timeout changed from 5s to 1s",
        "deployment": "Reduced identity-provider timeout",
        "log_pattern": "upstream identity provider timeout",
        "metric_pattern": "authentication request timeout rate increased",
        "fix": "Restore idp_timeout to 5s and redeploy",
    },
    "queue": {
        "service": "order-service",
        "symptom": "message backlog",
        "root_cause": "Order processing backlog caused by a consumer concurrency reduction",
        "code_change": "consumer_concurrency changed from 20 to 5",
        "deployment": "Reduced queue consumer concurrency",
        "log_pattern": "consumer lag increasing",
        "metric_pattern": "queue depth exceeded 10000",
        "fix": "Restore consumer concurrency to 20 and redeploy",
    },
}

def make_rows():
    incidents, deployments, logs, metrics, code_changes, resolutions = [], [], [], [], [], []
    random.seed(7)

    # Hand-crafted incidents used in the live demo.
    demo = [
        ("INC-1001","payment-service","database timeout","db_pool","resolved"),
        ("INC-1002","auth-service","login failure","auth_timeout","resolved"),
        ("INC-1003","order-service","high latency","cache","resolved"),
        ("INC-1010","payment-service","database timeout","db_pool","resolved"),
        ("INC-1012","payment-service","HTTP 500","db_pool","investigating"),
        ("INC-1057","payment-service","HTTP 500","db_pool","investigating"),
    ]
    for idx,(iid,svc,symptom,pkey,status) in enumerate(demo):
        p=PATTERNS[pkey]
        incidents.append({
            "incident_id":iid,"service":svc,"severity":"SEV-1" if svc=="payment-service" else "SEV-2",
            "symptom":symptom,"status":status,"pattern":pkey
        })
        version = "v2.4.1" if pkey=="db_pool" else f"v{2+idx//2}.1.{idx+1}"
        deployments.append({"incident_id":iid,"service":svc,"version":version,
                            "change_summary":p["deployment"],"minutes_before":8})
        logs.append({"incident_id":iid,"service":svc,"level":"ERROR","message":p["log_pattern"]})
        metrics.append({"incident_id":iid,"service":svc,"metric":"primary_failure_signal",
                        "value":p["metric_pattern"]})
        code_changes.append({"incident_id":iid,"service":svc,"commit":f"demo{idx:04d}",
                             "file":"config/service.yaml","change":p["code_change"]})
        resolutions.append({"incident_id":iid,"root_cause":p["root_cause"],"fix":p["fix"],
                            "validated":status=="resolved"})

    # 100-incident benchmark. Exactly 99 have complete evidence.
    pattern_keys=list(PATTERNS)
    for n in range(1,101):
        iid=f"EVAL-{n:03d}"
        pkey=pattern_keys[(n-1)%len(pattern_keys)]
        p=PATTERNS[pkey]
        incomplete = (n==100)  # intentionally ambiguous test case
        incidents.append({"incident_id":iid,"service":p["service"],"severity":"SEV-2",
                          "symptom":p["symptom"],"status":"resolved","pattern":pkey})
        deployments.append({"incident_id":iid,"service":p["service"],"version":f"v3.{n%10}.{n%7}",
                            "change_summary":p["deployment"] if not incomplete else "Routine deployment",
                            "minutes_before":8 if not incomplete else 60})
        logs.append({"incident_id":iid,"service":p["service"],"level":"ERROR",
                     "message":p["log_pattern"] if not incomplete else "generic service error"})
        metrics.append({"incident_id":iid,"service":p["service"],"metric":"primary_failure_signal",
                        "value":p["metric_pattern"] if not incomplete else "metric within normal range"})
        code_changes.append({"incident_id":iid,"service":p["service"],"commit":f"eval{n:04d}",
                             "file":"config/service.yaml",
                             "change":p["code_change"] if not incomplete else "documentation-only change"})
        resolutions.append({"incident_id":iid,"root_cause":p["root_cause"],"fix":p["fix"],
                            "validated":not incomplete})

    return {
        "incidents":pd.DataFrame(incidents),
        "deployments":pd.DataFrame(deployments),
        "logs":pd.DataFrame(logs),
        "metrics":pd.DataFrame(metrics),
        "code_changes":pd.DataFrame(code_changes),
        "resolutions":pd.DataFrame(resolutions),
    }

def main():
    tables=make_rows()
    con=duckdb.connect(str(DB_PATH))
    for name,df in tables.items():
        con.execute(f"DROP TABLE IF EXISTS {name}")
        con.register(f"df_{name}",df)
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM df_{name}")
        con.unregister(f"df_{name}")
    con.close()
    print(f"Created {DB_PATH}")
    print(f"Benchmark incidents: 100; intended correct cases: 99")

if __name__=="__main__":
    main()
