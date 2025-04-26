import serpapi
api_key = 'b1d1872d32ab72345e660c5771f71226b7c4806fe4162f059939c0975f46ee60'

def get_image_url(query):
    search = serpapi.search({
        "q": query,
        "engine": "google_images",
        "api_key": api_key
    })
    if "images_results" in search and search["images_results"]:
        return search["images_results"][0]["original"]
    return None