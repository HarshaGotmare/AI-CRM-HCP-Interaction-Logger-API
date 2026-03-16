# AI-CRM-HCP-Interaction-Logger-API
# AI CRM HCP Interaction Logger

An AI-powered full-stack application that converts natural language healthcare interaction notes into structured, CRM-ready records.

This project is designed to simplify how Healthcare Professional (HCP) interactions are logged. Instead of manually filling multiple fields, the user can enter an interaction note in natural language, and the system automatically extracts important details such as doctor name, date, time, interaction type, topics discussed, sentiment, and follow-up actions.

A key highlight of this project is its **correction-aware workflow**. If a user updates details like the doctor’s name or interaction time, the system updates the **same interaction record** instead of creating duplicate entries.

---

## Features

- Natural language interaction logging
- Automatic extraction of:
  - Doctor name
  - Date
  - Time
  - Interaction type
  - Topics discussed
  - Sentiment
  - Follow-up actions
- Auto-fill form support in the frontend
- Correction-aware backend logic
- Update existing interaction records without duplicate database entries
- API-based interaction save, update, and fetch flow

---

## Tech Stack

### Frontend
- React
- JavaScript
- CSS
- Axios

### Backend
- FastAPI
- Python
- Uvicorn
- Pydantic

### AI Workflow
- LangGraph
- ChatGroq

---

## Project Workflow

1. User enters an HCP interaction in natural language.
2. The system processes the text and extracts structured details.
3. The frontend form is automatically filled with extracted values.
4. If the user sends a correction such as:
   - `sorry name is Dr Disha`
   - `time is 4 pm`
   
   the same interaction is updated instead of creating a new record.
5. Final corrected data is stored in the database.

---

## Example Input

```text
I met Dr Shivani on 10 April 2026 at 9:30 AM to discuss diabetes therapy and shared a brochure.
```

### Example Corrections

```text
sorry name is Dr Disha
time is 4 pm
```

---

## Key Problem Solved

One of the main challenges solved in this project was **handling correction messages properly**.

In many cases, users may revise an interaction after the first entry. This project ensures that correction messages update the **current interaction record** instead of inserting duplicate rows into the database. This improves data consistency and makes the workflow closer to a real-world CRM system.

---

## API Endpoints

### `GET /`
Basic health/root endpoint.

### `POST /process`
Processes the natural language interaction and extracts structured data.

### `GET /interactions`
Fetches all saved interactions.

### `PUT /update/{interaction_id}`
Updates an existing interaction record.

### Swagger Docs
Available at:

```text
http://127.0.0.1:8000/docs

## Project Structure

```text
AI-CRM-HCP-Interaction-Logger-API/
├── backend/
│   ├── agent.py
│   ├── main.py
│   ├── database.py
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── ...
│   └── ...
├── requirements.txt
├── crm.db
└── README.md
```

---

## How to Run the Project

### Backend

Run the backend server:

```bash
uvicorn backend.main:app --reload
```

If needed, you can also use:

```bash
python -m uvicorn backend.main:app --reload
```

Backend will run on:

```text
http://127.0.0.1:8000
```

### Frontend

Move to frontend folder and start the React app:

```bash
cd frontend
npm install
npm start
```

Frontend will usually run on:

```text
http://localhost:3000
```

---

## Sample Test Flow

1. Start backend and frontend
2. Enter a natural language interaction in the UI
3. Verify the form auto-fills
4. Send a correction message like:
   - `name is Dr Vidya`
   - `time is 2 pm`
5. Click update interaction
6. Check `/interactions` or Swagger docs to confirm:
   - same record updated
   - no duplicate row created

---

## Learning Outcomes

This project helped me strengthen my understanding of:

- Full-stack development
- API integration
- Backend debugging
- AI workflow design
- Natural language data extraction
- Data consistency handling in CRUD workflows

---

## Future Improvements

- Authentication and user-based interaction history
- Better entity extraction and validation
- More robust date/time parsing
- Dashboard for analytics and reporting
- Production deployment

---
