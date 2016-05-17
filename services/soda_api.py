from sodapy import Socrata

client = Socrata("data.cityofnewyork.us", "Z9djfh6hUgBAIHC7gpZRscVBj")


def get_data(content_type="json", **kwargs):
    number_per_page = 5000
    #pages = range(number_per_page, 200000, number_per_page)
    pages = []
    data = client.get("e4qk-cpnv", content_type=content_type, limit=500000, **kwargs)
    for page in pages:
        temp_data = client.get("e4qk-cpnv", content_type=content_type, limit=500000, offset=page-number_per_page, **kwargs)
        data.extend(temp_data)
        if len(temp_data) < number_per_page:
            break
    return data

