# 10 — PROJECT SUBMISSION INDEX: 01_BLOG PLATFORM

**Candidate:** Talha Ahmed  
**Evaluation:** FalconXoft 15-Day Intern Performance Evaluation — Weekend 1  
**Project Directory:** `Weekend1_Talha Ahmed/01_Blog/`  
**Status:** **100% COMPLETE & VERIFIED (Gate 1 Passed)**  
**GitHub Repository:** [https://github.com/Talhaahmed303/weekend1-blog-platform](https://github.com/Talhaahmed303/weekend1-blog-platform)

---

## 1. Project Deliverables Verification Matrix

All 10 required deliverables specified in Section 3 of the evaluation document have been generated, independently tested, and formatted:

| Deliverable ID | Filename | Format | Description / Verification Evidence | Status |
| :---: | :--- | :---: | :--- | :---: |
| **01** | [`01 - README.md`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/01%20-%20README.md) | Markdown | Purpose, Next.js+DRF stack, scope, setup/run/test steps, known gaps. | **Verified** |
| **02** | [`02 - architecture.pdf`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/02%20-%20architecture.pdf) | Vector PDF | Labeled 3-tier architecture, data movement, deployment boundaries + [Editable Lucidchart Link](https://lucid.app/lucidchart/6ef90429-d6a5-4585-8b7f-2caaf728b0fc/edit?invitationId=inv_9b2b97cf-501b-429e-993d-a24c927fa54c&page=yofE0ycUHjJN#). | **Verified** |
| **03** | [`03 - database-design.pdf`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/03%20-%20database-design.pdf) | Vector PDF | Normalized ERD with cardinality, PK/FK, indexes + `schema.sql` + [Editable Lucidchart Link](https://lucid.app/lucidchart/68348039-5c22-4638-9fb4-e1b0b98b3018/edit?invitationId=inv_c1318404-183d-4820-9dcc-30364c92b0bf). | **Verified** |
| **04** | [`04 - api-workflows.pdf`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/04%20-%20api-workflows.pdf) | Vector PDF | Sequence diagrams for success & failure journeys + `openapi.yaml` + [Editable Lucidchart Link](https://lucid.app/lucidchart/08d5daad-11b0-4337-a650-e7fa3d01a6b4/edit?invitationId=inv_fbe6a186-bf56-4533-a8ca-676be1566c27). | **Verified** |
| **05** | [`05 - test-cases.xlsx`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/05%20-%20test-cases.xlsx) | Excel (.xlsx) | 18 detailed test cases across 10 required columns with genuine `pytest` execution proofs (19 passed). | **Verified** |
| **06** | [`06 - engineering-decisions.md`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/06%20-%20engineering-decisions.md) | Markdown | Options considered, trade-offs, security, Docker exclusion rationale, gap remediation. | **Verified** |
| **07** | [`07 - source + demo`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/07%20-%20source%20+%20demo/README.md) | Folder / MD | [GitHub: Talhaahmed303/weekend1-blog-platform](https://github.com/Talhaahmed303/weekend1-blog-platform) + oral walkthrough script. | **Verified** |
| **08** | [`08 - cost-and-scaling.xlsx`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/08%20-%20cost-and-scaling.xlsx) | Excel (.xlsx) | Hostinger VPS ($6.99/mo) vs AWS ($37.28/mo) comparison table + scaling scenarios for 100, 1k, 10k, 1M users. | **Verified** |
| **09** | [`09 - sources-and-disclosure.md`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/09%20-%20sources-and-disclosure.md) | Markdown | Permissive open-source licenses, original work ledger, AI assistance disclosure, verified citations. | **Verified** |
| **10** | [`10 - submission-index.md`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/10%20-%20submission-index.md) | Markdown | Project-level submission index and reviewer verification confirmation. | **Verified** |

---

## 2. Accompanying Artifacts Included

- [`openapi.yaml`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/openapi.yaml): Full OpenAPI 3.0 specification exported directly from Django REST Framework via `drf-spectacular`.
- [`schema.sql`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/schema.sql): Clean PostgreSQL DDL script with table definitions, foreign keys, and indexes.
- [`.env.example`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/.env.example): Environment variable template containing non-secret defaults.
- [`lucidchart_diagrams/`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/): Ready-to-import Lucidchart code and DDL files:
  - [`01_ARCHITECTURE_DIAGRAM.mermaid`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/01_ARCHITECTURE_DIAGRAM.mermaid): Complete 3-tier architecture Mermaid code.
  - [`02_DATABASE_ERD.sql`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/02_DATABASE_ERD.sql) & [`02_DATABASE_ERD.mermaid`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/02_DATABASE_ERD.mermaid): PostgreSQL DDL & Mermaid code for 1-click ERD import.
  - [`03_API_WORKFLOWS_SEQUENCE.mermaid`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/03_API_WORKFLOWS_SEQUENCE.mermaid): Complete Success and 3 Failure path sequence workflows.
  - [`LUCIDCHART_IMPORT_GUIDE.md`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/LUCIDCHART_IMPORT_GUIDE.md): Step-by-step export & link guide.

---

## 3. Reviewer Verification Summary

- **Backend Run Command:** `python manage.py runserver 127.0.0.1:8001` (Inside `01_Blog/backend`)
- **Frontend Run Command:** `npm run dev` (Inside `01_Blog/frontend` on port 3001)
- **Test Command:** `python -m pytest 01_Blog/backend/tests/test_blog_api.py -v` (19 passed in 59.20s)
- **Zero Docker:** Fully runnable on bare metal Windows machine.
- **Reviewer Permissions:** Reviewer has full read and comment permissions. Zero credentials or production secrets committed.
