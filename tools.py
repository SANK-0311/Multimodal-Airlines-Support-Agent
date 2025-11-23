# tools.py - All tool functions for ERWIQ Airlines

import json
import random
import base64
from io import BytesIO
from typing import List, Dict, Tuple

from config import TICKET_PRICES, FLIGHTS_DB, BOOKINGS_DB

# Store refund requests
refund_requests = {}


def get_ticket_price(destination_city: str, travel_class: str = "economy") -> str:
    """
    Get the ticket price for a destination.
    """
    print(f"🔧 Tool called: get_ticket_price({destination_city}, {travel_class})")
    
    city = destination_city.lower().strip()
    travel_class = travel_class.lower().strip()
    
    if city not in TICKET_PRICES:
        available = ', '.join(TICKET_PRICES.keys())
        return f"Sorry, we don't fly to {destination_city}. Available destinations: {available}"
    
    if travel_class not in TICKET_PRICES[city]:
        return "Invalid class. Choose from: economy, business, first"
    
    price = TICKET_PRICES[city][travel_class]
    return f"₹{price:,} for {travel_class.title()} class to {destination_city.title()}"


def get_flight_status(flight_number: str) -> str:
    """
    Get the current status of a flight.
    """
    print(f"🔧 Tool called: get_flight_status({flight_number})")
    
    flight_number = flight_number.upper().strip()
    
    if flight_number not in FLIGHTS_DB:
        return f"Flight {flight_number} not found. Please check the flight number. Our flights start with 'EQ' (e.g., EQ101, EQ202)."
    
    flight = FLIGHTS_DB[flight_number]
    return f"Flight {flight_number} ({flight['route']}): Departure {flight['departure']}, Status: {flight['status']}"


def lookup_booking(pnr: str) -> str:
    """
    Look up a booking by PNR (booking reference).
    """
    print(f"🔧 Tool called: lookup_booking({pnr})")
    
    pnr = pnr.upper().strip()
    
    if pnr not in BOOKINGS_DB:
        return f"Booking {pnr} not found. Please check your booking reference."
    
    booking = BOOKINGS_DB[pnr]
    return f"""Booking {pnr}:
- Passenger: {booking['passenger']}
- Flight: {booking['flight']} ({booking['route']})
- Date: {booking['date']}
- Class: {booking['class']}, Seat: {booking['seat']}
- Status: {booking['status']}
- Meal Preference: {booking['meal']}"""


def process_refund(pnr: str, reason: str) -> str:
    """
    Process a refund request for a booking.
    """
    print(f"🔧 Tool called: process_refund({pnr}, {reason})")
    
    pnr = pnr.upper().strip()
    
    if pnr not in BOOKINGS_DB:
        return f"Cannot process refund: Booking {pnr} not found."
    
    booking = BOOKINGS_DB[pnr]
    
    if "Cancelled" in booking['status']:
        return f"Booking {pnr} is already cancelled. Refund is being processed."
    
    # Generate refund reference
    refund_ref = f"REF{random.randint(100000, 999999)}"
    
    # Calculate refund amount (simplified - in Rupees)
    class_multiplier = {"Economy": 1, "Business": 2.5, "First": 5}
    base_price = 4999
    refund_amount = int(base_price * class_multiplier.get(booking['class'], 1))
    
    # Store refund request
    refund_requests[refund_ref] = {
        "pnr": pnr,
        "reason": reason,
        "amount": refund_amount,
        "status": "Approved"
    }
    
    return f"""Refund Request Processed:
- Reference: {refund_ref}
- Booking: {pnr}
- Passenger: {booking['passenger']}
- Refund Amount: ₹{refund_amount:,}
- Status: Approved - Will be credited in 5-7 business days
- Reason: {reason}"""


def get_destination_image(city: str, openai_client) -> str:
    """
    Generate an image of a travel destination.
    """
    print(f"🔧 Tool called: get_destination_image({city})")
    
    try:
        prompt = f"A beautiful vibrant travel poster showcasing {city}, India as a travel destination, featuring iconic landmarks, local culture, temples, markets, and atmosphere. High quality, inspiring wanderlust, colorful Indian aesthetic."
        
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            n=1,
            response_format="b64_json"
        )
        
        # Save image
        image_data = base64.b64decode(response.data[0].b64_json)
        filename = f"destination_{city.lower().replace(' ', '_')}.png"
        
        with open(filename, 'wb') as f:
            f.write(image_data)
        
        return f"I've generated a beautiful travel image of {city} for you! The image showcases the iconic landmarks and vibrant culture of this amazing Indian destination."
    
    except Exception as e:
        return f"Sorry, I couldn't generate an image for {city}: {str(e)}"


# Tool definitions for OpenAI
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket_price",
            "description": "Get the price of a flight ticket to a destination city in India. Use this when a customer asks about ticket prices or how much it costs to fly somewhere.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destination_city": {
                        "type": "string",
                        "description": "The Indian city the customer wants to fly to (e.g., 'Mumbai', 'Delhi', 'Bangalore', 'Goa')"
                    },
                    "travel_class": {
                        "type": "string",
                        "enum": ["economy", "business", "first"],
                        "description": "The travel class. Defaults to economy if not specified."
                    }
                },
                "required": ["destination_city"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_status",
            "description": "Get the current status of an ERWIQ Airlines flight (on time, delayed, cancelled, boarding). Flight numbers start with 'EQ'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "flight_number": {
                        "type": "string",
                        "description": "The flight number (e.g., 'EQ101', 'EQ202')"
                    }
                },
                "required": ["flight_number"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_booking",
            "description": "Look up a booking using the PNR (booking reference). Use this when a customer wants to check their booking details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pnr": {
                        "type": "string",
                        "description": "The 6-character booking reference (e.g., 'ABC123')"
                    }
                },
                "required": ["pnr"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Process a refund request for a cancelled or unwanted booking. Use this when a customer wants to cancel and get a refund.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pnr": {
                        "type": "string",
                        "description": "The booking reference to refund"
                    },
                    "reason": {
                        "type": "string",
                        "description": "The reason for the refund request"
                    }
                },
                "required": ["pnr", "reason"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_destination_image",
            "description": "Generate a beautiful travel image of an Indian destination city. Use this when a customer wants to see what a destination looks like.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The Indian city to generate an image for"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }
]


# Tool executor
def execute_tool(tool_name: str, tool_arguments: str, openai_client=None) -> str:
    """
    Execute a tool by name with the given arguments.
    """
    args = json.loads(tool_arguments)
    
    if tool_name == "get_ticket_price":
        return get_ticket_price(**args)
    elif tool_name == "get_flight_status":
        return get_flight_status(**args)
    elif tool_name == "lookup_booking":
        return lookup_booking(**args)
    elif tool_name == "process_refund":
        return process_refund(**args)
    elif tool_name == "get_destination_image":
        return get_destination_image(args.get("city"), openai_client)
    else:
        return f"Error: Unknown tool '{tool_name}'"