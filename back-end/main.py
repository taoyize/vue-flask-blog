from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import db, User, Passage, Article, Tag, ArticleTag, Like
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)  # 开启跨域支持

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

# 错误处理
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': '请求参数错误'}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': '资源不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': '服务器内部错误'}), 500

# 用户相关API
@app.route('/api/users', methods=['GET'])
def get_users():
    """获取所有用户列表"""
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户信息"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.json
        required_fields = ['username', 'email', 'password', 'real_name', 'phone']
        
        # 验证必填字段
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 验证用户名和邮箱是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': '用户名已存在'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': '邮箱已存在'}), 400
        
        # 验证邮箱格式
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({'error': '邮箱格式不正确'}), 400
        
        # 验证手机号格式
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, data['phone']):
            return jsonify({'error': '手机号格式不正确'}), 400
        
        # 创建新用户
        user = User(
            username=data['username'],
            email=data['email'],
            real_name=data['real_name'],
            phone=data['phone'],
            authority=0  # 默认为普通用户
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        # 支持用户名或邮箱登录
        user = User.query.filter(
            db.or_(User.username == username, User.email == username)
        ).first()
        
        if user and user.check_password(password):
            return jsonify({
                'code': 200,
                'message': '登录成功',
                'user': user.to_dict()
            })
        else:
            return jsonify({
                'code': 401,
                'message': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户信息"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        data = request.json
        if 'real_name' in data:
            user.real_name = data['real_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'avatar' in data:
            user.avatar = data['avatar']
        
        db.session.commit()
        return jsonify({'message': '更新成功', 'user': user.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'用户 {user_id} 删除成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 文章相关API
@app.route('/api/articles', methods=['GET'])
def get_articles():
    """获取文章列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        tag = request.args.get('tag')
        author = request.args.get('author')
        
        query = Article.query.filter_by(status='published')
        
        if tag:
            query = query.join(ArticleTag).join(Tag).filter(Tag.name == tag)
        
        if author:
            query = query.join(User).filter(User.username == author)
        
        articles = query.order_by(Article.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'articles': [article.to_dict() for article in articles.items],
            'total': articles.total,
            'pages': articles.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """获取单篇文章详情"""
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        # 增加浏览量
        article.views += 1
        db.session.commit()
        
        return jsonify(article.to_dict())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles', methods=['POST'])
def create_article():
    """创建新文章"""
    try:
        data = request.json
        required_fields = ['title', 'content', 'author_id']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 生成摘要
        excerpt = data['content'][:200] + '...' if len(data['content']) > 200 else data['content']
        
        article = Article(
            title=data['title'],
            content=data['content'],
            excerpt=excerpt,
            author_id=data['author_id'],
            status=data.get('status', 'published')
        )
        
        db.session.add(article)
        db.session.flush()  # 获取article.id
        
        # 处理标签
        if 'tags' in data and data['tags']:
            for tag_name in data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()
                
                article_tag = ArticleTag(article_id=article.id, tag_id=tag.id)
                db.session.add(article_tag)
        
        db.session.commit()
        return jsonify({'message': '文章创建成功', 'article': article.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """更新文章"""
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        data = request.json
        if 'title' in data:
            article.title = data['title']
        if 'content' in data:
            article.content = data['content']
            article.excerpt = data['content'][:200] + '...' if len(data['content']) > 200 else data['content']
        if 'status' in data:
            article.status = data['status']
        
        db.session.commit()
        return jsonify({'message': '更新成功', 'article': article.to_dict()})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """删除文章"""
    try:
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': '文章删除成功'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 热门文章API
@app.route('/api/articles/hot', methods=['GET'])
def get_hot_articles():
    """获取热门文章"""
    try:
        limit = request.args.get('limit', 10, type=int)
        articles = Article.query.filter_by(status='published')\
            .order_by(Article.views.desc(), Article.likes_count.desc())\
            .limit(limit).all()
        
        return jsonify([article.to_dict() for article in articles])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 标签相关API
@app.route('/api/tags', methods=['GET'])
def get_tags():
    """获取所有标签"""
    try:
        tags = Tag.query.all()
        return jsonify([tag.to_dict() for tag in tags])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tags', methods=['POST'])
def create_tag():
    """创建新标签"""
    try:
        data = request.json
        if not data.get('name'):
            return jsonify({'error': '标签名称不能为空'}), 400
        
        # 检查标签是否已存在
        if Tag.query.filter_by(name=data['name']).first():
            return jsonify({'error': '标签已存在'}), 400
        
        tag = Tag(
            name=data['name'],
            color=data.get('color', 'blue')
        )
        
        db.session.add(tag)
        db.session.commit()
        
        return jsonify({'message': '标签创建成功', 'tag': tag.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 点赞相关API
@app.route('/api/articles/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    """点赞文章"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400
        
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        # 检查是否已经点赞
        existing_like = Like.query.filter_by(user_id=user_id, article_id=article_id).first()
        
        if existing_like:
            # 取消点赞
            db.session.delete(existing_like)
            article.likes_count = max(0, article.likes_count - 1)
            message = '取消点赞成功'
        else:
            # 添加点赞
            like = Like(user_id=user_id, article_id=article_id)
            db.session.add(like)
            article.likes_count += 1
            message = '点赞成功'
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'likes_count': article.likes_count,
            'is_liked': not bool(existing_like)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/articles/<int:article_id>/like', methods=['GET'])
def check_like_status(article_id):
    """检查用户是否已点赞文章"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': '用户ID不能为空'}), 400
        
        like = Like.query.filter_by(user_id=user_id, article_id=article_id).first()
        return jsonify({'is_liked': bool(like)})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 统计相关API
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取网站统计信息"""
    try:
        total_users = User.query.count()
        total_articles = Article.query.filter_by(status='published').count()
        total_views = db.session.query(db.func.sum(Article.views)).scalar() or 0
        total_likes = db.session.query(db.func.sum(Article.likes_count)).scalar() or 0
        
        return jsonify({
            'total_users': total_users,
            'total_articles': total_articles,
            'total_views': total_views,
            'total_likes': total_likes
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 保留原有API以兼容现有前端
@app.route('/api/addusers', methods=['POST'])
def add_user():
    """添加用户（兼容旧版本）"""
    try:
        data = request.json
        print(f"接收到的数据: {data}")  # 调试信息
        
        if not data:
            print("错误: 请求数据为空")
            return jsonify({'error': '请求数据为空'}), 400
        
        # 验证必填字段
        if not data.get('name'):
            print("错误: 用户名为空")
            return jsonify({'error': '用户名不能为空'}), 400
        if not data.get('email'):
            print("错误: 邮箱为空")
            return jsonify({'error': '邮箱不能为空'}), 400
        # 密码为可选，未提供则使用默认值
        provided_password = data.get('password', '').strip() if isinstance(data.get('password'), str) else ''
        
        print(f"验证用户名: {data['name']}")
        print(f"验证邮箱: {data['email']}")
        
        # 检查用户名和邮箱是否已存在
        try:
            existing_user = User.query.filter_by(username=data['name']).first()
            if existing_user:
                print(f"错误: 用户名 {data['name']} 已存在")
                return jsonify({'error': '用户名已存在'}), 400
        except Exception as e:
            print(f"查询用户名时出错: {str(e)}")
            return jsonify({'error': '数据库查询错误'}), 500
        
        try:
            existing_email = User.query.filter_by(email=data['email']).first()
            if existing_email:
                print(f"错误: 邮箱 {data['email']} 已存在")
                return jsonify({'error': '邮箱已存在'}), 400
        except Exception as e:
            print(f"查询邮箱时出错: {str(e)}")
            return jsonify({'error': '数据库查询错误'}), 500
        
        # 处理authority字段，确保是整数
        authority = 0  # 默认为普通用户
        if 'authority' in data:
            try:
                authority = int(data['authority'])
                if authority not in [0, 1]:
                    authority = 0
                print(f"权限设置为: {authority}")
            except (ValueError, TypeError) as e:
                print(f"权限转换错误: {str(e)}")
                authority = 0
        
        print(f"创建用户: username={data['name']}, email={data['email']}, authority={authority}")
        
        user = User(
            username=data['name'],
            email=data['email'],
            authority=authority,
            real_name=data.get('name', ''),  # 使用用户名作为真实姓名
            phone=''  # 默认为空
        )
        # 设置密码：优先使用前端提供的密码，否则使用默认密码
        user.set_password(provided_password if provided_password else '123456')
        
        db.session.add(user)
        db.session.commit()
        
        print(f"用户创建成功: {user.username}")
        return jsonify({'message': '添加成功'})
        
    except Exception as e:
        db.session.rollback()
        print(f"添加用户错误: {str(e)}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        return jsonify({'error': f'添加用户失败: {str(e)}'}), 500

@app.route('/api/deleteusers', methods=['POST'])
def delete_user_old():
    """删除用户（兼容旧版本）"""
    try:
        data = request.json
        user_id = data['id']
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': '没有该用户'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'用户{user_id} 删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/passages', methods=['GET'])
def get_passages():
    """获取文章列表（兼容旧版本）"""
    try:
        passages = Passage.query.all()
        return jsonify([passage.to_dict() for passage in passages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/getusers', methods=['GET', 'POST'])
def get_single_passage():
    """获取用户文章（兼容旧版本）"""
    try:
        data = request.json
        user_name = data['name']
        passages = Passage.query.filter_by(username=user_name).all()
        return jsonify([passage.to_dict() for passage in passages])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_passages', methods=['POST'])
def add_passages():
    """添加文章（兼容旧版本）"""
    try:
        data = request.json
        passage = Passage(content=data['content'], username=data['username'])
        db.session.add(passage)
        db.session.commit()
        return jsonify({'message': '添加成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "理想主义者后端API服务"

if __name__ == "__main__":
    app.run(port=5000, debug=True)



