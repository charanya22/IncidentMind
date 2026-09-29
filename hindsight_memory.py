import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
LOCAL_PATH=Path("data/local_memory.json")

class Memory:
    def __init__(self):
        self.api_key=os.getenv("HINDSIGHT_API_KEY","").strip()
        self.base_url=os.getenv("HINDSIGHT_BASE_URL","https://api.hindsight.vectorize.io")
        self.bank_id=os.getenv("HINDSIGHT_BANK_ID","incidentmind")
        self.client=None
        if self.api_key and self.api_key != "your_api_key_here":
            try:
                from hindsight_client import Hindsight
                self.client=Hindsight(base_url=self.base_url, api_key=self.api_key)
                self.client.create_bank(bank_id=self.bank_id, name="IncidentMind")
            except Exception as e:
                print("Hindsight unavailable; using local fallback:", e)
                self.client=None
        LOCAL_PATH.parent.mkdir(exist_ok=True)
        if not LOCAL_PATH.exists():
            LOCAL_PATH.write_text("[]", encoding="utf-8")

    @property
    def mode(self):
        return "Hindsight Cloud" if self.client else "Local demo fallback"

    def retain(self, content, context="incident learning"):
        if self.client:
            try:
                self.client.retain(bank_id=self.bank_id, content=content, context=context)
                return True
            except Exception as e:
                print("Hindsight retain failed:", e)
        memories=json.loads(LOCAL_PATH.read_text(encoding="utf-8"))
        memories.append({"content":content,"context":context})
        LOCAL_PATH.write_text(json.dumps(memories,indent=2),encoding="utf-8")
        return True

    def recall(self, query, limit=5):
        if self.client:
            try:
                result=self.client.recall(bank_id=self.bank_id, query=query, max_tokens=3000, budget="mid")
                return [{"text":r.text,"type":getattr(r,"type","memory")} for r in result.results[:limit]]
            except Exception as e:
                print("Hindsight recall failed:", e)
        words=set(query.lower().split())
        memories=json.loads(LOCAL_PATH.read_text(encoding="utf-8"))
        scored=[]
        for m in memories:
            score=sum(1 for w in words if len(w)>3 and w in m["content"].lower())
            if score:
                scored.append((score,m))
        scored.sort(key=lambda x:x[0],reverse=True)
        return [{"text":m["content"],"type":"local","score":s} for s,m in scored[:limit]]

    def reflect(self, query, context):
        if self.client:
            try:
                r=self.client.reflect(bank_id=self.bank_id, query=query, context=context, budget="mid")
                return {"text":r.text,"based_on":[str(x) for x in getattr(r,"based_on",[]) ]}
            except Exception as e:
                print("Hindsight reflect failed:", e)
        return {"text":"Local fallback: reasoning is supplied by the deterministic evidence engine.",
                "based_on":[]}
