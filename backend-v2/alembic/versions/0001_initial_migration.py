"""
Initial migration for HintAI V2

Revision ID: 0001
Revises: 
Create Date: 2024-11-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create all tables for HintAI V2."""
    
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    
    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=True, server_default='student'),
        sa.Column('avatar_url', sa.String(length=255), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('school_level_id', sa.Integer(), nullable=True),
        sa.Column('school_class_id', sa.Integer(), nullable=True),
        sa.Column('country', sa.String(length=50), nullable=True, server_default='Togo'),
        sa.Column('city', sa.String(length=50), nullable=True),
        sa.Column('credits', sa.Integer(), nullable=True, server_default='20'),
        sa.Column('xp', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('subscription_status', sa.String(length=20), nullable=True, server_default='pending'),
        sa.Column('subscription_plan_id', sa.Integer(), nullable=True),
        sa.Column('subscription_end_date', sa.DateTime(), nullable=True),
        sa.Column('preferred_language', sa.String(length=10), nullable=True, server_default='fr'),
        sa.Column('theme', sa.String(length=10), nullable=True, server_default='light'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('is_premium', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['school_level_id'], ['school_levels.id'], ),
        sa.ForeignKeyConstraint(['school_class_id'], ['school_classes.id'], ),
        sa.ForeignKeyConstraint(['subscription_plan_id'], ['subscription_plans.id'], ),
    )
    
    # User Logins
    op.create_table(
        'user_logins',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('device_info', postgresql.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # School Levels
    op.create_table(
        'school_levels',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
    )
    
    # School Classes
    op.create_table(
        'school_classes',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('level_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('short_name', sa.String(length=10), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.ForeignKeyConstraint(['level_id'], ['school_levels.id'], ),
    )
    
    # Subjects
    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True),
        sa.Column('short_name', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True, server_default='#4F46E5'),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
    )
    
    # Subject-Class relationship
    op.create_table(
        'subject_classes',
        sa.Column('subject_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('class_id', sa.Integer(), nullable=False, primary_key=True),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['class_id'], ['school_classes.id'], ondelete='CASCADE'),
    )
    
    # Chapters
    op.create_table(
        'chapters',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('subject_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    )
    
    # Exam Types
    op.create_table(
        'exam_types',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_official', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
    )
    
    # Exam Papers
    op.create_table(
        'exam_papers',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('class_id', sa.Integer(), nullable=True),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('exam_type_id', sa.Integer(), nullable=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('country', sa.String(length=50), nullable=True, server_default='Togo'),
        sa.Column('difficulty_level', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='published'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('access_level', sa.String(length=20), nullable=True, server_default='free'),
        sa.Column('is_public', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('tags', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('metadata', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['class_id'], ['school_classes.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['exam_type_id'], ['exam_types.id'], ),
    )
    
    # Exam Documents
    op.create_table(
        'exam_documents',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('exam_paper_id', sa.Integer(), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=False),
        sa.Column('file_url', sa.String(length=500), nullable=True),
        sa.Column('file_name', sa.String(length=255), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('file_hash', sa.String(length=64), nullable=False),
        sa.Column('file_type', sa.String(length=50), nullable=True, server_default='pdf'),
        sa.Column('page_count', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True, server_default='fr'),
        sa.Column('access_level', sa.String(length=20), nullable=True, server_default='free'),
        sa.Column('is_public', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['exam_paper_id'], ['exam_papers.id'], ondelete='CASCADE'),
    )
    
    # Exam Solutions
    op.create_table(
        'exam_solutions',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('exam_paper_id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('is_official', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('verified_by', sa.Integer(), nullable=True),
        sa.Column('verification_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['document_id'], ['exam_documents.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['exam_paper_id'], ['exam_papers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['verified_by'], ['users.id'], ),
    )
    
    # Exam Favorites
    op.create_table(
        'exam_favorites',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exam_paper_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['exam_paper_id'], ['exam_papers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'exam_paper_id', name='uq_user_exam_favorite'),
    )
    
    # Exam Attempts
    op.create_table(
        'exam_attempts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('exam_paper_id', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='in_progress'),
        sa.Column('total_score', sa.Float(), nullable=True, server_default='0'),
        sa.Column('max_score', sa.Float(), nullable=True, server_default='0'),
        sa.Column('percentage', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['exam_paper_id'], ['exam_papers.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Exam Answers
    op.create_table(
        'exam_answers',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('attempt_id', sa.Integer(), nullable=False),
        sa.Column('question_number', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=True),
        sa.Column('question_type', sa.String(length=20), nullable=True),
        sa.Column('user_answer', sa.Text(), nullable=True),
        sa.Column('is_correct', sa.Boolean(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True, server_default='0'),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('correct_answer', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['attempt_id'], ['exam_attempts.id'], ondelete='CASCADE'),
    )
    
    # Exam Results
    op.create_table(
        'exam_results',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('attempt_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('total_score', sa.Float(), nullable=False),
        sa.Column('max_score', sa.Float(), nullable=False),
        sa.Column('percentage', sa.Float(), nullable=False),
        sa.Column('grade', sa.String(length=10), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('strengths', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('weaknesses', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('recommendations', sa.Text(), nullable=True),
        sa.Column('ai_analysis', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['attempt_id'], ['exam_attempts.id'], ondelete='CASCADE'),
    )
    
    # Study Sessions
    op.create_table(
        'study_sessions',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('chapter', sa.String(length=255), nullable=True),
        sa.Column('goal', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('started_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('ended_at', sa.DateTime(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('actual_duration_minutes', sa.Integer(), nullable=True),
        sa.Column('focus_time_minutes', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='in_progress'),
        sa.Column('pomodoro_interval', sa.Integer(), nullable=True, server_default='25'),
        sa.Column('pomodoro_breaks', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('pomodoro_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('productivity_score', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Study Goals
    op.create_table(
        'study_goals',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('chapter', sa.String(length=255), nullable=True),
        sa.Column('target_date', sa.Date(), nullable=True),
        sa.Column('target_xp', sa.Integer(), nullable=True),
        sa.Column('target_hours', sa.Float(), nullable=True),
        sa.Column('current_xp', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('current_hours', sa.Float(), nullable=True, server_default='0'),
        sa.Column('progress_percentage', sa.Float(), nullable=True, server_default='0'),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Study Plans
    op.create_table(
        'study_plans',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('class_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['class_id'], ['school_classes.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Study Plan Events
    op.create_table(
        'study_plan_events',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('chapter', sa.String(length=255), nullable=True),
        sa.Column('start_time', sa.DateTime(), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('reminder_sent', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('reminder_time', sa.DateTime(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('completion_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['study_plans.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    )
    
    # Study Groups
    op.create_table(
        'study_groups',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('max_members', sa.Integer(), nullable=True, server_default='10'),
        sa.Column('is_private', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('invite_code', sa.String(length=20), nullable=True, unique=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Study Group Members
    op.create_table(
        'study_group_members',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=True, server_default='member'),
        sa.Column('joined_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['study_groups.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('group_id', 'user_id', name='uq_group_user'),
    )
    
    # Flashcards
    op.create_table(
        'flashcards',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('front_text', sa.Text(), nullable=False),
        sa.Column('back_text', sa.Text(), nullable=False),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('chapter', sa.String(length=255), nullable=True),
        sa.Column('tags', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('difficulty_level', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('difficulty', sa.String(length=20), nullable=True, server_default='medium'),
        sa.Column('last_reviewed', sa.DateTime(), nullable=True),
        sa.Column('next_review', sa.DateTime(), nullable=True),
        sa.Column('review_count', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('mastery_level', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_public', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Flashcard Reviews
    op.create_table(
        'flashcard_reviews',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('flashcard_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('ease_factor', sa.Float(), nullable=True, server_default='2.5'),
        sa.Column('interval_days', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('performance', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('next_review_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['flashcard_id'], ['flashcards.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # User Achievements
    op.create_table(
        'user_achievements',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('xp_reward', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('credit_reward', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_unlocked', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('unlocked_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'achievement_type', name='uq_user_achievement'),
    )
    
    # User XP
    op.create_table(
        'user_xp',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('extra_data', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('reference_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Leaderboards
    op.create_table(
        'leaderboards',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('period', sa.String(length=20), nullable=False),
        sa.Column('period_start', sa.DateTime(), nullable=False),
        sa.Column('xp', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('level', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('exam_score', sa.Float(), nullable=True, server_default='0'),
        sa.Column('study_time_minutes', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'period', 'period_start', name='uq_leaderboard_user_period'),
    )
    
    # Subscription Plans
    op.create_table(
        'subscription_plans',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('monthly_price', sa.Integer(), nullable=False),
        sa.Column('yearly_price', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=True, server_default='XOF'),
        sa.Column('credit_bonus', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('initial_credits', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('features', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('max_exam_attempts', sa.Integer(), nullable=True),
        sa.Column('max_annales_access', sa.String(length=20), nullable=True, server_default='full'),
        sa.Column('max_study_groups', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('max_flashcards', sa.Integer(), nullable=True),
        sa.Column('max_ai_requests', sa.Integer(), nullable=True),
        sa.Column('max_file_uploads', sa.Integer(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('is_popular', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
    )
    
    # Credit Transactions
    op.create_table(
        'credit_transactions',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=20), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('extra_data', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('reference_id', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Payments
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=True, server_default='XOF'),
        sa.Column('method', sa.String(length=20), nullable=False),
        sa.Column('transaction_id', sa.String(length=100), nullable=True, unique=True),
        sa.Column('reference_id', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True, server_default='pending'),
        sa.Column('failure_reason', sa.Text(), nullable=True),
        sa.Column('extra_data', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Learning Resources
    op.create_table(
        'learning_resources',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('class_id', sa.Integer(), nullable=True),
        sa.Column('chapter_id', sa.Integer(), nullable=True),
        sa.Column('resource_type', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(length=255), nullable=True),
        sa.Column('file_url', sa.String(length=500), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('file_hash', sa.String(length=64), nullable=True),
        sa.Column('is_public', sa.Boolean(), nullable=True, server_default=True),
        sa.Column('is_premium', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('access_level', sa.String(length=20), nullable=True, server_default='free'),
        sa.Column('author', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=255), nullable=True),
        sa.Column('tags', postgresql.JSON(), nullable=True, server_default='[]'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('verified_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ),
        sa.ForeignKeyConstraint(['class_id'], ['school_classes.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['verified_by'], ['users.id'], ),
    )
    
    # Document Embeddings
    op.create_table(
        'document_embeddings',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('document_type', sa.String(length=20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('content_text', sa.Text(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=False),
        sa.Column('extra_data', postgresql.JSON(), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    
    # Concepts
    op.create_table(
        'concepts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject_id', sa.Integer(), nullable=True),
        sa.Column('chapter_id', sa.Integer(), nullable=True),
        sa.Column('difficulty_level', sa.Integer(), nullable=True, server_default='3'),
        sa.Column('importance', sa.Integer(), nullable=True, server_default='5'),
        sa.Column('is_verified', sa.Boolean(), nullable=True, server_default=False),
        sa.Column('verified_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_onupdate=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['chapter_id'], ['chapters.id'], ),
        sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
        sa.ForeignKeyConstraint(['verified_by'], ['users.id'], ),
    )
    
    # Concept Relations
    op.create_table(
        'concept_relations',
        sa.Column('from_concept_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('to_concept_id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('relation_type', sa.String(length=50), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=True, server_default='1'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['from_concept_id'], ['concepts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['to_concept_id'], ['concepts.id'], ondelete='CASCADE'),
    )
    
    # Create indexes
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_school_level_id'), 'users', ['school_level_id'])
    op.create_index(op.f('ix_users_school_class_id'), 'users', ['school_class_id'])
    op.create_index(op.f('ix_users_subscription_plan_id'), 'users', ['subscription_plan_id'])
    
    op.create_index(op.f('ix_user_logins_user_id'), 'user_logins', ['user_id'])
    op.create_index(op.f('ix_user_subscriptions_user_id'), 'user_subscriptions', ['user_id'])
    
    op.create_index(op.f('ix_school_classes_level_id'), 'school_classes', ['level_id'])
    
    op.create_index(op.f('ix_exam_papers_class_id'), 'exam_papers', ['class_id'])
    op.create_index(op.f('ix_exam_papers_subject_id'), 'exam_papers', ['subject_id'])
    op.create_index(op.f('ix_exam_papers_exam_type_id'), 'exam_papers', ['exam_type_id'])
    op.create_index(op.f('ix_exam_papers_year'), 'exam_papers', ['year'])
    
    op.create_index(op.f('ix_exam_documents_exam_paper_id'), 'exam_documents', ['exam_paper_id'])
    op.create_index(op.f('ix_exam_solutions_exam_paper_id'), 'exam_solutions', ['exam_paper_id'])
    op.create_index(op.f('ix_exam_favorites_user_id'), 'exam_favorites', ['user_id'])
    op.create_index(op.f('ix_exam_favorites_exam_paper_id'), 'exam_favorites', ['exam_paper_id'])
    
    op.create_index(op.f('ix_exam_attempts_user_id'), 'exam_attempts', ['user_id'])
    op.create_index(op.f('ix_exam_attempts_exam_paper_id'), 'exam_attempts', ['exam_paper_id'])
    op.create_index(op.f('ix_exam_answers_attempt_id'), 'exam_answers', ['attempt_id'])
    op.create_index(op.f('ix_exam_results_attempt_id'), 'exam_results', ['attempt_id'])
    
    op.create_index(op.f('ix_study_sessions_user_id'), 'study_sessions', ['user_id'])
    op.create_index(op.f('ix_study_goals_user_id'), 'study_goals', ['user_id'])
    op.create_index(op.f('ix_study_plans_user_id'), 'study_plans', ['user_id'])
    op.create_index(op.f('ix_study_plan_events_plan_id'), 'study_plan_events', ['plan_id'])
    
    op.create_index(op.f('ix_study_groups_created_by'), 'study_groups', ['created_by'])
    op.create_index(op.f('ix_study_group_members_group_id'), 'study_group_members', ['group_id'])
    op.create_index(op.f('ix_study_group_members_user_id'), 'study_group_members', ['user_id'])
    
    op.create_index(op.f('ix_flashcards_user_id'), 'flashcards', ['user_id'])
    op.create_index(op.f('ix_flashcards_subject_id'), 'flashcards', ['subject_id'])
    op.create_index(op.f('ix_flashcard_reviews_flashcard_id'), 'flashcard_reviews', ['flashcard_id'])
    
    op.create_index(op.f('ix_user_achievements_user_id'), 'user_achievements', ['user_id'])
    op.create_index(op.f('ix_user_xp_user_id'), 'user_xp', ['user_id'])
    op.create_index(op.f('ix_leaderboards_user_id'), 'leaderboards', ['user_id'])
    
    op.create_index(op.f('ix_credit_transactions_user_id'), 'credit_transactions', ['user_id'])
    op.create_index(op.f('ix_payments_user_id'), 'payments', ['user_id'])
    
    op.create_index(op.f('ix_learning_resources_subject_id'), 'learning_resources', ['subject_id'])
    op.create_index(op.f('ix_learning_resources_class_id'), 'learning_resources', ['class_id'])
    
    op.create_index(op.f('ix_document_embeddings_user_id'), 'document_embeddings', ['user_id'])
    op.create_index(op.f('ix_concepts_subject_id'), 'concepts', ['subject_id'])
    op.create_index(op.f('ix_concepts_chapter_id'), 'concepts', ['chapter_id'])
    op.create_index(op.f('ix_concept_relations_from'), 'concept_relations', ['from_concept_id'])
    op.create_index(op.f('ix_concept_relations_to'), 'concept_relations', ['to_concept_id'])


def downgrade():
    """Drop all tables for HintAI V2."""
    op.drop_index(op.f('ix_concept_relations_to'), table_name='concept_relations')
    op.drop_index(op.f('ix_concept_relations_from'), table_name='concept_relations')
    op.drop_index(op.f('ix_concepts_chapter_id'), table_name='concepts')
    op.drop_index(op.f('ix_concepts_subject_id'), table_name='concepts')
    op.drop_index(op.f('ix_document_embeddings_user_id'), table_name='document_embeddings')
    op.drop_index(op.f('ix_learning_resources_class_id'), table_name='learning_resources')
    op.drop_index(op.f('ix_learning_resources_subject_id'), table_name='learning_resources')
    op.drop_index(op.f('ix_payments_user_id'), table_name='payments')
    op.drop_index(op.f('ix_credit_transactions_user_id'), table_name='credit_transactions')
    op.drop_index(op.f('ix_leaderboards_user_id'), table_name='leaderboards')
    op.drop_index(op.f('ix_user_xp_user_id'), table_name='user_xp')
    op.drop_index(op.f('ix_user_achievements_user_id'), table_name='user_achievements')
    op.drop_index(op.f('ix_flashcard_reviews_flashcard_id'), table_name='flashcard_reviews')
    op.drop_index(op.f('ix_flashcards_subject_id'), table_name='flashcards')
    op.drop_index(op.f('ix_flashcards_user_id'), table_name='flashcards')
    op.drop_index(op.f('ix_study_group_members_user_id'), table_name='study_group_members')
    op.drop_index(op.f('ix_study_group_members_group_id'), table_name='study_group_members')
    op.drop_index(op.f('ix_study_groups_created_by'), table_name='study_groups')
    op.drop_index(op.f('ix_study_plan_events_plan_id'), table_name='study_plan_events')
    op.drop_index(op.f('ix_study_plans_user_id'), table_name='study_plans')
    op.drop_index(op.f('ix_study_goals_user_id'), table_name='study_goals')
    op.drop_index(op.f('ix_study_sessions_user_id'), table_name='study_sessions')
    op.drop_index(op.f('ix_exam_results_attempt_id'), table_name='exam_results')
    op.drop_index(op.f('ix_exam_answers_attempt_id'), table_name='exam_answers')
    op.drop_index(op.f('ix_exam_attempts_exam_paper_id'), table_name='exam_attempts')
    op.drop_index(op.f('ix_exam_attempts_user_id'), table_name='exam_attempts')
    op.drop_index(op.f('ix_exam_favorites_exam_paper_id'), table_name='exam_favorites')
    op.drop_index(op.f('ix_exam_favorites_user_id'), table_name='exam_favorites')
    op.drop_index(op.f('ix_exam_solutions_exam_paper_id'), table_name='exam_solutions')
    op.drop_index(op.f('ix_exam_documents_exam_paper_id'), table_name='exam_documents')
    op.drop_index(op.f('ix_exam_papers_year'), table_name='exam_papers')
    op.drop_index(op.f('ix_exam_papers_exam_type_id'), table_name='exam_papers')
    op.drop_index(op.f('ix_exam_papers_subject_id'), table_name='exam_papers')
    op.drop_index(op.f('ix_exam_papers_class_id'), table_name='exam_papers')
    op.drop_index(op.f('ix_school_classes_level_id'), table_name='school_classes')
    op.drop_index(op.f('ix_user_subscriptions_user_id'), table_name='user_subscriptions')
    op.drop_index(op.f('ix_user_logins_user_id'), table_name='user_logins')
    op.drop_index(op.f('ix_users_subscription_plan_id'), table_name='users')
    op.drop_index(op.f('ix_users_school_class_id'), table_name='users')
    op.drop_index(op.f('ix_users_school_level_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    
    op.drop_table('concept_relations')
    op.drop_table('concepts')
    op.drop_table('document_embeddings')
    op.drop_table('learning_resources')
    op.drop_table('payments')
    op.drop_table('credit_transactions')
    op.drop_table('leaderboards')
    op.drop_table('user_xp')
    op.drop_table('user_achievements')
    op.drop_table('flashcard_reviews')
    op.drop_table('flashcards')
    op.drop_table('study_group_members')
    op.drop_table('study_groups')
    op.drop_table('study_plan_events')
    op.drop_table('study_plans')
    op.drop_table('study_goals')
    op.drop_table('study_sessions')
    op.drop_table('exam_results')
    op.drop_table('exam_answers')
    op.drop_table('exam_attempts')
    op.drop_table('exam_favorites')
    op.drop_table('exam_solutions')
    op.drop_table('exam_documents')
    op.drop_table('exam_papers')
    op.drop_table('exam_types')
    op.drop_table('chapters')
    op.drop_table('subject_classes')
    op.drop_table('subjects')
    op.drop_table('school_classes')
    op.drop_table('school_levels')
    op.drop_table('user_subscriptions')
    op.drop_table('user_logins')
    op.drop_table('users')
    op.drop_table('subscription_plans')
    
    op.execute("DROP EXTENSION IF EXISTS vector")
