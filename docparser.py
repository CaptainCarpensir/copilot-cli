import marko
from bs4 import BeautifulSoup as bs, NavigableString, Tag

def readFileAsString(fileName: str):
    file = open(fileName)
    return file.read()

def parseMdToJson(inStream: str, fileName: str, weblink: str):
    res = ""
    inStream = inStream.replace("`", "")
    markoStream = marko.convert(inStream)
    soup = bs(markoStream, 'html.parser')

    fileName = fileName.split('.')[0]
    
    for tag in soup.find_all("p"):
        ancestors = ""
        href = ""
        field = ""
        type = ""
        description = ""
        for children in tag.contents:
            if isinstance(children, Tag):
                if "class" in children.attrs:
                    if "parent-field" in children.attrs["class"]:
                        ancestors = children.string
                    if "field" in children.attrs["class"]:
                        field = children.string
                        href = children.attrs["href"]
                    if "type" in children.attrs["class"]:
                        type = children.string
            if isinstance(children, NavigableString):
                description = str(children).strip()
                description = description.replace("\n", " ")

        #
        #   If 'desc' matches '% include' then print as ref
        #   If 'type' is not "" then print as field
        #

        if type != "":
            res = res + "{\n\t\"field\": \"" + ancestors + field + "\"\n"
            res = res + "\t\"type\": \"" + type + "\"\n"
            res = res + "\t\"desc\": \"" + description + "\"\n"
            res = res + "\t\"link\": \"" + weblink + fileName + "/" + href + "\"\n"
            res = res + "}\n"
        if "% include" in description:
            description = description.replace("{% include \'", "")
            description = description.replace(".md\' %}", "")
            res = res + "{\n\t\"ref\": \"" + description + "\"\n"
            res = res + "}\n"

    res = res.strip()

    return res