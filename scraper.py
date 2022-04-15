import bs4
import requests
from bs4 import BeautifulSoup
import json

from scraperUtils import initializeMajorRequirements, parseMajorRequirementsData


# Aggregate all URLs in a JSON file
urls = [
    "/2021/undergraduate/programs/ah/history",
    "/2021/undergraduate/programs/ah/latin-american-studies",
    "/2021/undergraduate/programs/ah/literature",
    "/2021/undergraduate/programs/ah/literature-creative-writing",
    "/2021/undergraduate/programs/ah/literature-rhetoric-and-communication",
    "/2021/undergraduate/programs/ah/literature-spanish",
    "/2021/undergraduate/programs/ah/philosophy",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-art-history",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-communication",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-dance",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-film",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-interdisciplinary-arts",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-music",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-photo-video-digital",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-theatre",
    "/2021/undergraduate/programs/ah/visual-and-performing-arts-visual-arts",
    "/2021/undergraduate/programs/atec/arts-and-technology",
    "/2021/undergraduate/programs/atec/arts-and-technology-animation",
    "/2021/undergraduate/programs/atec/arts-and-technology-critical-media-studies",
    "/2021/undergraduate/programs/atec/arts-and-technology-emerging-media-arts",
    "/2021/undergraduate/programs/bbs/child-learning-and-development",
    "/2021/undergraduate/programs/bbs/cognitive-science",
    "/2021/undergraduate/programs/bbs/neuroscience",  # CORNY
    "/2021/undergraduate/programs/bbs/psychology",
    "/2021/undergraduate/programs/bbs/speech-language-and-hearing-sciences",
    "/2021/undergraduate/programs/epps/criminology",
    "/2021/undergraduate/programs/epps/criminology-biology",
    "/2021/undergraduate/programs/epps/economics",
    "/2021/undergraduate/programs/epps/economics-finance",
    "/2021/undergraduate/programs/epps/geospatial-information-science",

    "/2021/undergraduate/programs/epps/international-political-economy",
    "/2021/undergraduate/programs/epps/international-political-economy-global-business",  # CORNY
    "/2021/undergraduate/programs/epps/political-science",
    "/2021/undergraduate/programs/epps/public-affairs",
    "/2021/undergraduate/programs/epps/public-policy",
    "/2021/undergraduate/programs/epps/sociology",
    "/2021/undergraduate/programs/ecs/biomedical-engineering",  # CORNY
    "/2021/undergraduate/programs/ecs/computer-engineering",
    "/2021/undergraduate/programs/ecs/computer-science",
    "/2021/undergraduate/programs/data-science",
    "/2021/undergraduate/programs/ecs/electrical-engineering",
    "/2021/undergraduate/programs/ecs/mechanical-engineering",
    "/2021/undergraduate/programs/ecs/software-engineering",
    "/2021/undergraduate/programs/is/american-studies",
    # "/2021/undergraduate/programs/is/healthcare",  # VERY CORNY
    "/2021/undergraduate/programs/is/education",  # CORNY
    "/2021/undergraduate/programs/is/interdisciplinary-studies",
    "/2021/undergraduate/programs/jsom/accounting",
    "/2021/undergraduate/programs/jsom/business-administration",
    "/2021/undergraduate/programs/jsom/business-analytics",
    "/2021/undergraduate/programs/jsom/finance",
    "/2021/undergraduate/programs/jsom/finance-economics",
    "/2021/undergraduate/programs/jsom/global-business",
    "/2021/undergraduate/programs/jsom/global-business-human-resource-management",  # CORNY
    "/2021/undergraduate/programs/jsom/global-business-international-political-economy",  # CORNY
    "/2021/undergraduate/programs/jsom/global-business-marketing",
    "/2021/undergraduate/programs/jsom/global-business-supply-chain-management",
    "/2021/undergraduate/programs/jsom/healthcare-management",
    "/2021/undergraduate/programs/jsom/healthcare-management-biology",
    "/2021/undergraduate/programs/jsom/healthcare-management-molecular-biology",
    "/2021/undergraduate/programs/jsom/human-resource-management",
    "/2021/undergraduate/programs/jsom/global-business-human-resource-management",
    "/2021/undergraduate/programs/jsom/information-technology-systems",
    "/2021/undergraduate/programs/jsom/marketing",
    "/2021/undergraduate/programs/jsom/global-business-marketing",
    "/2021/undergraduate/programs/jsom/supply-chain-management",
    "/2021/undergraduate/programs/jsom/global-business-supply-chain-management",
    "/2021/undergraduate/programs/nsm/biology",
    "/2021/undergraduate/programs/nsm/biology-criminology",
    "/2021/undergraduate/programs/nsm/biology-healthcare-management",
    "/2021/undergraduate/programs/nsm/molecular-biology",
    "/2021/undergraduate/programs/nsm/molecular-biology-healthcare-management",
    # "/2021/undergraduate/programs/nsm/biochemistry",  # VERY CORNY
    # "/2021/undergraduate/programs/nsm/chemistry",  # VERY CORNY
    "/2021/undergraduate/programs/nsm/geosciences",
    "/2021/undergraduate/programs/nsm/actuarial-science",
    "/2021/undergraduate/programs/data-science",
    # "/2021/undergraduate/programs/nsm/mathematics", # LOOK LATER
    "/2021/undergraduate/programs/nsm/physics",
    # "/2021/undergraduate/programs/nsm/biomedical-sciences"  # VERY CORNY
]

for url in urls:
    page = requests.get("https://catalog.utdallas.edu/2021" + url)
    print("SUCCESS")

    soup = BeautifulSoup(page.content, "html.parser")

    # List of all relevant html elements
    content: "list[bs4.element.Tag]" = soup.find_all(["p", "h5", "h3"])

    # Initialize JSON file
    headers = soup.findAll("h2")
    name = None
    abbrev = None
    hours = soup.find("p", class_="cat-degh").text.split(" ")[2][1:]
    for header in headers:
        if "Bachelor" in header.text:
            name = header.text
        elif "(BS)" in header.text or "(BA)" in header.text:
            abbrev = header.text

    json_data = {}
    json_data["name"] = name
    json_data["abbreviation"] = abbrev
    json_data["minimum_credit_hours"] = hours
    json_data["subtype"] = "major"

    # Initialize json file
    json_data, content = initializeMajorRequirements(json_data, content)

    # Store major requirements data here

    major = parseMajorRequirementsData(content)

    json_data["requirements"] = major
    json_str = json.dumps(json_data)

    with open("./degreeData/" + json_data["name"] + '.json', 'w') as outfile:
        outfile.write(json_str)
    print(json_data["name"])
