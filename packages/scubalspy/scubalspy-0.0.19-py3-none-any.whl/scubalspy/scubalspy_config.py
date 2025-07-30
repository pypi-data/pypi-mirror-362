"""
Configuration parameters for Scubalspy.
"""

from dataclasses import dataclass
from enum import Enum


class Language(str, Enum):
    """
    Possible languages with Scubalspy.
    """

    CSHARP = "csharp"
    PYTHON = "python"
    RUST = "rust"
    JAVA = "java"
    KOTLIN = "kotlin"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GO = "go"
    RUBY = "ruby"
    DART = "dart"
    CPP = "cpp"

    def __str__(self) -> str:
        return self.value

@dataclass
class ScubalspyConfig:
    """
    Configuration parameters
    """
    code_language: Language
    trace_lsp_communication: bool = False
    start_independent_lsp_process: bool = True

    @classmethod
    def from_dict(cls, env: dict):
        """
        Create a ScubalspyConfig instance from a dictionary
        """
        import inspect
        return cls(**{
            k: v for k, v in env.items() 
            if k in inspect.signature(cls).parameters
        })
