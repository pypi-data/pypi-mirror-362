import pytest

from hectofinancial_mcp_server.core import documents
from hectofinancial_mcp_server.core.document_repository import initialize_repository
from hectofinancial_mcp_server.tools.get_docs import get_docs
from hectofinancial_mcp_server.tools.list_docs import list_docs
from hectofinancial_mcp_server.tools.search_docs import search_docs


@pytest.fixture(autouse=True, scope="module")
def setup_docs_repository():
    initialize_repository(documents)


def test_list_docs():
    result = list_docs()
    assert isinstance(result, dict)
    assert "문서목록" in result


def test_get_docs():
    result = get_docs(doc_id="1")
    assert isinstance(result, dict)


def test_search_docs():
    result = search_docs("결제")
    assert isinstance(result, dict)
