# -*- coding: utf-8 -*-

output_filename = "LondonFlats.lst.csv"
url_mode = "QUERY_DRIVEN"

def noAction(value):
    return value

def priceToMonthly(value):
    value = (value or "").replace(u"£", "").replace(",", "").split("p")
    if len(value) < 2:
        return ""
    else:
        price, interval = value
        return float(price) if interval=="m" else float(price)*4.357

url_prefix = "https://www.gumtree.com"
#url_base = "https://www.gumtree.com/search?q=&search_category=single-room-flatshare&search_location=London&distance=0.0001"
url_base = "https://www.gumtree.com/search?page=1&guess_search_category=single-room-flatshare&sort=date&q=&search_category=single-room-flatshare&search_location=central-london&distance=0"
url_jQuery_next_page = ["li.next>a.btn-secondary[title='Next page']", "href"]

url_stepper = {
    "prefix": "http://www.go-sport.com/sport/randonne/sacs-dos/l-7301401-",
    "func": "prefix + index + '.html'",
    "min": 1,
    "max": 4
}


jQuery_base = "article.listing-maxi>a.listing-link"
jQuery_mapping = [
    # field,    jQuery,                   attrib, method
    ("title", "h2.listing-title",           "", noAction),
    #("description", "p.listing-description", "", noAction),
    ("location", "div.listing-location>span", "", noAction),
    ("price", "strong.listing-price", "", priceToMonthly),
    ("product_url", "a.listing-link", "href", noAction)
]

# jQuery_mapping = {
#     "title": ["h2.listing-title", ""],
#     "description":  ["p.listing-description", ""],
#     "location": ["div.listing-location>span", ""],
#     "price": ["strong.listing-price", ""],
#     "product_url": ["a.listing-link", "href"]
# }
