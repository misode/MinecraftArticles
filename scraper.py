import io
import itertools
import urllib.request
import urllib.error
import html2text

articles = {
    "1.12-pre2":    "minecraft-112-pre-release-2",
    "1.12-pre5":    "minecraft-112-pre-release-3",
    "1.12-pre7":    "minecraft-112-pre-release-6",
    "1.12":         "world-color-released",
    "1.12.1":       "minecraft-1121-released",
    "1.12.2":       "minecraft-1122-released",
    "1.13":         "update-aquatic-out-java",
    "1.14-pre7":    "minecraft-1-14-4-pre-release-1",
    "1.14":         "village---pillage-out-java-",
    "1.14.1-pre2":  "minecraft-1-14-1-pre-release-1",
    "1.14.1":       "minecraft-java-edition-1-14-1",
    "1.14.2-pre4":  "minecraft-1-14-2-pre-release-1",
    "1.14.2":       "minecraft-java-edition-1-14-2",
    "1.14.3-pre4":  "minecraft-1-14-3-pre-release-1",
    "1.14.3":       "minecraft-java-edition-1-14-3",
    "1.14.4-pre7":  "minecraft-1-14-4-pre-release-1",
    "1.14.4":       "minecraft-java-1-14-4-released",
    "1.15-pre1":    "minecraft-1-15-pre-release-1",
    "1.15":         "buzzy-bees-out-now-in-java"
}

site = "https://www.minecraft.net/en-us/article/"
bodyStartDetect = 'end-with-block'
bodyEndDetect = '<p>Report bugs here:</p>'
bodyEndDetect2 = 'Report bugs here:'
dateStartDetect = 'pubDate" data-value="'
dateEndDetect = 'T'

def loadArticle(article):
    try:
        response = urllib.request.urlopen(site + article);
        html = response.read().decode("utf-8")

        bodyStartIndex = html.find(bodyStartDetect)
        bodyStartIndex = html.find("<p>", bodyStartIndex)
        bodyEndIndex = html.find(bodyEndDetect, bodyStartIndex)
        if bodyEndIndex == -1:
            bodyEndIndex = html.find(bodyEndDetect2, bodyStartIndex)
        body = html[bodyStartIndex:bodyEndIndex]

        dateStartIndex = html.find(dateStartDetect) + len(dateStartDetect)
        dateEndIndex = html.find(dateEndDetect, dateStartIndex)
        date = html[dateStartIndex:dateEndIndex]

        return (date, body)
    except urllib.error.URLError as e:
        return None

def scrapeArticle(name, article):
    article = loadArticle(article)
    if article is None:
        return

    (date, body) = article
    text = html2text.html2text(body)

    print(f"[{name}] {date} {text[0:40]}")
    with io.open('./articles/' + name + '.md', 'w', encoding="utf-8") as f:
        f.write('# ' + name + '\n')
        f.write('Published on ' + date + '\n\n')
        f.write(text)
        f.write('\n')

for (year, week) in itertools.product(range(17, 20), range(1, 54)):
    name = f"{year}w{week:02}a"
    scrapeArticle(name, "minecraft-snapshot-" + name)

for name, article in articles.items():
    scrapeArticle(name, article)
