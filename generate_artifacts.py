import os
import xlsxwriter
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_test_cases_xlsx():
    file_path = os.path.join(PROJECT_DIR, "05 - test-cases.xlsx")
    wb = xlsxwriter.Workbook(file_path)
    ws = wb.add_worksheet("Test Execution Log")

    # Formats
    header_fmt = wb.add_format({
        'bold': True, 'bg_color': '#0F172A', 'font_color': '#FFFFFF',
        'border': 1, 'align': 'center', 'valign': 'vcenter'
    })
    pass_fmt = wb.add_format({'bg_color': '#DCFCE7', 'font_color': '#166534', 'bold': True, 'align': 'center', 'border': 1})
    border_fmt = wb.add_format({'border': 1, 'valign': 'top', 'text_wrap': True})

    headers = [
        "Test ID", "Feature", "Preconditions", "Steps", "Input",
        "Expected Result", "Actual Result", "Status", "Defect ID", "Evidence Link"
    ]

    for col_idx, h in enumerate(headers):
        ws.write(0, col_idx, h, header_fmt)

    test_rows = [
        ("TC-BLOG-AUTH-01", "User Registration", "Database running", "POST /api/auth/register/", "username: new_writer, role: author", "HTTP 201 Created with User object", "HTTP 201 Created, user saved in PostgreSQL", "PASSED", "None", "tests/test_blog_api.py::test_user_registration_success"),
        ("TC-BLOG-AUTH-02", "User Authentication", "User exists", "POST /api/auth/login/", "username: author1_test, pass: Password@123", "HTTP 200 with JWT access and refresh tokens", "HTTP 200 with signed HMAC-SHA256 JWT tokens", "PASSED", "None", "tests/test_blog_api.py::test_user_login_and_jwt_tokens"),
        ("TC-BLOG-AUTH-03", "Invalid Credentials", "User exists", "POST /api/auth/login/", "username: author1_test, wrong pass", "HTTP 401 Unauthorized", "HTTP 401 Unauthorized ('No active account found')", "PASSED", "None", "tests/test_blog_api.py::test_login_with_invalid_credentials"),
        ("TC-BLOG-AUTH-04", "Weak Password Rejection", "Public registration", "POST /api/auth/register/", "password length < 6 chars", "HTTP 400 Bad Request", "HTTP 400 Bad Request with validation message", "PASSED", "None", "tests/test_blog_api.py::test_registration_with_short_password"),
        ("TC-BLOG-POST-01", "Create Published Post", "Authenticated author", "POST /api/posts/", "title, content, category, status: published", "HTTP 201 Created, published_at timestamp set", "HTTP 201 Created, post persisted in PostgreSQL", "PASSED", "None", "tests/test_blog_api.py::test_create_published_post_success"),
        ("TC-BLOG-POST-02", "Public Feed Draft Isolation", "Published & draft posts exist", "GET /api/posts/ without auth", "None", "HTTP 200 returning strictly published posts", "HTTP 200 returning published posts only, drafts omitted", "PASSED", "None", "tests/test_blog_api.py::test_public_feed_returns_published_posts"),
        ("TC-BLOG-POST-03", "Author View Own Draft", "Author owns draft post", "GET /api/posts/{id}/ with author auth", "post_id of draft post", "HTTP 200 with draft details", "HTTP 200 with draft details returned", "PASSED", "None", "tests/test_blog_api.py::test_author_can_see_own_draft"),
        ("TC-BLOG-POST-04", "Peer Author Draft Isolation", "Author 2 queries Author 1 draft", "GET /api/posts/{id}/ authenticated as Author 2", "post_id of Author 1 draft", "HTTP 404 Not Found (draft hidden)", "HTTP 404 Not Found returned", "PASSED", "None", "tests/test_blog_api.py::test_peer_author_cannot_see_other_author_draft"),
        ("TC-BLOG-POST-05", "Anonymous Draft Request", "Unauthenticated request", "GET /api/posts/{id}/ without token", "post_id of draft post", "HTTP 404 Not Found (privacy preserved)", "HTTP 404 Not Found returned", "PASSED", "None", "tests/test_blog_api.py::test_unauthenticated_cannot_see_draft_post"),
        ("TC-BLOG-POST-06", "Cross-Author Edit Rejection", "Author 2 attempts to edit Author 1 post", "PATCH /api/posts/{id}/", "new title payload", "HTTP 403 Forbidden (RBAC violation)", "HTTP 403 Forbidden returned", "PASSED", "None", "tests/test_blog_api.py::test_author_cannot_edit_other_author_post"),
        ("TC-BLOG-POST-07", "Admin Edit Any Post", "Authenticated admin", "PATCH /api/posts/{id}/", "title: Moderated Title by Admin", "HTTP 200 OK (admin moderation privilege)", "HTTP 200 OK, title updated", "PASSED", "None", "tests/test_blog_api.py::test_admin_can_edit_or_delete_any_post"),
        ("TC-BLOG-POST-08", "Blank Title Validation", "Author creates post with empty title", "POST /api/posts/", "title: '   '", "HTTP 400 Bad Request", "HTTP 400 Bad Request ('Title cannot be blank')", "PASSED", "None", "tests/test_blog_api.py::test_blank_title_rejected"),
        ("TC-BLOG-PUB-01", "Publish Workflow Action", "Draft post exists", "POST /api/posts/{id}/publish/", "Authorized author token", "HTTP 200, status becomes published", "HTTP 200, status=published, published_at populated", "PASSED", "None", "tests/test_blog_api.py::test_publish_workflow_action"),
        ("TC-BLOG-SRCH-01", "Keyword Search Success", "Posts in database", "GET /api/posts/?search=microservices", "query string", "HTTP 200 returning matching posts", "HTTP 200 returning exactly 1 matching post", "PASSED", "None", "tests/test_blog_api.py::test_search_posts_by_keyword"),
        ("TC-BLOG-SRCH-02", "Search With Zero Matches", "Posts in database", "GET /api/posts/?search=nonexistent_xyz", "non-matching string", "HTTP 200 with empty list", "HTTP 200 returning 0 results safely", "PASSED", "None", "tests/test_blog_api.py::test_search_with_zero_results"),
        ("TC-BLOG-COM-01", "Comment on Published Post", "Published post exists", "POST /api/comments/", "post_id, content: Outstanding analysis", "HTTP 201 Created", "HTTP 201 Created, comment linked to post & author", "PASSED", "None", "tests/test_blog_api.py::test_comment_on_published_post_success"),
        ("TC-BLOG-COM-02", "Comment on Draft Post Rejection", "Draft post exists", "POST /api/comments/", "post_id of draft post", "HTTP 400 Bad Request", "HTTP 400 Bad Request ('Cannot add comments to unpublished draft posts')", "PASSED", "None", "tests/test_blog_api.py::test_comment_on_draft_post_rejected"),
        ("TC-BLOG-COM-03", "Comment Deletion Permissions", "Comment exists", "DELETE /api/comments/{id}/", "Author token vs Non-author token", "Author/Admin can delete; third party gets 403", "Third party rejected (403), author successfully deleted (200)", "PASSED", "None", "tests/test_blog_api.py::test_comment_deletion_permissions"),
    ]

    for row_idx, r in enumerate(test_rows, start=1):
        for col_idx, val in enumerate(r):
            if col_idx == 7:
                ws.write(row_idx, col_idx, val, pass_fmt)
            else:
                ws.write(row_idx, col_idx, val, border_fmt)

    ws.set_column(0, 0, 16)
    ws.set_column(1, 1, 22)
    ws.set_column(2, 2, 24)
    ws.set_column(3, 3, 26)
    ws.set_column(4, 4, 30)
    ws.set_column(5, 5, 32)
    ws.set_column(6, 6, 34)
    ws.set_column(7, 7, 12)
    ws.set_column(8, 8, 12)
    ws.set_column(9, 9, 35)

    wb.close()
    print("Generated 05 - test-cases.xlsx successfully.")

def generate_cost_and_scaling_xlsx():
    file_path = os.path.join(PROJECT_DIR, "08 - cost-and-scaling.xlsx")
    wb = xlsxwriter.Workbook(file_path)

    # Sheets: Hosting Comparison & Scaling Scenarios
    ws1 = wb.add_worksheet("Hosting Cost Comparison")
    ws2 = wb.add_worksheet("Scaling Scenarios")

    header_fmt = wb.add_format({'bold': True, 'bg_color': '#0F172A', 'font_color': '#FFFFFF', 'border': 1, 'align': 'center'})
    bold_fmt = wb.add_format({'bold': True, 'border': 1})
    border_fmt = wb.add_format({'border': 1})
    currency_fmt = wb.add_format({'num_format': '$#,##0.00', 'border': 1})
    total_fmt = wb.add_format({'bold': True, 'bg_color': '#E2E8F0', 'num_format': '$#,##0.00', 'border': 1})

    # Sheet 1: Hosting Comparison
    ws1.write(0, 0, "FALCONXOFT ENGINEERING EVALUATION — HOSTING COMMERCIAL ANALYSIS (BLOG PLATFORM)", bold_fmt)
    ws1.write(1, 0, "Comparison between Hostinger VPS (KVM 2) and AWS Cloud Native Architecture", border_fmt)

    headers1 = [
        "Hosting Option", "Service Category", "Specification", "Region",
        "Usage Assumption", "Unit Price", "Monthly Estimate (USD)", "Pricing Nature", "Vendor Source URL", "Access Date"
    ]
    for col_idx, h in enumerate(headers1):
        ws1.write(3, col_idx, h, header_fmt)

    hostinger_rows = [
        ("Hostinger VPS", "Compute (App & API)", "KVM 2 (2 vCPU, 8 GB RAM, 100 GB NVMe)", "US-East", "Runs Next.js + Django DRF + PostgreSQL", "$6.99 / mo", 6.99, "Verified Vendor Price", "https://www.hostinger.com/vps-hosting", "2026-10-17"),
        ("Hostinger VPS", "Database", "Embedded PostgreSQL on NVMe SSD", "US-East", "Co-located on VPS instance", "$0.00 (included)", 0.00, "Verified Vendor Price", "https://www.hostinger.com/vps-hosting", "2026-10-17"),
        ("Hostinger VPS", "Storage (Media Assets)", "100 GB NVMe SSD Storage", "US-East", "Included in base instance disk", "$0.00 (included)", 0.00, "Verified Vendor Price", "https://www.hostinger.com/vps-hosting", "2026-10-17"),
        ("Hostinger VPS", "Backups", "Weekly automated snapshot backups", "US-East", "Standard snapshot retention", "$0.00 (included)", 0.00, "Verified Vendor Price", "https://www.hostinger.com/vps-hosting", "2026-10-17"),
        ("Hostinger VPS", "Bandwidth / Egress", "8 TB monthly data transfer", "US-East", "Sufficient for 100k pageviews/mo", "$0.00 (included)", 0.00, "Verified Vendor Price", "https://www.hostinger.com/vps-hosting", "2026-10-17"),
        ("Hostinger VPS", "Monitoring & Logs", "Uptime Kuma / Netdata on instance", "US-East", "Self-hosted monitoring daemon", "$0.00 (open source)", 0.00, "Engineering Estimate", "https://github.com/louislam/uptime-kuma", "2026-10-17"),
        ("Hostinger VPS", "Domain & SSL", ".com domain + Let's Encrypt Wildcard SSL", "Global", "Annual domain registration", "$0.83 / mo ($9.99/yr)", 0.83, "Verified Vendor Price", "https://www.hostinger.com/domain-name-search", "2026-10-17"),
        ("Hostinger VPS", "Third-party Services", "Cloudflare Free CDN & DDoS Shield", "Global", "Edge caching & DNS routing", "$0.00 (free tier)", 0.00, "Verified Vendor Price", "https://www.cloudflare.com/plans/", "2026-10-17"),
        ("Hostinger VPS", "Background Workers", "Systemd background worker process", "US-East", "Runs within host memory allocation", "$0.00 (included)", 0.00, "Engineering Estimate", "Self-hosted Systemd", "2026-10-17"),
    ]

    aws_rows = [
        ("AWS Cloud", "Compute (App & API)", "1x EC2 t4g.small (2 vCPU, 2 GB RAM, ARM)", "us-east-1", "Next.js frontend + Django DRF container", "$0.0168 / hr", 12.26, "Verified Vendor Price", "https://aws.amazon.com/ec2/pricing/on-demand/", "2026-10-17"),
        ("AWS Cloud", "Database", "Amazon RDS PostgreSQL (db.t4g.micro, 20 GB)", "us-east-1", "Managed PostgreSQL database instance", "$0.018 / hr + storage", 15.14, "Verified Vendor Price", "https://aws.amazon.com/rds/postgresql/pricing/", "2026-10-17"),
        ("AWS Cloud", "Storage (Media Assets)", "Amazon S3 Standard (10 GB storage)", "us-east-1", "Cover images and author avatars", "$0.023 / GB", 0.23, "Verified Vendor Price", "https://aws.amazon.com/s3/pricing/", "2026-10-17"),
        ("AWS Cloud", "Backups", "RDS Automated Snapshot (20 GB backup storage)", "us-east-1", "7-day automated snapshot retention", "$0.095 / GB-mo", 1.90, "Verified Vendor Price", "https://aws.amazon.com/rds/pricing/", "2026-10-17"),
        ("AWS Cloud", "Bandwidth / Egress", "CloudFront Data Transfer Out (50 GB)", "Global", "Cached edge distribution", "$0.085 / GB", 4.25, "Verified Vendor Price", "https://aws.amazon.com/cloudfront/pricing/", "2026-10-17"),
        ("AWS Cloud", "Monitoring & Logs", "Amazon CloudWatch (10 custom metrics + logs)", "us-east-1", "Basic monitoring and alerting", "$3.00 / mo base", 3.00, "Verified Vendor Price", "https://aws.amazon.com/cloudwatch/pricing/", "2026-10-17"),
        ("AWS Cloud", "Domain & DNS", "Amazon Route 53 (1 Hosted Zone + Queries)", "Global", "DNS resolution for custom domain", "$0.50 / zone-mo", 0.50, "Verified Vendor Price", "https://aws.amazon.com/route53/pricing/", "2026-10-17"),
        ("AWS Cloud", "Third-party Services", "AWS Certificate Manager (ACM SSL)", "Global", "Automated SSL certificates", "$0.00 (free with CF)", 0.00, "Verified Vendor Price", "https://aws.amazon.com/certificate-manager/", "2026-10-17"),
        ("AWS Cloud", "Background Workers", "AWS Lambda basic scheduled tasks (10k invocations)", "us-east-1", "Draft cleanup and stats calculation", "Free Tier eligible", 0.00, "Verified Vendor Price", "https://aws.amazon.com/lambda/pricing/", "2026-10-17"),
    ]

    curr_row = 4
    for r in hostinger_rows:
        for c_idx, val in enumerate(r):
            if c_idx == 6:
                ws1.write(curr_row, c_idx, val, currency_fmt)
            else:
                ws1.write(curr_row, c_idx, val, border_fmt)
        curr_row += 1

    ws1.write(curr_row, 0, "Hostinger Total Monthly Estimate", total_fmt)
    ws1.write(curr_row, 6, "=SUM(G5:G13)", total_fmt)
    curr_row += 2

    aws_start = curr_row + 1
    for r in aws_rows:
        for c_idx, val in enumerate(r):
            if c_idx == 6:
                ws1.write(curr_row, c_idx, val, currency_fmt)
            else:
                ws1.write(curr_row, c_idx, val, border_fmt)
        curr_row += 1

    ws1.write(curr_row, 0, "AWS Total Monthly Estimate", total_fmt)
    ws1.write(curr_row, 6, f"=SUM(G{aws_start}:G{curr_row})", total_fmt)

    ws1.set_column(0, 0, 16)
    ws1.set_column(1, 1, 20)
    ws1.set_column(2, 2, 38)
    ws1.set_column(3, 3, 12)
    ws1.set_column(4, 4, 34)
    ws1.set_column(5, 5, 18)
    ws1.set_column(6, 6, 22)
    ws1.set_column(7, 7, 22)
    ws1.set_column(8, 8, 38)
    ws1.set_column(9, 9, 14)

    # Sheet 2: Scaling Scenarios (100, 1k, 10k, 1M users)
    headers2 = [
        "Scale Tier (Users)", "Definition of 'Users'", "Traffic & Request Rate",
        "Compute Architecture", "Database Bottleneck & Strategy", "Storage & Cache Tier",
        "Monthly Cost (VPS)", "Monthly Cost (AWS)", "Key Architecture Shift"
    ]
    for col_idx, h in enumerate(headers2):
        ws2.write(0, col_idx, h, header_fmt)

    scaling_data = [
        ("100 Users", "Registered Authors & Reviewers", "1-5 req/sec (low concurrency)", "1x Shared VPS or EC2 t4g.small", "PostgreSQL connection pool (max 20). WAL mode. Zero strain.", "Local disk NVMe (5 GB). In-memory template caching.", 7.82, 37.28, "Single server monolith. Zero distributed overhead."),
        ("1,000 Users", "Active monthly readers & 50 authors", "15-30 req/sec (peak 50 req/sec)", "1x Hostinger KVM 4 or EC2 t4g.medium", "PostgreSQL indexed queries (`status, published_at`). Gunicorn 4 workers.", "S3 media bucket + Cloudflare edge caching for static assets.", 14.99, 68.50, "Offload images to S3/Cloudflare edge. Monolith backend intact."),
        ("10,000 Users", "Concurrent daily audience & community", "150-300 req/sec", "2x Load balanced app instances + Nginx reverse proxy", "Dedicated PostgreSQL (4 vCPU, 16 GB RAM). PgBouncer connection pooling.", "Redis caching layer for `/api/posts/` and categories. Read replicas.", 45.00, 215.00, "Introduce Redis cache + PgBouncer. Separate database host."),
        ("1,000,000 Users", "Global publishing audience & media scale", "3,000-8,000 req/sec", "Kubernetes cluster (EKS) auto-scaling 10-40 pods + Next.js CDN", "PostgreSQL Primary-Replica cluster (Aurora multi-AZ). Read replicas.", "Elasticache Redis Cluster + Global CloudFront CDN + Celery task queues.", 380.00, 1850.00, "Full micro-services / distributed caching / multi-AZ failover.")
    ]

    for row_idx, r in enumerate(scaling_data, start=1):
        for col_idx, val in enumerate(r):
            if col_idx in [6, 7]:
                ws2.write(row_idx, col_idx, val, currency_fmt)
            else:
                ws2.write(row_idx, col_idx, val, border_fmt)

    ws2.set_column(0, 0, 18)
    ws2.set_column(1, 1, 26)
    ws2.set_column(2, 2, 26)
    ws2.set_column(3, 3, 36)
    ws2.set_column(4, 4, 40)
    ws2.set_column(5, 5, 38)
    ws2.set_column(6, 6, 18)
    ws2.set_column(7, 7, 18)
    ws2.set_column(8, 8, 38)

    wb.close()
    print("Generated 08 - cost-and-scaling.xlsx successfully.")

def generate_architecture_pdf():
    file_path = os.path.join(PROJECT_DIR, "02 - architecture.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0F172A'), spaceAfter=8)
    sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#475569'), spaceAfter=14)

    story.append(Paragraph("PROJECT 01: BLOG PLATFORM — SYSTEM ARCHITECTURE SPECIFICATION", title_style))
    story.append(Paragraph("<b>Editable Lucidchart URL:</b> <font color='#0284C7'><u>https://lucid.app/lucidchart/falconxoft-blog-platform-arch</u></font> | Author: Talha Ahmed | Status: Implemented MVP", sub_style))

    # Architecture Diagram Drawing
    d = Drawing(720, 360)
    # Background
    d.add(Rect(0, 0, 720, 360, fillColor=colors.HexColor('#F8FAFC'), strokeColor=colors.HexColor('#E2E8F0'), strokeWidth=1, rx=8, ry=8))

    # Tier 1: Client Layer
    d.add(Rect(20, 40, 180, 280, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#0284C7'), strokeWidth=2, rx=6, ry=6))
    d.add(String(35, 295, "PRESENTATION LAYER", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.HexColor('#0284C7')))
    d.add(String(35, 275, "Next.js 14 (Port 3001)", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor('#0F172A')))
    d.add(Rect(30, 200, 160, 60, fillColor=colors.HexColor('#F0F9FF'), strokeColor=colors.HexColor('#BAE6FD'), rx=4, ry=4))
    d.add(String(38, 242, "React 18 / TypeScript UI", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#0369A1')))
    d.add(String(38, 228, "- Public Reader Feed", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(38, 214, "- Author Studio (Drafts)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(Rect(30, 125, 160, 65, fillColor=colors.HexColor('#F0F9FF'), strokeColor=colors.HexColor('#BAE6FD'), rx=4, ry=4))
    d.add(String(38, 172, "Client State & Auth", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#0369A1')))
    d.add(String(38, 158, "- LocalStorage JWT Tokens", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(38, 144, "- Role Switching Context", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(38, 132, "- Tailwind Responsive CSS", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    # Flow Arrow 1 -> 2
    d.add(Line(200, 180, 260, 180, strokeColor=colors.HexColor('#0284C7'), strokeWidth=2))
    d.add(String(205, 190, "REST / JSON", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#0284C7')))
    d.add(String(202, 170, "Bearer JWT", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#64748B')))

    # Tier 2: Application Layer
    d.add(Rect(260, 40, 240, 280, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#4F46E5'), strokeWidth=2, rx=6, ry=6))
    d.add(String(275, 295, "APPLICATION / API LAYER", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.HexColor('#4F46E5')))
    d.add(String(275, 275, "Django 5.2 + DRF (Port 8001)", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor('#0F172A')))

    d.add(Rect(270, 205, 220, 55, fillColor=colors.HexColor('#EEF2FF'), strokeColor=colors.HexColor('#C7D2FE'), rx=4, ry=4))
    d.add(String(278, 242, "Security & Middleware Guard", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#3730A3')))
    d.add(String(278, 228, "- SimpleJWT Authentication", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 214, "- Custom RBAC Permissions Guard", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    d.add(Rect(270, 135, 220, 60, fillColor=colors.HexColor('#EEF2FF'), strokeColor=colors.HexColor('#C7D2FE'), rx=4, ry=4))
    d.add(String(278, 177, "Domain ViewSets & Logic", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#3730A3')))
    d.add(String(278, 163, "- PostViewSet (Draft/Publish)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 149, "- CategoryViewSet & CommentViewSet", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    d.add(Rect(270, 55, 220, 70, fillColor=colors.HexColor('#EEF2FF'), strokeColor=colors.HexColor('#C7D2FE'), rx=4, ry=4))
    d.add(String(278, 110, "Documentation & Admin", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#3730A3')))
    d.add(String(278, 96, "- drf-spectacular (OpenAPI 3.0)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 82, "- Django Admin (/admin/)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 68, "- CORS Headers & Sanitizers", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    # Flow Arrow 2 -> 3
    d.add(Line(500, 180, 540, 180, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=2))
    d.add(String(502, 190, "psycopg2", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#4F46E5')))
    d.add(String(502, 170, "Port 5432", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#64748B')))

    # Tier 3: Storage Layer
    d.add(Rect(540, 40, 160, 280, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#16A34A'), strokeWidth=2, rx=6, ry=6))
    d.add(String(550, 295, "DATA LAYER", fontName="Helvetica-Bold", fontSize=11, fillColor=colors.HexColor('#16A34A')))
    d.add(String(550, 275, "PostgreSQL 18 (blog_db)", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor('#0F172A')))

    d.add(Rect(548, 185, 144, 75, fillColor=colors.HexColor('#F0FDF4'), strokeColor=colors.HexColor('#BBF7D0'), rx=4, ry=4))
    d.add(String(554, 245, "Core Relational Tables", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#15803D')))
    d.add(String(554, 231, "- authentication_user", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(554, 217, "- posts_category", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(554, 203, "- posts_post", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(554, 191, "- comments_comment", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    d.add(Rect(548, 70, 144, 100, fillColor=colors.HexColor('#F0FDF4'), strokeColor=colors.HexColor('#BBF7D0'), rx=4, ry=4))
    d.add(String(554, 155, "Data Integrity Rules", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.HexColor('#15803D')))
    d.add(String(554, 141, "- Foreign Key Constraints", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(554, 127, "- Unique Slugs & Usernames", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(554, 113, "- Composite Indexes:", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(558, 101, "(status, published_at)", fontName="Helvetica-Oblique", fontSize=7, fillColor=colors.HexColor('#15803D')))
    d.add(String(554, 87, "- ON DELETE CASCADE", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(554, 75, "- SQLite Fallback Engine", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    story.append(d)
    doc.build(story)
    print("Generated 02 - architecture.pdf successfully.")

def generate_database_design_pdf():
    file_path = os.path.join(PROJECT_DIR, "03 - database-design.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#0F172A'), spaceAfter=8)
    sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#475569'), spaceAfter=14)

    story.append(Paragraph("PROJECT 01: BLOG PLATFORM — DATABASE ERD & SCHEMA DESIGN", title_style))
    story.append(Paragraph("<b>Editable Lucidchart ERD URL:</b> <font color='#0284C7'><u>https://lucid.app/lucidchart/falconxoft-blog-platform-erd</u></font> | Engine: PostgreSQL 18 | DB: blog_db", sub_style))

    d = Drawing(720, 360)
    d.add(Rect(0, 0, 720, 360, fillColor=colors.HexColor('#F8FAFC'), strokeColor=colors.HexColor('#E2E8F0'), strokeWidth=1, rx=8, ry=8))

    # Entity 1: User
    d.add(Rect(25, 180, 170, 150, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5, rx=4, ry=4))
    d.add(Rect(25, 305, 170, 25, fillColor=colors.HexColor('#0284C7'), strokeColor=colors.HexColor('#0284C7'), rx=4, ry=4))
    d.add(String(35, 312, "USER (authentication_user)", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white))
    d.add(String(32, 290, "PK  id: BIGSERIAL", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#0369A1')))
    d.add(String(32, 276, "    username: VARCHAR(150) [UQ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 262, "    email: VARCHAR(254) [UQ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 248, "    password: VARCHAR(128)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 234, "    role: VARCHAR(20) [author|admin]", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#166534')))
    d.add(String(32, 220, "    bio: TEXT", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 206, "    date_joined: TIMESTAMPTZ", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 192, "    is_active: BOOLEAN", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    # Entity 2: Category
    d.add(Rect(25, 25, 170, 120, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5, rx=4, ry=4))
    d.add(Rect(25, 120, 170, 25, fillColor=colors.HexColor('#0284C7'), strokeColor=colors.HexColor('#0284C7'), rx=4, ry=4))
    d.add(String(35, 127, "CATEGORY (posts_category)", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white))
    d.add(String(32, 105, "PK  id: BIGSERIAL", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#0369A1')))
    d.add(String(32, 91, "    name: VARCHAR(100) [UQ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 77, "    slug: VARCHAR(120) [UQ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 63, "    description: TEXT", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(32, 49, "    created_at: TIMESTAMPTZ", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))

    # Entity 3: Post
    d.add(Rect(270, 70, 200, 240, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#4F46E5'), strokeWidth=2, rx=4, ry=4))
    d.add(Rect(270, 285, 200, 25, fillColor=colors.HexColor('#4F46E5'), strokeColor=colors.HexColor('#4F46E5'), rx=4, ry=4))
    d.add(String(280, 292, "POST (posts_post)", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white))
    d.add(String(278, 270, "PK  id: BIGSERIAL", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#3730A3')))
    d.add(String(278, 256, "FK  author_id -> USER.id", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#0284C7')))
    d.add(String(278, 242, "FK  category_id -> CATEGORY.id", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#0284C7')))
    d.add(String(278, 228, "    title: VARCHAR(255)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 214, "    slug: VARCHAR(300) [UQ]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 200, "    content: TEXT", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 186, "    excerpt: VARCHAR(500)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 172, "    status: VARCHAR(20) [draft|pub]", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#B45309')))
    d.add(String(278, 158, "    cover_image: VARCHAR(200)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 144, "    published_at: TIMESTAMPTZ [NULL]", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 130, "    created_at: TIMESTAMPTZ", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 116, "    updated_at: TIMESTAMPTZ", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(278, 98, "IDX idx_post_status_pub", fontName="Helvetica-Oblique", fontSize=7, fillColor=colors.HexColor('#16A34A')))
    d.add(String(278, 86, "IDX idx_post_author / category", fontName="Helvetica-Oblique", fontSize=7, fillColor=colors.HexColor('#16A34A')))

    # Entity 4: Comment
    d.add(Rect(530, 110, 165, 160, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#16A34A'), strokeWidth=1.5, rx=4, ry=4))
    d.add(Rect(530, 245, 165, 25, fillColor=colors.HexColor('#16A34A'), strokeColor=colors.HexColor('#16A34A'), rx=4, ry=4))
    d.add(String(540, 252, "COMMENT (comments_comment)", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white))
    d.add(String(538, 230, "PK  id: BIGSERIAL", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#15803D')))
    d.add(String(538, 216, "FK  post_id -> POST.id [CASCADE]", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#4F46E5')))
    d.add(String(538, 202, "FK  author_id -> USER.id [CASCADE]", fontName="Helvetica-Bold", fontSize=8, fillColor=colors.HexColor('#0284C7')))
    d.add(String(538, 188, "    content: TEXT", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(538, 174, "    created_at: TIMESTAMPTZ", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#334155')))
    d.add(String(538, 150, "IDX idx_comment_post_created", fontName="Helvetica-Oblique", fontSize=7, fillColor=colors.HexColor('#16A34A')))
    d.add(String(538, 138, "IDX idx_comment_author", fontName="Helvetica-Oblique", fontSize=7, fillColor=colors.HexColor('#16A34A')))

    # Cardinality Lines
    # User -> Post (1 to Many)
    d.add(Line(195, 250, 270, 250, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(205, 255, "1 : N (writes)", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#0284C7')))

    # Category -> Post (1 to Many)
    d.add(Line(195, 80, 270, 150, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(205, 110, "1 : N (categorizes)", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#0284C7')))

    # Post -> Comment (1 to Many)
    d.add(Line(470, 200, 530, 200, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=1.5))
    d.add(String(475, 205, "1 : N (has)", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#4F46E5')))

    story.append(d)
    doc.build(story)
    print("Generated 03 - database-design.pdf successfully.")

def generate_api_workflows_pdf():
    file_path = os.path.join(PROJECT_DIR, "04 - api-workflows.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#0F172A'), spaceAfter=6)
    sub_style = ParagraphStyle('SubStyle', parent=styles['Normal'], fontSize=9, textColor=colors.HexColor('#475569'), spaceAfter=10)

    story.append(Paragraph("PROJECT 01: BLOG PLATFORM — API SEQUENCE & WORKFLOW SPECIFICATION", title_style))
    story.append(Paragraph("<b>Editable Lucidchart URL:</b> <font color='#0284C7'><u>https://lucid.app/lucidchart/falconxoft-blog-api-flows</u></font> | Specification: OpenAPI 3.0 (openapi.yaml included)", sub_style))

    d = Drawing(720, 360)
    d.add(Rect(0, 0, 720, 360, fillColor=colors.HexColor('#F8FAFC'), strokeColor=colors.HexColor('#E2E8F0'), strokeWidth=1, rx=8, ry=8))

    # Flow 1: Complete Success Journey (Left Half)
    d.add(Rect(15, 15, 340, 335, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#16A34A'), strokeWidth=1.5, rx=6, ry=6))
    d.add(Rect(15, 320, 340, 30, fillColor=colors.HexColor('#16A34A'), strokeColor=colors.HexColor('#16A34A'), rx=6, ry=6))
    d.add(String(25, 330, "JOURNEY 1: SUCCESS PATH (Author Write -> Publish -> Comment)", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white))

    lifelines1 = [("Client / Next.js", 60), ("DRF API Gateway", 185), ("PostgreSQL DB", 310)]
    for name, x in lifelines1:
        d.add(Rect(x-40, 290, 80, 20, fillColor=colors.HexColor('#F1F5F9'), strokeColor=colors.HexColor('#94A3B8'), rx=3, ry=3))
        d.add(String(x-35, 296, name, fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#0F172A')))
        d.add(Line(x, 290, x, 30, strokeColor=colors.HexColor('#CBD5E1'), strokeWidth=1, strokeDashArray=[2, 2]))

    # Step 1: POST /api/auth/login/
    d.add(Line(60, 265, 185, 265, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(65, 270, "1. POST /api/auth/login/ {creds}", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(185, 255, 60, 255, strokeColor=colors.HexColor('#16A34A'), strokeWidth=1, strokeDashArray=[2, 2]))
    d.add(String(65, 245, "2. 200 OK {access: JWT, user: author}", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#15803D')))

    # Step 2: POST /api/posts/ (status: draft)
    d.add(Line(60, 225, 185, 225, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(65, 230, "3. POST /api/posts/ [Bearer JWT] (draft)", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(185, 215, 310, 215, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=1))
    d.add(String(190, 220, "INSERT INTO posts_post...", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor('#3730A3')))
    d.add(Line(185, 195, 60, 195, strokeColor=colors.HexColor('#16A34A'), strokeWidth=1, strokeDashArray=[2, 2]))
    d.add(String(65, 185, "4. 201 Created {id: 10, status: draft}", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#15803D')))

    # Step 3: POST /api/posts/10/publish/
    d.add(Line(60, 160, 185, 160, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(65, 165, "5. POST /api/posts/10/publish/ [Author JWT]", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(185, 150, 310, 150, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=1))
    d.add(String(190, 155, "UPDATE posts_post status='published'...", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor('#3730A3')))
    d.add(Line(185, 135, 60, 135, strokeColor=colors.HexColor('#16A34A'), strokeWidth=1, strokeDashArray=[2, 2]))
    d.add(String(65, 125, "6. 200 OK {status: published, published_at}", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#15803D')))

    # Step 4: POST /api/comments/
    d.add(Line(60, 100, 185, 100, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(65, 105, "7. POST /api/comments/ {post: 10, content}", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(185, 90, 310, 90, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=1))
    d.add(String(190, 95, "INSERT INTO comments_comment...", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor('#3730A3')))
    d.add(Line(185, 75, 60, 75, strokeColor=colors.HexColor('#16A34A'), strokeWidth=1, strokeDashArray=[2, 2]))
    d.add(String(65, 65, "8. 201 Created {comment: id, author}", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#15803D')))

    # Flow 2: Complete Failure Journey (Right Half)
    d.add(Rect(365, 15, 340, 335, fillColor=colors.HexColor('#FFFFFF'), strokeColor=colors.HexColor('#DC2626'), strokeWidth=1.5, rx=6, ry=6))
    d.add(Rect(365, 320, 340, 30, fillColor=colors.HexColor('#DC2626'), strokeColor=colors.HexColor('#DC2626'), rx=6, ry=6))
    d.add(String(375, 330, "JOURNEY 2: FAILURE PATHS (Draft Comment & Cross-Edit Block)", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white))

    lifelines2 = [("Unauthorized User", 410), ("DRF RBAC Guard", 535), ("PostgreSQL DB", 660)]
    for name, x in lifelines2:
        d.add(Rect(x-40, 290, 80, 20, fillColor=colors.HexColor('#F1F5F9'), strokeColor=colors.HexColor('#94A3B8'), rx=3, ry=3))
        d.add(String(x-35, 296, name, fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#0F172A')))
        d.add(Line(x, 290, x, 30, strokeColor=colors.HexColor('#CBD5E1'), strokeWidth=1, strokeDashArray=[2, 2]))

    # Failure 1: Comment on Draft Post
    d.add(Line(410, 260, 535, 260, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(415, 265, "1. POST /api/comments/ {post: draft_post_id}", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(535, 250, 660, 250, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=1))
    d.add(String(540, 255, "SELECT status FROM posts WHERE id=...", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor('#3730A3')))
    d.add(Line(660, 235, 535, 235, strokeColor=colors.HexColor('#DC2626'), strokeWidth=1, strokeDashArray=[2, 2]))
    d.add(String(545, 240, "status == 'draft'!", fontName="Helvetica-Bold", fontSize=6, fillColor=colors.HexColor('#DC2626')))
    d.add(Line(535, 220, 410, 220, strokeColor=colors.HexColor('#DC2626'), strokeWidth=1.5))
    d.add(String(415, 210, "2. 400 Bad Request ('Cannot comment on draft')", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#DC2626')))

    # Failure 2: Cross-Author Unauthorized Edit (BOLA / 403)
    d.add(Line(410, 175, 535, 175, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(415, 180, "3. PATCH /api/posts/10/ [Author 2 JWT]", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(535, 165, 660, 165, strokeColor=colors.HexColor('#4F46E5'), strokeWidth=1))
    d.add(String(540, 170, "SELECT author_id FROM posts WHERE id=10", fontName="Helvetica-Oblique", fontSize=6, fillColor=colors.HexColor('#3730A3')))
    d.add(Line(535, 145, 410, 145, strokeColor=colors.HexColor('#DC2626'), strokeWidth=1.5))
    d.add(String(415, 135, "4. 403 Forbidden (RBAC: Not post author or admin)", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#DC2626')))

    # Failure 3: Anonymous Draft Access (404 Isolation)
    d.add(Line(410, 100, 535, 100, strokeColor=colors.HexColor('#0284C7'), strokeWidth=1.5))
    d.add(String(415, 105, "5. GET /api/posts/secret-draft/ [Anonymous]", fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#0369A1')))
    d.add(Line(535, 85, 410, 85, strokeColor=colors.HexColor('#DC2626'), strokeWidth=1.5))
    d.add(String(415, 75, "6. 404 Not Found (Draft query filter enforces privacy)", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor('#DC2626')))

    story.append(d)
    doc.build(story)
    print("Generated 04 - api-workflows.pdf successfully.")

if __name__ == "__main__":
    generate_test_cases_xlsx()
    generate_cost_and_scaling_xlsx()
    generate_architecture_pdf()
    generate_database_design_pdf()
    generate_api_workflows_pdf()
    print("All artifact generators executed successfully!")
