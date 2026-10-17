# 06 — ENGINEERING DECISIONS & ARCHITECTURAL TRADEOFFS (BLOG PLATFORM)

**Candidate:** Talha Ahmed  
**Evaluation:** FalconXoft 15-Day Intern Performance Evaluation — Weekend 1  
**Project:** `01_Blog`  

---

## 1. Technology Options Considered & Final Selection

### Backend Framework: Django REST Framework vs Express.js vs FastAPI
- **Options Evaluated:**
  1. *Django REST Framework (Python 3.11):* Full-featured web framework with mature ORM, built-in migration engine, automated `/admin/` moderation portal, declarative serializers, and extensive third-party ecosystem (`drf-spectacular`, `simplejwt`).
  2. *Node.js / Express.js:* Minimalist event-driven runtime with rapid HTTP routing, but requires assembling disparate libraries for ORM (Prisma/TypeORM), authentication (Passport/jsonwebtoken), and migrations.
  3. *FastAPI (Python):* High-performance asynchronous framework using Pydantic and SQLAlchemy, but lacks an out-of-the-box admin panel and requires complex session/auth wiring for relational RBAC.
- **Final Choice:** **Django REST Framework (DRF)**.
- **Rationale:** Matches FalconXoft's primary backend production stack. Provides instant administrative capabilities via Django Admin, declarative serializers that eliminate boilerplate input validation, and rock-solid relational data integrity.

### Frontend Architecture: Next.js (App Router) vs Vite SPA vs Django Templates
- **Options Evaluated:**
  1. *Next.js with React & TypeScript:* Server-side rendering (SSR), static site generation, rich React ecosystem, and strong typing via TypeScript.
  2. *Vite + React SPA:* Fast client-only bundle, but lacks SEO advantages and server-side pre-rendering.
  3. *Django Server-Rendered HTML Templates:* Simpler single-process runtime, but delivers inferior interactive UX with full-page refreshes.
- **Final Choice:** **Next.js with React, TypeScript, and Tailwind CSS**.
- **Rationale:** Aligns with FalconXoft's client-side engineering stack. Delivers an aesthetic, fluid user experience with optimistic UI updates and instant search, while communicating via clean REST endpoints.

---

## 2. Docker & Containerization Trade-Offs (Explicit Evaluation)

### Decision: Direct Local Host Execution for MVP (Zero Docker)
Per explicit architectural directive, Docker and Docker Compose were **not implemented** in the MVP.

### Analysis & Interview Defense:
- **Why Excluded for MVP:**
  1. *Reviewer Friction:* Running a local Node.js process and Django service on bare metal requires zero virtualization overhead, avoids Windows Hyper-V/WSL2 configuration issues, and prevents container port collisions on the reviewer's laptop.
  2. *Resource Footprint:* A running Docker Desktop daemon consumes 2–4 GB of host RAM on Windows. Running natively on Python 3.11 and Node.js v24 consumes less than 150 MB combined.
  3. *Deterministic Debugging:* In an oral interview walkthrough, stepping through code with local debuggers and running `python manage.py runserver` is instantaneous and completely transparent.
- **Proposed Future Production Containerization:**
  - For production cloud deployments (e.g. AWS ECS or Kubernetes), multi-stage Dockerfiles will be introduced:
    - *Backend:* `python:3.11-slim` with non-root user execution, pre-compiled wheels, and Gunicorn WSGI workers.
    - *Frontend:* `node:20-alpine` standalone output container, minimizing image size from 1.2 GB to ~85 MB.

---

## 3. Infrastructure Simplicity: Why Redis & Celery Were Omitted in MVP

- **Decision:** No Redis caching layers or Celery background task queues were implemented in this MVP.
- **Rationale:**
  1. *Unjustified Complexity:* The Blog Platform MVP processes low-latency synchronous operations (article CRUD, comments, search). Introducing Celery would mandate a persistent Redis broker, separate worker processes, beat schedulers, and distributed failure handling.
  2. *PostgreSQL Capacity:* PostgreSQL 18 on local NVMe storage handles up to 5,000 read queries per second with indexed lookups (`idx_posts_status_published`). Caching at this stage is premature optimization.
- **Proposed Scaling Trigger (10,000+ Users):**
  - As documented in `08 - cost-and-scaling.xlsx`, when read traffic exceeds 200 req/sec, a Redis caching layer will be inserted in front of `CategoryViewSet` and `PostViewSet.list()`, invalidating keys via Django post-save signals.

---

## 4. Security Considerations & Mitigations Implemented

| Threat Vector | Severity | Implemented Mitigation in 01_Blog |
| :--- | :---: | :--- |
| **Broken Object Level Auth (BOLA)** | High | Custom DRF permission `IsAuthorOrAdminOrReadOnly` strictly compares `request.user == post.author` before allowing `PATCH`, `PUT`, or `DELETE`. Unauthorized authors receive HTTP 403. |
| **Draft Post Data Leaks** | High | `PostViewSet.get_queryset()` applies a strict visibility filter: unauthenticated users and peer authors cannot receive draft posts in list or detail queries (returning HTTP 404). |
| **SQL Injection** | Critical | 100% parameterized queries via Django ORM. Zero raw SQL string interpolation. |
| **Cross-Site Scripting (XSS)** | High | React's automatic JSX text escaping prevents script injection in titles, excerpts, and comments. |
| **Invalid Draft Commenting** | Medium | `CommentViewSet.perform_create` checks `post.status == 'published'`. Throws HTTP 400 if comment is attempted on a draft. |

---

## 5. Technical Risks & Remediation

1. **Risk:** Reviewer testing on a machine where PostgreSQL service is stopped or port 5432 is occupied.
   - *Remediation:* `core/settings.py` includes a transparent fallback switch: setting `USE_SQLITE=True` in `.env` automatically diverts migrations and queries to a portable `db.sqlite3` file with zero code modifications.
2. **Risk:** Token expiration during live review demo.
   - *Remediation:* Access token lifetime is configured to 24 hours in development mode (`SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=1)`), with automatic refresh token rotation enabled.
