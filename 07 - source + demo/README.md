# 07 — SOURCE REPOSITORY & 3-5 MINUTE DEMO WALKTHROUGH (BLOG PLATFORM)

**Candidate:** Talha Ahmed  
**Evaluation:** FalconXoft 15-Day Intern Performance Evaluation — Weekend 1  
**Project:** `01_Blog`  

---

## 1. Source Repository Information

- **Local Repository Path:** `d:/Weekend1_Talha Ahmed/01_Blog/`
- **Backend Entrypoint:** `01_Blog/backend/manage.py` (Port 8001)
- **Frontend Entrypoint:** `01_Blog/frontend/src/app/page.tsx` (Port 3001)
- **Git Branch:** `main`
- **GitHub Repository Link (Submission):** `https://github.com/talhaahmed303/weekend1-blog-platform` *(configured for evaluation review)*
- **Demo Recording Link:** [Watch Blog Platform Demo Video](https://drive.google.com/file/d/1AW2mPPcViKTWvYFIVnQBvcWWYluvTLST/view?usp=sharing) *(accessible to HR and Junior 1/2 reviewer)*

---

## 2. Structured 3–5 Minute Demo Script (Interview Walkthrough Guide)

This script is structured for the Monday oral technical interview walkthrough. Follow these exact steps to demonstrate all required acceptance criteria to the reviewer:

### Segment 1: Environment & System Overview (0:00 – 0:45)
- Open terminal and demonstrate the two running services:
  - Backend: `python manage.py runserver 127.0.0.1:8001` (Django 5.2 + DRF)
  - Frontend: `npm run dev` on port 3001 (Next.js 14 + Tailwind CSS)
- Highlight connection to PostgreSQL 18 database `blog_db`.
- Show OpenAPI documentation at `http://127.0.0.1:8001/api/docs/`.

### Segment 2: Public Reader Experience & Instant Search (0:45 – 1:30)
- Navigate to `http://localhost:3001` as **Public Reader**.
- Demonstrate that all visible posts have `status = 'published'`. Note that private drafts are invisible.
- Click category pills: *"System Design"*, *"Engineering Excellence"*, *"DevOps & Cloud"*. Observe instantaneous filtering.
- Type `"microservices"` in the search bar. Observe live search query matching title and body text.

### Segment 3: Author Workflow & Draft Lifecycle (1:30 – 2:45)
- Click the top demo switch: **"✍️ Author 1 (Talha)"**.
- Notice the UI immediately updates to show Talha's authenticated avatar and role badge.
- Click **"My Posts Studio"**.
- Point out the draft: *"[DRAFT] Technical Notes on Raft and Paxos Consensus Algorithms"*.
- Switch to **"✍️ Author 2 (Sara)"**: show that Sara **CANNOT** see Talha's draft! (Proves draft isolation).
- Switch back to Talha and click **"🚀 Publish Now"** on the draft.
- Show that the post transitions to `status = 'published'`, `published_at` timestamp is generated, and the article is now live on the public feed!

### Segment 4: Comments & Business Rule Enforcement (2:45 – 3:30)
- Open the newly published article.
- Submit a technical comment: *"Great insights on distributed consensus."*
- Show that the comment is saved in PostgreSQL and displayed in real-time.
- Explain the business rule: Comments on drafts are rejected with HTTP 400.
- Delete the comment using author moderation privileges.

### Segment 5: Admin Moderation & Test Suite Proof (3:30 – 4:30)
- Switch to **"👑 Admin"**.
- Demonstrate that Admin can edit, moderate, or delete any post on the platform.
- Open terminal and run the automated test suite:
  ```bash
  python -m pytest 01_Blog/backend/tests/test_blog_api.py -v
  ```
- Show that all **19 tests pass 100%**, covering positive, negative, boundary, permissions, and regression flows.
