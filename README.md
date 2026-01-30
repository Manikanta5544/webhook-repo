# GitHub Webhook Assignment – Techstax

This repository contains the webhook endpoint and UI implementation for the Techstax assignment. It listens to GitHub webhook events, stores required data in MongoDB, and exposes an API for the UI to display recent activity.

## What This Project Does

* Receives GitHub webhook events for:
  * Push
  * Pull Request
  * Merge (bonus)
* Stores only the required fields in MongoDB
* Prevents duplicate events
* Exposes an API that the UI polls every 15 seconds
* Displays only fresh events within the refresh window

## Application Flow
```
action-repo
   ↓ (GitHub Webhooks)
Flask Backend (/webhook)
   ↓
MongoDB
   ↓ (poll every 15s)
  UI
```

## Project Structure
```
webhook-repo/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── db/
│   └── mongodb.py
│
├── routes/
│   ├── webhook_route.py
│   └── events_route.py
│
├── services/
│   ├── parser.py
│   └── deduplications.py
│
└── ui/
    ├── index.html
    ├── script.js
    └── styles.css
```

## Tech Stack

* **Backend:** Python, Flask
* **Database:** MongoDB (Atlas)
* **Webhooks:** GitHub Webhooks
* **Frontend:** HTML, CSS, JavaScript
* **Polling:** Every 15 seconds

## Database Schema (As required)

**Database:** `webhook_db`  
**Collection:** `events`
```json
{
  "request_id": "string",
  "author": "string",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "string | null",
  "to_branch": "string",
  "timestamp": "ISODate"
}
```

### Indexes

* `request_id` – unique (deduplication)
* `timestamp` – for time-based queries

## Environment Setup

Create a `.env` file in the project root:
```env
MONGO_URI=mongodb+srv://<username>:<password>@webhook-cluster.xxxxx.mongodb.net/webhook_db
FLASK_PORT=5000
FLASK_ENV=development
```

`.env` is excluded via `.gitignore`.

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the server
```bash
python app.py
```

The app runs at:
```
http://localhost:5000
```

## API Endpoints

### POST `/webhook`

* Receives GitHub webhook events
* Handles `push`, `pull_request`, and `merge`
* Always returns 200 OK
* Deduplicates events using MongoDB unique index

### GET `/events`

* Used by the UI
* Returns events from the last 30 seconds
* Sorted by newest first
* Timestamps returned in ISO format

## Deduplication & Refresh Logic

* Duplicate events are prevented using a unique index on `request_id`
* UI polls every 15 seconds
* Backend returns only events within a time window
* Older or already displayed events are not shown again

## Testing

* Webhooks configured on the `action-repo`
* Events tested:
  * Push
  * Pull Request
  * Merge (bonus)
* MongoDB Atlas used for persistence

## Related Repository

* [**action-repo**](https://github.com/Manikanta5544/action-repo) – used to trigger GitHub events (push, PR, merge)

## Submission Notes

This assignment was implemented strictly according to the requirements outlined in the provided PDF.

### Key points of the submission:

* GitHub Webhooks are used (not GitHub Actions) to receive real events from a separate action-repo.
* The backend processes push, pull request, and merge events, storing only the required fields.
* MongoDB is used with a unique index on request_id to prevent duplicate records.
* The /events endpoint returns only recent events within a defined time window to support polling.
* The UI polls the backend every 15 seconds and renders events in the exact text format specified in the assignment.
* All timestamps are handled in UTC and stored as ISO dates in MongoDB.
* The project is structured with clear separation of concerns (routes, services, database, UI).

**The system was tested end-to-end using real GitHub webhook deliveries, including:**

* Push events
* Pull request creation
* Pull request merge 
