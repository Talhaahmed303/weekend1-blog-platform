# LUCIDCHART DIAGRAM IMPORT & EXPORT GUIDE (STEP-BY-STEP)

**Author:** Talha Ahmed  
**Project:** `01_Blog` — Multi-Author Publishing Platform  
**Evaluation:** FalconXoft 15-Day Intern Performance Evaluation — Weekend 1  

---

## 📌 Khulasa (Overview)
FalconXoft evaluation sheet Section 3 mein explicitly likha hai ke:
- `02 - architecture.pdf`
- `03 - database-design.pdf`
- `04 - api-workflows.pdf`

Ye teeno files **Lucidchart se export hui PDF** honi chahiye aur inke andar **Editable Lucidchart Link** hona zaroori hai.

Aapko Lucidchart mein ghanton manually boxes drag karne ki zaroorat nahi hai! Humne 3 ready-made import files generate kar di hain jo **1 click mein Lucidchart mein import ho jati hain**:
1. `01_ARCHITECTURE_DIAGRAM.mermaid` (Complete 3-Tier System Architecture)
2. `02_DATABASE_ERD.sql` & `02_DATABASE_ERD.mermaid` (Database ERD with PK/FK/Indexes)
3. `03_API_WORKFLOWS_SEQUENCE.mermaid` (API Success & Failure Sequence Workflows)

---

## 🚀 Step 1: Diagram 1 — System Architecture (`02 - architecture.pdf`)

1. Browser mein **[Lucidchart (lucid.app)](https://lucid.app)** open karein aur login karein (Free account is completely fine).
2. **`+ New` -> `Lucidchart Document` -> `Blank Document`** pe click karein.
3. Left toolbar ya top menu se:
   - **`Insert`** menu pe click karein -> **`Mermaid`** select karein.
   - (Agar menu mein na dikhe toh left panel pe shapes mein search karein `Mermaid`).
4. Ek code box open hoga. Is file ka poora text copy karke paste karein:
   - File Path: [`01_Blog/lucidchart_diagrams/01_ARCHITECTURE_DIAGRAM.mermaid`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/01_ARCHITECTURE_DIAGRAM.mermaid)
5. **`Insert Diagram`** pe click karein.
   - Lucidchart turant poora architecture diagram (Next.js 14, Django DRF, PostgreSQL 18, Protocols, Ports, and Layers) render kar dega!
6. **Share Link lena:**
   - Top right corner pe orange **`Share`** button pe click karein.
   - **"Shareable link"** enable karein -> Permission: **"Anyone with link can edit"** ya **"view/comment"**.
   - **Copy Link** karein (yeh aapka actual Editable Lucidchart Link hai).
7. **Export as PDF:**
   - Top menu: **`File` -> `Export` -> `PDF`**.
   - Page scale: **"Fit to page"** select karein aur **`Download`** pe click karein.
   - Download hui PDF ko `d:\Weekend1_Talha Ahmed\01_Blog\02 - architecture.pdf` ke naam se replace/save kar dein.

---

## 🚀 Step 2: Diagram 2 — Database ERD (`03 - database-design.pdf`)

Lucidchart mein ERD banane ka official tareeqa:

### Option A: Direct SQL Import (Recommended by Lucidchart):
1. Lucidchart mein New Blank Document banayein.
2. Top menu: **`File` -> `Import Data` -> `Entity Relationship (ERD)`**.
3. Database type mein **`PostgreSQL`** choose karein.
4. Upload file dialog mein yeh file choose karein ya text paste karein:
   - File Path: [`01_Blog/lucidchart_diagrams/02_DATABASE_ERD.sql`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/02_DATABASE_ERD.sql)
5. **`Import`** pe click karein.
   - Lucidchart charon tables (`authentication_user`, `posts_category`, `posts_post`, `comments_comment`) with Primary Keys, Foreign Keys, aur 1:N cardinality khud draw kar dega!
6. Canvas pe tables ko clean layout mein align karein.

### Option B: Mermaid Import:
1. `Insert` -> `Mermaid` -> File [`01_Blog/lucidchart_diagrams/02_DATABASE_ERD.mermaid`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/02_DATABASE_ERD.mermaid) paste karein aur Insert karein.

7. **Share Link copy karein** (`Share` button -> Copy Link).
8. **Export as PDF:** `File` -> `Export` -> `PDF` -> Download karke `d:\Weekend1_Talha Ahmed\01_Blog\03 - database-design.pdf` save karein.

---

## 🚀 Step 3: Diagram 3 — API Sequence Workflows (`04 - api-workflows.pdf`)

1. Lucidchart mein New Blank Document banayein.
2. Top menu: **`Insert` -> `Mermaid`**.
3. Is file ka text copy karke paste karein:
   - File Path: [`01_Blog/lucidchart_diagrams/03_API_WORKFLOWS_SEQUENCE.mermaid`](file:///d:/Weekend1_Talha%20Ahmed/01_Blog/lucidchart_diagrams/03_API_WORKFLOWS_SEQUENCE.mermaid)
4. **`Insert Diagram`** pe click karein.
   - Lucidchart Success Path (Login -> Create Draft -> Publish -> Comment) aur 3 Failure Paths (Draft Comment rejection 400, Cross-Author edit 403, Anonymous draft 404) auto-generate kar dega!
5. **Share Link copy karein** (`Share` button -> Copy Link).
6. **Export as PDF:** `File` -> `Export` -> `PDF` -> Download karke `d:\Weekend1_Talha Ahmed\01_Blog\04 - api-workflows.pdf` save karein.

---

## 📋 Step 4: Real Links Update Karna

Jab aapke paas teeno links aa jayein:
1. Architecture Link: `https://lucid.app/lucidchart/...`
2. ERD Link: `https://lucid.app/lucidchart/...`
3. API Flow Link: `https://lucid.app/lucidchart/...`

Aap mujhe yeh links chat mein bhej dein, main foran:
- `10 - submission-index.md`
- `01 - README.md`
- `09 - sources-and-disclosure.md`
- Aur PDF headers mein in links ko update kar dunga!
