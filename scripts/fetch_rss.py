import feedparser
from datetime import datetime, timedelta
import os

# 수집할 RSS 피드
FEEDS = [
    "https://fe-developers.kakaoent.com/rss.xml",
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
    "https://engineering.linecorp.com/ko/feed/",
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
    feed = feedparser.parse(url)
    if feed.bozo:
        if hasattr(feed, "bozo_exception"):
            print(f"[⚠️ 실패] {url} - 이유: {feed.bozo_exception}")
        else:
            print(f"[⚠️ 실패] {url} - 이유 알 수 없음 (bozo=True)")
        continue

    for entry in feed.entries:
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
    f.write("<html><head><meta charset='utf-8'><title>최근 글</title></head><body>")
    f.write("<h1>고독한 개발자의 하루...</h1><ul>")
    for e in entries:
        f.write(f"<li><a href='{e['link']}' target='_blank'>{e['title']}</a> - {e['published']}</li>")
    f.write("</ul></body></html>")

# index.html 업데이트 (링크 목록으로)
existing_files = sorted(
    [fn for fn in os.listdir("output") if fn.endswith(".html") and fn != "index.html"]
)

with open("output/index.html", "w", encoding="utf-8") as f:
    f.write("<html><head><meta charset='utf-8'><title>RSS 인덱스</title></head><body>")
    f.write("<h1>고독한 개발자의 기록</h1><ul>")
    for fn in existing_files:
        f.write(f"<li><a href='{fn}'>{fn}</a></li>")
    f.write("</ul></body></html>")