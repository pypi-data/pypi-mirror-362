from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI()

class LogEntry(BaseModel):
    timestamp: str
    message: str

class Checkpoint(BaseModel):
    timestamp: str
    logs: List[LogEntry]

class TensionFlag(BaseModel):
    condition: str

class GraphNode(BaseModel):
    id: str
    label: str

class GraphEdge(BaseModel):
    from_node: str
    to_node: str

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class Logbook(BaseModel):
    entries: List[LogEntry] = []

class CheckpointList(BaseModel):
    checkpoints: List[Checkpoint] = []

class TensionFlagList(BaseModel):
    flags: List[TensionFlag] = []

logbook = Logbook(entries=[])
checkpoints = CheckpointList(checkpoints=[])
tension_flags = TensionFlagList(flags=[])
graph_data = GraphData(nodes=[], edges=[])

@app.post("/logbook/")
def add_log_entry(entry: LogEntry):
    logbook.entries.append(entry)
    return {"message": "Log entry added successfully"}

@app.get("/logbook/")
def get_logbook():
    return logbook

@app.post("/checkpoints/")
def add_checkpoint(checkpoint: Checkpoint):
    checkpoints.checkpoints.append(checkpoint)
    return {"message": "Checkpoint added successfully"}

@app.get("/checkpoints/")
def get_checkpoints():
    return checkpoints

@app.post("/tension_flags/")
def add_tension_flag(flag: TensionFlag):
    tension_flags.flags.append(flag)
    return {"message": "Tension flag added successfully"}

@app.get("/tension_flags/")
def get_tension_flags():
    return tension_flags

@app.post("/graph/")
def update_graph(data: GraphData):
    global graph_data
    graph_data.nodes = data.nodes
    graph_data.edges = data.edges
    return {"message": "Graph data updated successfully"}

@app.get("/graph/")
def get_graph():
    return graph_data

@app.post("/webhook/")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        event_type = request.headers.get("X-GitHub-Event")

        print(f"Received webhook event: {event_type}")

        if event_type == "issues":
            handle_issues_event(payload)
        elif event_type == "pull_request":
            handle_pull_request_event(payload)
        elif event_type == "issue_comment":
            handle_issue_comment_event(payload)
        elif event_type == "push":
            handle_push_event(payload)

        return {"status": "success"}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def handle_issues_event(payload):
    action = payload.get("action")
    issue = payload.get("issue")
    if action in ["opened", "edited", "closed"]:
        process_issue(issue)

def handle_pull_request_event(payload):
    action = payload.get("action")
    pull_request = payload.get("pull_request")
    if action in ["opened", "edited", "closed"]:
        process_pull_request(pull_request)

def handle_issue_comment_event(payload):
    action = payload.get("action")
    comment = payload.get("comment")
    issue = payload.get("issue")
    if action in ["created", "edited", "deleted"]:
        process_issue_comment(comment, issue)

def handle_push_event(payload):
    commits = payload.get("commits")
    if commits:
        process_commits(commits)

def process_issue(issue):
    # Placeholder for processing issue
    pass

def process_pull_request(pull_request):
    # Placeholder for processing pull request
    pass

def process_issue_comment(comment, issue):
    # Placeholder for processing issue comment
    pass

def process_commits(commits):
    # Placeholder for processing commits
    pass
