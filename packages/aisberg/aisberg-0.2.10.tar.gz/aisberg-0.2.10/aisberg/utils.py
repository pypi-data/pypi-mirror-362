from typing import Iterator, Union, Dict
import json


def parse_chat_line(
    line: str, *, full_chunk: bool = True
) -> Iterator[Union[str, dict]]:
    """
    Parse une ligne de stream JSON (commençant par `data:`) et yield un ou plusieurs éléments utilisables.

    Args:
        line (str): Ligne du flux à traiter.
        full_chunk (bool): Contrôle le format de sortie (chunk brut ou contenu transformé).

    Yields:
        Union[str, dict]: Le chunk complet ou un morceau de texte/fonction/tool_call.
    """
    if not line.startswith("data:"):
        return

    data = line[len("data:") :].strip()
    if data == "[DONE]":
        return

    try:
        chunk: dict = json.loads(data)

        if chunk["object"] != "chat.completion.chunk":
            raise ValueError(f"Unexpected object type: {chunk['object']}")

        if not chunk.get("choices", []):
            return

        if chunk["choices"][0]["finish_reason"] == "stop":
            return

        if full_chunk:
            yield chunk
            return

        delta = chunk.get("choices", [{}])[0].get("delta", {})

        if "content" in delta and delta["content"]:
            yield delta["content"]

        elif "function_call" in delta and delta["function_call"]:
            yield f"[FUNCTION_CALL]{delta['function_call']}"

        elif "tool_calls" in delta and delta["tool_calls"]:
            yield f"[TOOL_CALLS]{delta['tool_calls']}"

    except json.JSONDecodeError:
        return


class WorkflowLineParser:
    def __init__(self, full_chunk: bool = True):
        self.full_chunk = full_chunk
        self._buckets: Dict[str, Dict] = {}

    def __call__(self, line: str) -> Iterator[Union[str, dict]]:
        if not line.startswith("data:"):
            return
        data = line[len("data:") :].strip()
        if data == "[DONE]":
            return

        try:
            payload = json.loads(data)

            # Gestion des events chunk + slices
            if payload.get("type") == "chunk":
                self._buckets[payload["id"]] = {
                    "totalSlices": payload["totalSlices"],
                    "slices": [None] * payload["totalSlices"],
                }

            elif payload.get("type") == "chunk_slice":
                bucket = self._buckets.get(payload["id"])
                if bucket:
                    bucket["slices"][payload["index"]] = payload["slice"]

            elif payload.get("type") == "chunk_end":
                bucket = self._buckets.pop(payload["id"], None)
                if bucket:
                    full_json = "".join(bucket["slices"])
                    try:
                        yield from self._yield_chunk(full_json)
                    except json.JSONDecodeError:
                        return

            else:
                # Message "normal" non splitté
                yield from self._yield_chunk(data)

        except json.JSONDecodeError:
            return

    def _yield_chunk(self, raw: str) -> Iterator[Union[str, dict]]:
        chunk = json.loads(raw)

        if "slice" in chunk:
            try:
                if isinstance(chunk["slice"], str):
                    # Si la slice est déjà un JSON string, on la parse
                    parsed_slice = json.loads(chunk["slice"])
                    yield parsed_slice
                elif isinstance(chunk["slice"], dict):
                    # Si la slice est déjà un dict, on la yield directement
                    yield chunk["slice"]
            except json.JSONDecodeError:
                return
        else:
            return
