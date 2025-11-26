#File for building prompts, no storing in db, no llm calls, just buidling

def build_prompt1(data: dict) -> str:
    profile = data["profile"]
    summary = data.get("summary", "")
    relevant_qa = data.get("relevant_qa", [])
    missing_fields = data.get("missing_fields", [])
    current_sector = data.get("current_sector", None)
    qa_in_sector = data.get("qa_in_sector", [])

    prompt = f"""
    identity ...
    instructions..
    {profile}
    {summary}
    {relevant_qa}
    {missing_fields}
    {relevant_qa}
    {current_sector}
    {qa_in_sector}

    1. generate next question (cover scope 1, 2 and 3)
    2. update sector completion flag if sector complete, if complete then also tell the next sector its going to ask
       unless analyis complete
    3. Extract STRUCTURED_FIELDS from the user's LAST ANSWER:
         - entity_id (create new if needed) , e.g.: diesel_generator
         - field_name, e.g.: number of hours operated(day)
         - field_type, e.g: float/text
         - field_value, e.g: 12
    4. if all sectors complete and no more questions to ask then mark analysis completion flag
    5. give updated_missing_field only if there was any missing field.

    respond only in this JSON format:
    {{
        "next_question": "...",
        "sector_complete": true/false,
        "next_sector": null or "sector_name",
        "analysis_complete": true/false,
        "updated_missing_field": [...]
        "extracted fields": [
            {
                "entity_id": "...",
                "field_name": "...",
                "field_type": "...",
                "field_value_text": "...",
                "field_vale_float": ...
            }
        ]
    }}
    """

    return prompt.strip()

def build_prompt2(data: dict) -> str:
    previous_summary = data.get("previous_summary", "")
    recent_qa = data.get("recent_qa", [])

    prompt = f"""
    identity ...
    instructions..
    {previous_summary}
    {recent_qa}

    Update the summary so it remains concise but complete.
    NEVER lose previously included information.

    Respond ONLY as:
    {{
        "updated_summary": "..."
    }}
    """

    return prompt.strip()

def build_prompt3A(data: dict) -> str:
    summary = data["summary"]
    sector = data["sector"]
    structured_fields = data["structured_fields"]
    correction_note = data.get("correction_note", None)

    prompt = f"""
    identity...
    instructions...

    {sector}
    {summary}
    {structured_fields}
    {correction_note}

    RULES:
    - Convert ALL data to ANNUAL emissions (yearly CO₂e).
    - Show ALL unit conversions (daily → weekly → yearly, etc.)
    - Provide:
        * raw_emissions (JSON)
        * raw_calculation_steps (text)
        * Correction Note in case wrong calculation (given by prompt 3B)

    Respond ONLY in this JSON shape:

    {{
        "raw_emissions": {{ ... }},
        "raw_calculation_steps": "...",
    }}
    """
    return prompt.strip()

def build_prompt3B(data: dict) -> str:
    """
    Prompt 3B: Critique emissions + give confidence score.
    Requires:
        - identity
        - instructions
        - raw_emissions
        - raw_calculation_steps
        - structured_fields
    """
    raw_emissions = data["raw_emissions"]
    raw_steps = data["raw_steps"]
    structured_fields = data["structured_fields"]

    prompt = f"""
    identity...
    instructions...

    {raw_emissions}
    {raw_steps}
    {structured_fields}

    CHECK:
    1. Identify any errors in unit conversion.
    2. Identify missing inputs that harm accuracy.
    3. Give a confidence score 0-1.
    4. Provide notes for correction if needed.

    Respond ONLY in this JSON shape:

    {{
        "calculation_valid": true/false,
        "confidence_model": float,
        "missing_fields": [...],
        "top_sources": [...],
        "final_calculation_steps": "..."
    }}
    """
    return prompt.strip()