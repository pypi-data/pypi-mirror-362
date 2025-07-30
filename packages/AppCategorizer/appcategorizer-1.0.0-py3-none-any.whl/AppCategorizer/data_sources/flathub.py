import requests

def get_app_info(app_name):
    try:
        url_search = f"https://flathub.org/api/v2/compat/apps/search/{app_name}"
        headers = {"accept": "application/json"}
        
        response_search = requests.get(url_search, headers=headers)
        response_search.raise_for_status()
        
        data_search = response_search.json()
        
        app_info = None
        for app in data_search:
            if app["name"].lower() == app_name.lower():
                app_id = app["flatpakAppId"]
                url_app = f"https://flathub.org/api/v2/compat/apps/{app_id}"
                response_app = requests.get(url_app, headers=headers)
                response_app.raise_for_status()
                data_app = response_app.json()
                
                app_info = {
                    "category": [category["name"] for category in data_app["categories"]],
                    "description": app["summary"]
                }
                break
        
        return app_info
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_categories(app_name):
    app_info = get_app_info(app_name)
    if app_info:
        return app_info["category"]
    else:
        return None

def get_description(app_name):
    app_info = get_app_info(app_name)
    if app_info:

        print(app_info["description"])
        return app_info["description"]
    else:
        return None