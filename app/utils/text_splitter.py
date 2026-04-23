import re
from typing import List

class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", " ", ""]

    def split_text(self, text: str) -> List[str]:
        return self._split_text(text, self.separators)

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        separator = separators[-1]
        new_separators = []
        for i, s in enumerate(separators):
            if s == "":
                separator = s
                break
            if re.search(s, text):
                separator = s
                new_separators = separators[i + 1:]
                break

        splits = self._split_with_separator(text, separator)
        good_splits = []
        for s in splits:
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:
                if good_splits:
                    merged_text = self._merge_splits(good_splits, separator)
                    final_chunks.extend(merged_text)
                    good_splits = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    other_splits = self._split_text(s, new_separators)
                    final_chunks.extend(other_splits)
        if good_splits:
            merged_text = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged_text)
        return final_chunks

    def _split_with_separator(self, text: str, separator: str) -> List[str]:
        if separator:
            return text.split(separator)
        else:
            return list(text)

    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        docs = []
        current_doc = []
        total = 0
        for d in splits:
            _len = len(d)
            if total + _len + (len(separator) if current_doc else 0) > self.chunk_size:
                if total > self.chunk_size:
                    pass
                if current_doc:
                    doc = separator.join(current_doc)
                    if doc.strip():
                        docs.append(doc)
                    while total > self.chunk_overlap or (total + _len + len(separator) > self.chunk_size and total > 0):
                        first = current_doc[0]
                        total -= len(first) + (len(separator) if total > len(first) else 0)
                        current_doc = current_doc[1:]
            current_doc.append(d)
            total += _len + (len(separator) if len(current_doc) > 1 else 0)
        if current_doc:
            doc = separator.join(current_doc)
            if doc.strip():
                docs.append(doc)
        return docs