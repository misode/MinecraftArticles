import io
import itertools
import json
import urllib.request
import urllib.error
import html2text

bodyStartDetect = 'end-with-block' # minecraft.net
bodyStartDetect2 = '<article class="single-post post-content">' # mojang.com
bodyStartDetect3 = 'data-emptytext="Content Fragment"' # minecraft.net
bodyEndDetect = '<p>Report bugs here:</p>'
bodyEndDetect2 = 'Report bugs here:'
bodyEndDetect3 = '<div class="article-attribution-container"' # minecraft.net
bodyEndDetect4 = '</article>' # mojang.com

dateStartDetect = 'pubDate" data-value="' # minecraft.net
dateStartDetect2 = 'Posted on ' # mojang.com
dateEndDetect = 'T' # minecraft.net
dateEndDetect2 = 'by' # mojang.com

def loadArticle(url):
    try:
        response = urllib.request.urlopen(url);
        html = response.read().decode("utf-8")

        bodyStartIndex = html.find(bodyStartDetect)
        if bodyStartIndex == -1:
            bodyStartIndex = html.find(bodyStartDetect3)
        if bodyStartIndex == -1:
            bodyStartIndex = html.find(bodyStartDetect2)
        else:
            bodyStartIndex = html.find("<p>", bodyStartIndex)

        bodyEndIndex = html.find(bodyEndDetect, bodyStartIndex)
        if bodyEndIndex == -1:
            bodyEndIndex = html.find(bodyEndDetect2)
        if bodyEndIndex == -1:
            bodyEndIndex = html.find(bodyEndDetect3)
        if bodyEndIndex == -1:
            bodyEndIndex = html.find(bodyEndDetect4) + len(bodyEndDetect4)
        

        body = html[bodyStartIndex:bodyEndIndex]

        dateStartIndex = html.find(dateStartDetect)
        dateEndIndex = dateStartIndex
        if dateStartIndex == -1:
            dateStartIndex = html.find(dateStartDetect2) + len(dateStartDetect2)
            dateEndIndex = html.find(dateEndDetect2, dateStartIndex)
        else:
            dateStartIndex += len(dateStartDetect)
            dateEndIndex = html.find(dateEndDetect, dateStartIndex)
        date = html[dateStartIndex:dateEndIndex].strip()

        return (date, body)
    except urllib.error.URLError as e:
        return None

def scrapeArticle(name, url):
    article = loadArticle(url)
    if article is None:
        print(f"Invalid article url {url}")
        return

    (date, body) = article
    text = html2text.html2text(body)

    print(f"[{name}] {date} {text[0:40]}")
    with io.open('./articles/' + name + '.md', 'w', encoding="utf-8") as f:
        f.write('# ' + name + '\n')
        f.write('Published on ' + date + '\n\n')
        f.write(text)
        f.write('\n')

with open('articles.json', 'r') as f:
    articles = json.load(f)
    for name, url in articles.items():
        scrapeArticle(name, url)
