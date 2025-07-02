import json
import random

def generate_report_text(data):
    incident = data.get("incident_type", "An incident")
    location = data.get("location", "an unspecified location")
    report = f"A {incident.lower()} occurred at {location}."
    if "duration" in data:
        report += f" The event lasted for {data['duration']}."
    if "resolved" in data and data["resolved"]:
        report += " The issue has been resolved."
    else:
        report += " The issue is pending resolution."
    return report

if __name__ == "__main__":
    sample_data_points = [
        {"incident_type": "Power Outage", "duration": "3 hours", "location": "Zone 4", "cause": "tree fall", "resolved": True, "compliance_flag": True},
        {"incident_type": "Gas Leak", "duration": "45 minutes", "location": "Substation B", "cause": "valve failure", "resolved": True, "compliance_flag": False},
        {"incident_type": "Transformer Fire", "duration": "5 hours", "location": "Industrial Park", "cause": "overload", "resolved": True, "compliance_flag": True},
        {"incident_type": "Voltage Fluctuation", "duration": "15 minutes", "location": "Residential Grid 9", "resolved": True, "compliance_flag": False},
        {"incident_type": "Water Pressure Drop", "duration": "2 hours", "location": "Pumping Station 3", "resolved": True, "compliance_flag": False},
        {"incident_type": "Water Main Burst", "location": "Residential Block 7", "resolved": False, "compliance_flag": False},
        {"incident_type": "System Blackout", "location": "Downtown Core", "cause": "cascading failure", "resolved": False, "compliance_flag": True},
        {"incident_type": "Network Outage", "location": "Data Center A", "resolved": False, "compliance_flag": False},
        {"incident_type": "Scheduled Maintenance", "duration": "8 hours", "location": "Sector Alpha", "resolved": True, "compliance_flag": False},
        {"incident_type": "Equipment Failure", "duration": "90 minutes", "location": "Substation C", "cause": "component wear", "resolved": True, "compliance_flag": False},
        {"incident_type": "Customer Complaint", "location": "Service Area 5", "cause": "billing system error", "resolved": True, "compliance_flag": False},
        {"incident_type": "Brief Interruption", "location": "Commercial District", "resolved": True},
        {"incident_type": "Pressure Alert", "location": "Pipeline Section 12", "resolved": False},
        {"incident_type": "Power Surge", "location": "Hospital Grid", "cause": "lightning strike", "resolved": True, "compliance_flag": True, "duration": "1 second"},
        {"incident_type": "Contaminant Detected", "location": "Reservoir 2", "resolved": False, "compliance_flag": True},
        {"incident_type": "Communication Link Down", "duration": "4 hours", "location": "Control Center", "cause": "fiber cut", "resolved": True, "compliance_flag": False},
        {"incident_type": "Emergency Shutdown", "location": "Nuclear Plant Sector 1", "cause": "seismic sensor trip", "resolved": True, "compliance_flag": False},
        {"incident_type": "Unauthorized Access", "location": "SCADA System", "resolved": True, "cause": "security breach", "compliance_flag": True, "duration": "12 minutes"},
        {"incident_type": "Animal Interference", "location": "Pole 734B", "resolved": True, "duration": "1 hour", "compliance_flag": False},
        {"incident_type": "Severe Weather Disruption", "location": "Coastal Power Lines", "resolved": False, "compliance_flag": False},
        {"incident_type": "Human Error", "location": "Switching Yard 4", "duration": "25 minutes", "resolved": True, "compliance_flag": True},
        {"incident_type": "Scheduled System Upgrade", "duration": "6 hours", "location": "Central Server Farm", "resolved": True, "compliance_flag": False},
        {"incident_type": "Pipeline Integrity Test (PIG)", "duration": "12 hours", "location": "Gas Trunkline 7B", "resolved": True, "compliance_flag": False},
        {"incident_type": "Backup Generator Test", "duration": "30 minutes", "location": "Hospital Substation", "resolved": True, "compliance_flag": False},
        {"incident_type": "SCADA Software Patch", "location": "Main Control Room", "resolved": True, "duration": "15 minutes", "compliance_flag": False},
        {"incident_type": "Sensor Malfunction", "location": "Reservoir Dam Sluice Gate 3", "cause": "moisture damage", "resolved": True, "duration": "2 hours"},
        {"incident_type": "Data Logging Failure", "location": "Metering System #45", "cause": "disk space full", "resolved": True},
        {"incident_type": "Intermittent Signal Loss", "location": "Remote Cell Tower 1138", "resolved": False},
        {"incident_type": "Flooding", "location": "Substation F (Low-lying Area)", "cause": "heavy rainfall", "resolved": False, "compliance_flag": True},
        {"incident_type": "High Wind Warning", "location": "Transmission Lines P-45 to P-48", "resolved": True, "cause": "preventative de-energization"},
        {"incident_type": "Vegetation Overgrowth", "location": "Utility Easement 9", "cause": "tree contact", "resolved": True, "duration": "45 minutes"},
        {"incident_type": "Vehicle Collision", "location": "Utility Pole #881, Main St.", "cause": "traffic accident", "resolved": False, "compliance_flag": True},
        {"incident_type": "Low Pressure Warning", "location": "Gas Main - Sector Gamma", "resolved": True, "cause": "upstream regulator fault", "duration": "35 minutes"},
        {"incident_type": "Taste and Odor Complaint", "location": "Water System, Maple Ave District", "cause": "algae bloom in reservoir", "resolved": False, "compliance_flag": True},
        {"incident_type": "Leak Detection Alert", "location": "Pipeline Junction K-12", "resolved": False},
        {"incident_type": "Forced Entry Alarm", "location": "Perimeter Fence, Pumping Station 2", "resolved": True, "cause": "false alarm, animal", "duration": "20 minutes"},
        {"incident_type": "Operational Procedure Violation", "location": "Control Room A", "cause": "operator error", "resolved": True, "compliance_flag": True},
        {"incident_type": "Cybersecurity Alert", "location": "Corporate IT Network", "cause": "phishing attempt detected", "resolved": True, "compliance_flag": False},
        {"incident_type": "Theft of Materials", "location": "Storage Yard C", "cause": "vandalism", "resolved": False, "compliance_flag": True},
        {"incident_type": "Grid Frequency Anomaly", "duration": "800 milliseconds", "location": "Western Interconnect", "resolved": True, "cause": "large load balancing event"},
        {"incident_type": "Cascading Trip", "location": "Grids 5, 6, and 8", "cause": "initial fault at Substation Alpha", "resolved": False, "compliance_flag": True},
        {"incident_type": "Brownout", "duration": "1 hour", "location": "Residential Sector Delta", "cause": "high demand voltage reduction", "resolved": True},
        {"incident_type": "Boil Water Advisory Issued", "location": "Town of Springfield", "cause": "E. coli detected post-main-burst", "resolved": False, "compliance_flag": True},
        {"incident_type": "Unidentified Alarm", "location": "SCADA Panel 3", "resolved": False},
        {"incident_type": "Customer-reported Flickering Lights", "location": "Service Area 12", "resolved": False},
        {"incident_type": "Abnormal Temperature Reading", "location": "Transformer T-102", "resolved": False, "cause": "under investigation"},
        {"incident_type": "Flow Reversal Detected", "location": "Aqueduct 4", "resolved": True, "cause": "pump malfunction"},
        {"incident_type": "Static on Communication Lines", "location": "Field Operations Channel", "resolved": False},
        {"incident_type": "Air Quality Alert", "location": "Near Gas Regulator Station 5", "resolved": False, "compliance_flag": True},
        {"incident_type": "Substation Entry Logged", "location": "Substation H", "cause": "routine inspection", "resolved": True, "duration": "2 hours"}
    ]
    prompt_template = """### Instruction:
    Generate a compliance report summary from the following structured data.

    ### Input:
    {input_json}

    ### Response:
    {response_text}"""
    with open("train_dataset.jsonl", "w") as f:
        for sample in sample_data_points:
            report_text = generate_report_text(sample)
            input_json = json.dumps(sample)
            full_prompt = prompt_template.format(input_json=input_json, response_text=report_text)
            f.write(json.dumps({"text": full_prompt}) + "\n")
    print("Successfully created train_dataset.jsonl")