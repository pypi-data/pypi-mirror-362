import requests

is_gh = True
url = "https://stainlesteel.github.io/squid-game-api"

def set_hostname(string):
    global url
    global is_gh
    if validators.hostname(string.lower()):
        if not string.lower() == "github.io":
            is_gh = True
            string.lower() == url
        else:
            is_gh = False
            string.lower() == url
        if url.endswith("/"):
            url.removesuffix("/")
    else:
        return("sg-api.py: Not a valid hostname")

def characters(season, number, field=None):
    global is_gh
    global url
    if is_gh == True:
        no_s3 = True
    else:
        no_s3 = False
    mustard = f"{number:03}"
    ketchup = f"{season}"
    if season == 3 and is_gh == True:
        actual_url = f"{url}/s2/characters/{mustard}.json"
    else:
        actual_url = f"{url}/s{ketchup}/characters/{mustard}.json"
    resp = requests.get(actual_url)
    data = resp.json()
    if field == "title":
        return(f"{data['title']}")
    elif field == "name":
        return(f"{data['name']}")
    elif field == "aliases":
        return(f"{data['aliases']}")
    elif field == "family":
        return(f"{data['family']}")
    elif field == "relations":
        return(f"{data['relations']}")
    elif field == "affliation":
        return(f"{data['affliation']}")
    elif field == "occupation":
        return(f"{data['occupation']}") 
    elif field == "birth":
        return(f"{data['born']}")
    elif field == "fate":
        return(f"{data['fate']}")
    elif field == "appearances":
        return(f"{data['appearances']}")
    else:    
     for key, value in data.items():
        return(f"{key}: {value}")
 

def episodes(season, number, field=None):
    global is_gh
    global url
    if is_gh == True:
        no_s3 = True
    else:
        no_s3 = False
    mustard = f"{number:03}"
    ketchup = f"{season}" 
    if season == 3 and is_gh == True:
        actual_url = f"{url}/s2/episodes-s3/{mustard}.json"
    else:
        actual_url = f"{url}/s{ketchup}/episodes/{mustard}.json"
    resp = requests.get(actual_url)
    data = resp.json()
    if field == "title":
        return(f"{data['title']}")
    elif field == "details":
        return(f"{data['episode_details']}")
    elif field == "info":
        return(f"{data['episode_information']}")
    elif field == "guide":
        return(f"{data['episode_guide']}")
    else:    
     for key, value in data.items():
        return(f"{key}: {value}")
