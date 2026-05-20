import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# load openai api key from .env
load_dotenv()
# create client, grabs api key automatically
client = OpenAI()

def analyze_vehicle(db_data, listing_text, carfax_text, vehicle_id):
    # prompt to tell AI what to do with information, and response
    system_prompt = """
    You are Auto Assess, an expert automotive diagnostic AI. 
    Your job is to analyze database records, seller listings, and CARFAX reports to evaluate a used vehicle purchase.
    Be objective, balanced, and analytical. Do not use pleasantries. 
    
    CRITICAL INSTRUCTIONS:
    - Brevity Rule: You must use plain language and minimal adjectives/adverbs. Get straight to the point. Strip out all filler text, and excessive explanations.
    - You are evaluating a used vehicle; expect normal wear and tear. 
    - Differentiate between active/unmitigated catastrophic red flags and known platform flaws that have been actively mitigated by recorded maintenance.
    - Reward dense, consistent service records. Do not heavily penalize the vehicle for a database-known risk if the CARFAX or listing indicates the relevant component was recently serviced or replaced.
    - Seller Restrictions: You MUST flag EXPLICIT restrictions placed by the seller (e.g., "no test drives", "as-is") as a High Severity (8+) red flag under 'Listing Inference'. DO NOT infer restrictions from silence; only flag them if explicitly written in the listing text.
    - Historical Damage: Historical accidents from the CARFAX MUST always be included in 'critical_red_flags', even if repaired. Adjust the severity score downward based on the time elapsed and subsequent driving history.
    - Approaching Maintenance Cliffs: Include database-known issues in 'critical_red_flags' if the vehicle's mileage is within 20% of the typical failure window.
    
    You MUST respond strictly in valid JSON using the following structure:
    {
        "year": "<string, the 4-digit model year>",
        "make": "<string, the vehicle manufacturer>",
        "model": "<string, the specific vehicle model and trim>",
        "kms": "<string, the total distance driven in kilometers, formatted with commas, e.g., '63,000'>",
        "price": "<string, the vehicle asking price including currency symbol, e.g., 'CA$19,000'>",
        "risk_score": <int 1-10, 10 being highest overall risk. Weigh positive maintenance against known flaws and restrictions>,
        "verdict": "<A balanced evaluation. Start with a clear paragraph summarizing the buy/pass recommendation, weighing the risks against the positive indicators. Follow with a newline and a bulleted list explaining your reasoning.>",
        "critical_red_flags": [
            {
                "item": "<string describing the specific active issue, unmitigated flaw, seller restriction, historical accident, or approaching failure>",
                "severity_score": <int 1-10, 10 being catastrophic failure or severe buying restriction>,
                "source": "<Must be exactly one of: 'Database Match', 'Listing Inference', 'CARFAX Flag', 'AI Knowledge'>"
            }
        ],
        "positive_indicators": [
            {
                "item": "<string describing excellent maintenance, low mileage, mitigated risks, or high-value features>",
                "source": "<Must be exactly one of: 'Database Match', 'Listing Inference', 'CARFAX Flag', 'AI Knowledge'>"
            }
        ],
        "leverage_points": ["<string>", "<string>"]
    }
    
    Source Definitions:
    - 'Database Match': Information explicitly found in the provided DATABASE RECORDS.
    - 'Listing Inference': Information deduced from the SELLER LISTING TEXT.
    - 'CARFAX Flag': Information explicitly stated in the CARFAX REPORT.
    - 'AI Knowledge': Known platform information not present in the database but known to you.
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
            model="gpt-5.1",
            temperature=0.2, # low temp to focus on objective answer
            response_format={ "type": "json_object" }, # force return as JSON for frontend
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        # print number of tokens used in console
        usage = response.usage

        # Calculate approximate cost based on gpt-5.1 pricing per 1M tokens
        cached_tokens = getattr(usage.prompt_tokens_details, 'cached_tokens', 0) if hasattr(usage, 'prompt_tokens_details') else 0
        uncached_prompt_tokens = usage.prompt_tokens - cached_tokens
        
        # calculate approx cost per request 
        cost = (
            (uncached_prompt_tokens * 1.25 / 1_000_000) + 
            (cached_tokens * 0.125 / 1_000_000) + 
            (usage.completion_tokens * 10.00 / 1_000_000)
        )

        print(f"[API USAGE] Prompt Tokens: {usage.prompt_tokens} (Cached: {cached_tokens}) | Completion Tokens: {usage.completion_tokens} | Total: {usage.total_tokens} | Cost: ${cost:.3f}")

       # grab relevant response, inject vehicle_id, and return
        raw_json_string = response.choices[0].message.content
        analysis_data = json.loads(raw_json_string)
        
        # inject the ID directly into the dictionary root
        analysis_data['vehicle_id'] = vehicle_id 
        
        return analysis_data

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
            "positive_indicators": [], # Added to accommodate the new schema
            "leverage_points": []
        }