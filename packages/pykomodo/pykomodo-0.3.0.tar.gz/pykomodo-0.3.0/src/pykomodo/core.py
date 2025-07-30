import os
import fnmatch
from typing import List, Optional

class PriorityRule:
    def __init__(self, pattern, score):
        self.pattern: str = pattern
        self.score: int = score

class PyCConfig:
    def __init__(self):
        self.max_size: int = 0
        self.token_mode: bool = False
        self.output_dir: Optional[str] = None
        self.stream: bool = False
        
        self.ignore_patterns: List[str] = []
        self.unignore_patterns: List[str] = [] 
        self.priority_rules: List[PriorityRule] = []
        self.binary_exts: List[str] = []

    def add_ignore_pattern(self, pattern: str) -> None:
        self.ignore_patterns.append(pattern)

    def add_unignore_pattern(self, pattern: str) -> None:
        self.unignore_patterns.append(pattern)

    def add_priority_rule(self, pattern: str, score: int) -> None:
        self.priority_rules.append(PriorityRule(pattern, score))

    def should_ignore(self, path: str) -> bool:
        for pat in self.unignore_patterns:
            if fnmatch.fnmatch(path, pat):
                return False

        for pat in self.ignore_patterns:
            if fnmatch.fnmatch(path, pat):
                return True

        return False

    def calculate_priority(self, path: str) -> int:
        highest = 0
        for rule in self.priority_rules:
            if fnmatch.fnmatch(path, rule.pattern):
                if rule.score > highest:
                    highest = rule.score
        return highest

    def is_binary_file(self, path: str) -> bool:
        _, ext = os.path.splitext(path)
        ext = ext.lstrip(".").lower()
        if ext in (b.lower() for b in self.binary_exts):
            return True

        try:
            with open(path, "rb") as f:
                chunk = f.read(512)
        except OSError:
            return True

        if b"\0" in chunk:
            return True

        return False

    def read_file_contents(self, path: str) -> str:
        try:
            with open(path, "rb") as f:
                data = f.read()
            return data.decode("utf-8", errors="replace")
        except OSError:
            return "<NULL>"

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def make_c_string(self, text: Optional[str]) -> str:
        if text is None:
            return "<NULL>"
        return text

    def __repr__(self) -> str:
        return (f"PyCConfig(max_size={self.max_size}, token_mode={self.token_mode}, "
                f"output_dir={self.output_dir!r}, stream={self.stream}, "
                f"ignore_patterns={self.ignore_patterns}, "
                f"unignore_patterns={self.unignore_patterns}, "
                f"priority_rules={[ (r.pattern, r.score) for r in self.priority_rules ]}, "
                f"binary_exts={self.binary_exts})")
