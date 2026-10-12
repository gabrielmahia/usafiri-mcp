"""UsafiriMCP — Kenya Transport Navigation (5 tools). All data DEMO."""
from __future__ import annotations

from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP(name="usafiri-mcp", instructions="Kenya transport and logistics tools. DEMO data only.")

@mcp.tool(name="matatu_route_finder", description="Estimate a matatu or bus fare between two Kenyan towns and list ways to book. Use when someone asks roughly what a trip costs. Fares come from a table of five Nairobi routes (Mombasa, Kisumu, Nakuru, Eldoret, Thika); any other pair gets a flat KES 500 placeholder and fare_is_placeholder is true. Returns the origin, destination, estimated_fare_kes, fare_is_placeholder, booking options and a note to confirm fares at the terminal. Fares and routes are labelled DEMO and change often. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def matatu_route_finder(origin: Annotated[str, Field(description="Starting town or suburb, such as Nairobi.")], destination: Annotated[str, Field(description="Destination town, such as Mombasa.")]) -> dict:
    """Find matatu (minibus) routes, fare estimates, and stages between Kenya towns and Nairobi suburbs."""
    fare_est = {"nairobi_mombasa": 1200, "nairobi_kisumu": 900, "nairobi_nakuru": 350,
                "nairobi_eldoret": 700, "nairobi_thika": 100, "default": 500}
    key = f"{origin.lower().replace(' ','_')}_{destination.lower().replace(' ','_')}"
    fare = fare_est.get(key, fare_est["default"])
    return {"source": "DEMO — fares and routes change frequently", "origin": origin, "destination": destination,
            "estimated_fare_kes": fare, "fare_is_placeholder": key not in fare_est, "booking_options": ["Bus terminals (Machakos, Muthurwa, Westlands)", 
                "Online: buupass.com, flixbus", "Apps: Little, Quickbus"],
            "note": "Confirm current fares at departure terminal. NTSA sets maximum fares for some routes."}

@mcp.tool(name="ntsa_services_guide", description="Explain NTSA services: driving licence, annual vehicle inspection, PSV licence and logbook ownership transfer, with the process, documents, indicative fees and duration. Use when someone asks how to complete an NTSA service. service is matched by name (spaces become underscores); an unrecognised service returns an error listing the valid ones. Returns the source label, the service, its process, documents or cost and duration, and NTSA contact details. Fees are labelled DEMO and unverified: confirm at tims.ntsa.go.ke. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def ntsa_services_guide(service: Annotated[str, Field(description="Service name such as driving licence, vehicle inspection, psv licence or transfer ownership.")]) -> dict:
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
    matched = next((v for k, v in SERVICES.items() if k in s or s in k), None)
    if matched is None:
        return {"error": f"Unknown NTSA service {service!r}.", "valid_services": list(SERVICES)}
    return {"source": "DEMO — tims.ntsa.go.ke for official process", "service": service, **matched,
            "ntsa": "tims.ntsa.go.ke | 0800723474"}

@mcp.tool(name="boda_licensing_guide", description="List what a boda boda (motorcycle taxi) operator needs in Kenya: licence class, PSV licence, insurance, county permit, reflective jacket with SACCO number, helmets and SACCO membership. Use when someone asks how to legally operate or whether a rider is compliant. Takes an optional county that is only echoed back: the requirements are the same for every county. Returns the source label, the county, the requirements, the NTSA fee, insurance notes and SACCO benefits. Indicative figures labelled DEMO: confirm with NTSA and the county. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def boda_licensing_guide(county: str | None = Field(None, description="County to get boda boda licensing information for.")) -> dict:
    """Return motorcycle (boda boda) operator licensing requirements, NTSA registration, and rider rights."""
    return {"source": "DEMO — NTSA/county requirements", "county": county,
            "requirements": ["Class G driving licence (motorcycle)", "PSV licence",
                             "Insurance: Third party minimum KES 3,000/year",
                             "County government permit (KES 1,000–3,000/year)",
                             "Reflective jacket with SACCO number", "Helmet (rider and pillion)",
                             "SACCO membership (most counties mandatory)"],
            "ntsa_fee": "PSV licence: KES 2,050/year", "insurance": "Jubilee, GA, or APA offer boda policies",
            "sacco_benefit": "SACCO membership provides accident insurance, savings, and loan access."}

@mcp.tool(name="freight_logistics_guide", description="Compare ways to move goods in Kenya: full-load truck, bus parcel, motorbike courier and SGR cargo, with indicative price ranges and example providers. Use when someone asks how to ship cargo and roughly what it costs. origin, destination and cargo_type are only echoed back; the same options are returned for every route. Returns the source label, the echoed inputs and the options with price range and providers. Indicative prices labelled DEMO: get quotes from providers. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def freight_logistics_guide(origin: Annotated[str, Field(description="Origin town; only echoed back.")], destination: Annotated[str, Field(description="Destination town; only echoed back.")], cargo_type: Annotated[str | None, Field(description="Cargo type such as general; only echoed back.")] = "general") -> dict:
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

@mcp.tool(name="transport_rights_query", description="Explain passenger and shipper rights in Kenyan transport: overcharging, vehicle safety, accidents, goods loss or damage and disability access. Use when someone asks what a passenger or customer can demand or where to report. Keywords in topic select entries; if none match, ALL rights are returned. Returns the source label, the topic, the rights, NTSA's number and a not-legal-advice disclaimer. Static summary labelled DEMO: verify with NTSA. Read-only; no side effects.", annotations={"readOnlyHint": True, "openWorldHint": False})
def transport_rights_query(topic: Annotated[str, Field(description="Rights topic such as overcharging, safety, accident, goods or disability.")]) -> dict:
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

def main() -> None:
    """Console entry point."""
    mcp.run()
