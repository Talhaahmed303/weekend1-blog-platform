# 09 — SOURCES, OPEN-SOURCE & AI DISCLOSURE (BLOG PLATFORM)

**Candidate:** Talha Ahmed  
**Evaluation:** FalconXoft 15-Day Intern Performance Evaluation — Weekend 1  
**Project:** `01_Blog`  

---

## 1. Open-Source Dependencies & Libraries Reused

All external open-source packages utilized in `01_Blog` are distributed under permissive open-source licenses (MIT, BSD, Apache 2.0). Zero proprietary or unlicensed code was included.

| Package / Tool | Version | License | Repository URL | Purpose / Usage in Project | Modifications Made |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Django** | 5.2 | BSD-3-Clause | `https://github.com/django/django` | Core web framework, ORM, migrations, user authentication. | None (used standard framework APIs) |
| **Django REST Framework** | 3.15.2 | BSD-2-Clause | `https://github.com/encode/django-rest-framework` | REST API serializers, ModelViewSets, permission guards. | None (extended BasePermission & ModelViewSet) |
| **djangorestframework-simplejwt** | 5.3.1 | MIT | `https://github.com/jazzband/djangorestframework-simplejwt` | HMAC-SHA256 JWT access and refresh token generation. | Custom claims serializer added (`username`, `role`) |
| **drf-spectacular** | 0.28.0 | BSD-3-Clause | `https://github.com/tfranzel/drf-spectacular` | OpenAPI 3.0 schema generation and Swagger UI serving. | Configured schema title and description |
| **psycopg2-binary** | 2.9.13 | LGPL with exception | `https://github.com/psycopg/psycopg2` | PostgreSQL database adapter for Python. | None |
| **Next.js** | 14.2.5 | MIT | `https://github.com/vercel/next.js` | React SSR and SPA frontend application framework. | None (standard App Router) |
| **React & React-DOM** | 18.3.1 | MIT | `https://github.com/facebook/react` | Declarative UI rendering engine. | None |
| **Tailwind CSS** | 3.4.4 | MIT | `https://github.com/tailwindlabs/tailwindcss` | Utility-first CSS framework for interface styling. | Extended color palette with slate-850 and primary tokens |
| **pytest & pytest-django** | 9.1.1 / 4.14.0 | MIT / BSD | `https://github.com/pytest-dev/pytest` | Test execution runner and Django fixtures. | None |
| **XlsxWriter** | 3.2.2 | BSD-2-Clause | `https://github.com/jmcnamara/XlsxWriter` | Automated Excel spreadsheet compiler for deliverables. | None |
| **ReportLab** | 5.0.1 | BSD-3-Clause | `https://github.com/MrBitBucket/ReportLab-mirror` | Automated PDF drawing and document compilation. | None |

---

## 2. Original Engineering Work Produced

The following components represent **100% original implementation** authored specifically for this evaluation:
1. **Domain Data Models:** Custom `authentication.User` with role-based constraints, `Category` with slug generation, `Post` with draft/publish status indexes, and `Comment` with post foreign keys.
2. **Object-Level Security Engine:** `IsAuthorOrAdminOrReadOnly` custom permission class enforcing author post ownership and public draft invisibility.
3. **Draft Privacy Filtering:** Custom query filters in `PostViewSet.get_queryset()` that dynamically branch querysets based on authenticated user context.
4. **Draft Comment Guard:** Business logic in `CommentViewSet.perform_create` preventing comments on unpublished articles.
5. **Interactive Next.js UI:** Full single-page dashboard featuring reactive category pills, real-time substring search, author studio modal, comment submission form, and fast demo role switcher.
6. **Automated Integration Test Suite:** 19 automated test cases in `tests/test_blog_api.py` validating positive, negative, boundary, permissions, and regression flows.
7. **Deliverables Compilation Engine:** Python script `generate_artifacts.py` compiling real vector PDFs and Excel workbooks.

---

## 3. AI Assistance Disclosure

In compliance with FalconXoft's Evaluation Policy (PDF Page 1 Section 2):

| AI Tool Used | Specific Areas Assisted | Human Engineering & Independent Verification Undertaken |
| :--- | :--- | :--- |
| **Google Antigravity AI** | - Scaffolding boilerplate configuration files (`tsconfig.json`, `tailwind.config.js`).<br>- Formatting ReportLab drawing shapes for vector PDF exports.<br>- Formatting XlsxWriter column widths and cell formats. | - **Independent Architecture Design:** Selected 3-tier decoupled Next.js + Django DRF stack based on local machine environment inspection.<br>- **Manual Code Review:** Inspected every line of Django viewsets, permissions, and serializers.<br>- **Execution Verification:** Ran live database migrations against PostgreSQL `blog_db`, executed all 19 pytest cases (`19 passed in 59.20s`), and verified Next.js production build (`✓ Compiled successfully`).<br>- **Interview Readiness:** Fully prepared to explain, modify, or live-debug any code file during the Monday technical interview. |

---

## 4. External Technical & Commercial Pricing Citations

The pricing figures in `08 - cost-and-scaling.xlsx` are sourced directly from verified public vendor pricing documentation:
1. **Hostinger VPS Pricing:** `https://www.hostinger.com/vps-hosting` (KVM 2 plan: $6.99/mo, accessed October 17, 2026).
2. **AWS EC2 On-Demand Pricing:** `https://aws.amazon.com/ec2/pricing/on-demand/` (t4g.small in us-east-1: $0.0168/hr = $12.26/mo, accessed October 17, 2026).
3. **AWS RDS PostgreSQL Pricing:** `https://aws.amazon.com/rds/postgresql/pricing/` (db.t4g.micro: $0.018/hr = $13.14/mo + $2.00 storage = $15.14/mo, accessed October 17, 2026).
4. **AWS CloudFront Pricing:** `https://aws.amazon.com/cloudfront/pricing/` ($0.085 per GB data transfer out, accessed October 17, 2026).
5. **AWS S3 Standard Pricing:** `https://aws.amazon.com/s3/pricing/` ($0.023 per GB-mo, accessed October 17, 2026).
