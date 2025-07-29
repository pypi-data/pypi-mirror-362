import os
import json
import sys
import asyncio
import signal

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

sys.unraisablehook = lambda unraisable: None

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

SERVER_URL = os.environ["SERVER_URL"]
MCP_URL = SERVER_URL + '/mcp/'
TD_API_KEY = os.environ["TWELVE_DATA_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


@pytest_asyncio.fixture(scope="function")
async def run_server():
    proc = await asyncio.create_subprocess_exec(
        "python", "-m", "mcp_server_twelve_data",
        "-t", "streamable-http",
        "-k", TD_API_KEY,
        "-u", OPENAI_API_KEY,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )

    for _ in range(40):
        try:
            import httpx
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{SERVER_URL}/health")
                if r.status_code == 200:
                    break
        except Exception:
            await asyncio.sleep(1)
    else:
        proc.terminate()
        raise RuntimeError("Server did not start")

    yield
    proc.send_signal(signal.SIGINT)
    await proc.wait()


@pytest.mark.asyncio
@pytest.mark.parametrize("query, expected_title_keyword", [
    ("what does the macd indicator do?", "MACD"),
    ("how to fetch time series data?", "Time Series"),
    ("supported intervals for time_series?", "interval"),
])
async def test_doc_tool_async(query, expected_title_keyword, run_server):
    headers = {
        "Authorization": f"apikey {TD_API_KEY}",
        "x-openapi-key": OPENAI_API_KEY
    }

    async with streamablehttp_client(MCP_URL, headers=headers) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            call_result = await session.call_tool("doc-tool", arguments={"query": query})
        await read_stream.aclose()
        await write_stream.aclose()

    assert not call_result.isError, f"doc-tool error: {call_result.content}"
    raw = call_result.content[0].text
    payload = json.loads(raw)

    assert payload["error"] is None
    assert payload["result"] is not None
    assert expected_title_keyword.lower() in payload["result"].lower(), (
        f"Expected '{expected_title_keyword}' in result Markdown:\n{payload['result']}"
    )
    assert len(payload["top_candidates"]) > 0
