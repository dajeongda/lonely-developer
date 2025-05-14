import feedparser
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 수집할 RSS 피드
FEEDS = [
    "https://tech.kakaoent.com/rss.xml",
    "https://techblog.woowahan.com/feed/",
    "https://medium.com/feed/daangn",
    "https://medium.com/feed/29cm",
    "https://d2.naver.com/d2.atom",
    "https://tech.kakaoenterprise.com/feed/",
    "https://tech.kakao.com/feed/",
    "https://tech.kakaobank.com/index.xml",
    "https://tech.kakaopay.com/rss",
    "https://medium.com/feed/coupang-tech",
    "https://dev.gmarket.com/rss",
    "https://medium.com/feed/deliverytechkorea",
    "https://medium.com/feed/zigbang",
    "https://tech.devsisters.com/rss.xml",
    "https://techblog.yogiyo.co.kr/feed/",
    "https://helloworld.kurly.com/feed.xml",
    "https://medium.com/feed/watcha",
    "https://techblog.lycorp.co.jp/ko/feed/index.xml",
    "https://ridicorp.com/story-category/tech-blog/feed/",
    "https://oliveyoung.tech/rss.xml",
    "https://gsretail.tistory.com/xml"
]

# 24시간 이내 글만
cutoff = datetime.utcnow() - timedelta(days=1)
today_str = datetime.utcnow().strftime("%y%m%d") 
print(f">>>> {cutoff}")
print(f">>>> {today_str}")

entries = []

for url in FEEDS:
    print(f">>>>>>>>> {url}")

    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            raise ValueError("bozo feed")

        fetched_entries = feed.entries

    except:
        print(f"{url}은 깨짐. fallback 방식으로 재시도 중...")
        res = requests.get(url, verify=False)
        soup = BeautifulSoup(res.content, "html5lib")
        feed = feedparser.parse(str(soup))
        fetched_entries = feed.entries

    for entry in fetched_entries:
        published = entry.get("published_parsed")
        print(f">>>> {published}")
        if not published:
            continue
        pub_date = datetime(*published[:6])
        if pub_date > cutoff:
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", ""),
                "published": pub_date.strftime("%Y-%m-%d %H:%M")
            })

    print(f"{url} - 총 {len(entries)}개의 글을 수집했습니다.")
    print("파일 생성 시작...")


os.makedirs("output", exist_ok=True)

# 날짜별 파일 생성: e.g. output/250409.html
daily_filename = f"output/{today_str}.html"
with open(daily_filename, "w", encoding="utf-8") as f:
    f.write("<h1>고독한 개발자의 하루...</h1>")

    if entries:
        f.write("<ul>")
        for e in entries:
            f.write(f"<li><a href='{e['link']}' target='_blank'>{e['title']}</a> - {e['published']}</li>")
        f.write("</ul>")
    else:
        f.write("<p>너무 고독해... 🍂</p>")

    f.write("</body></html>")

# output 디렉토리의 파일명 중 날짜 형식만 골라서 정렬
daily_files = []

today = datetime.today()
for i in range(0, 30):  # 오늘은 제외하고 어제로부터 30일 전까지
    day = today - timedelta(days=i)
    filename = day.strftime("%y%m%d") + ".html"
    daily_files.append(filename)

with open("output/index.html", "w", encoding="utf-8") as f:
    f.write("<html><head><meta charset='utf-8'><title>RSS 인덱스</title></head><body>")
    f.write("<h1>고독한 개발자의 기록 (최근 30일)</h1><ul>")
    for fn in daily_files:
        f.write(f"<li><a href='{fn}'>{fn}</a></li>")
    f.write("</ul></body></html>")
    