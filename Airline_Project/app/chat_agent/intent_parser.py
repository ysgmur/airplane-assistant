import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_intent(message):
    # ✨ Extra manual extraction (for fallback)
    flight_match = re.search(r"flight\s*(\d+)", message.lower())
    ticket_match = re.search(r"ticket\s*(\d+)", message.lower())

    system_prompt = """
You are a smart flight booking assistant.

Based on the user's message, extract and return only the following fields as pure JSON:

{
  "intent": "buy" | "search" | "checkin" | "add_flight",
  "from": "airport_code",     // optional, e.g. "IST"
  "to": "airport_code",       // optional, e.g. "AMS"
  "date": "YYYY-MM-DD",       // optional, e.g. "2025-06-13"
  "capacity": integer,        // optional (for adding flight)
  "duration": integer,        // optional (for adding flight)
  "flight_id": integer,       // optional (for checkin/buy)
  "ticket_id": integer        // optional (for checkin)
}

Rules:
- Return only valid JSON object.
- Set null for unknown or missing fields.
- DO NOT add comments or explanation.
If user uses words like "book", "purchase", or "get a ticket", classify it as "buy".

"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0
        )

        content = response.choices[0].message.content
        print("🧠 OpenAI raw output:", content)

        parsed = json.loads(content)

        # Override with regex if not extracted
        if flight_match and not parsed.get("flight_id"):
            parsed["flight_id"] = int(flight_match.group(1))
        if ticket_match and not parsed.get("ticket_id"):
            parsed["ticket_id"] = int(ticket_match.group(1))

        return parsed

    except Exception as e:
        print("❌ Failed to parse JSON from OpenAI:", e)
        return {
            "intent": "unknown",
            "from": None,
            "to": None,
            "date": None,
            "capacity": None,
            "duration": None,
            "flight_id": flight_match.group(1) if flight_match else None,
            "ticket_id": ticket_match.group(1) if ticket_match else None
        }
