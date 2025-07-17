import openai
from .config import OPENAI_API_KEY
from .supabase_client import get_part_from_supabase
from .plotly_utils import create_all_charts
from datetime import datetime
import re

openai.api_key = OPENAI_API_KEY

# Relevant months and columns
MONTHS = [
    'jan2023','feb2023','mar2023','apr2023','may2023','jun2023','jul2023','aug2023','sep2023','oct2023','nov2023','dec2023',
    'jan2024','feb2024','mar2024','apr2024','may2024','jun2024','jul2024','aug2024','sep2024','oct2024','nov2024','dec2024',
    'jan2025','feb2025','mar2025','apr2025','may2025','jun2025','jul2025','aug2025','sep2025','oct2025','nov2025','dec2025'
]

PART_REGEX = r'([A-Z]{2,}-\d{4,})'
PCT_REGEX = r'(\d+\.?\d*)\s*%'

async def analyze_part(db, message: str):
    # Extract part number and percentage
    part_match = re.search(PART_REGEX, message, re.IGNORECASE)
    pct_match = re.search(PCT_REGEX, message)
    part_number = part_match.group(1).strip().upper() if part_match else None
    pct_increase = float(pct_match.group(1)) if pct_match else 0.0

    if not part_number:
        return {
            'text': 'Please specify the part number (e.g., PA-10197) and describe the situation, including if the supplier is requesting a price increase and what the new price or percentage is.',
            'charts': [],
            'summary': None,
            'impact_analysis': None,
            'recommendations': None
        }

    print(f"Searching for PartNumber: '{part_number}'")
    # Search for the part using Supabase REST
    part = await get_part_from_supabase(part_number)
    if not part:
        return {
            'text': f'Part {part_number} was not found.',
            'charts': [],
            'summary': None,
            'impact_analysis': None,
            'recommendations': None
        }

    # Prices and volumes
    price_cols = [f'price{m}' for m in MONTHS]
    vol_cols = [f'vol{m}' for m in MONTHS]
    mkt_cols = [f'Pricemktindex{m}' for m in MONTHS]
    prices = [part.get(c, 0) for c in price_cols]
    vols = [part.get(c, 0) for c in vol_cols]
    mkt_prices = [part.get(c, None) for c in mkt_cols]

    # Current month
    now = datetime.now()
    current_month = now.strftime('%b').lower() + str(now.year)
    try:
        idx = MONTHS.index(current_month)
    except ValueError:
        idx = len(MONTHS) - 1

    current_price = prices[idx] if prices[idx] else 0
    new_price = current_price * (1 + pct_increase/100)
    currency = part.get('currency', '')

    # Estimated annual impact (2025)
    vols_2025 = [v or 0 for v in vols[24:]]
    impact_2025 = sum([v * (new_price - (prices[i+24] or 0)) for i, v in enumerate(vols_2025)])
    total_cost_2025 = sum([v * new_price for v in vols_2025])

    # Create all charts
    months_labels = [m.capitalize() for m in MONTHS]
    charts_data = create_all_charts(
        [p or 0 for p in prices],
        [m if m is not None else 0 for m in mkt_prices],
        [v or 0 for v in vols],
        months_labels,
        current_price,
        new_price
    )

    prompt = f"""
You are a procurement and negotiation expert. Analyze the following situation and provide a structured response in English:

**SUPPLIER INFORMATION:**
- Supplier: {part.get('suppliername', '')} ({part.get('suppliernumber', '')})
- Contact: {part.get('suppliercontactname', '')} ({part.get('suppliercontactemail', '')})
- Location: {part.get('suppliermanufacturinglocation', '')}

**PART INFORMATION:**
- Part: {part.get('PartNumber', '')} - {part.get('partname', '')}
- Material: {part.get('material', '')}
- Currency: {currency}

**PRICE ANALYSIS:**
- Current price: {current_price} {currency}
- Proposed new price: {new_price} {currency}
- Requested increase: {pct_increase}%
- Estimated impact in 2025: {impact_2025} {currency}
- Total estimated cost 2025: {total_cost_2025} {currency}

**User message:** {message}

Provide a structured response with the following sections:

1. **EXECUTIVE SUMMARY** (2-3 lines)
2. **IMPACT ANALYSIS** (detailed with numbers)
3. **NEGOTIATION RECOMMENDATIONS** (specific strategies)
4. **SUGGESTED RESPONSE** (full explanation for the user)

Format the response using markdown for better presentation. Do not include any label or title like 'Structured Response' in your answer.
"""
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a procurement and negotiation expert. Provide structured analysis and practical recommendations in English."},
            {"role": "user", "content": prompt}
        ]
    )
    
    full_text = response.choices[0].message.content.strip()
    
    # Parse the response to extract sections
    sections = parse_ai_response(full_text)
    
    return {
        'text': full_text,
        'charts': charts_data,
        'summary': sections.get('summary', ''),
        'impact_analysis': sections.get('impact_analysis', ''),
        'recommendations': sections.get('recommendations', '')
    }

def parse_ai_response(text: str) -> dict:
    """Parse AI response to extract different sections"""
    sections = {}
    if not text:
        return sections
    # Find sections by headers
    if '**EXECUTIVE SUMMARY**' in text:
        start = text.find('**EXECUTIVE SUMMARY**')
        end = text.find('**', start + 20)
        if end == -1:
            end = len(text)
        summary_text = text[start:end].replace('**EXECUTIVE SUMMARY**', '')
        if summary_text:
            summary_text = summary_text.strip()
        sections['summary'] = summary_text if summary_text else ''
    if '**IMPACT ANALYSIS**' in text:
        start = text.find('**IMPACT ANALYSIS**')
        end = text.find('**', start + 20)
        if end == -1:
            end = len(text)
        impact_text = text[start:end].replace('**IMPACT ANALYSIS**', '')
        if impact_text:
            impact_text = impact_text.strip()
        sections['impact_analysis'] = impact_text if impact_text else ''
    if '**NEGOTIATION RECOMMENDATIONS**' in text:
        start = text.find('**NEGOTIATION RECOMMENDATIONS**')
        end = text.find('**', start + 30)
        if end == -1:
            end = len(text)
        rec_text = text[start:end].replace('**NEGOTIATION RECOMMENDATIONS**', '')
        if rec_text:
            rec_text = rec_text.strip()
        sections['recommendations'] = rec_text if rec_text else ''
    return sections 