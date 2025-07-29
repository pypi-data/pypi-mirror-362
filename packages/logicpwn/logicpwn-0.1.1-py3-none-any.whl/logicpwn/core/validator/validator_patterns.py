"""
Vulnerability patterns and regexes for LogicPwn response validation.
"""

class VulnerabilityPatterns:
    """Pre-defined patterns for common vulnerability detection."""
    # SQL Injection patterns
    SQL_INJECTION = [
        r"SQL syntax.*MySQL",
        r"Warning.*mysql_",
        r"valid MySQL result",
        r"ORA-[0-9]{4,5}",
        r"Microsoft.*ODBC.*SQL",
        r"PostgreSQL.*ERROR",
        r"SQLite.*error",
        r"SQL syntax.*MariaDB"
    ]
    # XSS patterns
    XSS_INDICATORS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"onerror\s*=",
        r"onload\s*=",
        r"onclick\s*=",
        r"onmouseover\s*="
    ]
    # Directory traversal patterns
    DIRECTORY_TRAVERSAL = [
        r"root:.*:0:0:",
        r"\[boot loader\]",
        r"<DIR>\s+\.\.",
        r"/etc/passwd",
        r"/var/www/",
        r"C:\\Windows\\"
    ]
    # Authentication bypass patterns
    AUTH_BYPASS = [
        r"admin.*panel",
        r"privileged.*access",
        r"unauthorized.*admin",
        r"bypass.*authentication"
    ]
    # Information disclosure patterns
    INFO_DISCLOSURE = [
        r"stack trace",
        r"debug.*information",
        r"internal.*error",
        r"version.*information",
        r"database.*error"
    ] 