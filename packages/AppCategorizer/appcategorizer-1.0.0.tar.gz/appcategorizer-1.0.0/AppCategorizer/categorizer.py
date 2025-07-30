import csv
from transformers import pipeline
from .data_sources import snap, flathub, apple_store, gog, itch_io, myabandonware, wikidata
from .utils.helpers import normalize_labels
from .category_processing.processor import (
    select_main_category,
    select_sub_categories,
)

def fetch_app_data(app_name):
    """Fetch application data from all sources."""
    snap_cats = snap.get_categories(app_name)
    flat_cats = flathub.get_categories(app_name)
    apple_cats = apple_store.get_categories(app_name)
    gog_cats = gog.get_categories(app_name)
    itch_cats = itch_io.get_categories(app_name)
    abandon_cats = myabandonware.get_categories(app_name)
    wiki_cats = wikidata.get_categories(app_name)

    # Organize all results in a dictionary
    raw_categories = {
        "Snapcraft": snap_cats,
        "Flathub": flat_cats,
        "Apple Store": apple_cats,
        "Gog": gog_cats,
        "Itch.io": itch_cats,
        "My Abandonware": abandon_cats,
        "Wikidata": wiki_cats,
    }

    # Filter empty results
    non_empty_results = {k: v for k, v in raw_categories.items() if v}
    return non_empty_results

def fetch_app_descriptions(app_name):
    """Fetch application descriptions from all sources."""
    # Fetch data from all sources
    flat_desc = flathub.get_description(app_name)
    snap_desc = snap.get_description(app_name)
    apple_desc = apple_store.get_description(app_name)
    gog_desc = gog.get_description(app_name)
    itch_desc = itch_io.get_description(app_name)

    # Organize all results in a dictionary
    raw_descriptions = {
        "Flathub": flat_desc,
        "Snapcraft": snap_desc,
        "Apple Store": apple_desc,
        "Gog": gog_desc,
        "Itch.io": itch_desc,
    }

    # Filter empty results
    non_empty_descriptions = {k: v for k, v in raw_descriptions.items() if v}

    if non_empty_descriptions:
        source_names = ', '.join(non_empty_descriptions.keys())
        descriptions = ' '.join(non_empty_descriptions.values())
        return {source_names: descriptions}
    else:
        return {}

def categorize_app(classifier, tags, descriptions):
    """Categorize the application based on tags and descriptions."""
    all_tags = []
    all_descriptions = list(descriptions.values())

    for tag_list in tags.values():
        all_tags.extend(tag_list)

    all_tags = list(set(all_tags))  # Remove duplicates
    normalized_tags = normalize_labels(all_tags).split(', ')

    results = []
 
    for description in all_descriptions:
        outputs = classifier(
            description, 
            normalized_tags,
            multi_label=True
        )
        results.append({
            "description": description,
            "labels": outputs['labels'],
            "scores": outputs['scores']
        })

    return results

# def load_model():
#     """Load and return the zero-shot classification model"""
#     return pipeline(
#         "zero-shot-classification",
#         model="facebook/bart-large-mnli"
#     )

def load_model():
    try:
        return pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        return None



def process_app(app_name, classifier=None):
    """Process a single application and return categories"""
    # if classifier is None:
    #     classifier = load_model()

    if classifier is None:
        classifier = load_model()
        if classifier is None:
            raise ValueError("Failed to load model")
        
    # Fetch data from all sources
    non_empty_results = fetch_app_data(app_name)
    if not non_empty_results:
        return app_name, "Unknown", None, []

    # Process categories
    main_cat = select_main_category(app_name, non_empty_results)
    sub_cats = select_sub_categories(main_cat, non_empty_results)

    # Fetch descriptions
    descriptions = fetch_app_descriptions(app_name)
    
    # AI categorization
    ai_category = None
    if descriptions:
        categorized_results = categorize_app(classifier, non_empty_results, descriptions)
        if categorized_results:
            ai_category = categorized_results[0]['labels'][0]
    
    return app_name, main_cat, ai_category, sub_cats

def batch_process(input_file, output_file, classifier=None):
    """Process applications from a file in batch mode"""
    if classifier is None:
        classifier = load_model()
    
    # Read input file
    with open(input_file, 'r') as f:
        apps = [line.strip() for line in f.readlines()]
    
    results = []
    
    # Process each application
    for app_name in apps:
        if app_name:  # Skip empty lines
            _, main_cat, ai_cat, _ = process_app(app_name, classifier)
            results.append((app_name, main_cat, ai_cat))
    
    # Write results to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Application', 'RuleBasedCategory', 'AICategory'])
        writer.writerows(results)
    
    return output_file