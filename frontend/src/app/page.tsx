'use client';

import React, { useState, useEffect } from 'react';
import { api, Post, Category, Comment, User } from '@/lib/api';

export default function BlogDashboard() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [debouncedSearch, setDebouncedSearch] = useState<string>('');
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [initialLoading, setInitialLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<'feed' | 'my_posts'>('feed');
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string>('');
  const [successMsg, setSuccessMsg] = useState<string>('');

  // Modals
  const [activePost, setActivePost] = useState<Post | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState<string>('');
  const [isEditorOpen, setIsEditorOpen] = useState<boolean>(false);
  const [editingPostId, setEditingPostId] = useState<number | null>(null);
  const [editorTitle, setEditorTitle] = useState<string>('');
  const [editorContent, setEditorContent] = useState<string>('');
  const [editorCategory, setEditorCategory] = useState<string>('');
  const [editorStatus, setEditorStatus] = useState<'draft' | 'published'>('draft');
  const [editorCover, setEditorCover] = useState<string>('');

  // Auth modal
  const [isAuthOpen, setIsAuthOpen] = useState<boolean>(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [authUsername, setAuthUsername] = useState<string>('');
  const [authPassword, setAuthPassword] = useState<string>('');
  const [authRole, setAuthRole] = useState<'author' | 'admin'>('author');

  // Load user, categories & initial posts on mount
  useEffect(() => {
    try {
      const user = api.getCurrentUser();
      setCurrentUser(user);
    } catch (e) {
      console.error(e);
    }
    loadCategories();
    loadPosts();
  }, []);

  // Debounce search query by 280ms
  useEffect(() => {
    if (searchQuery !== debouncedSearch) {
      setIsSearching(true);
    }
    const timer = setTimeout(() => {
      setDebouncedSearch(searchQuery);
    }, 280);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Load posts whenever selectedCategory, debouncedSearch, or activeTab changes
  useEffect(() => {
    loadPosts();
  }, [selectedCategory, debouncedSearch, activeTab]);

  const showToast = (msg: string, isError = false) => {
    if (isError) {
      setErrorMsg(msg);
      setTimeout(() => setErrorMsg(''), 4000);
    } else {
      setSuccessMsg(msg);
      setTimeout(() => setSuccessMsg(''), 4000);
    }
  };

  const loadCategories = async () => {
    console.log('>>> loadCategories STARTED');
    try {
      const data = await api.getCategories();
      console.log('>>> loadCategories GOT DATA:', data);
      setCategories(data);
    } catch (err: any) {
      console.error('Failed to load categories', err);
    }
  };

  const loadPosts = async () => {
    console.log('>>> loadPosts STARTED, activeTab:', activeTab);
    try {
      if (activeTab === 'my_posts' && currentUser) {
        console.log('>>> calling getMyPosts');
        const data = await api.getMyPosts();
        console.log('>>> getMyPosts GOT DATA:', data);
        setPosts(data);
      } else {
        console.log('>>> calling getPosts');
        const data = await api.getPosts({
          category: selectedCategory || undefined,
          search: debouncedSearch || undefined,
          status: 'published',
        });
        console.log('>>> getPosts GOT DATA:', data);
        setPosts(data);
      }
    } catch (err: any) {
      console.error('>>> loadPosts ERROR:', err);
      showToast(err.message, true);
    } finally {
      console.log('>>> loadPosts FINALLY setting initialLoading to false');
      setInitialLoading(false);
      setLoading(false);
      setIsSearching(false);
    }
  };

  // Demo user fast switcher
  const switchDemoUser = async (username: string, pass: string) => {
    try {
      await api.login({ username, password: pass });
      const user = api.getCurrentUser();
      setCurrentUser(user);
      showToast(`Switched account to @${username} (${user?.role.toUpperCase()})`);
      loadPosts();
    } catch (err: any) {
      showToast(`Failed to switch demo user: ${err.message}`, true);
    }
  };

  const handleLogout = () => {
    api.logout();
    setCurrentUser(null);
    setActiveTab('feed');
    showToast('Logged out successfully');
    loadPosts();
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanUsername = authUsername.trim();
    if (!cleanUsername) {
      showToast('Please enter a username', true);
      return;
    }
    try {
      if (authMode === 'login') {
        await api.login({ username: cleanUsername, password: authPassword });
        showToast('Logged in successfully!');
      } else {
        await api.register({
          username: cleanUsername,
          password: authPassword,
          role: authRole,
        });
        // Auto login
        await api.login({ username: cleanUsername, password: authPassword });
        showToast('Account created and logged in!');
      }
      setCurrentUser(api.getCurrentUser());
      setIsAuthOpen(false);
      setAuthUsername('');
      setAuthPassword('');
      loadPosts();
    } catch (err: any) {
      showToast(err.message, true);
    }
  };

  // Post detail & comments
  const openPostDetail = async (post: Post) => {
    setActivePost(post);
    try {
      const comms = await api.getComments(post.id);
      setComments(comms);
    } catch (err: any) {
      console.error(err);
    }
  };

  const handleAddComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activePost || !newComment.trim()) return;
    try {
      const added = await api.createComment(activePost.id, newComment);
      const safeComment: Comment = {
        ...added,
        author: added.author || currentUser || {
          id: currentUser?.id || 0,
          username: currentUser?.username || 'Author',
          email: '',
          role: 'author',
        },
      };
      setComments([...comments, safeComment]);
      setNewComment('');
      showToast('Comment submitted successfully');
      loadPosts();
    } catch (err: any) {
      showToast(err.message, true);
    }
  };

  const handleDeleteComment = async (commentId: number) => {
    try {
      await api.deleteComment(commentId);
      setComments(comments.filter(c => c.id !== commentId));
      showToast('Comment deleted');
      loadPosts();
    } catch (err: any) {
      showToast(err.message, true);
    }
  };

  const PRESET_COVERS = [
    { label: '💻 Coding', url: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80' },
    { label: '☁️ Cloud', url: 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80' },
    { label: '⚙️ Architecture', url: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80' },
    { label: '🤖 AI & Data', url: 'https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1200&q=80' },
  ];

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      showToast('Image size should be less than 5MB', true);
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        setEditorCover(reader.result);
        showToast('Local image loaded from PC!');
      }
    };
    reader.readAsDataURL(file);
  };

  // Editor actions
  const openNewPostEditor = () => {
    setEditingPostId(null);
    setEditorTitle('');
    setEditorContent('');
    setEditorCategory(categories[0]?.id ? String(categories[0].id) : '');
    setEditorStatus('draft');
    setEditorCover(PRESET_COVERS[0].url);
    setIsEditorOpen(true);
  };

  const openEditPostEditor = (post: Post) => {
    setEditingPostId(post.id);
    setEditorTitle(post.title);
    setEditorContent(post.content || post.excerpt || '');
    setEditorCategory(post.category?.id ? String(post.category.id) : '');
    setEditorStatus(post.status);
    setEditorCover(post.cover_image || '');
    setIsEditorOpen(true);
  };

  const handleSavePost = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editorTitle.trim()) {
      showToast('Title is required', true);
      return;
    }
    try {
      const payload = {
        title: editorTitle,
        content: editorContent,
        category: editorCategory ? parseInt(editorCategory) : undefined,
        status: editorStatus,
        cover_image: editorCover,
      };

      if (editingPostId) {
        await api.updatePost(editingPostId, payload);
        showToast('Post updated successfully!');
      } else {
        await api.createPost(payload);
        showToast(`Post created as ${editorStatus.toUpperCase()}!`);
      }
      setIsEditorOpen(false);
      loadPosts();
    } catch (err: any) {
      showToast(err.message, true);
    }
  };

  const handleTogglePublish = async (post: Post) => {
    try {
      if (post.status === 'published') {
        await api.unpublishPost(post.id);
        showToast(`Post reverted to Draft`);
      } else {
        await api.publishPost(post.id);
        showToast(`Post Published Live!`);
      }
      loadPosts();
      if (activePost?.id === post.id) {
        const updated = await api.getPost(post.id);
        setActivePost(updated);
      }
    } catch (err: any) {
      showToast(err.message, true);
    }
  };

  const handleDeletePost = async (id: number) => {
    if (!confirm('Are you sure you want to delete this post?')) return;
    try {
      await api.deletePost(id);
      showToast('Post deleted successfully');
      if (activePost?.id === id) setActivePost(null);
      loadPosts();
    } catch (err: any) {
      showToast(err.message, true);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Toast Alert */}
      {errorMsg && (
        <div className="fixed top-5 right-5 z-50 bg-red-600 text-white px-5 py-3 rounded-lg shadow-xl flex items-center space-x-2 animate-bounce">
          <span>⚠️ {errorMsg}</span>
        </div>
      )}
      {successMsg && (
        <div className="fixed top-5 right-5 z-50 bg-emerald-600 text-white px-5 py-3 rounded-lg shadow-xl flex items-center space-x-2">
          <span>✅ {successMsg}</span>
        </div>
      )}

      {/* Top Header */}
      <header className="glass-nav text-white sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center font-bold text-lg shadow-lg">
              DP
            </div>
            <div>
              <span className="font-extrabold tracking-tight text-lg text-white">DevPulse</span>
              <span className="ml-2 text-xs uppercase px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/30 font-semibold">
                Publishing Platform
              </span>
            </div>
          </div>

          {/* Quick Demo Switcher */}
          <div className="hidden lg:flex items-center space-x-2 bg-slate-900/80 p-1.5 rounded-xl border border-slate-700/60 text-xs">
            <span className="text-slate-400 px-2 font-medium">Demo Switch:</span>
            <button
              onClick={() => switchDemoUser('admin', 'Admin@123')}
              className={`px-2.5 py-1 rounded-lg transition ${currentUser?.username === 'admin' ? 'bg-indigo-600 text-white font-bold' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              👑 Admin
            </button>
            <button
              onClick={() => switchDemoUser('talha_author', 'Author@123')}
              className={`px-2.5 py-1 rounded-lg transition ${currentUser?.username === 'talha_author' ? 'bg-sky-600 text-white font-bold' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              ✍️ Author 1 (Talha)
            </button>
            <button
              onClick={() => switchDemoUser('sara_writer', 'Author@123')}
              className={`px-2.5 py-1 rounded-lg transition ${currentUser?.username === 'sara_writer' ? 'bg-sky-600 text-white font-bold' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              ✍️ Author 2 (Sara)
            </button>
            <button
              onClick={handleLogout}
              className={`px-2.5 py-1 rounded-lg transition ${!currentUser ? 'bg-emerald-600 text-white font-bold' : 'hover:bg-slate-800 text-slate-300'}`}
            >
              👀 Public Reader
            </button>
          </div>

          {/* User actions */}
          <div className="flex items-center space-x-3">
            {currentUser ? (
              <div className="flex items-center space-x-3">
                <button
                  onClick={openNewPostEditor}
                  className="bg-sky-500 hover:bg-sky-600 text-white px-4 py-1.5 rounded-lg text-sm font-semibold shadow-md flex items-center space-x-1.5 transition"
                >
                  <span>+</span>
                  <span>Write Post</span>
                </button>
                <div className="flex items-center space-x-2 pl-2 border-l border-slate-700">
                  <div className="text-right">
                    <div className="text-xs font-bold text-slate-200">@{currentUser.username}</div>
                    <span className="text-[10px] uppercase font-semibold text-sky-400 bg-sky-950/60 px-1.5 py-0.2 rounded border border-sky-800/60">
                      {currentUser.role}
                    </span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="text-xs text-slate-400 hover:text-red-400 p-1"
                    title="Log Out"
                  >
                    Logout
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={() => { setAuthMode('login'); setIsAuthOpen(true); }}
                className="bg-sky-500 hover:bg-sky-600 text-white px-4 py-1.5 rounded-lg text-sm font-semibold shadow transition"
              >
                Sign In / Join
              </button>
            )}
          </div>
        </div>

        {/* Mobile Quick Demo Switcher Bar */}
        <div className="lg:hidden bg-slate-950/95 border-b border-slate-800 px-3 py-1.5 flex items-center justify-between text-[11px] overflow-x-auto gap-1">
          <span className="text-slate-400 font-medium whitespace-nowrap">Switch:</span>
          <button
            onClick={() => switchDemoUser('admin', 'Admin@123')}
            className={`px-2 py-0.5 rounded transition whitespace-nowrap ${currentUser?.username === 'admin' ? 'bg-indigo-600 text-white font-bold' : 'text-slate-300 bg-slate-900'}`}
          >
            👑 Admin
          </button>
          <button
            onClick={() => switchDemoUser('talha_author', 'Author@123')}
            className={`px-2 py-0.5 rounded transition whitespace-nowrap ${currentUser?.username === 'talha_author' ? 'bg-sky-600 text-white font-bold' : 'text-slate-300 bg-slate-900'}`}
          >
            ✍️ Talha
          </button>
          <button
            onClick={() => switchDemoUser('sara_writer', 'Author@123')}
            className={`px-2 py-0.5 rounded transition whitespace-nowrap ${currentUser?.username === 'sara_writer' ? 'bg-sky-600 text-white font-bold' : 'text-slate-300 bg-slate-900'}`}
          >
            ✍️ Sara
          </button>
          <button
            onClick={handleLogout}
            className={`px-2 py-0.5 rounded transition whitespace-nowrap ${!currentUser ? 'bg-emerald-600 text-white font-bold' : 'text-slate-300 bg-slate-900'}`}
          >
            👀 Reader
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="mb-8 p-8 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-850 to-indigo-950 text-white shadow-xl relative overflow-hidden border border-slate-800">
          <div className="relative z-10 max-w-3xl">
            <div className="inline-block px-3 py-1 rounded-full bg-sky-500/20 text-sky-300 border border-sky-400/30 text-xs font-semibold uppercase tracking-wider mb-3">
              Technical Architecture & Insights
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-2">
              Multi-Author Publishing Platform
            </h1>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              Explore system design, distributed architectures, and commercial hosting benchmarks. Protected by server-side Role-Based Access Control and strict draft isolation.
            </p>
          </div>
          <div className="absolute right-0 bottom-0 opacity-10 translate-x-10 translate-y-10 text-9xl font-black select-none pointer-events-none">
            DRF
          </div>
        </div>

        {/* Feed View Mode Switcher (When logged in) */}
        {currentUser && (
          <div className="flex flex-wrap items-center justify-between gap-3 mb-5 p-2 bg-slate-100/90 rounded-2xl border border-slate-200">
            <div className="inline-flex p-1 bg-white rounded-xl shadow-sm border border-slate-200/80">
              <button
                onClick={() => setActiveTab('feed')}
                className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center space-x-2 ${activeTab === 'feed'
                    ? 'bg-slate-900 text-white shadow'
                    : 'text-slate-600 hover:text-slate-900'
                  }`}
              >
                <span>🌐</span>
                <span>Community Feed (All Authors)</span>
              </button>
              <button
                onClick={() => setActiveTab('my_posts')}
                className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center space-x-2 ${activeTab === 'my_posts'
                    ? 'bg-indigo-600 text-white shadow'
                    : 'text-slate-600 hover:text-slate-900'
                  }`}
              >
                <span>📁</span>
                <span>My Posts Studio (@{currentUser.username})</span>
              </button>
            </div>
            <div className="text-[11px] text-slate-500 font-medium px-2">
              {activeTab === 'feed' ? (
                <span>Browsing <strong>Public Published Articles</strong> by all authors</span>
              ) : (
                <span className="text-indigo-700 font-semibold">Author Workspace: Showing your articles & private drafts</span>
              )}
            </div>
          </div>
        )}

        {/* Navigation & Filter Bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          {/* Category Pills */}
          <div className="flex items-center space-x-2 overflow-x-auto pb-2 md:pb-0">
            <button
              onClick={() => { setSelectedCategory(''); setActiveTab('feed'); }}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold transition ${selectedCategory === '' && activeTab === 'feed' ? 'bg-sky-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'}`}
            >
              All Articles
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => { setSelectedCategory(cat.slug); setActiveTab('feed'); }}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition ${selectedCategory === cat.slug && activeTab === 'feed' ? 'bg-sky-500 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'}`}
              >
                {cat.name} ({cat.posts_count})
              </button>
            ))}
          </div>

          {/* Search Box */}
          <div className="flex items-center space-x-3">

            <div className="relative">
              <input
                type="text"
                placeholder="Search articles & authors..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 pr-7 py-1.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent bg-white w-48 sm:w-64"
              />
              <span className="absolute left-2.5 top-2 text-slate-400 text-xs">
                {isSearching ? '⏳' : '🔍'}
              </span>
              {searchQuery && (
                <button
                  onClick={() => {
                    setSearchQuery('');
                    setDebouncedSearch('');
                  }}
                  className="absolute right-2 top-1.5 text-slate-400 hover:text-slate-600 text-xs font-bold"
                >
                  ✕
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Tab Status Notice */}
        {activeTab === 'my_posts' && (
          <div className="mb-6 p-4 rounded-xl bg-indigo-50 border border-indigo-200 text-indigo-900 text-xs flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="text-lg">📁</span>
              <div>
                <span className="font-bold">Author Studio Active:</span> Showing all published posts and private drafts authored by you.
              </div>
            </div>
            <button
              onClick={openNewPostEditor}
              className="bg-indigo-600 text-white px-3 py-1 rounded text-xs font-semibold hover:bg-indigo-700"
            >
              + Create New Post
            </button>
          </div>
        )}

        {/* Feed Grid */}
        {initialLoading ? (
          <div className="text-center py-20 text-slate-400 text-sm">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-sky-500 mb-3"></div>
            <div>Loading verified articles from PostgreSQL...</div>
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-2xl border border-slate-200 p-8">
            <span className="text-4xl mb-3 block">📭</span>
            <h3 className="text-base font-bold text-slate-800">No articles match your filter</h3>
            <p className="text-slate-500 text-xs mt-1">Try clearing your search query or choosing another category.</p>
          </div>
        ) : (
          <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 transition-opacity duration-200 ${isSearching ? 'opacity-60' : 'opacity-100'}`}>
            {posts.map((post) => {
              const isOwner = Boolean(currentUser?.id && post.author?.id && currentUser.id === post.author.id);
              const isAdmin = currentUser?.role === 'admin';
              const canManage = isOwner || isAdmin;

              return (
                <div
                  key={post.id}
                  className="glass-panel rounded-2xl overflow-hidden hover:shadow-xl transition-all duration-300 flex flex-col group border border-slate-200/90"
                >
                  {/* Card Header Image */}
                  <div
                    onClick={() => openPostDetail(post)}
                    className="h-44 w-full bg-slate-800 relative cursor-pointer overflow-hidden"
                  >
                    <img
                      src={post.cover_image || 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80'}
                      alt={post.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition duration-500"
                    />
                    <div className="absolute top-3 left-3 flex items-center space-x-1.5">
                      <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-slate-900/80 text-white backdrop-blur-md">
                        {post.category?.name || 'General'}
                      </span>
                    </div>

                    <div className="absolute top-3 right-3">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${post.status === 'published' ? 'bg-emerald-600 text-white shadow' : 'bg-amber-500 text-slate-950 font-black shadow'}`}>
                        {post.status}
                      </span>
                    </div>
                  </div>

                  {/* Card Body */}
                  <div className="p-5 flex-1 flex flex-col justify-between">
                    <div>
                      <h2
                        onClick={() => openPostDetail(post)}
                        className="text-base font-bold text-slate-900 line-clamp-2 hover:text-sky-600 cursor-pointer transition mb-2"
                      >
                        {post.title}
                      </h2>
                      <p className="text-slate-600 text-xs line-clamp-3 leading-relaxed mb-4">
                        {post.excerpt}
                      </p>
                    </div>

                    <div>
                      {/* Author & Meta */}
                      <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                        <div className="flex items-center space-x-2">
                          <div className="w-6 h-6 rounded-full bg-sky-100 text-sky-700 font-bold flex items-center justify-center text-[10px]">
                            {post.author?.username ? post.author.username[0].toUpperCase() : 'A'}
                          </div>
                          <span className="font-medium text-slate-700">@{post.author?.username || 'Author'}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-[11px]">
                          <span>💬 {post.comments_count}</span>
                          <span>•</span>
                          <span>{post.published_at ? new Date(post.published_at).toLocaleDateString() : 'Draft'}</span>
                        </div>
                      </div>

                      {/* Author / Admin Action Bar */}
                      {canManage && (
                        <div className="mt-3 pt-2 border-t border-dashed border-slate-200 flex items-center justify-between text-[11px]">
                          <button
                            onClick={() => handleTogglePublish(post)}
                            className={`font-semibold hover:underline ${post.status === 'published' ? 'text-amber-600' : 'text-emerald-600'}`}
                          >
                            {post.status === 'published' ? 'Revert to Draft' : '🚀 Publish Now'}
                          </button>
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => openEditPostEditor(post)}
                              className="text-slate-600 hover:text-sky-600 font-medium"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => handleDeletePost(post.id)}
                              className="text-red-500 hover:text-red-700 font-medium"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>

      {/* Post Detail & Comments Modal */}
      {activePost && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-200">
            {/* Header image */}
            <div className="h-56 w-full relative bg-slate-900">
              <img
                src={activePost.cover_image || 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80'}
                alt={activePost.title}
                className="w-full h-full object-cover"
              />
              <button
                onClick={() => setActivePost(null)}
                className="absolute top-4 right-4 bg-slate-900/80 hover:bg-slate-900 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold"
              >
                ✕
              </button>
              <div className="absolute bottom-4 left-6 flex items-center space-x-2">
                <span className="px-3 py-1 rounded-full text-xs font-bold uppercase bg-slate-900/80 text-white backdrop-blur">
                  {activePost.category?.name || 'General'}
                </span>
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase ${activePost.status === 'published' ? 'bg-emerald-600 text-white' : 'bg-amber-500 text-slate-900 font-black'}`}>
                  {activePost.status}
                </span>
              </div>
            </div>

            {/* Content Body */}
            <div className="p-6 sm:p-8">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-4 leading-tight">
                {activePost.title}
              </h1>

              {/* Author bar */}
              <div className="flex items-center justify-between pb-6 mb-6 border-b border-slate-200 text-xs text-slate-500">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-sky-400 to-indigo-600 text-white font-bold flex items-center justify-center text-sm shadow">
                    {activePost.author?.username ? activePost.author.username[0].toUpperCase() : 'A'}
                  </div>
                  <div>
                    <div className="font-bold text-slate-900 text-sm">@{activePost.author?.username || 'Author'}</div>
                    <div className="text-slate-500">{activePost.author?.bio || 'Contributing Author at FalconXoft'}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div>Status: <span className="font-semibold text-slate-800">{activePost.status}</span></div>
                  <div>{activePost.published_at ? new Date(activePost.published_at).toLocaleDateString() : 'Unpublished Draft'}</div>
                </div>
              </div>

              {/* Post Content */}
              <div className="text-slate-800 text-sm sm:text-base leading-relaxed whitespace-pre-line mb-8 font-serif">
                {activePost.content || activePost.excerpt}
              </div>

              {/* Comments Section */}
              <div className="mt-8 pt-6 border-t border-slate-200">
                <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center space-x-2">
                  <span>💬 Discussion</span>
                  <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full font-semibold">
                    {comments.length}
                  </span>
                </h3>

                {/* Comment Submission */}
                {activePost.status !== 'published' ? (
                  <div className="p-3 bg-amber-50 border border-amber-200 text-amber-800 text-xs rounded-xl mb-6">
                    ⚠️ Comments are disabled for draft posts per business acceptance criteria.
                  </div>
                ) : currentUser ? (
                  <form onSubmit={handleAddComment} className="mb-6">
                    <textarea
                      placeholder="Write your technical perspective..."
                      value={newComment}
                      onChange={(e) => setNewComment(e.target.value)}
                      rows={3}
                      className="w-full p-3 text-xs sm:text-sm rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 bg-slate-50"
                      required
                    />
                    <div className="mt-2 flex justify-end">
                      <button
                        type="submit"
                        className="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-4 py-2 rounded-lg shadow"
                      >
                        Post Comment
                      </button>
                    </div>
                  </form>
                ) : (
                  <div className="p-4 bg-slate-50 border border-slate-200 text-slate-600 text-xs rounded-xl mb-6 flex items-center justify-between">
                    <span>Sign in as an author or reader to participate in this discussion.</span>
                    <button
                      onClick={() => setIsAuthOpen(true)}
                      className="bg-sky-500 text-white text-xs font-bold px-3 py-1.5 rounded-lg"
                    >
                      Sign In
                    </button>
                  </div>
                )}

                {/* Comments List */}
                <div className="space-y-3">
                  {comments.length === 0 ? (
                    <div className="text-xs text-slate-400 py-4 text-center">No comments yet. Be the first to share your thoughts!</div>
                  ) : (
                    comments.map((comm) => {
                      const canDelete =
                        Boolean(currentUser?.id && comm.author?.id && currentUser.id === comm.author.id) ||
                        Boolean(currentUser?.id && activePost.author?.id && currentUser.id === activePost.author.id) ||
                        currentUser?.role === 'admin';

                      return (
                        <div key={comm.id} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="font-bold text-slate-800">@{comm.author?.username || 'Member'}</span>
                            <div className="flex items-center space-x-2 text-[11px] text-slate-400">
                              <span>{new Date(comm.created_at).toLocaleDateString()}</span>
                              {canDelete && (
                                <button
                                  onClick={() => handleDeleteComment(comm.id)}
                                  className="text-red-500 hover:text-red-700 font-semibold"
                                >
                                  Delete
                                </button>
                              )}
                            </div>
                          </div>
                          <p className="text-slate-700 leading-normal">{comm.content}</p>
                        </div>
                      );
                    })
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Post Editor Modal */}
      {isEditorOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto">
          <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 p-6 sm:p-8">
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-200">
              <h2 className="text-lg font-bold text-slate-900">
                {editingPostId ? 'Edit Article' : 'Compose New Article'}
              </h2>
              <button
                onClick={() => setIsEditorOpen(false)}
                className="text-slate-400 hover:text-slate-600 font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSavePost} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Article Title *</label>
                <input
                  type="text"
                  placeholder="e.g. Distributed Consensus in Cloud-Native Applications"
                  value={editorTitle}
                  onChange={(e) => setEditorTitle(e.target.value)}
                  className="w-full p-2.5 text-sm rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
                  required
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Category</label>
                  <select
                    value={editorCategory}
                    onChange={(e) => setEditorCategory(e.target.value)}
                    className="w-full p-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
                  >
                    <option value="">Select a Category</option>
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Publication Status</label>
                  <select
                    value={editorStatus}
                    onChange={(e) => setEditorStatus(e.target.value as any)}
                    className="w-full p-2 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
                  >
                    <option value="draft">Draft (Private to You & Admin)</option>
                    <option value="published">Published (Visible to All Readers)</option>
                  </select>
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-bold text-slate-700">Cover Image</label>
                  <span className="text-[10px] text-slate-400">Upload from PC or paste image link</span>
                </div>

                {/* PC Upload and URL input */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <label className="flex items-center justify-center space-x-2 p-2.5 rounded-lg border-2 border-dashed border-sky-300 bg-sky-50/70 hover:bg-sky-100/70 cursor-pointer text-sky-700 transition">
                    <span className="text-base">📁</span>
                    <span className="text-xs font-bold">Upload from PC</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </label>

                  <input
                    type="text"
                    placeholder="Or paste image link (https://...)"
                    value={editorCover.startsWith('data:') ? '📎 Local PC file attached' : editorCover}
                    onChange={(e) => setEditorCover(e.target.value)}
                    className="w-full p-2.5 text-xs rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
                  />
                </div>

                {/* Quick Preset Buttons */}
                <div className="flex items-center space-x-1.5 pt-1 overflow-x-auto text-[11px]">
                  <span className="text-slate-400 font-medium">Quick Covers:</span>
                  {PRESET_COVERS.map((preset) => (
                    <button
                      key={preset.label}
                      type="button"
                      onClick={() => setEditorCover(preset.url)}
                      className="px-2 py-0.5 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition"
                    >
                      {preset.label}
                    </button>
                  ))}
                </div>

                {/* Live Preview Box */}
                {editorCover && (
                  <div className="relative mt-2 rounded-xl overflow-hidden border border-slate-200 h-28 bg-slate-900 group">
                    <img
                      src={editorCover}
                      alt="Cover Preview"
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition flex items-center justify-between px-4 text-xs text-white">
                      <span className="font-semibold truncate max-w-xs">
                        {editorCover.startsWith('data:') ? '📎 Local PC Image Ready' : '🌐 Web URL Ready'}
                      </span>
                      <button
                        type="button"
                        onClick={() => setEditorCover('')}
                        className="bg-red-600 hover:bg-red-700 text-white px-2.5 py-1 rounded text-[11px] font-bold shadow"
                      >
                        ✕ Remove
                      </button>
                    </div>
                  </div>
                )}
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Content Body *</label>
                <textarea
                  placeholder="Draft your comprehensive technical analysis here..."
                  value={editorContent}
                  onChange={(e) => setEditorContent(e.target.value)}
                  rows={8}
                  className="w-full p-3 text-xs sm:text-sm rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 font-mono"
                  required
                />
              </div>

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200">
                <button
                  type="button"
                  onClick={() => setIsEditorOpen(false)}
                  className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold px-5 py-2 rounded-lg shadow"
                >
                  {editingPostId ? 'Update Article' : editorStatus === 'published' ? 'Publish Article Live' : 'Save as Draft'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Authentication Modal */}
      {isAuthOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-sm w-full shadow-2xl border border-slate-200 p-6">
            <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-200">
              <h3 className="font-bold text-slate-900">
                {authMode === 'login' ? 'Sign In to Blog Platform' : 'Create Author Account'}
              </h3>
              <button onClick={() => setIsAuthOpen(false)} className="text-slate-400 font-bold">✕</button>
            </div>

            <form onSubmit={handleAuthSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Username</label>
                <input
                  type="text"
                  placeholder="e.g. Ahsan khan or ahsan_khan"
                  value={authUsername}
                  onChange={(e) => setAuthUsername(e.target.value)}
                  className="w-full p-2 text-xs rounded-lg border border-slate-300 focus:ring-2 focus:ring-sky-500"
                  required
                />
                <p className="text-[10px] text-slate-400 mt-1">Letters, numbers, spaces, and @/./+/-/_ allowed</p>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Password</label>
                <input
                  type="password"
                  value={authPassword}
                  onChange={(e) => setAuthPassword(e.target.value)}
                  className="w-full p-2 text-xs rounded-lg border border-slate-300 focus:ring-2 focus:ring-sky-500"
                  required
                />
              </div>

              {authMode === 'register' && (
                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">Role</label>
                  <select
                    value={authRole}
                    onChange={(e) => setAuthRole(e.target.value as any)}
                    className="w-full p-2 text-xs rounded-lg border border-slate-300 bg-white"
                  >
                    <option value="author">Author (Publish & Draft Posts)</option>
                    <option value="admin">Admin (Site Moderator)</option>
                  </select>
                </div>
              )}

              <button
                type="submit"
                className="w-full bg-sky-500 hover:bg-sky-600 text-white text-xs font-bold py-2.5 rounded-lg shadow transition mt-2"
              >
                {authMode === 'login' ? 'Authenticate with JWT' : 'Register Account'}
              </button>

              <div className="text-center pt-2 text-[11px] text-slate-500">
                {authMode === 'login' ? (
                  <span>Need an account? <button type="button" onClick={() => setAuthMode('register')} className="text-sky-600 font-bold hover:underline">Register</button></span>
                ) : (
                  <span>Already registered? <button type="button" onClick={() => setAuthMode('login')} className="text-sky-600 font-bold hover:underline">Sign In</button></span>
                )}
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Clean Minimalist Footer */}
      <footer className="border-t border-slate-200 bg-white/80 backdrop-blur py-6 mt-16 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-3">
            <div className="w-6 h-6 rounded-lg bg-slate-900 text-white font-black text-xs flex items-center justify-center">
              DP
            </div>
            <span className="font-bold text-slate-800 text-sm tracking-tight">DevPulse</span>
            <span className="text-slate-300">•</span>
            <span className="text-slate-500">Multi-Author Publishing Platform</span>
          </div>

          <div className="flex items-center space-x-1.5 text-slate-600">
            <span>Crafted & Engineered by</span>
            <span className="font-bold text-slate-900 px-2.5 py-0.5 bg-slate-100 rounded-md border border-slate-200">
              Talha Ahmed
            </span>
          </div>

          <div className="flex items-center space-x-4 text-[11px] text-slate-400">
            <span className="flex items-center space-x-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              <span>PostgreSQL 18</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-sky-500"></span>
              <span>Django DRF</span>
            </span>
            <span className="flex items-center space-x-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-indigo-500"></span>
              <span>Next.js 14</span>
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
