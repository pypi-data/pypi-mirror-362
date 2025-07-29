from src.hectofinancial_mcp_server.core.document_repository import (
    HectoDocumentRepository,
)

SAMPLE_DOCS = {
    "test1.md": "# 제목1\n본문1\n## 소제목1\n본문2",
    "test2.md": "# 제목2\n본문3\n## 소제목2\n본문4",
}


def test_repository_creation():
    repo = HectoDocumentRepository(SAMPLE_DOCS)
    assert repo is not None
    assert len(repo.documents) > 0


def test_list_documents():
    repo = HectoDocumentRepository(SAMPLE_DOCS)
    docs = repo.list_documents()
    assert isinstance(docs, dict)
    assert "문서목록" in docs


def test_search_documents():
    repo = HectoDocumentRepository(SAMPLE_DOCS)
    result = repo.search_documents(["제목"])
    assert isinstance(result, dict)
