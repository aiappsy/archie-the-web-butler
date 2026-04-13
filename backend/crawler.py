import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import os

class ArchieCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.to_visit = [base_url]
        self.results = {
            "pages": [],
            "media": [],
            "broken_links": [],
            "audit": {
                "total_pages": 0,
                "duplicate_titles": 0,
                "thin_content_pages": 0
            }
        }

    async def crawl(self, max_pages=10):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            count = 0
            while self.to_visit and count < max_pages:
                url = self.to_visit.pop(0)
                if url in self.visited:
                    continue
                
                print(f"Crawling: {url}")
                self.visited.add(url)
                
                try:
                    response = await page.goto(url, timeout=30000)
                    if response.status != 200:
                        self.results["broken_links"].append({"url": url, "status": response.status})
                        continue

                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract page info
                    title = soup.title.string if soup.title else "No Title"
                    text_content = soup.get_text()
                    
                    page_data = {
                        "url": url,
                        "title": title,
                        "word_count": len(text_content.split()),
                        "status": 200
                    }
                    self.results["pages"].append(page_data)

                    # Extract media
                    for img in soup.find_all('img'):
                        src = img.get('src')
                        if src:
                            full_src = urljoin(url, src)
                            self.results["media"].append({
                                "src": full_src,
                                "alt": img.get('alt', ''),
                                "parent_page": url
                            })

                    # Find internal links
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href:
                            full_href = urljoin(url, href)
                            if urlparse(full_href).netloc == self.domain and full_href not in self.visited:
                                self.to_visit.append(full_href)

                    count += 1
                except Exception as e:
                    print(f"Error crawling {url}: {e}")
                    self.results["broken_links"].append({"url": url, "error": str(e)})

            await browser.close()
            self._finalize_audit()
            return self.results

    def _finalize_audit(self):
        self.results["audit"]["total_pages"] = len(self.results["pages"])
        titles = [p["title"] for p in self.results["pages"]]
        self.results["audit"]["duplicate_titles"] = len(titles) - len(set(titles))
        self.results["audit"]["thin_content_pages"] = len([p for p in self.results["pages"] if p["word_count"] < 100])

if __name__ == "__main__":
    # Test run
    crawler = ArchieCrawler("https://example.com")
    results = asyncio.run(crawler.crawl(max_pages=2))
    print(json.dumps(results, indent=2))
