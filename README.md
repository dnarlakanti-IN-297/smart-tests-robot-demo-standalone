# Smart Tests Demo: Issue Tracker Application
<!-- Updated: 2026-06-04 -->

![Tests](https://github.com/xgalanxhi/issues-tracker-app/actions/workflows/tests.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Smart Tests](https://img.shields.io/badge/Smart%20Tests-Enabled-brightgreen.svg)

**A demonstration repository showcasing [CloudBees Smart Tests](https://www.cloudbees.com/products/smart-tests) predictive test selection capabilities with a Python application and pytest test suite.**


**Ready to see Smart Tests in action? Start with [QUICKSTART GUIDE](./QUICKSTART.md)!** 🚀

This repository contains a fully functional Issue Tracker application built with FastAPI, complete with 140+ tests (unit, integration, and E2E) that demonstrate how Smart Tests uses AI to intelligently predict and select only the relevant tests based on code changes, reducing CI execution time by 50% or more.

## 🎯 What This Repository Demonstrates

- **AI-Powered Test Selection**: Smart Tests analyzes code changes and predicts which tests are affected
- **Observation Mode**: All tests run while Smart Tests validates prediction accuracy in the UI
- **Multi-Suite Support**: Unit, integration, and E2E tests all integrated with Smart Tests
- **CI/CD Integration**: GitHub Actions workflows with complete Smart Tests integration
- **Demo Patches**: Pre-built code changes that simulate real development scenarios with test failures

## 🚀 Get Started

**Choose your path based on what you want to do:**

<details>
<summary><strong>🎬 I Want to Run the Smart Tests Demo</strong></summary>

<br>

**→ [QUICKSTART.md](./QUICKSTART.md)** - Complete step-by-step guide to:
- Fork the repository and set up Smart Tests
- Run baseline tests and view results in CloudBees
- Apply demo patches that break tests
- See how Smart Tests predicts which tests will fail
- Analyze prediction accuracy and time savings

**Time Required:** 15-20 minutes
**Prerequisites:** GitHub account, CloudBees account (free tier)

</details>

<details>
<summary><strong>🔧 I Want to Run the Application Locally</strong></summary>

<br>

**→ [TECHNICAL_REFERENCE.md - Section 7: Local Development Setup](./TECHNICAL_REFERENCE.md#7-local-development-setup)**

Quick commands:
```bash
# Clone and setup
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Initialize database
make db-init && make migrate && make seed

# Run application
make run
```

Application runs at: http://localhost:8000

</details>

<details>
<summary><strong>📚 I Want Complete Technical Documentation</strong></summary>

<br>

**→ [TECHNICAL_REFERENCE.md](./TECHNICAL_REFERENCE.md)** - Comprehensive reference covering:
1. Application Specifications (tech stack, dependencies, configuration)
2. Database Schema and Models (all 6 models documented)
3. API Endpoints (complete endpoint inventory)
4. Testing Architecture (140+ tests, fixtures, configuration)
5. GitHub Actions and CI/CD (workflow specifications)
6. Smart Tests Integration (complete workflow documentation)
7. Local Development Setup (step-by-step guide)
8. Docker Deployment (containerization guide)
9. Code Quality and Standards (formatting, linting, style)
10. Project Structure (directory tree, architecture)

</details>

<details>
<summary><strong>🧪 I Want to Understand the Test Suite</strong></summary>

<br>

**→ [TECHNICAL_REFERENCE.md - Section 4: Testing Architecture](./TECHNICAL_REFERENCE.md#4-testing-architecture)**

Test organization:
- **Unit Tests**: 6 files testing services
- **Integration Tests**: 5 files testing API endpoints
- **E2E Tests**: 3 files with Playwright browser automation

Run tests:
```bash
make test              # Unit + integration
make test-e2e         # End-to-end tests
make test-all         # All tests
```

</details>

<details>
<summary><strong>🔬 I Want to Understand Smart Tests Integration</strong></summary>

<br>

**→ [TECHNICAL_REFERENCE.md - Section 6: Smart Tests Integration](./TECHNICAL_REFERENCE.md#6-smart-tests-integration)**

Learn about:
- How Smart Tests CLI integrates with pytest
- The 6-step workflow (record build → create subset → run tests → record results)
- Observation mode vs production mode
- JUnit XML configuration
- Viewing results in CloudBees platform

</details>

<details>
<summary><strong>🎨 I Want to Create New Demo Patches</strong></summary>

<br>

**→ [patches/CREATING_NEW_PATCHES.md](./patches/CREATING_NEW_PATCHES.md)** - Complete guide including:
- What makes a good demo patch
- Step-by-step patch creation process
- Testing and validation
- 6+ example patch ideas

**→ [patches/AI_PATCH_GENERATION_PROMPT.txt](./patches/AI_PATCH_GENERATION_PROMPT.txt)** - Ready-to-use AI prompt for generating patches with Claude/ChatGPT

**→ [patches/README.md](./patches/README.md)** - Documentation of existing patches

</details>

<details>
<summary><strong>🔄 I Want to Understand the CI/CD Workflows</strong></summary>

<br>

**→ [TECHNICAL_REFERENCE.md - Section 5: GitHub Actions and CI/CD](./TECHNICAL_REFERENCE.md#5-github-actions-and-cicd)**

GitHub Actions workflows:
- **Tests Workflow**: Runs unit, integration, and E2E tests with Smart Tests
- **Apply Demo Patch Workflow**: Applies breaking changes to demonstrate CI behavior

Both workflows fully documented with step-by-step breakdowns.

</details>



