from docparser import parseMdToJson, readFileAsString

file = "lb-web-service.en.md"
weblink = "https://aws.github.io/copilot-cli/docs/manifest/"
print(parseMdToJson(readFileAsString(file), file, weblink))