-- =============================================================================
-- FALCONXOFT INTERN EVALUATION — PROJECT 01: BLOG PLATFORM
-- Database Engine: PostgreSQL 18
-- Target Database: blog_db
-- Author: Talha Ahmed
-- =============================================================================

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Authentication User Table (Extended Custom User)
CREATE TABLE IF NOT EXISTS authentication_user (
    id BIGSERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMPTZ NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(20) NOT NULL DEFAULT 'author' CHECK (role IN ('author', 'admin')),
    bio TEXT NOT NULL DEFAULT '',
    avatar_url VARCHAR(200) NOT NULL DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_user_username ON authentication_user (username);
CREATE INDEX IF NOT EXISTS idx_user_role ON authentication_user (role);

-- 2. Blog Categories Table
CREATE TABLE IF NOT EXISTS posts_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_category_slug ON posts_category (slug);

-- 3. Blog Posts Table (Draft / Publish Lifecycle)
CREATE TABLE IF NOT EXISTS posts_post (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(300) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    excerpt VARCHAR(500) NOT NULL DEFAULT '',
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published')),
    cover_image TEXT NOT NULL DEFAULT '',
    published_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id BIGINT NOT NULL REFERENCES authentication_user(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    category_id BIGINT NULL REFERENCES posts_category(id) ON DELETE SET NULL DEFERRABLE INITIALLY DEFERRED
);

-- Strategic Indexes for High-Traffic Read Patterns
CREATE INDEX IF NOT EXISTS posts_post_status_pub_idx ON posts_post (status, published_at DESC);
CREATE INDEX IF NOT EXISTS posts_post_author_idx ON posts_post (author_id);
CREATE INDEX IF NOT EXISTS posts_post_category_idx ON posts_post (category_id);
CREATE INDEX IF NOT EXISTS posts_post_slug_idx ON posts_post (slug);

-- 4. Blog Comments Table
CREATE TABLE IF NOT EXISTS comments_comment (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    author_id BIGINT NOT NULL REFERENCES authentication_user(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    post_id BIGINT NOT NULL REFERENCES posts_post(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX IF NOT EXISTS comments_comment_post_created_idx ON comments_comment (post_id, created_at);
CREATE INDEX IF NOT EXISTS comments_comment_author_idx ON comments_comment (author_id);
