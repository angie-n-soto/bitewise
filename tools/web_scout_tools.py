import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any

def search_pet_food_brands(query: str) -> str:
    """
    Search online for pet food brands and products matching the description.
    
    Args:
        query: The search description (e.g. "grain-free wet cat food for seniors").
        
    Returns:
        A list of matching brand and product suggestions with basic details.
    """
    # Pragmatic mock representation of scouting results.
    # In a real app, this could query a product database or search API.
    data = [
        {"brand": "Orijen", "product": "Fit & Trim Dry Cat Food", "features": "High protein, grain-free, contains chicken, turkey, wild-caught fish"},
        {"brand": "Acana", "product": "Wild Atlantic Dry Dog Food", "features": "70% whole fish ingredients, grain-free, high protein"},
        {"brand": "Wellness", "product": "Complete Health Senior Wet Dog Food", "features": "Flaked chicken and peas, supports joint health, low sodium"},
        {"brand": "Royal Canin", "product": "Veterinary Diet Hydrolyzed Protein", "features": "For dogs/cats with food sensitivities, hydrolyzed soy protein"},
        {"brand": "Hill's Science Diet", "product": "Sensitive Stomach & Skin Dry Dog Food", "features": "Prebiotic fiber, highly digestible, gentle on stomach"}
    ]
    
    # Filter mocks loosely based on the query for a dynamic feel
    results = []
    query_lower = query.lower()
    for item in data:
        if (item["brand"].lower() in query_lower or 
            item["product"].lower() in query_lower or 
            any(f.lower() in query_lower for f in item["features"].split())):
            results.append(item)
            
    if not results:
        results = data[:3] # Default fallback suggestions
        
    return json.dumps({"suggestions": results}, indent=2)


def search_veterinary_articles(query: str) -> str:
    """
    Search vet-backed articles and academic sources (like Google Scholar mocks) 
    for health guidelines, allergies, and dietary recommendations.
    
    Args:
        query: Medical topic or condition (e.g., "pancreatitis in dogs diet", "hydrolyzed protein").
        
    Returns:
        A summary of recommendations and citations from veterinary sources.
    """
    db = {
        "pancreatitis": {
            "guideline": "Dogs recovering from pancreatitis require a highly digestible, ultra-low-fat diet (<10-12% fat on dry matter basis). Avoid table scraps and high-fat treats.",
            "sources": ["Journal of Veterinary Internal Medicine (2021) - Canine Pancreatitis Nutritional Management", "AAHA Guidelines on Low-Fat Diets (2023)"]
        },
        "allergy": {
            "guideline": "For suspected food allergies, an elimination trial using a hydrolyzed protein diet or novel protein (e.g., venison, rabbit) for 8-12 weeks is recommended.",
            "sources": ["Veterinary Dermatology Review (2020) - Food Allergies in Cats and Dogs", "World Small Animal Veterinary Association (WSAVA) Nutrition Guidelines"]
        },
        "skin": {
            "guideline": "Diets rich in Omega-3 and Omega-6 fatty acids (EPA/DHA from fish oil) support skin barrier health and reduce inflammation in pets with atopic dermatitis.",
            "sources": ["American Journal of Veterinary Research (2022)", "Vet Clinics of North America: Small Animal Practice"]
        }
    }
    
    query_lower = query.lower()
    for key, info in db.items():
        if key in query_lower:
            return json.dumps(info, indent=2)
            
    return json.dumps({
        "guideline": "Consult a veterinarian to perform bloodwork and tailor nutrition. General recommendation is to feed WSAVA-compliant brands (e.g., Hill's, Royal Canin, Purina Pro Plan) which undergo clinical feeding trials.",
        "sources": ["WSAVA Global Nutrition Committee Guidelines"]
    }, indent=2)


def check_pet_food_recalls(brand: str) -> str:
    """
    Search latest safety reports, FDA recall lists, and news articles for safety warning issues.
    
    Args:
        brand: The brand name to check (e.g., "Orijen", "Purina").
        
    Returns:
        FDA recall history or active safety alerts for the brand.
    """
    # Mocks representing FDA recall database
    recalls = [
        {"brand": "Darwin's", "date": "2023-09-15", "reason": "Potential Salmonella contamination in select raw pet food batches", "severity": "High"},
        {"brand": "Midwestern Pet Foods", "date": "2021-03-22", "reason": "Aflatoxin levels exceeding safety limits", "severity": "Critical"},
        {"brand": "Sportmix", "date": "2021-01-11", "reason": "Aflatoxin contamination", "severity": "Critical"}
    ]
    
    brand_lower = brand.lower()
    matches = [r for r in recalls if r["brand"].lower() in brand_lower]
    
    if matches:
        return json.dumps({"brand": brand, "has_recalls": True, "details": matches}, indent=2)
    else:
        return json.dumps({"brand": brand, "has_recalls": False, "status": "No active FDA recall history or news safety warnings found in the database."}, indent=2)


def analyze_ingredients(ingredients: str) -> str:
    """
    Analyze pet food ingredient list to flag allergies, fillers, and toxic ingredients.
    
    Args:
        ingredients: A comma-separated list of ingredients.
        
    Returns:
        An analysis report of the ingredients with warnings and recommendations.
    """
    ingredients_list = [i.strip().lower() for i in ingredients.split(",")]
    
    flags = []
    toxic_warnings = []
    
    # Check for known dangerous ingredients
    toxic_items = ["onion", "garlic", "grape", "raisin", "chocolate", "xylitol", "macadamia nut"]
    for toxic in toxic_items:
        if any(toxic in ing for ing in ingredients_list):
            toxic_warnings.append(f"CRITICAL WARNING: Contains '{toxic}', which is toxic to dogs and cats!")
            
    # Check for controversial artificial preservatives / fillers
    fillers = ["corn gluten meal", "wheat gluten", "soy hulls", "powdered cellulose"]
    for filler in fillers:
        if any(filler in ing for ing in ingredients_list):
            flags.append(f"Filler: '{filler}' is used to increase bulk and protein content cheaply, but offers less biological value than whole meat.")
            
    preservatives = ["bha", "bht", "ethoxyquin", "propylene glycol", "carrageenan"]
    for pres in preservatives:
        if any(pres == ing or pres in ing.split() for ing in ingredients_list):
            flags.append(f"Preservative/Additive Warning: '{pres}' is a controversial artificial additive or binding agent linked to potential health risks in long-term feeding.")

    # Check for whole meat source
    has_whole_meat = False
    if ingredients_list and any(meat in ingredients_list[0] for meat in ["chicken", "turkey", "beef", "salmon", "lamb", "duck", "fish"]):
        has_whole_meat = True
        
    report = {
        "ingredient_count": len(ingredients_list),
        "first_ingredient": ingredients_list[0] if ingredients_list else "None",
        "has_whole_meat_first": has_whole_meat,
        "toxic_ingredients": toxic_warnings,
        "controversial_ingredients_or_fillers": flags,
        "assessment": "Excellent starting profile" if has_whole_meat and not flags and not toxic_warnings else "Needs review"
    }
    
    return json.dumps(report, indent=2)
