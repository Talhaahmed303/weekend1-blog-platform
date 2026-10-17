# FALCONXOFT WEEKEND 1 — BLOG PLATFORM MVP
## Complete Browser Testing & Viva Defense Guide (Roman Urdu & English)

**Author:** Talha Ahmed  
**Project:** 01_Blog (Multi-Author Publishing Platform)  
**Frontend URL:** `http://localhost:3001`  
**Backend API URL:** `http://127.0.0.1:8001/api/`  
**Database:** PostgreSQL 18 (`blog_db`)  

---

## 1. Task Background — Aapko Task Kya Mila Tha? (Requirements Overview)

FalconXoft Weekend 1 assessment ka pehla project tha ek **Multi-Author Publishing Platform MVP** banana.
Yeh koi aam, simple blog website nahi thi jisme sirf hardcoded cards dikh rahe hon. Requirement thi ek **production-grade full-stack architecture**:

1. **Authentication & Authorization:** JWT-based login, register, aur distinct roles (`Author` vs `Admin`).
2. **Draft vs Published Lifecycle:** Articles ka strict state machine (`draft` aur `published`). Public users sirf published articles dekh sakein. Drafts strictly private hon aur kisi unauthorized user ko API ya frontend pe nazar na aayein (404/403).
3. **Role-Based Access Control (RBAC):** Ek author kisi doosre author ka post edit ya delete na kar sake. Lekin `Admin` ke paas global moderation rights hon (woh kisi ka bhi inappropriate content delete ya edit kar sake).
4. **Categories & Search:** Real-time topic filtering aur keyword search (title, content, category mein).
5. **Community Comments:** Authenticated readers comments kar sakein, lekin drafts par commenting strictly blocked ho.
6. **Zero Docker Constraint:** Application direct local machine par run ho (Python 3.11 + Next.js 14 + PostgreSQL 18), taake interview evaluation ke waqt zero latency aur straightforward verification ho.

---

## 2. Humne Kya Aur Kaise Banaya? (Architecture & Technical Decisions)

### Tech Stack:
- **Backend:** Python 3.11 + **Django 5.2** + **Django REST Framework (DRF)**.
  - JWT Authentication: `djangorestframework-simplejwt`.
  - API Documentation: `drf-spectacular` (OpenAPI 3.0 / Swagger schema).
- **Frontend:** **Next.js 14** (App Router, React 18, TypeScript) + **Tailwind CSS**.
  - Modern dark-mode glassmorphism UI, toast notifications, responsive card grid.
  - Built-in **1-Click Demo Switcher** navbar mein lagaya hai taake bina bar bar credentials type kiye viva mein live demo diya ja sake.
- **Database:** **PostgreSQL 18** (`blog_db`) 3NF relational schema.
- **Testing:** `pytest` + `pytest-django` ke **19 automated test cases** (100% pass rate).

### Database Schema (Tables):
1. **`authentication_user`:** Custom user model jisme `role` field hai (`author` ya `admin`).
2. **`posts_category`:** Blog categories (`name`, `slug`, `description`).
3. **`posts_post`:** `title`, `slug`, `content`, `cover_image`, `status` (`draft` ya `published`), `author_id` (ForeignKey), `category_id` (ForeignKey), `created_at`, `updated_at`.
4. **`comments_comment`:** `post_id` (ForeignKey), `author_id` (ForeignKey), `content`, `created_at`.

### Security & Business Logic Handled:
- **Custom Permission `IsAuthorOrAdminOrReadOnly`:** Check karta hai ke GET requests sabke liye open hain (sirf published posts), jabke POST/PUT/DELETE sirf logged-in post owner ya global admin kar sakta hai.
- **Draft Isolation Queryset:** `get_queryset()` method mein check hota hai: agar user public/anonymous hai to sirf `status='published'` filter hoga. Agar user author hai to usey published posts ke sath sirf *apne* drafts nazar aayenge. Doosron ke drafts database level par filter out ho jate hain.
- **Draft Comment Block:** `CommentCreateView` me validation lagi hui hai: agar post ka status `draft` hai to API `400 Bad Request` throw karti hai (`"Cannot comment on draft posts"`).

---

## 3. Demo Accounts & Login Credentials (Kis Account Se Login Karein?)

Frontend navbar ke top-right pe humne **"Demo Switch"** buttons diye hue hain, aap ek click se user switch kar sakte hain. Manual login ke credentials yeh hain:

| Role | Username | Password | Purpose & Power in System |
| :--- | :--- | :--- | :--- |
| 👑 **Site Admin** | `admin` | `Admin@123` | **Global Moderation:** Har author ka post edit/delete kar sakta hai, koi bhi comment delete kar sakta hai. |
| ✍️ **Author 1 (Talha)** | `talha_author` | `Author@123` | **Primary Author:** Apne articles create, edit, publish/unpublish kar sakta hai. Apne private drafts dekh sakta hai. |
| ✍️ **Author 2 (Sara)** | `sara_writer` | `Author@123` | **Peer Author:** Iska account prove karta hai ke Talha Sara ke posts edit nahi kar sakta aur na uske drafts dekh sakta hai. |
| 👀 **Public Reader** | *(Logout/Guest)* | N/A | **Unauthenticated Guest:** Sirf published articles padh sakta hai aur search kar sakta hai. Write ya comment ke liye login zaroori hai. |

---

## 4. Browser Testing Walkthrough — Step-by-Step Test Kaise Karein?

Dono servers already terminal mein chal rahe hain:
- **Backend API:** `http://127.0.0.1:8001`
- **Frontend App:** `http://localhost:3001`

Apne browser mein **`http://localhost:3001`** open karein aur ye steps follow karein:

### Step 1: Public Feed & Search Verification (Bina Login Ke)
1. Browser me `http://localhost:3001` kholein.
2. Check karein ke upar top bar me **"👀 Public Reader"** active hai.
3. Feed me published articles nazar aayenge (jaise *"Mastering DRF and Next.js"* aur *"Hostinger VPS vs AWS"*).
4. **Test Search Bar:** Search box me `DRF` ya `AWS` type karein. Instant filter hoga.
5. **Test Category Filter:** Category buttons ("Engineering Excellence", "DevOps & Cloud") par click karein. Cards usi category ke filter honge.
6. Notice karein ke yahan koi bhi `[DRAFT]` post nazar nahi aa raha — drafts public ke liye 100% hidden hain!

### Step 2: Login as Author 1 (Talha) & Test "My Studio"
1. Top bar me **"✍️ Author 1 (Talha)"** button par click karein (ya Login button daba kar `talha_author` / `Author@123` enter karein).
2. Screen ke top-right pe toast message aayega: `Switched account to @talha_author (AUTHOR)`.
3. Ab feed ke upar do tabs nazar aayenge: **"Public Feed"** aur **"My Studio (Author)"**.
4. **"My Studio" tab par click karein:**
   - Yahan Talha ke apne posts dikhenge, including uska private draft: `[DRAFT] Technical Notes on Raft and Paxos Consensus Algorithms`.
   - Notice karein ke draft ke upar yellow badge laga hua hai: `DRAFT`.

### Step 3: Publish / Unpublish Lifecycle Test (1-Click)
1. Us draft post ke card par **"Publish Now"** button hoga. Us par click karein!
2. Instant notification aayega: `Post Published Live!`. Post ka badge green ho jayega: `PUBLISHED`.
3. Ab "Public Feed" tab me jayein — ye post ab sabke liye live ho chuka hai!
4. Phir se "My Studio" me ja kar **"Unpublish"** click karein. Post wapas private draft ban jayega aur public feed se gayab ho jayega.

### Step 4: Create a New Post
1. Top right me **"+ Write Post"** button par click karein.
2. Modal open hoga. Form bharein:
   - **Title:** `Building Scalable APIs with Django and Next.js`
   - **Category:** Select `System Design`
   - **Status:** Select `Draft` ya `Published`
   - **Content:** Markdown content likhein.
3. **"Save Article"** par click karein. Post instantly create ho jayega!

### Step 5: Test Multi-Author Security & Ownership Isolation (Crucial for Viva!)
1. Ab top bar me **"✍️ Author 2 (Sara)"** button par click karein.
2. Sara ka profile load ho jayega.
3. Sara ke "My Studio" me jayein. Yahan Sara ka apna private draft dikhega (`[DRAFT] Unreleased Cloud Architecture Whitepaper`). Talha ka draft yahan bilkul nazar nahi aayega!
4. Public feed me ja kar Talha ke post par click karein. Notice karein ke Sara ke pas Talha ke post ko **"Edit"** ya **"Delete"** karne ka button nahi hai! System strictly 403 Forbidden enforce karta hai.

### Step 6: Test Comments System
1. Kisi bhi published post ke card par click karein (modal ya detail view khulega).
2. Bottom me comments section hoga.
3. Input box me likhein: `"Great architectural insights! Very helpful."` aur **"Post Comment"** dabayein.
4. Comment foran list me add ho jayega author avatar aur timestamp ke sath!

### Step 7: Test Admin Moderation (Superuser Powers)
1. Top bar me **"👑 Admin"** button par click karein.
2. Admin ke pas violet crown badge aayega.
3. Ab kisi bhi post ya comment par jayein. Admin ke pas har user ke post par **"Edit"** aur **"Delete"** ka option hoga.
4. Yeh prove karta hai ke system me server-side Role-Based Access Control (RBAC) 100% active hai.

---

## 5. Viva / Interview Defense Guide (Examiner Questions & Model Answers)

Jab examiner aapse Blog Platform ke baare me sawalat poochega, to aapko ye confident aur technically precise answers dene hain:

### Q1: "Aapne authentication aur session management kaise handle ki hai?"
> **Answer:**  
> "Maine Django REST Framework ke sath `SimpleJWT` use kiya hai. Login par server HMAC-SHA256 se sign kiya hua short-lived Access Token aur long-lived Refresh Token issue karta hai. Frontend (Next.js) token ko HTTP Authorization header me `Bearer <token>` ke sath har request me bhejta hai. Server stateless rehta hai, jisse horizontal scaling aasan hoti hai."

### Q2: "Drafts ki privacy kaise ensure ki? Kya frontend se sirf hide kiya hai ya backend par bhi secure hai?"
> **Answer:**  
> "Sirf frontend hide karna security nahi hoti. Maine database query level par isolation ki hai. Django DRF ke `PostViewSet` ke `get_queryset()` method me custom filtering logic hai:  
> Agar request unauthenticated hai, to query me `status='published'` hard-filter hota hai.  
> Agar logged-in user author hai, to `Q(status='published') | Q(author=request.user)` filter hota hai. Kisi doosre author ka draft database se fetch hi nahi hota, is liye API se koi data leak possible nahi hai."

### Q3: "RBAC (Role Based Access Control) kaise enforce kiya hai?"
> **Answer:**  
> "Maine DRF me custom permission class banayi hai: `IsAuthorOrAdminOrReadOnly`.  
> SAFE_METHODS (GET, HEAD, OPTIONS) sab ke liye allow hain. Lekin PUT, PATCH, aur DELETE ke liye `has_object_permission` check karta hai: `obj.author == request.user or request.user.role == 'admin'`. Agar condition match na ho to DRF automatic HTTP 403 Forbidden return karta hai."

### Q4: "Aapne automated testing kaise ki hai aur kya kya test kiya hai?"
> **Answer:**  
> "Maine `pytest` aur `pytest-django` use karke **19 automated integration tests** likhe hain jo 100% pass hote hain:
> - User registration aur JWT token generation.
> - Author post creation (Draft aur Published).
> - Permissions testing: Ek author doosre ke post ko update nahi kar sakta (assert HTTP 403).
> - Admin override: Admin kisi ka bhi post update/delete kar sakta hai (assert HTTP 200/204).
> - Draft isolation: Anonymous user draft ID access kare to HTTP 404 milta hai.
> - Draft comment block: Draft post par comment submit karne par HTTP 400 milta hai."

### Q5: "Architecture diagrams aur deliverables kahan hain?"
> **Answer:**  
> "Project folder me PDF format me ReportLab se generate kiye huye vector diagrams mojood hain:
> - `02 - architecture.pdf`: 3-Tier C4 container architecture diagram.
> - `03 - database-design.pdf`: Relational 3NF ERD diagram with tables & keys.
> - `04 - api-workflows.pdf`: Sequence diagrams for JWT auth, post lifecycle, & commenting.
> - `openapi.yaml`: Full OpenAPI 3.0 specification for all endpoints."

---

## 6. Summary Checklist for Viva

- [x] Backend running on `http://127.0.0.1:8001`
- [x] Frontend running on `http://localhost:3001`
- [x] 4 Seed users active (`admin`, `talha_author`, `sara_writer`, Guest)
- [x] 1-Click demo account switcher tested in navbar
- [x] 19/19 Pytest tests passing
- [x] All 10 documentation deliverables present in `01_Blog/`
