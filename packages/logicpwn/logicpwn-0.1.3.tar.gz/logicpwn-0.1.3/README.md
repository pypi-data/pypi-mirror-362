# LogicPwn

LogicPwn is a modern, extensible framework for automated business logic vulnerability assessment, exploit chaining, and professional reporting.

## Features
- 🔐 **Authentication**: Flexible session management
- 🚀 **Request Runner**: Advanced HTTP operations
- ✅ **Response Validator**: Powerful response analysis
- 🔍 **Access Detector**: Automated IDOR & access control detection
- ⚡ **Exploit Engine**: Automated exploit chaining
- 📄 **Report Generator**: Professional, multi-format reporting (Markdown, HTML, JSON)
- 🧩 **Extensible**: Plugin-ready, template-driven, and highly modular
- 🛡️ **Security**: Automatic sensitive data redaction, CVSS scoring, and privacy compliance

## Quickstart

```python
from logicpwn.core.reporter.orchestrator import ReportGenerator, ReportConfig, VulnerabilityFinding, ReportMetadata
from datetime import datetime

# Configure the report
config = ReportConfig(
    target_url="https://target.com",
    report_title="Security Assessment Report"
)
reporter = ReportGenerator(config)

# Add a finding
finding = VulnerabilityFinding(
    id="IDOR-001",
    title="IDOR in User Profile",
    severity="High",
    description="User profile accessible without auth...",
    affected_endpoints=["/api/users/{id}"],
    proof_of_concept="GET /api/users/123",
    impact="Sensitive data exposure",
    remediation="Add access control",
    discovered_at=datetime.now()
)
reporter.add_finding(finding)

# Set metadata
reporter.metadata = ReportMetadata(
    report_id="RPT-001",
    title="Security Assessment Report",
    target_url="https://target.com",
    scan_start_time=datetime.now(),
    scan_end_time=datetime.now(),
    logicpwn_version="1.0.0",
    total_requests=100,
    findings_count={"High": 1}
)

# Generate and export
reporter.export_to_file("report.md", "markdown")
reporter.export_to_file("report.html", "html")
```

## Reporting Module Highlights
- **Multi-format**: Markdown, HTML, JSON (PDF coming soon)
- **Templates**: Customizable with Jinja2 or fallback
- **Streaming**: Handles large reports efficiently
- **Redaction**: Built-in and custom regex rules
- **CVSS**: Automated, extensible scoring
- **API Docs**: Full Sphinx documentation in `docs/`
- **Tests**: Comprehensive pytest suite in `tests/core/reporter/`

## Documentation
- **API Reference**: See `docs/build/index.html` (after running `poetry run sphinx-build docs/source docs/build`)
- **Getting Started**: See `docs/source/getting_started.rst`
- **Examples**: See `examples/reports/`

## Testing
Run all tests with:
```sh
poetry run pytest tests/core/reporter/
```

## Contributing
- PRs welcome! Please add tests and docstrings for new features.
- For questions or feature requests, open an issue.

---
LogicPwn © 2024 | MIT License 