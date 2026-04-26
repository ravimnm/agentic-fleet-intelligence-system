from utils.embedding import embed_text, embed_texts
from utils.vector_store import VectorStore
from database.mongo_client import MongoConnection
from typing import List

class RAGPipeline:
    def __init__(self, db: MongoConnection):
        self.db = db
        self.vector_store = VectorStore()
        self._build_index()

    def _build_index(self):
        docs = []
        # Embed telemetry summaries
        telemetry = list(self.db.get_collection("telemetry").find().limit(1000))
        for t in telemetry:
            summary = f"Vehicle {t.get('vehicleId')}: Temp {t.get('temperature', 'N/A')}, RPM {t.get('rpm', 'N/A')}, Location {t.get('latitude', 'N/A')},{t.get('longitude', 'N/A')}"
            docs.append(summary)

        # Embed predictions
        predictions = list(self.db.get_collection("predictions").find().limit(1000))
        for p in predictions:
            summary = f"Vehicle {p.get('vehicleId')}: Predicted {p.get('event', 'N/A')} with {p.get('probability', 0)*100:.1f}% probability"
            docs.append(summary)

        # Embed risk logs
        risks = list(self.db.get_collection("risk_logs").find().limit(1000))
        for r in risks:
            summary = f"Vehicle {r.get('vehicleId')}: Risk {r.get('category', 'N/A')} score {r.get('risk_score', 0):.2f}, reasons: {', '.join(r.get('reasons', []))}"
            docs.append(summary)

        if docs:
            embeddings = embed_texts(docs)
            self.vector_store.add_documents(embeddings, docs)

    def get_context(self, query: str, top_k: int = 3) -> str:
        query_emb = embed_text(query)
        results = self.vector_store.search(query_emb, top_k)
        
        # Get recent telemetry and risk summaries
        recent_telemetry = list(self.db.get_collection("telemetry").find().sort("timestamp", -1).limit(5))
        recent_risks = list(self.db.get_collection("risk_logs").find().sort("timestamp", -1).limit(5))
        
        telemetry_summaries = [f"Vehicle {t.get('vehicleId')}: Temp {t.get('temperature', 'N/A')}, RPM {t.get('rpm', 'N/A')}" for t in recent_telemetry]
        risk_summaries = [f"Vehicle {r.get('vehicleId')}: Risk {r.get('category', 'N/A')} score {r.get('risk_score', 0):.2f}" for r in recent_risks]
        
        structured_context = f"""
        Retrieved Documents: {', '.join([doc for doc, _ in results])}
        Recent Telemetry: {', '.join(telemetry_summaries)}
        Recent Risk Logs: {', '.join(risk_summaries)}
        """
        return structured_context