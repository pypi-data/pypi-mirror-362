from dataclasses import asdict
import streamlit as st
import pandas as pd
import datetime
import asyncio

from bramble.logs import MessageType
from bramble.backends import FileReader
from bramble.backends.base import BrambleReader


@st.cache_data
def load_branches_and_tags():
    def _load_branches_and_tags():
        backend: BrambleReader = st.session_state.backend
        if isinstance(backend, tuple):
            from bramble.backends import RedisReader

            host, port = backend
            backend = RedisReader.from_socket(host, port)

        async def _load():
            all_branch_ids = await backend.async_get_branch_ids()
            all_branch_data = await backend.async_get_branches(all_branch_ids)
            return all_branch_data

        all_branch_data = asyncio.run(_load())

        branches = []
        tags = set()

        for unformatted_data in all_branch_data.values():
            start = unformatted_data.messages[0].timestamp
            end = unformatted_data.messages[0].timestamp

            for message in unformatted_data.messages:
                start = min(start, message.timestamp)
                end = max(end, message.timestamp)

            branches.append(
                {
                    "name": unformatted_data.name,
                    "id": unformatted_data.id,
                    "tags": (
                        unformatted_data.tags
                        if len(unformatted_data.tags) > 0
                        else None
                    ),
                    "metadata": (
                        unformatted_data.metadata
                        if len(unformatted_data.metadata) > 0
                        else None
                    ),
                    "entries": len(unformatted_data.messages),
                    "start": datetime.datetime.fromtimestamp(start),
                    "end": datetime.datetime.fromtimestamp(end),
                }
            )
            tags.update(unformatted_data.tags)

        branches = pd.DataFrame(branches)
        return branches, tags

    if not "backend" in st.session_state:
        return [], []
    else:
        return _load_branches_and_tags()


@st.cache_data
def load_branch_data(id: str):
    def _load_branch_data(id: str):
        backend: BrambleReader = st.session_state.backend
        if isinstance(backend, tuple):
            from bramble.backends import RedisReader

            host, port = backend
            backend = RedisReader.from_socket(host, port)

        branch_data = asyncio.run(backend.async_get_branches([id]))
        branch_data = branch_data[id]

        start = branch_data.messages[0].timestamp
        end = branch_data.messages[0].timestamp

        for message in branch_data.messages:
            start = min(start, message.timestamp)
            end = max(end, message.timestamp)

        start = datetime.datetime.fromtimestamp(start)
        end = datetime.datetime.fromtimestamp(end)

        messages = branch_data.messages
        messages = sorted(messages, key=lambda x: x.timestamp)
        messages = [asdict(entry) for entry in messages]
        for message in messages:
            if isinstance(message["message_type"], str):
                message["message_type"] = MessageType(message["message_type"])

        return (
            branch_data.name,
            {
                "id": branch_data.id,
                "num": len(branch_data.messages),
                "start": start,
                "end": end,
                "duration": end - start,
                "tags": branch_data.tags if len(branch_data.tags) > 0 else None,
                "metadata": (
                    branch_data.metadata if len(branch_data.metadata) > 0 else None
                ),
                "parent": branch_data.parent,
                "children": branch_data.children,
            },
            messages,
        )

    if not "backend" in st.session_state:
        "", {}, []
    else:
        return _load_branch_data(id)


def start_file_backend(path: str):
    if not "backend" in st.session_state:
        st.session_state.backend = FileReader(path)

        load_branch_data.clear()
        load_branches_and_tags.clear()


def start_redis_backend(host: str, port: int):
    from bramble.backends import RedisReader

    if not "backend" in st.session_state:
        st.session_state.backend = (host, port)

        load_branch_data.clear()
        load_branches_and_tags.clear()
