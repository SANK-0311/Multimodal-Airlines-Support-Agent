# knowledge_base.py - RAG and Knowledge Base for ERWIQ Airlines

import json
import numpy as np
from typing import List, Dict

# Knowledge base documents (will be populated with embeddings)
knowledge_base = []



def initialize_knowledge_base():
    """
    Initialize the knowledge base with ERWIQ Airlines policies.
    """
    global knowledge_base
    
    knowledge_base = [
        # Baggage Policies
        {
            "id": "bag_001",
            "category": "Baggage",
            "title": "Carry-on Baggage Allowance",
            "content": """Carry-on baggage allowance for ERWIQ Airlines:
            - Economy Class: 1 carry-on bag (max 7kg), dimensions 55x40x20cm
            - Business Class: 2 carry-on bags (max 10kg each)
            - First Class: 2 carry-on bags (max 12kg each)
            All passengers may also bring 1 personal item (laptop bag, purse, small backpack).
            Carry-on must fit in overhead bin or under seat in front of you."""
        },
        {
            "id": "bag_002",
            "category": "Baggage",
            "title": "Checked Baggage Allowance",
            "content": """Checked baggage allowance for ERWIQ Airlines:
            - Economy Class: 1 bag, max 23kg, dimensions up to 158cm total
            - Business Class: 2 bags, max 32kg each
            - First Class: 3 bags, max 32kg each
            Additional bags: ₹2,500 for domestic routes per extra bag.
            Overweight bags (23-32kg): ₹1,500 extra fee.
            Oversized bags (158-203cm): ₹3,000 extra fee."""
        },
        {
            "id": "bag_003",
            "category": "Baggage",
            "title": "Prohibited Items",
            "content": """Items prohibited in carry-on baggage:
            - Sharp objects: knives, scissors (blade >6cm), razor blades
            - Sporting goods: cricket bats, hockey sticks, golf clubs
            - Firearms and weapons of any kind
            - Explosives and flammable items
            - Liquids over 100ml (must be in clear plastic bag)
            Items prohibited in all baggage:
            - Explosives, fireworks, flares
            - Lithium batteries over 160Wh
            - Toxic substances, radioactive materials"""
        },
        
        # Check-in Policies
        {
            "id": "checkin_001",
            "category": "Check-in",
            "title": "Online Check-in",
            "content": """ERWIQ Airlines online check-in:
            - Opens 48 hours before departure
            - Closes 2 hours before departure for all flights
            - Available at erwiqairlines.com or ERWIQ Airlines mobile app
            - Select seats, add bags, and get digital boarding pass
            - Passengers with checked bags must still visit bag drop counter
            - Web check-in available in Hindi, English, and regional languages"""
        },
        {
            "id": "checkin_002",
            "category": "Check-in",
            "title": "Airport Check-in Deadlines",
            "content": """Airport check-in counter deadlines:
            - Domestic flights: Counter closes 45 minutes before departure
            - Metro routes (Mumbai-Delhi, Delhi-Bangalore): Counter closes 60 minutes before
            - First/Business class: Dedicated counters with priority service at all major airports
            - Bag drop for online check-in: Closes 45 minutes before all flights
            Passengers arriving after deadline may be denied boarding without refund."""
        },
        
        # Booking & Cancellation
        {
            "id": "booking_001",
            "category": "Booking",
            "title": "Ticket Types and Flexibility",
            "content": """ERWIQ Airlines ticket types:
            - Saver Fare: No changes allowed, no refund. Seat assigned at check-in. Lowest price.
            - Flexi Fare: Changes allowed with ₹2,000 fee. Refund as travel credit minus ₹2,500 fee.
            - Premium Fare: Free changes up to 24 hours before departure, full refund available.
            - Business Fare: Free unlimited changes, full refund anytime.
            - First Class: Free unlimited changes, full refund anytime, dedicated support line."""
        },
        {
            "id": "booking_002",
            "category": "Booking",
            "title": "24-Hour Cancellation Policy",
            "content": """ERWIQ Airlines 24-hour free cancellation:
            - All tickets booked directly with ERWIQ Airlines can be cancelled within 24 hours of booking for full refund
            - Flight must be at least 7 days away from departure
            - Refund processed to original payment method within 7-10 business days
            - UPI refunds processed within 24-48 hours
            - This policy applies to all fare types including Saver Fare
            - Does not apply to tickets booked through third-party websites like MakeMyTrip, Goibibo"""
        },
        {
            "id": "booking_003",
            "category": "Booking",
            "title": "Refund Processing Time",
            "content": """Refund processing times at ERWIQ Airlines:
            - Credit card refunds: 7-10 business days
            - Debit card refunds: 10-14 business days
            - UPI refunds: 24-48 hours
            - Net banking: 5-7 business days
            - Travel credit: Issued immediately, valid for 12 months
            Refunds are processed to original form of payment only.
            For booking modifications, contact our support at 1800-ERWIQ-AIR (toll-free)."""
        },
        
        # Special Services
        {
            "id": "special_001",
            "category": "Special Services",
            "title": "Traveling with Pets",
            "content": """ERWIQ Airlines pet policy:
            - Small pets (dogs, cats under 8kg): Allowed in cabin, ₹3,500 each way
            - Pet must fit in carrier under seat (max 46x28x24cm)
            - Larger pets: Must travel in cargo hold, ₹7,500 each way
            - Service animals: Travel free in cabin with valid documentation
            - Book pet travel at least 48 hours before departure
            - Maximum 2 pets per passenger, 4 pets per flight
            - Pets not allowed on flights under 2 hours duration
            - Health certificate required, issued within 10 days of travel"""
        },
        {
            "id": "special_002",
            "category": "Special Services",
            "title": "Unaccompanied Minors",
            "content": """Unaccompanied minor service (UM Service):
            - Available for children ages 5-14 traveling alone
            - Children 15-17 may use service optionally
            - Fee: ₹3,000 each way for all domestic routes
            - Includes dedicated staff escort through airport and flight
            - Must be booked at least 48 hours in advance by calling customer care
            - Child delivered only to pre-authorized adult with valid government ID (Aadhaar/PAN/Passport)
            - Not available on flights with layover over 2 hours
            - Special meals for children available on request"""
        },
        {
            "id": "special_003",
            "category": "Special Services",
            "title": "Wheelchair and Mobility Assistance",
            "content": """Mobility assistance at ERWIQ Airlines:
            - Wheelchair assistance: Free of charge, request when booking or at least 48 hours before
            - Types: WCHR (to/from gate), WCHS (to/from seat), WCHC (full assistance)
            - Personal wheelchairs: Transported free as checked item
            - Electric wheelchairs/scooters: Accepted, must notify 48 hours ahead for battery handling
            - Stretcher service available on select routes (advance booking required)
            - Priority boarding for passengers needing extra time
            - All major Indian airports have accessibility features"""
        },
        
        # Loyalty Program
        {
            "id": "loyalty_001",
            "category": "Loyalty",
            "title": "ERWIQ Wings Rewards Program",
            "content": """ERWIQ Wings loyalty program:
            - Earn 10 Wings points per ₹100 spent on flights
            - Business class: Earn 15 Wings points per ₹100
            - First class: Earn 20 Wings points per ₹100
            - Points valid for 24 months from last activity
            - Redeem for flights starting at 5,000 points one-way (short routes)
            - Status tiers: Silver (10k points), Gold (25k), Platinum (50k), Diamond (100k)
            - Earn bonus points with ERWIQ co-branded credit cards (HDFC, ICICI, SBI)
            - Transfer points from partner hotels and banks"""
        },
        {
            "id": "loyalty_002",
            "category": "Loyalty",
            "title": "Elite Status Benefits",
            "content": """ERWIQ Wings Elite status benefits:
            Silver (10k points/year):
            - Priority check-in, 1 free checked bag, priority boarding
            Gold (25k points/year):
            - Above + complimentary seat selection, 2 free checked bags, lounge access (2 visits/year)
            Platinum (50k points/year):
            - Above + unlimited lounge access, complimentary upgrades when available, dedicated helpline
            Diamond (100k points/year):
            - Above + guaranteed upgrades, free companion ticket annually, exclusive airport meet & greet at metros"""
        },
        
        # Flight Delays & Compensation
        {
            "id": "delay_001",
            "category": "Delays",
            "title": "Flight Delay Compensation",
            "content": """ERWIQ Airlines delay compensation policy (as per DGCA guidelines):
            For delays within airline control:
            - 2+ hour delay: Refreshments (snacks and beverages)
            - 4+ hour delay: Meal voucher (₹500) + rebooking on next available flight
            - 6+ hour delay: Full refund option or hotel accommodation if overnight
            For weather or ATC delays:
            - Rebooking on next available flight at no charge
            - No meal or hotel compensation (outside airline control)
            - ERWIQ will assist with alternate arrangements where possible"""
        },
        {
            "id": "delay_002",
            "category": "Delays",
            "title": "Cancelled Flight Rights",
            "content": """Your rights when ERWIQ Airlines cancels your flight:
            - Full refund to original payment method, OR
            - Rebooking on next available ERWIQ flight at no charge, OR
            - Rebooking on partner airline if faster (subject to availability)
            If cancellation is within 24 hours of departure:
            - Meal vouchers provided during wait
            - Hotel accommodation if overnight wait required (for different-city connections)
            - Transportation to/from hotel arranged by ERWIQ
            For cancellations within airline control, compensation of ₹5,000 for delays over 6 hours.
            Contact: 1800-ERWIQ-AIR or visit nearest ERWIQ counter."""
        },
        
        # India-specific policies
        {
            "id": "india_001",
            "category": "India Specific",
            "title": "Valid ID Requirements",
            "content": """Valid ID for domestic travel on ERWIQ Airlines:
            Accepted government-issued photo IDs:
            - Aadhaar Card (most preferred)
            - Passport
            - PAN Card
            - Voter ID
            - Driving License
            - Government employee ID
            - Student ID with photo (for students under 18)
            For children under 5: Birth certificate with parent's ID
            DigiLocker documents accepted at all airports
            ID must match name on booking exactly"""
        },
        {
            "id": "india_002",
            "category": "India Specific",
            "title": "Payment Options",
            "content": """Payment options for ERWIQ Airlines bookings:
            - All major credit cards (Visa, Mastercard, RuPay, Amex)
            - Debit cards with 3D secure
            - UPI (Google Pay, PhonePe, Paytm, BHIM)
            - Net Banking (all major banks)
            - EMI options available on bookings above ₹5,000 (select banks)
            - ERWIQ Wallet (preloaded wallet with 2% bonus)
            - Corporate billing for business accounts
            All payments secured with Indian banking standards and RBI guidelines"""
        },
    ]
    
    return knowledge_base


def get_embedding(text: str, openai_client) -> List[float]:
    """
    Get embedding vector for a text using OpenAI.
    """
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def embed_knowledge_base(openai_client):
    """
    Add embeddings to all documents in the knowledge base.
    """
    global knowledge_base
    
    print(f"📊 Generating embeddings for {len(knowledge_base)} documents...")
    
    for i, doc in enumerate(knowledge_base):
        text_to_embed = f"{doc['title']}\n{doc['content']}"
        doc['embedding'] = get_embedding(text_to_embed, openai_client)
        print(f"   Embedded {i+1}/{len(knowledge_base)}: {doc['title'][:40]}...")
    
    print("✅ All documents embedded!")
    return knowledge_base


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


def search_knowledge_base(query: str, openai_client, top_k: int = 3) -> List[Dict]:
    """
    Search the knowledge base for relevant documents.
    """
    if not knowledge_base or 'embedding' not in knowledge_base[0]:
        print("⚠️ Knowledge base not embedded yet!")
        return []
    
    query_embedding = get_embedding(query, openai_client)
    
    results = []
    for doc in knowledge_base:
        similarity = cosine_similarity(query_embedding, doc['embedding'])
        results.append({
            'document': doc,
            'score': similarity
        })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:top_k]


def search_airline_policies(query: str, openai_client) -> str:
    """
    Search ERWIQ Airlines policies and FAQs.
    Tool function for the LLM.
    """
    print(f"🔧 Tool called: search_airline_policies({query})")
    
    results = search_knowledge_base(query, openai_client, top_k=3)
    
    if not results or results[0]['score'] < 0.3:
        return "No relevant policy information found for this query. Please contact ERWIQ Airlines customer care at 1800-ERWIQ-AIR for assistance."
    
    response = "Here's the relevant policy information:\n\n"
    for result in results:
        if result['score'] >= 0.3:
            doc = result['document']
            response += f"**{doc['title']}**\n{doc['content']}\n\n"
    
    return response


# RAG Tool definition
RAG_TOOL = {
    "type": "function",
    "function": {
        "name": "search_airline_policies",
        "description": "Search ERWIQ Airlines knowledge base for policies, FAQs, and procedures. Use this when a customer asks about baggage rules, check-in procedures, refund policies, pet travel, wheelchair assistance, loyalty programs, ID requirements, or any airline policy.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The topic or question to search for in the knowledge base"
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}


def save_knowledge_base(filepath: str = "knowledge_base.json"):
    """
    Save knowledge base to JSON file.
    """
    kb_serializable = []
    for doc in knowledge_base:
        doc_copy = doc.copy()
        if 'embedding' in doc_copy and isinstance(doc_copy['embedding'], (list, np.ndarray)):
            doc_copy['embedding'] = list(doc_copy['embedding']) if isinstance(doc_copy['embedding'], np.ndarray) else doc_copy['embedding']
        kb_serializable.append(doc_copy)
    
    with open(filepath, 'w') as f:
        json.dump(kb_serializable, f, indent=2)
    
    print(f"✅ Knowledge base saved to {filepath}")


def load_knowledge_base(filepath="knowledge_base.json"):
    global knowledge_base
    
    try:
        with open(filepath, 'r') as f:
            knowledge_base = json.load(f)
        print(f"✅ Knowledge base loaded: {len(knowledge_base)} documents")
        return True   # <--- success
    except FileNotFoundError:
        print("⚠️ Knowledge base file not found, initializing fresh...")
        initialize_knowledge_base()
        return False  # <--- failure




