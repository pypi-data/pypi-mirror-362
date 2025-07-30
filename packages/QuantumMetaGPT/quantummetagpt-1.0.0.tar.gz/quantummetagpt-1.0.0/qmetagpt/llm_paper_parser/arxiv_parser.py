import arxiv
from ..utils.logger import get_logger
from ..licensing import require_license

logger = get_logger(__name__)

@require_license(features=['pro'])
def parse_arxiv_paper(paper_id: str):
    try:
        client = arxiv.Client()
        search = arxiv.Search(id_list=[paper_id])
        paper = next(client.results(search))
        
        logger.info(f"Parsed paper: {paper.title}")
        return {
            "title": paper.title,
            "abstract": paper.summary,
            "authors": [a.name for a in paper.authors],
            "published": paper.published,
            "pdf_url": paper.pdf_url
        }
    except Exception as e:
        logger.error(f"Error parsing arXiv paper: {e}")
        raise