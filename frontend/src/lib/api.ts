export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001/api';

export interface User {
  id: number;
  username: string;
  email: string;
  role: 'author' | 'admin';
  bio?: string;
  avatar_url?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  posts_count: number;
}

export interface Post {
  id: number;
  title: string;
  slug: string;
  content?: string;
  excerpt: string;
  cover_image: string;
  status: 'draft' | 'published';
  author: User;
  category?: Category;
  comments_count: number;
  published_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Comment {
  id: number;
  post: number;
  author: User;
  content: string;
  created_at: string;
}

function getAuthHeader(): Record<string, string> {
  if (typeof window === 'undefined') return {};
  try {
    const token = localStorage.getItem('access_token');
    if (!token || token === 'undefined' || token === 'null') return {};
    return { Authorization: `Bearer ${token}` };
  } catch (e) {
    return {};
  }
}

export const api = {
  // Auth
  async login(credentials: { username: string; password: string }) {
    const res = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || data.message || 'Login failed');
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  async register(payload: { username: string; email?: string; password: string; role?: string; bio?: string }) {
    const res = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      const err = Object.values(data).flat().join(', ') || 'Registration failed';
      throw new Error(err);
    }
    return data;
  },

  logout() {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    }
  },

  getCurrentUser(): User | null {
    if (typeof window === 'undefined') return null;
    try {
      const userStr = localStorage.getItem('user');
      if (!userStr || userStr === 'undefined' || userStr === 'null') return null;
      return JSON.parse(userStr);
    } catch (e) {
      console.warn('Failed to parse user from localStorage', e);
      localStorage.removeItem('user');
      return null;
    }
  },

  // Categories
  async getCategories(): Promise<Category[]> {
    console.log('>>> api.getCategories fetch calling:', `${API_BASE_URL}/categories/`);
    try {
      const res = await fetch(`${API_BASE_URL}/categories/`);
      console.log('>>> api.getCategories response status:', res.status);
      if (!res.ok) return [];
      const data = await res.json();
      return Array.isArray(data) ? data : data.results || [];
    } catch (e) {
      console.error('Failed to get categories', e);
      return [];
    }
  },

  async createCategory(payload: { name: string; description?: string }) {
    const res = await fetch(`${API_BASE_URL}/categories/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.name?.[0] || 'Failed to create category');
    return data;
  },

  // Posts
  async getPosts(params?: { category?: string; search?: string; status?: string }): Promise<Post[]> {
    console.log('>>> api.getPosts fetch calling:', `${API_BASE_URL}/posts/`);
    try {
      const query = new URLSearchParams();
      if (params?.category) query.append('category', params.category);
      if (params?.search) query.append('search', params.search);
      if (params?.status) query.append('status', params.status);

      const url = `${API_BASE_URL}/posts/?${query.toString()}`;
      console.log('>>> fetch URL:', url);
      const res = await fetch(url, {
        headers: getAuthHeader(),
      });
      console.log('>>> api.getPosts response status:', res.status);
      if (!res.ok) return [];
      const data = await res.json();
      return Array.isArray(data) ? data : data.results || [];
    } catch (e) {
      console.error('Failed to get posts', e);
      return [];
    }
  },

  async getMyPosts(): Promise<Post[]> {
    const res = await fetch(`${API_BASE_URL}/posts/my_posts/`, {
      headers: getAuthHeader(),
    });
    const data = await res.json();
    return data.data || [];
  },

  async getPost(id: number): Promise<Post> {
    const res = await fetch(`${API_BASE_URL}/posts/${id}/`, {
      headers: getAuthHeader(),
    });
    const data = await res.json();
    if (!res.ok) throw new Error('Post not found or access denied');
    return data;
  },

  async createPost(payload: { title: string; content: string; category?: number; status?: string; cover_image?: string }) {
    const res = await fetch(`${API_BASE_URL}/posts/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) {
      const err = Object.values(data).flat().join(', ') || 'Failed to create post';
      throw new Error(err);
    }
    return data;
  },

  async updatePost(id: number, payload: any) {
    const res = await fetch(`${API_BASE_URL}/posts/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Failed to update post');
    return data;
  },

  async deletePost(id: number) {
    const res = await fetch(`${API_BASE_URL}/posts/${id}/`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || 'Failed to delete post');
    }
    return true;
  },

  async publishPost(id: number) {
    const res = await fetch(`${API_BASE_URL}/posts/${id}/publish/`, {
      method: 'POST',
      headers: getAuthHeader(),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to publish post');
    return data;
  },

  async unpublishPost(id: number) {
    const res = await fetch(`${API_BASE_URL}/posts/${id}/unpublish/`, {
      method: 'POST',
      headers: getAuthHeader(),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to unpublish post');
    return data;
  },

  // Comments
  async getComments(postId: number): Promise<Comment[]> {
    const res = await fetch(`${API_BASE_URL}/comments/?post=${postId}`, {
      headers: getAuthHeader(),
    });
    const data = await res.json();
    return Array.isArray(data) ? data : data.results || [];
  },

  async createComment(postId: number, content: string): Promise<Comment> {
    const res = await fetch(`${API_BASE_URL}/comments/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify({ post: postId, content }),
    });
    const data = await res.json();
    if (!res.ok) {
      const err = data.post?.[0] || data.content?.[0] || data.detail || 'Failed to add comment';
      throw new Error(err);
    }
    return data;
  },

  async deleteComment(commentId: number) {
    const res = await fetch(`${API_BASE_URL}/comments/${commentId}/`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.detail || 'Failed to delete comment');
    }
    return true;
  },
};
