# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of our software seriously. If you believe you have found a security vulnerability in the PhD Deep Read Workflow, please report it to us as described below.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to `heleninsights@gmail.com`.

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include

When reporting a vulnerability, please include as much information as possible to help us understand and reproduce the issue:

1. **Type of issue** (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
2. **Full paths of source file(s) related to the manifestation of the issue**
3. **The location of the affected source code** (tag, branch, commit, or direct URL)
4. **Any special configuration required to reproduce the issue**
5. **Step-by-step instructions to reproduce the issue**
6. **Proof-of-concept or exploit code** (if possible)
7. **Impact of the issue**, including how an attacker might exploit it

### Our Commitment

We will acknowledge your email within 48 hours, and will send a more detailed response within 96 hours indicating the next steps in handling your report. After the initial reply to your report, we will keep you informed of the progress toward a fix and full announcement, and may ask for additional information or guidance.

## Security Best Practices for Users

### PDF Processing Security

The PhD Deep Read Workflow processes PDF files, which can potentially contain malicious content. Please follow these security guidelines:

1. **Only process PDFs from trusted sources**
2. **Keep dependencies updated** (PyMuPDF, Tesseract OCR, etc.)
3. **Run in isolated environments** when processing untrusted PDFs
4. **Review extracted content** before using in production systems

### Environment Security

1. **Use virtual environments** to isolate dependencies
2. **Restrict file system permissions** for output directories
3. **Monitor disk usage** when processing large PDF collections
4. **Regularly update Python and system packages**

### Data Privacy

The workflow:
- Extracts text and images from PDFs
- May send content to Claude Code API for note generation (if configured)
- Stores extracted content locally

**Note:** If using Claude Code integration, be aware that content is sent to Anthropic's servers for processing. Review Anthropic's privacy policy for details.

## Security Updates

Security updates will be announced via:
- GitHub Releases
- Security advisories on the repository
- CHANGELOG.md updates

## Dependency Security

We regularly update dependencies to address security vulnerabilities. The `requirements.txt` and `requirements-dev.txt` files specify version ranges that include security patches.

To update dependencies:
```bash
pip install --upgrade -r requirements.txt
```

## Responsible Disclosure Timeline

- **48 hours**: Acknowledgment of receipt
- **7 days**: Initial assessment and severity classification
- **30 days**: Fix development and testing
- **45 days**: Public disclosure (if appropriate)

We appreciate your efforts to responsibly disclose your findings and will make every effort to acknowledge your contributions.

---

*This security policy is adapted from the [GitHub Security Policy template](https://github.com/github/security-policy-template).*