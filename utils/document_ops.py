from __future__ import annotations
from pathlib import Path
from typing import Iterable, List
from fastapi import UploadFile
from langchain.schema import Document
from langchain_community.document_loaders import CSVLoader
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import DocumentPortalChatException
SUPPORTED_EXTENSIONS = {".csv"}

def load_documents(paths: Iterable[Path]) -> List[Document]:
    """Load docs using appropriate loader based on extension."""
    docs: List[Document] = []
    try:
        for p in paths:
            ext = p.suffix.lower()
            if ext == ".csv":
                loader = CSVLoader(str(p))
            else:
                log.warning("Unsupported extension skipped", path=str(p))
                continue
            docs.extend(loader.load())
        log.info("Documents loaded", count=len(docs))
        return docs
    except Exception as e:
        log.error("Failed loading documents", error=str(e))
        raise DocumentPortalChatException("Error loading documents", e) from e