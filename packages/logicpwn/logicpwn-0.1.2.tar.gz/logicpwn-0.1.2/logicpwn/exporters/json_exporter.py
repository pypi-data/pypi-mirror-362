import json
from logicpwn.exporters import BaseExporter
from logicpwn.core.reporter.orchestrator import VulnerabilityFinding, ReportMetadata
from typing import List

class JSONExporter(BaseExporter):
    def export(self, findings: List[VulnerabilityFinding], metadata: ReportMetadata) -> str:
        report = {
            "report_metadata": metadata.model_dump() if hasattr(metadata, 'model_dump') else metadata.dict(),
            "findings": [f.model_dump() if hasattr(f, 'model_dump') else f.dict() for f in findings]
        }
        return json.dumps(report, indent=2, default=str) 