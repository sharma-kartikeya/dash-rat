import requests
from bs4 import BeautifulSoup
from .models.Paper import Paper

def scrap_papers_() -> str:
    keyword = 'artificial intelligence'
    page_size = 200
    papers = []
    page = 0
    while True:
        url = f'https://www.arxiv.org/search/?query={keyword.replace(" ", "+")}&searchtype=all&source=header&size={page_size}&order=-submitted_date&start={page*page_size}'
    
        response = requests.get(url)
        if not response.ok:
            return response.reason

        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('li', class_='arxiv-result')

        if not results:
            break
            
        for result in results:
            title = result.find('p', class_='title').text.strip()
            if not title:
                pass
            authors = [author.strip() for author in result.find('p', class_='authors').text.strip().replace("\n", " ").split(", ")]
            abstract = result.find('span', class_='abstract-full').text.strip()
            if not abstract:
                pass
            pdf_link = result.find('a', string='pdf')
            pdf_link = pdf_link['href'] if pdf_link else None
            pdf_link = f'https://arxiv.org{pdf_link}' if pdf_link and pdf_link.startswith('/') else pdf_link
            paper = Paper(title=title, authors=authors, abstract=abstract, link=pdf_link)
            paper.save()
        
        page += 1
    if len(papers) == 0:
        return 'Papers is empty'
    return 'Papers got scraped and saved'