from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.posts.models import Category, Post
from apps.comments.models import Comment

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database with initial users, categories, posts, and comments'

    def handle(self, *args, **options):
        self.stdout.write("Seeding 01_Blog database...")

        # 1. Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@falconxoft.com',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'bio': 'Lead System Administrator & Chief Content Moderator at FalconXoft.'
            }
        )
        admin_user.set_password('Admin@123')
        admin_user.save()

        author1, _ = User.objects.get_or_create(
            username='talha_author',
            defaults={
                'email': 'talha@falconxoft.com',
                'role': 'author',
                'bio': 'Full-stack software engineer writing about distributed systems, Next.js, and DRF.'
            }
        )
        author1.set_password('Author@123')
        author1.save()

        author2, _ = User.objects.get_or_create(
            username='sara_writer',
            defaults={
                'email': 'sara@falconxoft.com',
                'role': 'author',
                'bio': 'DevOps architect and cloud infrastructure enthusiast.'
            }
        )
        author2.set_password('Author@123')
        author2.save()

        # 2. Categories
        cat_sys, _ = Category.objects.get_or_create(
            slug='system-design',
            defaults={'name': 'System Design', 'description': 'Architectural patterns, scalability, and distributed primitives.'}
        )
        cat_eng, _ = Category.objects.get_or_create(
            slug='engineering',
            defaults={'name': 'Engineering Excellence', 'description': 'Best practices in backend and frontend web craftsmanship.'}
        )
        cat_cloud, _ = Category.objects.get_or_create(
            slug='devops-cloud',
            defaults={'name': 'DevOps & Cloud', 'description': 'Continuous delivery, infrastructure, and deployment cost trade-offs.'}
        )

        # 3. Posts
        # Published Post 1 (by talha_author)
        p1, _ = Post.objects.get_or_create(
            slug='mastering-drf-and-nextjs-integration',
            defaults={
                'title': 'Mastering DRF and Next.js Integration in High-Performance Teams',
                'author': author1,
                'category': cat_eng,
                'content': '''Building scalable web applications demands a crisp separation of concerns. By coupling Django REST Framework with Next.js, teams benefit from robust relational integrity on the backend alongside fluid, server-rendered and reactive user interfaces on the frontend.

In this deep dive, we explore JWT lifecycle management, optimistic UI updates, and how strict role-based access control (RBAC) ensures bulletproof tenant isolation.''',
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=2),
                'cover_image': 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80'
            }
        )

        # Published Post 2 (by sara_writer)
        p2, _ = Post.objects.get_or_create(
            slug='evaluating-vps-vs-aws-for-intern-projects',
            defaults={
                'title': 'Commercial Realities: Evaluating Hostinger VPS vs AWS for MVPs',
                'author': author2,
                'category': cat_cloud,
                'content': '''When launching an early-stage MVP, engineering decisions must be grounded in commercial realities. While AWS provides limitless elasticity with services like ECS, RDS, and CloudFront, a straightforward VPS from providers like Hostinger or DigitalOcean offers predictable $6 to $15 monthly costs.

Here is how we evaluate compute, egress bandwidth, and database backup pricing models before committing capital.''',
                'status': 'published',
                'published_at': timezone.now() - timezone.timedelta(days=1),
                'cover_image': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80'
            }
        )

        # Draft Post 1 (by talha_author - Private!)
        p3, _ = Post.objects.get_or_create(
            slug='upcoming-distributed-consensus-notes',
            defaults={
                'title': '[DRAFT] Technical Notes on Raft and Paxos Consensus Algorithms',
                'author': author1,
                'category': cat_sys,
                'content': '''This is an unpublished draft containing raw benchmarks on state machine replication. It must NOT be visible to public readers or peer authors until reviewed and published.''',
                'status': 'draft',
                'cover_image': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80'
            }
        )

        # Draft Post 2 (by sara_writer - Private!)
        p4, _ = Post.objects.get_or_create(
            slug='sara-unreleased-cloud-architecture-whitepaper',
            defaults={
                'title': '[DRAFT] Unreleased Cloud Architecture Whitepaper',
                'author': author2,
                'category': cat_cloud,
                'content': '''Internal draft by Sara. Confidential design thoughts on multi-region failovers.''',
                'status': 'draft',
                'cover_image': 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80'
            }
        )

        # 4. Comments
        Comment.objects.get_or_create(
            post=p1,
            author=author2,
            content='Phenomenal breakdown of DRF serializers and Next.js state synchronization! The JWT refresh pattern is particularly well-articulated.'
        )
        Comment.objects.get_or_create(
            post=p1,
            author=admin_user,
            content='Approved and featured on the FalconXoft engineering portal.'
        )
        Comment.objects.get_or_create(
            post=p2,
            author=author1,
            content='Great commercial comparison. The egress bandwidth pricing distinction on AWS vs flat VPS bandwidth is a huge differentiator.'
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with users, categories, posts, and comments!"))
