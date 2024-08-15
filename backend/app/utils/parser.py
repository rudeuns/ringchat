import re
from typing import Union
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from langchain.document_loaders import AsyncHtmlLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.schema import Document


class BeautifulSoupSelectorTransformer(BeautifulSoupTransformer):
    """
    A transformer that uses BeautifulSoup to select specific elements from HTML documents and extracts their text content.
    Supports content extraction from various website types (Tistory, Stack Overflow, etc.).

    Args:
        selector (Union[str, list[str]]): A CSS selector or a list of CSS selectors to select the HTML elements to extract.
        document_type (str): The type of website the document is from ('tistory', 'stackoverflow', 'official', etc.).

    Methods:
        normalize_newlines(self, text): Normalizes newlines in the given text.
        transform_documents(self, documents: list[Document]) -> list[Document]: Transforms the given list of documents.
    """

    def __init__(self, selector: Union[str, list[str]], document_type: str):
        super().__init__()
        self.selector = selector
        self.document_type = document_type

    def normalize_newlines(self, text):
        """
        Normalizes newlines in the given text.

        Args:
            text (str): The text to normalize.

        Returns:
            str: The normalized text.
        """

        return re.sub(r"\n{2,}", "\n", text)

    def transform_documents(self, documents: list[Document]) -> list[Document]:
        """
        Transforms the given list of documents.

        Args:
            documents (list[Document]): The list of documents to transform.

        Returns:
            list[Document]: The transformed list of documents.
        """
        transformed_documents = []
        for document in documents:
            soup = BeautifulSoup(document.page_content, "html.parser")
            if self.document_type == "tistory":
                elements = soup.select(self.selector)

                extracted_content = "".join(
                    [elements[x].text for x in range(len(elements))]
                )
                extracted_content = self.normalize_newlines(extracted_content)

                transformed_documents.append(
                    Document(
                        page_content=extracted_content,
                        metadata=document.metadata,
                    )
                )
            elif self.document_type == "stackoverflow":
                elements = soup.select(self.selector)

                extracted_content = "".join(
                    [elements[x].text for x in range(len(elements))]
                )
                extracted_content = self.normalize_newlines(extracted_content)

                transformed_documents.append(
                    Document(
                        page_content=extracted_content,
                        metadata=document.metadata,
                    )
                )

            elif self.document_type == "official":
                pass
            else:
                pass
        return transformed_documents


def detect_site_type(url):
    """
    Detects the type of website based on the URL.

    Args:
        url (str): The URL to analyze.

    Returns:
        str: The detected site type (e.g., 'tistory', 'stackoverflow').
    """

    parsed_url = urlparse(url)  # Parse the URL into its components
    hostname = (
        parsed_url.hostname
    )  # Extract the hostname (e.g., 'example.tistory.com')
    hostname = hostname.split(".")  # Split the hostname into parts using '.'

    if (
        len(hostname) > 2
    ):  # If there are more than two parts (e.g., 'subdomain.example.com')
        return hostname[1]  # Return the second part (e.g., 'example')
    else:  # Otherwise (e.g., 'example.com')
        return hostname[0]  # Return the first part (e.g., 'example')


def document_parse(urls):
    """
    Parses documents from the given URLs based on their site types.

    Args:
        urls (list[str]): A list of URLs to parse.

    Returns:
        list[Document]: A list of parsed documents.
    """

    for url in urls:
        site_type = detect_site_type(url)  # Detect the site type

        loader = AsyncHtmlLoader(url)  # Create an asynchronous HTML loader
        docs = loader.load()  # Load the HTML documents

        if site_type == "tistory":
            transform = BeautifulSoupSelectorTransformer(
                selector='[class*="article"]', document_type="tistory"
            )
        elif site_type == "official":
            transform = BeautifulSoupSelectorTransformer(
                selector='[class*="article"]', document_type="official"
            )
        elif site_type == "stackoverflow":
            transform = BeautifulSoupSelectorTransformer(
                selector=".s-prose", document_type="stackoverflow"
            )
        else:
            continue  # Skip unsupported site types

        documents = transform.transform_documents(
            docs
        )  # Transform the documents
        return documents  # Return the parsed documents
