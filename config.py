# config.py - Configuration and constants for ERWIQ Airlines

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Model names
OPENAI_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
GEMINI_MODEL = "gemini-2.0-flash"

# System message
SYSTEM_MESSAGE = """You are a helpful and factual customer support assistant for **ERWIQ Airlines**.
ERWIQ Airlines was founded by **SANTHOSH KUMAR**.

Your responsibilities:
- Help customers with flight bookings, cancellations, and modifications
- Provide accurate information about airline policies and procedures
- Answer questions about baggage, check-in, refunds, and special services
- Handle refund and compensation requests

IMPORTANT: When customers ask about policies, rules, or procedures:
- Use the search_airline_policies tool to find accurate information
- Base your answers on the retrieved policy documents
- Don't make up policies - if information isn't found, say so

Guidelines:
- Keep responses helpful and accurate
- Quote specific rules and limits from policies when relevant
- For complex issues, offer to escalate to a human agent
- All prices are in Indian Rupees (₹)

Available tools:
- get_ticket_price: Check flight prices
- get_flight_status: Get flight status updates
- lookup_booking: Find booking details by PNR
- process_refund: Process refund requests
- get_destination_image: Generate destination images
- search_airline_policies: Search FAQs and policies
"""

# Ticket prices (in Rupees)
TICKET_PRICES = {
    "mumbai": {"economy": 4999, "business": 12999, "first": 24999},
    "delhi": {"economy": 5499, "business": 14999, "first": 28999},
    "bangalore": {"economy": 4499, "business": 11999, "first": 22999},
    "chennai": {"economy": 4299, "business": 10999, "first": 21999},
    "kolkata": {"economy": 5999, "business": 15999, "first": 29999},
    "hyderabad": {"economy": 4599, "business": 11499, "first": 22499},
    "ahmedabad": {"economy": 3999, "business": 9999, "first": 19999},
    "pune": {"economy": 3499, "business": 8999, "first": 17999},
    "jaipur": {"economy": 4199, "business": 10499, "first": 20999},
    "goa": {"economy": 5499, "business": 13999, "first": 26999},
    "kochi": {"economy": 4799, "business": 12499, "first": 23999},
    "lucknow": {"economy": 3999, "business": 9499, "first": 18999},
}

# Flights database
FLIGHTS_DB = {
    "EQ101": {"route": "Mumbai → Delhi", "departure": "06:00", "status": "On Time"},
    "EQ202": {"route": "Delhi → Bangalore", "departure": "09:30", "status": "Delayed 30min"},
    "EQ303": {"route": "Chennai → Kolkata", "departure": "14:15", "status": "On Time"},
    "EQ404": {"route": "Hyderabad → Mumbai", "departure": "18:45", "status": "Cancelled"},
    "EQ505": {"route": "Bangalore → Goa", "departure": "11:00", "status": "Boarding"},
    "EQ606": {"route": "Pune → Jaipur", "departure": "07:30", "status": "On Time"},
    "EQ707": {"route": "Kochi → Chennai", "departure": "16:00", "status": "Delayed 1hr"},
    "EQ808": {"route": "Ahmedabad → Lucknow", "departure": "20:30", "status": "On Time"},
}

# Bookings database
BOOKINGS_DB = {
    "ABC123": {
        "passenger": "Rahul Sharma",
        "flight": "EQ101",
        "route": "Mumbai → Delhi",
        "date": "2025-06-15",
        "class": "Business",
        "seat": "2A",
        "status": "Confirmed",
        "meal": "Vegetarian"
    },
    "XYZ789": {
        "passenger": "Priya Patel",
        "flight": "EQ303",
        "route": "Chennai → Kolkata",
        "date": "2025-06-20",
        "class": "Economy",
        "seat": "24F",
        "status": "Confirmed",
        "meal": "Standard"
    },
    "DEF456": {
        "passenger": "Amit Kumar",
        "flight": "EQ404",
        "route": "Hyderabad → Mumbai",
        "date": "2025-06-18",
        "class": "First",
        "seat": "1A",
        "status": "Cancelled - Refund Pending",
        "meal": "Jain"
    },
    "PQR999": {
        "passenger": "Sneha Reddy",
        "flight": "EQ505",
        "route": "Bangalore → Goa",
        "date": "2025-06-22",
        "class": "Economy",
        "seat": "15C",
        "status": "Confirmed",
        "meal": "Non-Vegetarian"
    },
    "LMN555": {
        "passenger": "Vikram Singh",
        "flight": "EQ606",
        "route": "Pune → Jaipur",
        "date": "2025-06-25",
        "class": "Business",
        "seat": "4B",
        "status": "Confirmed",
        "meal": "Vegetarian"
    },
}