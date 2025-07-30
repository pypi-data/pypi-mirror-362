from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import faiss
import numpy as np

app = FastAPI()


class Issue(BaseModel):
    id: int
    title: str
    body: str
    milestone: Optional[str] = None
    discussion_themes: List[str] = []
    resolution_patterns: List[str] = []
    delayed_resolution_tracking: bool = False
    desired_outcome: str
    current_reality: str
    action_steps: List[str] = []
    creative_phase: str
    echo_nodes: List[str] = []
    contradictions: List[str] = []
    missing_links: List[str] = []
    status: str
    agent: str
    started_at: str
    ripple_refs: List[str] = []
    next_steps: List[str] = []


class Query(BaseModel):
    query: str


# Placeholder for the indexed issues
indexed_issues = []

# Placeholder for the FAISS index
index = None


@app.post("/index_issues/")
def index_issues(issues: List[Issue]):
    global indexed_issues, index
    indexed_issues = issues

    # Create FAISS index
    dimension = 768  # Example dimension for Sentence-BERT embeddings
    index = faiss.IndexFlatL2(dimension)

    # Add issues to FAISS index
    for issue in issues:
        embedding = np.random.rand(dimension).astype(
            'float32')  # Placeholder for actual embeddings
        index.add(np.array([embedding]))

    return {"message": "Issues indexed successfully"}


@app.post("/query_issues/")
def query_issues(query: Query):
    global index
    if index is None:
        raise HTTPException(status_code=400, detail="Index not initialized")

    # Placeholder for query embedding
    query_embedding = np.random.rand(768).astype('float32')

    # Search FAISS index
    D, I = index.search(np.array([query_embedding]), k=5)
    results = [indexed_issues[i] for i in I[0]]

    return {"results": results}


@app.get("/issues/{issue_id}")
def get_issue(issue_id: int):
    for issue in indexed_issues:
        if issue.id == issue_id:
            return issue
    raise HTTPException(status_code=404, detail="Issue not found")


@app.get("/priority_scores/")
def get_priority_scores():
    # Placeholder for priority scores
    priority_scores = [{"id": issue.id, "priority_score": np.random.rand()}
                       for issue in indexed_issues]
    return {"priority_scores": priority_scores}


@app.get("/misalignment_detection/")
def misalignment_detection():
    # Placeholder for misalignment detection
    misalignments = [{"id": issue.id, "misalignment_score": np.random.rand()}
                     for issue in indexed_issues]
    return {"misalignments": misalignments}
