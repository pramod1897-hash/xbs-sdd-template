#!/usr/bin/env python3
"""
Tests for validate_sdd.py
"""

import sys
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

# Add repo root to path so we can import validate_sdd
sys.path.insert(0, str(Path(__file__).parent.parent))
import validate_sdd


VALID_SDD = textwrap.dedent("""\
    # My Application Software Design Document

    ## 1. Introduction

    ### 1.1 Purpose
    This document describes the design of My Application.

    ### 1.2 Scope
    My Application handles user authentication and profile management.

    ### 1.3 Definitions, Acronyms, and Abbreviations
    | Term | Definition |
    |------|------------|
    | API  | Application Programming Interface |

    ### 1.4 References
    RFC 7519 - JSON Web Token

    ### 1.5 Overview
    The document is organized into sections covering architecture, components,
    interfaces, data design, security, and deployment.

    ---

    ## 2. System Overview
    My Application is a web-based user management platform built with a
    microservices architecture. It provides REST APIs consumed by mobile and
    web clients.

    ---

    ## 3. Architecture Design

    ### 3.1 High-Level Architecture
    The system follows a layered microservices architecture with an API Gateway
    at the entry point, backed by dedicated services for auth and profiles.

    ### 3.2 Architectural Patterns
    - Microservices
    - Event-driven messaging via Kafka
    - RESTful API design

    ### 3.3 Technology Stack
    | Layer      | Technology   |
    |------------|--------------|
    | Frontend   | React 18     |
    | Backend    | Node.js 20   |
    | Database   | PostgreSQL   |
    | Messaging  | Kafka        |
    | Deployment | Kubernetes   |

    ---

    ## 4. Component Design

    ### 4.1 Component Overview
    - Auth Service: handles login, token issuance, and refresh
    - Profile Service: manages user profile CRUD operations

    ### 4.2 Component Responsibilities
    Auth Service issues JWT tokens signed with RS256. Profile Service stores and
    retrieves user data from PostgreSQL.

    ---

    ## 5. Interface Design

    ### 5.1 External Interfaces
    REST API exposed on port 443, secured by TLS 1.3.

    ### 5.2 Internal Interfaces
    Services communicate via Kafka topics for async events.

    ### 5.3 API Specification
    POST /auth/login – authenticates a user and returns a JWT.
    GET  /profile/{id} – retrieves a user profile by ID.

    ---

    ## 6. Data Design

    ### 6.1 Data Model
    User entity: id, email, password_hash, created_at, updated_at.

    ### 6.2 Database Design
    Table: users (id UUID PK, email TEXT UNIQUE, password_hash TEXT, ...)

    ### 6.3 Data Flow
    Client -> API Gateway -> Auth Service -> PostgreSQL

    ---

    ## 7. Security Design

    ### 7.1 Authentication and Authorization
    JWT-based authentication with RS256 signing. RBAC for authorization.

    ### 7.2 Data Protection
    Passwords stored as bcrypt hashes. PII encrypted at rest.

    ### 7.3 Security Controls
    Input validation on all endpoints. Output encoding to prevent XSS.

    ---

    ## 8. Error Handling and Logging

    ### 8.1 Error Handling Strategy
    All errors return RFC 7807 Problem Details responses.

    ### 8.2 Logging Strategy
    Structured JSON logs sent to Elasticsearch. Retention: 90 days.

    ---

    ## 9. Performance and Scalability

    ### 9.1 Performance Requirements
    p99 response time < 200ms for auth endpoints under 1000 req/s.

    ### 9.2 Scalability Strategy
    Horizontal pod autoscaling in Kubernetes based on CPU utilization.

    ---

    ## 10. Deployment Design

    ### 10.1 Deployment Architecture
    Three environments: dev, staging, production. All on AWS EKS.

    ### 10.2 Configuration Management
    Environment variables managed via Kubernetes Secrets and ConfigMaps.

    ### 10.3 CI/CD Pipeline
    GitHub Actions: lint -> test -> build -> push image -> deploy to staging.

    ---

    ## 11. Testing Strategy

    ### 11.1 Unit Testing
    Jest unit tests for all service logic. Target: 80% coverage.

    ### 11.2 Integration Testing
    Supertest integration tests against a Docker Compose stack.

    ### 11.3 End-to-End Testing
    Playwright E2E tests against the staging environment.

    ---

    ## 12. Open Issues and Risks
    | ID | Issue/Risk          | Impact | Mitigation        |
    |----|---------------------|--------|-------------------|
    | 1  | DB migration risk   | High   | Rollback scripts  |

    ---

    ## 13. Revision History
    | Version | Date       | Author | Description   |
    |---------|------------|--------|---------------|
    | 1.0     | 2026-03-01 | Alice  | Initial draft |
""")

MISSING_SECTIONS_SDD = textwrap.dedent("""\
    # Incomplete SDD

    ## 1. Introduction

    ### 1.1 Purpose
    Some purpose.

    ## 2. System Overview
    Some overview.
""")

PLACEHOLDER_ONLY_SDD = textwrap.dedent("""\
    # Placeholder SDD

    ## 1. Introduction

    ### 1.1 Purpose
    _Describe the purpose of this document and the software system it covers._

    ### 1.2 Scope
    _Define the scope of the software system._

    ## 2. System Overview
    _Provide a high-level description of the system._

    ## 3. Architecture Design

    ### 3.1 High-Level Architecture
    _Describe the overall architecture of the system._

    ### 3.2 Architectural Patterns
    _Describe the architectural patterns used._

    ### 3.3 Technology Stack
    | Layer | Technology |
    |-------|------------|

    ## 4. Component Design

    ### 4.1 Component Overview
    _List and briefly describe each major component._

    ## 5. Interface Design

    ### 5.1 External Interfaces
    _Describe external interfaces._

    ## 6. Data Design

    ### 6.1 Data Model
    _Describe the data model._

    ## 7. Security Design

    ### 7.1 Authentication and Authorization
    _Describe the authentication and authorization mechanisms._

    ## 8. Error Handling and Logging

    ### 8.1 Error Handling Strategy
    _Describe the approach to error handling._

    ## 9. Performance and Scalability

    ### 9.1 Performance Requirements
    _Describe the performance requirements._

    ## 10. Deployment Design

    ### 10.1 Deployment Architecture
    _Describe the deployment topology._

    ## 11. Testing Strategy

    ### 11.1 Unit Testing
    _Describe the approach to unit testing._

    ## 12. Open Issues and Risks
    Some risk noted here.

    ## 13. Revision History
    | Version | Date | Author | Description |
    |---------|------|--------|-------------|
    | 1.0     |      |        | Initial draft |
""")


class TestExtractHeadings(unittest.TestCase):
    def test_extracts_all_heading_levels(self):
        content = "# H1\n## H2\n### H3\n#### H4"
        headings = validate_sdd.extract_headings(content)
        self.assertEqual(headings, ["H1", "H2", "H3", "H4"])

    def test_skips_non_heading_lines(self):
        content = "# Title\nSome text\n## Section"
        headings = validate_sdd.extract_headings(content)
        self.assertEqual(headings, ["Title", "Section"])

    def test_empty_document(self):
        self.assertEqual(validate_sdd.extract_headings(""), [])


class TestExtractSections(unittest.TestCase):
    def test_extracts_section_bodies(self):
        content = "## Introduction\nThis is the intro.\n## Overview\nThis is overview."
        sections = validate_sdd.extract_sections(content)
        self.assertIn("Introduction", sections)
        self.assertIn("Overview", sections)
        self.assertIn("intro", sections["Introduction"])

    def test_empty_section(self):
        content = "## Empty\n## Next\nContent here."
        sections = validate_sdd.extract_sections(content)
        self.assertEqual(sections["Empty"], "")

    def test_empty_document(self):
        self.assertEqual(validate_sdd.extract_sections(""), {})


class TestCheckRequiredSections(unittest.TestCase):
    def test_all_present(self):
        headings = [s for s in validate_sdd.REQUIRED_SECTIONS]
        missing = validate_sdd.check_required_sections(headings)
        self.assertEqual(missing, [])

    def test_some_missing(self):
        headings = ["1. Introduction", "2. System Overview"]
        missing = validate_sdd.check_required_sections(headings)
        self.assertIn("3. Architecture Design", missing)
        self.assertNotIn("1. Introduction", missing)

    def test_case_insensitive(self):
        headings = ["1. INTRODUCTION", "2. SYSTEM OVERVIEW"]
        missing = validate_sdd.check_required_sections(headings)
        self.assertNotIn("1. Introduction", missing)
        self.assertNotIn("2. System Overview", missing)


class TestCheckPlaceholderSections(unittest.TestCase):
    def test_detects_placeholder_only(self):
        sections = {
            "Purpose": "_Describe the purpose._",
        }
        placeholders = validate_sdd.check_placeholder_sections(sections)
        self.assertIn("Purpose", placeholders)

    def test_real_content_not_flagged(self):
        sections = {
            "Purpose": "This system handles user authentication.",
        }
        placeholders = validate_sdd.check_placeholder_sections(sections)
        self.assertNotIn("Purpose", placeholders)

    def test_mixed_content_not_flagged(self):
        sections = {
            "Purpose": "_Optionally describe here._\nActual content added.",
        }
        placeholders = validate_sdd.check_placeholder_sections(sections)
        self.assertNotIn("Purpose", placeholders)

    def test_empty_section_not_flagged(self):
        sections = {"Purpose": ""}
        placeholders = validate_sdd.check_placeholder_sections(sections)
        self.assertNotIn("Purpose", placeholders)


class TestCheckEmptySections(unittest.TestCase):
    def test_detects_empty_section(self):
        sections = {"Purpose": "", "Scope": "Some scope."}
        empty = validate_sdd.check_empty_sections(sections)
        self.assertIn("Purpose", empty)
        self.assertNotIn("Scope", empty)


class TestValidateFunction(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()

    def _write(self, filename, content):
        path = Path(self.tmpdir) / filename
        path.write_text(content, encoding="utf-8")
        return str(path)

    def test_valid_sdd_passes(self):
        sdd_path = self._write("valid.md", VALID_SDD)
        result = validate_sdd.validate(sdd_path, "sdd-template.md", strict=False)
        self.assertTrue(result)

    def test_missing_sections_fails(self):
        sdd_path = self._write("missing.md", MISSING_SECTIONS_SDD)
        result = validate_sdd.validate(sdd_path, "sdd-template.md", strict=False)
        self.assertFalse(result)

    def test_placeholder_only_passes_non_strict(self):
        sdd_path = self._write("placeholder.md", PLACEHOLDER_ONLY_SDD)
        result = validate_sdd.validate(sdd_path, "sdd-template.md", strict=False)
        self.assertTrue(result)

    def test_placeholder_only_fails_strict(self):
        sdd_path = self._write("placeholder.md", PLACEHOLDER_ONLY_SDD)
        result = validate_sdd.validate(sdd_path, "sdd-template.md", strict=True)
        self.assertFalse(result)

    def test_file_not_found_exits(self):
        with self.assertRaises(SystemExit) as cm:
            validate_sdd.read_file("/nonexistent/path/file.md")
        self.assertEqual(cm.exception.code, 2)


class TestMainEntryPoint(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmpdir = tempfile.mkdtemp()

    def _write(self, filename, content):
        path = Path(self.tmpdir) / filename
        path.write_text(content, encoding="utf-8")
        return str(path)

    def test_main_exits_0_on_valid_sdd(self):
        sdd_path = self._write("valid.md", VALID_SDD)
        with patch("sys.argv", ["validate_sdd.py", sdd_path]):
            with self.assertRaises(SystemExit) as cm:
                validate_sdd.main()
        self.assertEqual(cm.exception.code, 0)

    def test_main_exits_1_on_invalid_sdd(self):
        sdd_path = self._write("missing.md", MISSING_SECTIONS_SDD)
        with patch("sys.argv", ["validate_sdd.py", sdd_path]):
            with self.assertRaises(SystemExit) as cm:
                validate_sdd.main()
        self.assertEqual(cm.exception.code, 1)

    def test_main_strict_flag(self):
        sdd_path = self._write("placeholder.md", PLACEHOLDER_ONLY_SDD)
        with patch("sys.argv", ["validate_sdd.py", "--strict", sdd_path]):
            with self.assertRaises(SystemExit) as cm:
                validate_sdd.main()
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
