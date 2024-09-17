import warnings
import re
from typing import Union
from urllib.parse import urlparse
import copy
from lxml import html
from lxml.html import clean
import requests

from bs4 import BeautifulSoup
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.schema import Document

warnings.filterwarnings("ignore", category=FutureWarning)

 
class BeautifulSoupSelectorTransformer(BeautifulSoupTransformer):
    """
    A transformer that uses BeautifulSoup to select specific elements
    from HTML documents and extracts their text content.
    Supports content extraction
    from various website types (Tistory, Stack Overflow, etc.).

    Args:
        selector (Union[str, list[str]]): A CSS selector or a list of CSS selectors
        to select the HTML elements to extract.
        document_type (str): The type of website the document is from
        ('tistory', 'stackoverflow', 'official', etc.).

    Methods:
        normalize_newlines(self, text): Normalizes newlines in the given text.
        transform_documents(self, documents: list[Document])
        -> list[Document]: Transforms the given list of documents.
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
            
            elif self.document_type == 'normal': 
                pass
            
            else:
                pass
        return transformed_documents


class Configuration(object):
    def __init__(self):
        """
        문서를 스크래핑 할때 필요한 속성을 정의하는 클래스.
        """
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        self.accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8'
        self.language = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
        self.encoding = 'gzip, deflate'
        
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': self.accept,
            'Accept-Language': self.language,
            'Accept-Encoding': self.encoding
        }
        self.request_timeout = 5
    
    @staticmethod
    def get_parser(): 
        return Parser

class Parser:
    """파싱만 하는 클래스.
       
       파싱 클래스를 단독으로 만든 이유. 
       - 메모리 효율성
       - 간편 사용
       - 코드의 간결성
       - 테스트 용이성 
    """ 
    
    @classmethod
    def xpath_parse(cls, node, expression):
        return node.xpath(expression)
    
    @classmethod
    def drop_tag(cls, node):
        # 태그 제거 로직
        for elem in node.xpath(".//*"):
            elem.drop_tag()
        return node
    
    @classmethod
    def getText(cls, node):
        return node.text_content() if node is not None else ""


class DocumentCleaner:
    """HTML 문서 내에 공통적으로 제거할 태그를 지정하는 클래스.
    """
    
    def __init__(self):
        # 제거할 태그
        self.tags_to_remove = ['header', 'nav', 'aside', 'footer', 'script', 'style']
        self.classes_to_remove = ['advertisement', 'sidebar', 'social-share', 'related-links', 'printfooter',
                                  'widget', 'modal', 'popup', 'cookie-notice', 'privacy-notice', 'pagination', 'references']
        self.ids_to_remove = ['sidebar', 'ad-section', 'banner', 'references']
        
        # 텍스트 정제 
        self.tablines_replace = re.compile(r"[\s]+")
        
    
    def clean(self, doc):    
        """불필요한 태그, 클래스, ID, 주석을 제거하고 텍스트 안에 포함된 개행문자와 탭문자를 제거하는 함수.

        Args:
            doc (lxml.html.HtmlElement): Dom 객체.

        Returns:
            cleaned_doc (str): 정제된 문자열.
        """
         
        cleaner = clean.Cleaner(style=True, scripts=True, comments=True, javascript=True)
        cleaned_doc = cleaner.clean_html(doc)

        # 태그 제거
        for tag in self.tags_to_remove:
            for elem in cleaned_doc.xpath(f"//{tag}"):
                elem.getparent().remove(elem)

        # 클래스 기반 제거
        for cls in self.classes_to_remove:
            for elem in cleaned_doc.xpath(f"//*[contains(@class, '{cls}')]"):
                elem.getparent().remove(elem)

        # ID 기반 제거
        for id in self.ids_to_remove:
            for elem in cleaned_doc.xpath(f"//*[@id='{id}']"):
                elem.getparent().remove(elem)

        # 주석 제거
        for comment in cleaned_doc.xpath("//comment()"):
            comment.getparent().remove(comment)
            
        # 텍스트 정제         
        cleaned_doc = self.tablines_replace.sub(' ', cleaned_doc.text_content())

        return cleaned_doc 


class NormalScraper: 
    """사전에 분석되지 않은 일반적인 문서들의 본문 내용을 스크래핑 하는 클래스.
    """
    
    def __init__(self) -> None:
        self.config = Configuration() 
        self.doc = None
        self.new_doc = None
        self.html = "" 
    
    def parse(self, url):
        """_summary_

        Args:
            url (str): 파싱할 url 문자열.

        Returns:
            parsed_text (dict): 정제된 문서의 제목과 본문.
        """
        self.html = self.set_html(url)
        root = html.fromstring(self.html)
        self.doc = root
        
        self.clean_doc = copy.deepcopy(self.doc)
        
        title = self.set_title() 
        contents = self.set_contents()
        
        parsed_text =  {"title": title, 
                        "contents": contents}
        
        return parsed_text
    
    def set_html(self, url):
        headers = self.config.headers
        timeout = self.config.request_timeout
        
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return ""
    
    def set_title(self): 
        # 1. Title 태그 확인
        title = self.doc.xpath('//title/text()')
        if title:
            return title[0]
        
        # 2. Open Graph title 확인
        og_title = self.doc.xpath('//meta[@property="og:title"]/@content')
        if og_title:
            return og_title[0]
        
        # 3. 헤더 태그 확인
        for i in range(1, 7):
            header = self.doc.xpath(f'//h{i}')
            if header:
                return Parser.getText(header[0])
    
        return None
            
    def set_contents(self): 
        # 본문 내용을 한번에 찾을 수 없기 때문에 여러가지 시도 해야함. 
        content_xpaths = [
            '//main',
            '//body',
            '//article',
            '//section[contains(@class, "content") or contains(@id, "content")]',
            '//div[contains(@class, "article") or contains(@id, "article")]',
            '//div[contains(@class, "post") or contains(@id, "post")]',
            '//div[contains(@class, "main-content") or contains(@id, "main-content")]',
            '//div[contains(@class, "body") or contains(@id, "body")]'  # 'body'는 주의해서 사용
        ]
        document_cleaner = DocumentCleaner()
        
        for xpath in content_xpaths: 
            content = self.doc.xpath(xpath)
            if len(content) > 0:    # FutureWarning -> 'content is not None' test instead
                self.new_doc = document_cleaner.clean(content[0])
                return self.new_doc
            else: 
                continue
            
        return "Content not found"


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
    

def document_parse(url):
    """
    Parses documents from the given URLs based on their site types.

    Args:
        url (str): URL to parse.

    Returns:
        : A list of parsed documents.
    """
    
    site_type = detect_site_type(url)  # Detect the site type
    
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
        scraper = NormalScraper()
        docs = scraper.parse(url)
        
        documents = Document(metadata={"source": url, 
                                       "title": docs['title']}, 
                             page_content=docs['contents'], 
                             type="Document")
        return documents
    
    loader = AsyncHtmlLoader(url)  # Create an asynchronous HTML loader
    docs = loader.load()  # Load the HTML documents

    documents = transform.transform_documents(docs)  # Transform the documents
    
    return documents[0] if documents else Document(page_content="", metadata={"url": url, "error": "No content parsed"})  # Return the parsed documents
