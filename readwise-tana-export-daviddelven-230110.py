import datetime
import requests  # This may need to be installed from pip
import json
import re

token = 'Readwise API Token'

def fetch_from_export_api(updated_after=None):
    full_data = []
    next_page_cursor = None
    while True:
        params = {}
        if next_page_cursor:
            params['pageCursor'] = next_page_cursor
        if updated_after:
            params['updatedAfter'] = updated_after
        print("Making export api request with params " + str(params) + "...")
        response = requests.get(
            url="https://readwise.io/api/v2/export/",
            params=params,
            headers={"Authorization": f"Token {token}"}, verify=False
        )
        full_data.extend(response.json()['results'])
        next_page_cursor = response.json().get('nextPageCursor')
        if not next_page_cursor:
            break

    return full_data

# Get all of a user's books/highlights from all time
all_data = fetch_from_export_api()

json_object_string = json.dumps(all_data, indent=4)

json_object = json.loads(json_object_string)

for item in json_object:

    with open("readwise-tana-export", "a") as outfile:
        outfile.write("%%tana%%\n")


    bookTags = item["book_tags"]
    highlights = item["highlights"]
    title = item["title"]
    url = item["source_url"]
    category = item["category"]
    author = item["author"]
    with open("readwise-tana-export", "a") as outfile:

        outfile.write(f"- Rw-{title} #🅢webSource #🅢referenceNote\n") 

        def getBookTags():

            bookTagArray = []
            bookTagList = ""

            for bookTag in bookTags:

                bookTagItem = bookTag["name"]
                bookTagArray.append(f"@{bookTagItem}")
                bookTagList = ','.join(bookTagArray)

            return bookTagList
            
        bookTags = getBookTags()
        outfile.write(f"  - 🅢topic:: {bookTags} #🅢topic\n")
        outfile.write(f"  - 🅢source URL:: {url} #🅢link\n")
        outfile.write(f"  - 🅢author:: {author} #🅢author\n")
        outfile.write("  - 🅢full-title::\n")
        outfile.write(f"  - 🅢category:: {category}\n")
        outfile.write("  - 🅢highlight-Date::\n")
        outfile.write("  - 🅢highlight-Time::\n")
        outfile.write("  - 🅢highlight-Source::\n")
        outfile.write("  - highlights:\n")

        for highlight in highlights:

            
            tags = highlight["tags"]


            highlightText = highlight["text"]
            highlightNote = highlight["note"]

            lines = highlightText.split("\n");

            for line in lines:

                cleanedLine = re.sub("/•\s+/", "", line.strip());

                if (len(cleanedLine) > 0):

                    outfile.write(f"    - {cleanedLine} #🅢highlight\n")

                    def getHighlightTags():

                        tagList = ""
                        tagArray = []
                    
                        for tag in tags:
                            tagItem = tag["name"]
                            tagArray.append(f"@{tagItem}")
                            tagList = ','.join(tagArray)
                        return tagList

                    highlightTags = getHighlightTags()
                    outfile.write(f"      - 🅢topic:: {highlightTags} #🅢topic\n")
                    
                    outfile.write(f"      - 🅢highlight-Note:: {highlightNote} #🅢fleetingNote\n") 

    print(item["title"])
