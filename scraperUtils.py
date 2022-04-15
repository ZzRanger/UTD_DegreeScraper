def initializeMajorRequirements(json_data, content):
    html_tag = None
    index = 0
    try:
        while True:
            html_tag = content[index]
            if 'cat-reqa' in html_tag.attrs['class']:
                if "Core Curriculum Requirements" in html_tag.text:
                    break
            index += 1

    except:
        print(json_data)

    return json_data, content[index:]


def isCourse(html_tag):
    if not shouldIgnore(html_tag):
        prefix, hours = html_tag.text.split(
            " ")[0], html_tag.text.split(" ")[1]
        if hours.isnumeric() or (len(hours) == 4 and hours[2:].isnumeric()):
            return True
        return False


def shouldParse(html_tag):
    stop_keywords = ["Fast Track", "Honors Programs", "Minors"]
    if any(keyword in html_tag.text for keyword in stop_keywords):
        return False
    elif any("footnote" in keyword for keyword in html_tag['class']):
        return False
    return True


def shouldIgnore(html_tag):
    if (html_tag.name == "p" and html_tag.text.strip() != ""):
        id = html_tag.attrs['class'][0]
        if id == "cat-reqg" or id == "cat-cat5":  # Add all courses to section

            return True
        return False
    else:
        return True


def parseMajorRequirementsData(content):
    keyword_list = ["choose", "select", "any",
                    "from the following", "semester credit hours"]
    index = 0
    html_tag = content[index]
    # Initialize first category
    category = {
        "type": "collection",
        "name": html_tag.text,
        "required": 0,
        "options": []
    }
    index += 1
    major = []

    html_tag = content[index]
    # Run until element becomes "Elective Requirements"
    while shouldParse(html_tag):
        # Ignore if not p element
        if not shouldIgnore(html_tag):
            print(html_tag.text, html_tag.text.strip()
                  == "", html_tag.attrs['class'])
            print()
            # Check if category
            if html_tag.attrs['class'][0] == "cat-reqa":
                # Append previous category to major
                category["required"] = len(category["options"])
                major.append(category)
                category = {
                    "type": "collection",
                    "name": html_tag.text,
                    "required": 0,
                    "options": []
                }
            # Check if OR Course
            elif html_tag.attrs['class'][2] == "catreq-cont":
                prev = category["options"].pop()
                group, course = None, None
                # Check if group already exists
                if "courses" not in prev.keys():
                    course = prev
                    group = {"name": "Choose one",
                             "type": "collection", "required": 0,
                             "courses": [course]}
                else:
                    group = prev
                # Check if it's an ANY course
                if "any" in html_tag.text.lower():
                    other = {"type": "other"}
                    other["description"] = html_tag.text
                    group["courses"].append(other)
                else:
                    temp = html_tag.text.split(" ")
                    classRequirement = {"type": "course",
                                        "class_reference": temp[1] + " " + temp[2]}
                    group["courses"].append(classRequirement)
                group["required"] = len(group["courses"])
                category["options"].append(group)
            # Check if Course Group
            elif any(keyword in html_tag.text.lower() for keyword in keyword_list):
                group = {"name": html_tag.text, "type": "collection",
                         "required": 0, "courses": []}
                index += 1
                html_tag = content[index]

                while isCourse(html_tag):
                    temp = html_tag.text.split(" ")
                    classRequirement = {"type": "course",
                                        "class_reference": temp[0] + " " + temp[1]}
                    group["courses"].append(classRequirement)
                    index += 1
                    html_tag = content[index]
                # Check if OR
                if html_tag.text.split(' ')[0].lower() == "or" or html_tag.text.split(' ')[0].lower() == "any":
                    other = {"type": "other"}
                    other["description"] = html_tag.text
                    group["courses"].append(other)
                    index += 1
                index -= 1
                # Check if valid Course Group
                if len(group["courses"]) > 0:
                    nameArr = group["name"].split(" ")
                    nameArr = [x.lower() for x in nameArr]
                    if nameArr[0].isnumeric():
                        group["required"] = int(nameArr[0]) / 3
                    elif nameArr[1].isnumeric():
                        group["required"] = int(nameArr[1]) / 3
                    elif nameArr[2].isnumeric():
                        group["required"] = int(nameArr[2]) / 3
                    elif "one" in nameArr:
                        group["required"] = 1
                    else:  # Error
                        temp = 0
                        # print("Error")
                    category["options"].append(group)
                else:  # OtherRequirement
                    group["type"] = "other"
                    del group["courses"]
                    group["description"] = group["name"]
                    del group["name"]
                    category["options"].append(group)
                # Check if Course
            elif isCourse(html_tag):
                temp = html_tag.text.split(" ")
                # Create CourseRequirement
                classRequirement = {"type": "course",
                                    "class_reference": temp[0] + " " + temp[1]}
                category["options"].append(classRequirement)
            else:  # OtherRequirement
                other = {"type": "other"}
                other["description"] = html_tag.text
                category["options"].append(other)

        index += 1
        html_tag = content[index]
    category["required"] = len(category["options"])
    major.append(category)
    return major
