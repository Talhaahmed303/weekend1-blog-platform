-- =============================================================================
-- FALCONXOFT INTERN EVALUATION — PROJECT 01: BLOG PLATFORM
-- Database DDL for Lucidchart ERD Import (File -> Import Data -> ERD -> PostgreSQL)
-- Candidate: Talha Ahmed | Date: October 2026
-- =============================================================================

CREATE TABLE authentication_user (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'author' CHECK (role IN ('author', 'admin')),
    bio TEXT NOT NULL DEFAULT '',
    avatar_url VARCHAR(200) NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts_post (
    id BIGSERIAL PRIMARY KEY,
    author_id BIGINT NOT NULL,
    category_id BIGINT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(300) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    excerpt VARCHAR(500) NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published')),
    cover_image TEXT NOT NULL DEFAULT '',
    published_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_post_author FOREIGN KEY (author_id) REFERENCES authentication_user(id) ON DELETE CASCADE,
    CONSTRAINT fk_post_category FOREIGN KEY (category_id) REFERENCES posts_category(id) ON DELETE SET NULL
);

CREATE TABLE comments_comment (
    id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    author_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_comment_post FOREIGN KEY (post_id) REFERENCES posts_post(id) ON DELETE CASCADE,
    CONSTRAINT fk_comment_author FOREIGN KEY (author_id) REFERENCES authentication_user(id) ON DELETE CASCADE
);

-- Strategic Query Indexes
CREATE INDEX posts_post_status_pub_idx ON posts_post (status, published_at DESC);
CREATE INDEX posts_post_author_idx ON posts_post (author_id);
CREATE INDEX posts_post_category_idx ON posts_post (category_id);
CREATE INDEX comments_comment_post_created_idx ON comments_comment (post_id, created_at);
