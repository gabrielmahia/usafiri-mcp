"""UsafiriMCP — Kenya Transport Navigation (5 tools). All data DEMO."""
from __future__ import annotations
from typing import Annotated, Optional
from fastmcp import FastMCP
mcp = FastMCP(name="usafiri-mcp", instructions="Kenya transport and logistics tools. DEMO data only.")

@mcp.tool(name="matatu_route_finder", description="Find matatu routes between Kenyan towns. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def matatu_route_finder(origin: str, destination: str) -> dict:
    """Find matatu (minibus) routes, fare estimates, and stages between Kenya towns and Nairobi suburbs."""
    fare_est = {"nairobi_mombasa": 1200, "nairobi_kisumu": 900, "nairobi_nakuru": 350,
                "nairobi_eldoret": 700, "nairobi_thika": 100, "default": 500}
    key = f"{origin.lower().replace(' ','_')}_{destination.lower().replace(' ','_')}"
    fare = fare_est.get(key, fare_est["default"])
    return {"source": "DEMO — fares and routes change frequently", "origin": origin, "destination": destination,
            "estimated_fare_kes": fare, "booking_options": ["Bus terminals (Machakos, Muthurwa, Westlands)", 
                "Online: buupass.com, flixbus", "Apps: Little, Quickbus"],
            "note": "Confirm current fares at departure terminal. NTSA sets maximum fares for some routes."}

@mcp.tool(name="ntsa_services_guide", description="NTSA services guide: driving licence, vehicle inspection, permits. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def ntsa_services_guide(service: str) -> dict:
    """Return NTSA (National Transport and Safety Authority) services, requirements, and processes."""
    SERVICES = {
        "driving_licence": {"process": "Apply at tims.ntsa.go.ke. Theory test + practical exam. Fee: KES 3,050",
                            "documents": ["ID/Passport", "KES 3,050", "Medical certificate", "Passport photo"],
                            "duration": "4–8 weeks"},
        "vehicle_inspection": {"process": "Mandatory annually. Inspection at NTSA-accredited garage.",
                               "cost": "KES 2,000–5,000 depending on vehicle class",
                               "consequence": "Non-compliance: fine up to KES 20,000 or impound"},
        "psv_licence": {"process": "Public Service Vehicle licence for matatu/taxi operators. tims.ntsa.go.ke",
                        "documents": ["Valid driving licence (3yr+ PSV category)", "Good conduct certificate", "Medical"],
                        "note": "SACCOs required for matatu operators"},
        "transfer_ownership": {"process": "Logbook transfer at NTSA. Fee: KES 1,125",
                               "documents": ["Logbook", "Both parties' IDs", "KRA compliance certificate"],
                               "duration": "3–7 working days"},
    }
    s = service.lower().replace(" ","_")
    matched = next((v for k, v in SERVICES.items() if k in s or s in k), list(SERVICES.values())[0])
    return {"source": "DEMO — tims.ntsa.go.ke for official process", "service": service, **matched,
            "ntsa": "tims.ntsa.go.ke | 0800723474"}

@mcp.tool(name="boda_licensing_guide", description="Boda boda (motorcycle taxi, annotations={"readOnlyHint": True, "openWorldHint": False}) licensing requirements in Kenya. DEMO.")
def boda_licensing_guide(county: Annotated[Optional[str], "County to get boda boda licensing information for."] = None) -> dict:
    """Return motorcycle (boda boda) operator licensing requirements, NTSA registration, and rider rights."""
    return {"source": "DEMO — NTSA/county requirements", "county": county,
            "requirements": ["Class G driving licence (motorcycle)", "PSV licence",
                             "Insurance: Third party minimum KES 3,000/year",
                             "County government permit (KES 1,000–3,000/year)",
                             "Reflective jacket with SACCO number", "Helmet (rider and pillion)",
                             "SACCO membership (most counties mandatory)"],
            "ntsa_fee": "PSV licence: KES 2,050/year", "insurance": "Jubilee, GA, or APA offer boda policies",
            "sacco_benefit": "SACCO membership provides accident insurance, savings, and loan access."}

@mcp.tool(name="freight_logistics_guide", description="Freight logistics options for Kenya SMEs. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def freight_logistics_guide(origin: str, destination: str, cargo_type: Optional[str] = "general") -> dict:
    """Return freight transport options, truck routes, and logistics providers for Kenya."""
    return {"source": "DEMO — prices indicative", "origin": origin, "destination": destination, "cargo": cargo_type,
            "options": [
                {"mode": "Truck (full load)", "price_range": "KES 15,000–80,000 depending on distance",
                 "providers": ["SIGINON", "Mitchell Cotts", "local transporters via TruckAfrica"]},
                {"mode": "Bus parcel", "price_range": "KES 300–2,000 for small packages",
                 "providers": ["EasyCoach", "Guardian", "Modern Coast"]},
                {"mode": "Motorbike courier (Nairobi/Mombasa)", "price_range": "KES 200–800 same-day",
                 "providers": ["Sendy", "Glovo", "Jumia Fulfilment"]},
                {"mode": "SGR cargo (Nairobi–Mombasa)", "price_range": "KES 0.18–0.25 per kg/km",
                 "providers": ["Kenya Railways SGR cargo: www.krsgr.co.ke"]},
            ]}

@mcp.tool(name="transport_rights_query", description="Passenger rights for Kenya public transport. DEMO.", annotations={"readOnlyHint": True, "openWorldHint": False})
def transport_rights_query(topic: str) -> dict:
    RIGHTS = {
        "overcharging": "NTSA sets maximum fares. Report overcharging: NTSA 0800723474 or police.",
        "safety": "PSV must have valid inspection sticker. Seatbelts mandatory. Report unsafe vehicle: NTSA.",
        "accident": "Report to police within 24 hours. PSV operator liable for passenger injuries under Traffic Act.",
        "goods": "Carrier liable for loss/damage of goods. Get receipt. Small Claims Court for disputes under KES 1M.",
        "disability": "SGR and formal buses must provide disabled access. NTSA enforcing wheelchair standards.",
    }
    t = topic.lower()
    matched = {k: v for k, v in RIGHTS.items() if k in t or any(w in t for w in k.split("_"))}
    return {"source": "DEMO — Traffic Act, Consumer Protection Act", "topic": topic,
            "rights": matched or RIGHTS, "ntsa": "0800723474", "disclaimer": "Not legal advice."}
