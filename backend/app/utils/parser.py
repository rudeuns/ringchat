import re
from typing import Union
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.schema import Document


class BeautifulSoupSelectorTransformer(BeautifulSoupTransformer):
    def __init__(self, selector: Union[str, list[str], None] = None):
        super().__init__()
        self.selector = selector

    def normalize_newlines(self, text):
        return re.sub(r"\n{2,}", "\n", text)

    def transform_documents(self, documents: list[Document]) -> list[Document]:
        transformed_documents = []

        for document in documents:
            soup = BeautifulSoup(document.page_content, "html.parser")

            if self.selector is not None:
                elements = soup.select(self.selector)
            else:
                article_elements = soup.find_all("article")
                if article_elements:
                    elements = article_elements
                else:
                    elements = soup.find_all(["p", "code"])

            extracted_content = "".join(
                [element.get_text() for element in elements]
            )
            extracted_content = self.normalize_newlines(extracted_content)

            transformed_documents.append(
                Document(
                    page_content=extracted_content,
                    metadata=document.metadata,
                )
            )

        return transformed_documents


def detect_site_type(url: str) -> str:
    parsed_url = urlparse(url)
    hostname_parts = parsed_url.hostname.split(".")

    if (
        len(hostname_parts) > 2
    ):  # Handle subdomains (e.g., 'subdomain.example.com')
        return hostname_parts[1]  # Return the second-level domain
    return hostname_parts[0]  # Return the first part of the hostname


def parse_single_url(url: str) -> Union[list[Document], None]:
    site_type = detect_site_type(url)

    loader = AsyncHtmlLoader(url)
    docs = loader.load()

    if site_type == "tistory":
        transformer = BeautifulSoupSelectorTransformer(
            selector='[class*="article"]'
        )
    elif site_type == "stackoverflow":
        transformer = BeautifulSoupSelectorTransformer(selector=".s-prose")
    else:
        transformer = BeautifulSoupSelectorTransformer(selector=None)

    transformed_documents = transformer.transform_documents(docs)
    return transformed_documents