from datetime import datetime

def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def parse_github_event(event_type: str, payload: dict):
    try:
        # PUSH
        if event_type == "push":
            commit = payload.get("head_commit")
            if not commit:
                return None

            return {
                "request_id": commit["id"],
                "author": payload["pusher"]["name"],
                "action": "PUSH",
                "from_branch": None,
                "to_branch": payload["ref"].replace("refs/heads/", ""),
                "timestamp": _parse_iso(commit["timestamp"])
            }

        # PULL REQUEST
        if event_type == "pull_request":
            pr = payload.get("pull_request")
            if not pr:
                return None

            # MERGE 
            if payload.get("action") == "closed" and pr.get("merged") is True:
                return {
                    "request_id": str(pr["id"]),
                    "author": pr["merged_by"]["login"],
                    "action": "MERGE",
                    "from_branch": pr["head"]["ref"],
                    "to_branch": pr["base"]["ref"],
                    "timestamp": _parse_iso(pr["merged_at"])
                }

            # PULL REQUEST opened
            if payload.get("action") == "opened":
                return {
                    "request_id": str(pr["id"]),
                    "author": pr["user"]["login"],
                    "action": "PULL_REQUEST",
                    "from_branch": pr["head"]["ref"],
                    "to_branch": pr["base"]["ref"],
                    "timestamp": _parse_iso(pr["created_at"])
                }

    except KeyError as e:
        print(f"Parser error: missing field {e}")

    return None
