# 01_BLOG — MULTI-AUTHOR PUBLISHING PLATFORM MVP

**Author:** Talha Ahmed  
**Evaluation:** FalconXoft 15-Day Intern Performance Evaluation — Weekend 1  
**Target Ports:** Backend API: `http://127.0.0.1:8001` | Frontend: `http://localhost:3001`  
**Database:** PostgreSQL 18 (`blog_db`) on `127.0.0.1:5432`  
**GitHub Repository:** [https://github.com/Talhaahmed303/weekend1-blog-platform](https://github.com/Talhaahmed303/weekend1-blog-platform)  
**Live Editable Architecture:** [Open Architecture in Lucidchart](https://lucid.app/lucidchart/6ef90429-d6a5-4585-8b7f-2caaf728b0fc/edit?invitationId=inv_9b2b97cf-501b-429e-993d-a24c927fa54c&page=yofE0ycUHjJN#)  
**Live Editable Database ERD:** [Open Database ERD in Lucidchart](https://lucid.app/lucidchart/68348039-5c22-4638-9fb4-e1b0b98b3018/edit?invitationId=inv_c1318404-183d-4820-9dcc-30364c92b0bf)  
**Live Editable API Workflows Sequence:** [Open API Workflows in Lucidchart](https://lucid.app/lucidchart/08d5daad-11b0-4337-a650-e7fa3d01a6b4/edit?invitationId=inv_fbe6a186-bf56-4533-a8ca-676be1566c27)

---

## 1. Requirements, Business Goals & Scope Definition

### 1.1 Business Goals & Purpose
The **Blog Platform MVP** is an enterprise-grade multi-author technical publishing platform designed to empower engineering teams to author, collaborate, review, categorize, and publish technical insights while preserving strict draft privacy and high-integrity reader engagement.

### 1.2 User Personas & Roles
1. **Public Reader (Unauthenticated Guest):** Browses published articles, filters by category tags, conducts real-time keyword searches, and reads peer comments. Cannot create articles or submit comments without authentication.
2. **Author (Authenticated Creator):** Creates, edits, drafts, and publishes articles. Manages personal articles within "My Posts Studio". Can post comments on any published article and delete their own comments or moderate comments on their own articles. Cannot view other authors' unpublished drafts or edit other authors' posts.
3. **Site Administrator (Admin):** Possesses global oversight and moderation authority. Can edit, unpublish, or delete any article or comment on the platform, manage system categories, and monitor user accounts.

### 1.3 Role-Based Access Control (RBAC) Matrix

| Action / Endpoint | Public Reader | Author (Owner) | Author (Peer) | Site Admin |
| :--- | :---: | :---: | :---: | :---: |
| **Browse Published Feed** (`GET /api/posts/`) | ✅ Allow | ✅ Allow | ✅ Allow | ✅ Allow |
| **View Draft Post** (`GET /api/posts/{id}/`) | ❌ 404 Hidden | ✅ Allow | ❌ 404 Hidden | ✅ Allow |
| **Create Article** (`POST /api/posts/`) | ❌ 401 Unauthorized | ✅ Allow | ✅ Allow | ✅ Allow |
| **Edit/Update Article** (`PATCH /api/posts/{id}/`) | ❌ 401 Unauthorized | ✅ Allow | ❌ 403 Forbidden | ✅ Allow |
| **Delete Article** (`DELETE /api/posts/{id}/`) | ❌ 401 Unauthorized | ✅ Allow | ❌ 403 Forbidden | ✅ Allow |
| **Publish Article** (`POST /api/posts/{id}/publish/`) | ❌ 401 Unauthorized | ✅ Allow | ❌ 403 Forbidden | ✅ Allow |
| **Submit Comment on Published** (`POST /api/comments/`) | ❌ 401 Unauthorized | ✅ Allow | ✅ Allow | ✅ Allow |
| **Submit Comment on Draft** (`POST /api/comments/`) | ❌ 400 Bad Request | ❌ 400 Bad Request | ❌ 400 Bad Request | ❌ 400 Bad Request |
| **Delete Comment** (`DELETE /api/comments/{id}/`) | ❌ 401 Unauthorized | ✅ Own / On Own Post | ❌ 403 Forbidden | ✅ Allow |

### 1.4 System Assumptions & Boundaries
- **Bare-Metal Native Execution:** Zero Docker virtualization in MVP to minimize reviewer host friction and ensure instant debugging.
- **Single Currency/Region:** Architecture designed for primary deployment on US-East cloud instances or VPS.
- **Relational Integrity:** SQLite fallback provided in `.env` if PostgreSQL 18 local service is temporarily unavailable during offline testing.

### 1.5 Acceptance Criteria
- [x] **AC-1:** JWT-based user authentication with automatic token attachment in HTTP Authorization headers.
- [x] **AC-2:** Complete CRUD operations for blog posts with auto-generated URL slugs.
- [x] **AC-3:** Draft isolation: drafts must never appear in public feeds or search results.
- [x] **AC-4:** Transition lifecycle: publishing an article sets `published_at` timestamp and makes it visible across public feeds.
- [x] **AC-5:** Category filtering: articles can be grouped by categories with real-time post counts.
- [x] **AC-6:** Comments allowed exclusively on published posts; rejected with HTTP 400 if targeted at drafts.
- [x] **AC-7:** Instant, debounced search across titles, excerpts, body content, and categories.

### 1.6 Complete End-to-End User Journey
1. **Reader Discovery:** An anonymous visitor lands on `http://localhost:3001`, browses the curated feed of published technical articles, and filters by "System Design".
2. **Search:** The reader searches for "microservices" in the search bar; the feed updates without page reloads.
3. **Authentication:** The user logs in as `talha_author` using the top demo switcher.
4. **Draft Creation:** The author opens the Post Editor, selects local image upload or URL preset, types markdown content, and saves as `draft`.
5. **Draft Isolation Verification:** The author switches to `sara_writer`; the draft is completely invisible and unreachable.
6. **Publishing:** The author returns, opens "My Posts Studio", and clicks "Publish Now". The article is instantly live.
7. **Discussion:** Another author or admin leaves a comment on the published article.
8. **Moderation:** The author or admin deletes an inappropriate comment directly from the UI.

---

## 2. Technology Stack & Rationale

- **Backend:** Python 3.11 with **Django 5.2** and **Django REST Framework (DRF) 3.15**. Leverages Django's native ORM, custom permissions, and `drf-spectacular` for OpenAPI 3.0 generation.
- **Frontend:** **Next.js 14** (React 18 + TypeScript) styled with **Tailwind CSS**. Provides responsive card grids, glassmorphism accents, instant search, and a fast demo user switcher.
- **Database:** **PostgreSQL 18** (local service `postgresql-x64-18`) with 3NF schema, foreign key constraints, composite indexes, and a transparent SQLite fallback for portable evaluation.
- **Testing:** **`pytest` 9.1** and **`pytest-django` 4.14**. 19 automated integration tests covering positive, negative, boundary, permissions, and regression flows.
- **Documentation:** OpenAPI 3.0 YAML specification + Lucidchart-compatible architecture, ERD, and workflow sequence specifications.

---

## 3. Architecture Summary

The platform implements a decoupled **3-Tier Architecture**:
1. **Presentation Layer:** Next.js single-page application executing at `http://localhost:3001`. Manages client state, JWT persistence in localStorage, and optimistic UI transitions.
2. **API Layer:** Django REST Framework API listening at `http://127.0.0.1:8001/api/`. Enforces JWT verification, rate limiting, and object-level ownership checks (`IsAuthorOrAdminOrReadOnly`).
3. **Data Layer:** PostgreSQL 18 instance with `authentication_user`, `posts_category`, `posts_post`, and `comments_comment` relational tables.

---

## 4. Exact Setup & Run Instructions (Direct Local Machine — Zero Docker)

### Prerequisites:
- Python 3.11+ (with `pip`)
- Node.js v20+ / v24+ (with `npm`)
- PostgreSQL 18 service running locally on port 5432 (or set `USE_SQLITE=True` in `.env`)

### Step 1: Backend Setup
```bash
# Navigate to backend directory
cd 01_Blog/backend

# Verify migrations against PostgreSQL blog_db
python manage.py migrate

# Seed initial demo accounts, categories, and articles
python manage.py seed_data

# Start the Django REST Framework server on port 8001
python manage.py runserver 127.0.0.1:8001
```

### Step 2: Frontend Setup
```bash
# In a separate terminal, navigate to frontend directory
cd 01_Blog/frontend

# Install dependencies
npm install

# Run the Next.js development server on port 3001
npm run dev
```
Open **`http://localhost:3001`** in your browser.

### Step 3: Run Automated Test Suite
```bash
# From workspace root or 01_Blog/backend:
python -m pytest 01_Blog/backend/tests/test_blog_api.py -v
```
**Execution Proof:** 19 out of 19 tests pass in ~59 seconds. Detailed records in `05 - test-cases.xlsx`.

---

## 5. Seed Demo Credentials

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Site Admin** | `admin` | `Admin@123` | Global moderation, can edit/delete any post or comment |
| **Author 1** | `talha_author` | `Author@123` | Author of published articles and private draft |
| **Author 2** | `sara_writer` | `Author@123` | Peer author (cannot edit Talha's articles or view his drafts) |
| **Public Reader** | *Unauthenticated* | N/A | Public consumer, can browse feed, search, and view comments |

*(The Next.js frontend includes a convenient **Demo Switch** in the top navigation bar to instantaneously switch between these accounts with a single click).*

---

## 6. Lucidchart Diagrams & Deliverables Index

All diagrams required by the FalconXoft evaluation specification have been exported and provided in multiple formats for maximum defensibility. Clicking any preview diagram below will open the **live, editable Lucidchart workspace**:

### 6.1 System Architecture Diagram
[![System Architecture Diagram](02%20-%20architecture.png)](https://lucid.app/lucidchart/6ef90429-d6a5-4585-8b7f-2caaf728b0fc/edit?invitationId=inv_9b2b97cf-501b-429e-993d-a24c927fa54c&page=yofE0ycUHjJN#)
- **Vector PDF Deliverable:** [`02 - architecture.pdf`](02%20-%20architecture.pdf)
- **High-Res PNG Deliverable:** [`02 - architecture.png`](02%20-%20architecture.png)
- **Editable Lucidchart URL:** [Open Architecture in Lucidchart](https://lucid.app/lucidchart/6ef90429-d6a5-4585-8b7f-2caaf728b0fc/edit?invitationId=inv_9b2b97cf-501b-429e-993d-a24c927fa54c&page=yofE0ycUHjJN#)

---

### 6.2 Database ERD & Relational Schema
[![Database ERD Diagram](03%20-%20database-design.png)](https://lucid.app/lucidchart/68348039-5c22-4638-9fb4-e1b0b98b3018/edit?invitationId=inv_c1318404-183d-4820-9dcc-30364c92b0bf)
- **Vector PDF Deliverable:** [`03 - database-design.pdf`](03%20-%20database-design.pdf)
- **High-Res PNG Deliverable:** [`03 - database-design.png`](03%20-%20database-design.png)
- **Editable Lucidchart URL:** [Open Database ERD in Lucidchart](https://lucid.app/lucidchart/68348039-5c22-4638-9fb4-e1b0b98b3018/edit?invitationId=inv_c1318404-183d-4820-9dcc-30364c92b0bf)
- **PostgreSQL 1-Click DDL:** [`schema.sql`](schema.sql)

---

### 6.3 API Workflows & Sequence Workflows
[![API Sequence Workflows Diagram](04%20-%20api-workflows.png)](https://lucid.app/lucidchart/08d5daad-11b0-4337-a650-e7fa3d01a6b4/edit?invitationId=inv_fbe6a186-bf56-4533-a8ca-676be1566c27)
- **Vector PDF Deliverable:** [`04 - api-workflows.pdf`](04%20-%20api-workflows.pdf)
- **High-Res PNG Deliverable:** [`04 - api-workflows.png`](04%20-%20api-workflows.png)
- **Editable Lucidchart URL:** [Open API Workflows in Lucidchart](https://lucid.app/lucidchart/08d5daad-11b0-4337-a650-e7fa3d01a6b4/edit?invitationId=inv_fbe6a186-bf56-4533-a8ca-676be1566c27)
- **Complete OpenAPI 3.0 Contract:** [`openapi.yaml`](openapi.yaml)

---

## 7. Known Gaps & Future Improvements

1. **Email Verification:** Registration does not require email confirmation via SMTP in MVP; all registered accounts are activated immediately.
2. **Rich Text WYSIWYG:** Articles use standard Markdown/Plaintext formatting; a full rich-text editor (e.g. TipTap or ProseMirror) is planned for future milestones.
3. **Media CDN:** In MVP, images support direct local file upload (Base64) or external URLs; production deployments would offload media uploads directly to AWS S3 or Cloudflare R2.
