from database import list_incidents,get_resolution
from rca_engine import investigate

def main():
    df=list_incidents()
    eval_df=df[df.incident_id.str.startswith("EVAL-")].copy()
    rows=[]
    correct=0
    for iid in eval_df.incident_id:
        result=investigate(iid)
        expected=get_resolution(iid)["root_cause"]
        predicted=result["rca"]["root_cause"]
        ok=predicted==expected
        correct+=ok
        rows.append((iid,ok,result["rca"]["pattern"],result["rca"]["score"]))
    accuracy=correct/len(rows)*100
    print(f"Evaluated: {len(rows)}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")
    print("\nFailed cases:")
    for r in rows:
        if not r[1]:
            print(r)
if __name__=="__main__":
    main()
