from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # 改为可空
    password_hash = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(64))  # 保留字段但不再使用
    phone = db.Column(db.String(20))
    authority = db.Column(db.Integer, default=0)  # 0: 普通用户, 1: 管理员
    avatar = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    likes = db.relationship('Like', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'real_name': self.real_name,
            'authority': self.authority,
            'avatar': self.avatar,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='published')  # draft, published, archived
    views = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    tags = db.relationship('ArticleTag', backref='article', lazy='dynamic')
    likes = db.relationship('Like', backref='article', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'excerpt': self.excerpt,
            'author': self.author.username if self.author else None,
            'author_id': self.author_id,
            'status': self.status,
            'views': self.views,
            'likes_count': self.likes_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'tags': [tag.tag.name for tag in self.tags.all()]
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), default='blue')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关联关系
    articles = db.relationship('ArticleTag', backref='tag', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color
        }

class ArticleTag(db.Model):
    __tablename__ = 'article_tags'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 确保用户不能对同一篇文章点赞多次
    __table_args__ = (db.UniqueConstraint('user_id', 'article_id', name='unique_user_article_like'),)

# 保留原有的Passage模型以兼容现有数据
class Passage(db.Model):
    __tablename__ = 'passages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    username = db.Column(db.String(255))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'username': self.username,
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S') if self.time else None
        }

