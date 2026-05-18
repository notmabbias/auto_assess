import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# load openai api key from .env
load_dotenv()
# create client, grabs api key automatically
client = OpenAI()

def analyze_vehicle(db_data, listing_text, carfax_text):
    # prompt to tell AI what to do with information, and response
    system_prompt = """
    You are Auto Assess, an expert automotive diagnostic AI. 
    Your job is to analyze database records, seller listings, and CARFAX reports to evaluate a used vehicle purchase.
    Be objective, highly critical, and concise. Do not use pleasantries.
    
    You MUST respond strictly in valid JSON using the following structure:
    {
        "risk_score": <int 1-10, 10 being highest overall risk>,
        "verdict": "<short paragraph summarizing the buy/pass recommendation>",
        "critical_red_flags": [
            {
                "item": "<string describing the specific issue>",
                "severity_score": <int 1-10, 10 being catastrophic failure>,
                "source": "<Must be exactly one of: 'Database Match', 'Listing Inference', 'CARFAX Flag', 'AI Knowledge'>"
            }
        ],
        "leverage_points": ["<string>", "<string>"]
    }
    
    Source Definitions:
    - 'Database Match': Issues explicitly found in the provided DATABASE RECORDS.
    - 'Listing Inference': Risks deduced from reading between the lines of the SELLER LISTING TEXT.
    - 'CARFAX Flag': Issues explicitly stated in the CARFAX REPORT.
    - 'AI Knowledge': Known platform issues not present in the database but known to you.
    """

    # user prompt using json.dump to turn dictionary into readable string for AI
    user_prompt = f"""
    DATABASE RECORDS:
    {json.dumps(db_data, indent=2)}

    SELLER LISTING TEXT:
    {listing_text if listing_text else "No listing text provided."}

    CARFAX REPORT:
    {carfax_text if carfax_text else "No CARFAX provided."}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2, # low temp to focus on objective answer
            response_format={ "type": "json_object" }, # force return as JSON for frontend
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        # print number of tokens used in console
        usage = response.usage
        print(f"[API USAGE] Prompt Tokens: {usage.prompt_tokens} | Completion Tokens: {usage.completion_tokens} | Total: {usage.total_tokens}")

        # grab relevant response and return
        raw_json_string = response.choices[0].message.content
        return json.loads(raw_json_string)

    # error handling if AI doesnt connect
    except Exception as e:
        print(f"[API ERROR] {e}")
        return {
            "risk_score": -1, # -1 for frontend detection of failure
            "verdict": "ERROR: AI Analysis failed to complete.",
            "critical_red_flags": [
                {
                    "item": "API connection or parsing error.",
                    "severity_score": 10,
                    "source": "System Error"
                }
            ],
            "leverage_points": []
        }