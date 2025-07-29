from logicpwn.exporters import BaseExporter
from logicpwn.core.reporter.orchestrator import VulnerabilityFinding, ReportMetadata
from typing import List, Optional, IO
from logicpwn.core.reporter.template_renderer import TemplateRenderer
import os

class MarkdownExporter(BaseExporter):
    """
    Exports vulnerability findings and metadata to Markdown format.
    Supports template-based and streaming output for large reports.
    """
    def __init__(self):
        """
        Initialize the exporter with the default template directory.
        """
        self.template_dir = "logicpwn/templates"

    def set_template_dir(self, template_dir: str):
        """
        Set a custom template directory for rendering.
        :param template_dir: Path to the template directory.
        """
        self.template_dir = template_dir

    def export(self, findings: List[VulnerabilityFinding], metadata: ReportMetadata, template_dir: Optional[str] = None) -> str:
        """
        Export findings and metadata to a Markdown string.
        :param findings: List of VulnerabilityFinding objects.
        :param metadata: ReportMetadata object.
        :param template_dir: Optional custom template directory.
        :return: Markdown string.
        """
        renderer = TemplateRenderer(template_dir or self.template_dir)
        context = {
            "title": metadata.title,
            "target_url": metadata.target_url,
            "scan_start_time": metadata.scan_start_time,
            "scan_end_time": metadata.scan_end_time,
            "total_findings": sum(metadata.findings_count.values()),
            "critical_count": metadata.findings_count.get('Critical', 0),
            "findings": [f.model_dump() if hasattr(f, 'model_dump') else f.dict() for f in findings],
            "scan_duration": metadata.scan_end_time - metadata.scan_start_time,
            "logicpwn_version": metadata.logicpwn_version,
            "authenticated_user": metadata.authenticated_user or 'N/A',
        }
        try:
            return renderer.render("markdown_template.md", context)
        except Exception:
            # Fallback to inline rendering
            lines = [
                f"# {metadata.title}",
                f"\n**Target:** {metadata.target_url}",
                f"\n**Assessment Date:** {metadata.scan_start_time.strftime('%Y-%m-%d')} - {metadata.scan_end_time.strftime('%Y-%m-%d')}",
                f"\n**Total Findings:** {sum(metadata.findings_count.values())}",
                f"\n**Critical Issues:** {metadata.findings_count.get('Critical', 0)}",
                "\n---\n",
                "## Vulnerability Details\n"
            ]
            for finding in findings:
                lines.extend([
                    f"### {finding.severity} - {finding.title}",
                    f"**CVSS Score:** {finding.cvss_score if finding.cvss_score is not None else 'N/A'}",
                    f"**Affected Endpoints:** {', '.join(finding.affected_endpoints)}",
                    f"\n**Description:**\n{finding.description}",
                    f"\n**Proof of Concept:**\n```http\n{finding.proof_of_concept}\n```",
                    f"\n**Impact:**\n{finding.impact}",
                    f"\n**Remediation:**\n{finding.remediation}",
                    f"\n**References:** {', '.join(finding.references) if finding.references else 'N/A'}",
                    f"\n**Discovered At:** {finding.discovered_at.isoformat()}",
                    "\n---\n"
                ])
            lines.append("## Appendix\n")
            lines.append(f"- **Scan Duration:** {(metadata.scan_end_time - metadata.scan_start_time)}")
            lines.append(f"- **LogicPwn Version:** {metadata.logicpwn_version}")
            lines.append(f"- **Authentication:** {metadata.authenticated_user or 'N/A'}")
            return '\n'.join(lines)

    def stream_export(self, findings: List[VulnerabilityFinding], metadata: ReportMetadata, file: IO, template_dir: Optional[str] = None):
        """
        Stream findings and metadata to a file in Markdown format (for large reports).
        :param findings: List of VulnerabilityFinding objects.
        :param metadata: ReportMetadata object.
        :param file: File-like object to write to.
        :param template_dir: Optional custom template directory (unused in streaming).
        """
        # Stream header
        file.write(f"# {metadata.title}\n\n")
        file.write(f"**Target:** {metadata.target_url}\n")
        file.write(f"**Assessment Date:** {metadata.scan_start_time.strftime('%Y-%m-%d')} - {metadata.scan_end_time.strftime('%Y-%m-%d')}\n")
        file.write(f"**Total Findings:** {sum(metadata.findings_count.values())}\n")
        file.write(f"**Critical Issues:** {metadata.findings_count.get('Critical', 0)}\n\n---\n\n")
        file.write("## Vulnerability Details\n\n")
        # Stream findings
        for finding in findings:
            file.write(f"### {finding.severity} - {finding.title}\n")
            file.write(f"**CVSS Score:** {finding.cvss_score if finding.cvss_score is not None else 'N/A'}\n")
            file.write(f"**Affected Endpoints:** {', '.join(finding.affected_endpoints)}\n")
            file.write(f"\n**Description:**\n{finding.description}\n")
            file.write(f"\n**Proof of Concept:**\n```http\n{finding.proof_of_concept}\n```\n")
            file.write(f"\n**Impact:**\n{finding.impact}\n")
            file.write(f"\n**Remediation:**\n{finding.remediation}\n")
            file.write(f"\n**References:** {', '.join(finding.references) if finding.references else 'N/A'}\n")
            file.write(f"\n**Discovered At:** {finding.discovered_at.isoformat()}\n\n---\n\n")
        # Stream appendix
        file.write("## Appendix\n")
        file.write(f"- **Scan Duration:** {(metadata.scan_end_time - metadata.scan_start_time)}\n")
        file.write(f"- **LogicPwn Version:** {metadata.logicpwn_version}\n")
        file.write(f"- **Authentication:** {metadata.authenticated_user or 'N/A'}\n") 