from hindsight_memory import Memory

SEED=[
"""Historical validated incident INC-1001: payment-service database timeout.
Root cause was database connection pool exhaustion after a deployment configuration change.
Engineer learning: when payment-service shows database timeouts after deployment, check deployment configuration
and connection pool settings before blaming database infrastructure.""",
"""Historical validated incident INC-1010: payment-service database timeout.
The deployment reduced max_connections from 50 to 10. Logs showed connection pool exhaustion and metrics
showed database connection utilization at 100%. Future investigations should correlate deployment, code change,
logs, and metrics before assigning root cause.""",
"""Historical validated incident INC-1003: order-service high latency.
Root cause was an undersized cache configuration causing eviction spikes and a low cache hit ratio.
Check cache configuration changes when this pattern repeats."""
]

if __name__=="__main__":
    m=Memory()
    for x in SEED:
        m.retain(x,context="historical validated incident memory")
    print("Seeded",len(SEED),"historical memories using",m.mode)
