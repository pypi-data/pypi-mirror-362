from typing import List, Any
from logicpwn.core.reporter.orchestrator import VulnerabilityFinding, ReportMetadata

class BaseExporter:
    def export(self, findings: List[VulnerabilityFinding], metadata: ReportMetadata) -> str:
        raise NotImplementedError

def get_exporter(format: str):
    format = format.lower()
    if format in ("md", "markdown"):
        from .markdown_exporter import MarkdownExporter
        return MarkdownExporter()
    elif format == "json":
        from .json_exporter import JSONExporter
        return JSONExporter()
    elif format == "html":
        from .html_exporter import HTMLExporter
        return HTMLExporter()
    else:
        raise ValueError(f"Unsupported export format: {format}") 