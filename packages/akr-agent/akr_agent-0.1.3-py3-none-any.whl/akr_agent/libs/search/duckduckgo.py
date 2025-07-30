"""Util that calls DuckDuckGo Search.

No setup required. Free.
https://pypi.org/project/duckduckgo-search/
"""

from typing import Dict, List, Optional

from pydantic import BaseModel


class DuckDuckGoSearchAPIWrapper(BaseModel):
    """Wrapper for DuckDuckGo Search API.

    Free and does not require any setup.
    """

    region: Optional[str] = "wt-wt"
    safesearch: str = "moderate"
    time: Optional[str] = "y"
    max_results: int = 5
    backend: str = "auto"  # default
    source: str = "text"  # which function to use in DDGS (DDGS.text() or DDGS.news())

    def _ddgs_text(
        self, keywords: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo text search and return results."""
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(keywords=keywords)
            if ddgs_gen:
                return [r for r in ddgs_gen]
        return []

    def _ddgs_news(
        self, keywords: str, max_results: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo news search and return results."""
        from duckduckgo_search import DDGS

        with DDGS() as ddgs:
            ddgs_gen = ddgs.news(
                keywords=keywords,
                region=self.region,
                safesearch=self.safesearch,
                timelimit=self.time,
                max_results=max_results or self.max_results,
            )
            if ddgs_gen:
                return [r for r in ddgs_gen]
        return []

    def run(self, keywords: str) -> str:
        """Run query through DuckDuckGo and return concatenated results."""
        if self.source == "text":
            results = self._ddgs_text(keywords=keywords)
        elif self.source == "news":
            results = self._ddgs_news(keywords=keywords)
        else:
            results = []

        if not results:
            return "No good DuckDuckGo Search Result was found"
        return " ".join(r["body"] for r in results)

    def results(
        self, keywords: str, max_results: int, source: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Run query through DuckDuckGo and return metadata.

        Args:
            keywords: The query to search for.
            max_results: The number of results to return.
            source: The source to look from.

        Returns:
            A list of dictionaries with the following keys:
                snippet - The description of the result.
                title - The title of the result.
                link - The link to the result.
        """
        source = source or self.source
        if source == "text":
            results = [
                {"snippet": r["body"], "title": r["title"], "link": r["href"]}
                for r in self._ddgs_text(keywords=keywords, max_results=max_results)
            ]
        elif source == "news":
            results = [
                {
                    "snippet": r["body"],
                    "title": r["title"],
                    "link": r["url"],
                    "date": r["date"],
                    "source": r["source"],
                }
                for r in self._ddgs_news(keywords=keywords, max_results=max_results)
            ]
        else:
            results = []

        if results is None:
            results = [{"Result": "No good DuckDuckGo Search Result was found"}]

        return results


if __name__ == "__main__":
    ddgs = DuckDuckGoSearchAPIWrapper()
    print(ddgs.run("What should I pay attention to when strength training?"))
