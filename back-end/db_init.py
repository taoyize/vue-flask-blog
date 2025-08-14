from main import app, db
from models import User, Article, Tag, ArticleTag, Like, Passage
from datetime import datetime

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表创建成功")
        
        # 检查是否已有数据
        if User.query.first():
            print("数据库中已有数据，跳过初始化")
            return
        
        # 创建示例用户
        admin_user = User(
            username='admin',
            email='admin@example.com',
            real_name='管理员',
            phone='13800138000',
            authority=1
        )
        admin_user.set_password('admin123')
        
        user1 = User(
            username='tech_author',
            email='tech@example.com',
            real_name='技术达人',
            phone='13800138001',
            authority=0
        )
        user1.set_password('123456')
        
        user2 = User(
            username='python_expert',
            email='python@example.com',
            real_name='Python专家',
            phone='13800138002',
            authority=0
        )
        user2.set_password('123456')
        
        user3 = User(
            username='db_engineer',
            email='db@example.com',
            real_name='数据库工程师',
            phone='13800138003',
            authority=0
        )
        user3.set_password('123456')
        
        # 添加一个没有邮箱的用户示例
        user4 = User(
            username='minimal_user',
            email=None,  # 没有邮箱
            real_name='简约用户',
            phone=None,  # 没有手机号
            authority=0
        )
        user4.set_password('123456')
        
        db.session.add_all([admin_user, user1, user2, user3, user4])
        db.session.flush()  # 获取用户ID
        
        # 创建示例标签
        tags_data = [
            {'name': 'Vue3', 'color': 'green'},
            {'name': '前端', 'color': 'blue'},
            {'name': 'Flask', 'color': 'orange'},
            {'name': 'Python', 'color': 'purple'},
            {'name': 'MySQL', 'color': 'cyan'},
            {'name': '数据库', 'color': 'red'},
            {'name': 'JavaScript', 'color': 'yellow'},
            {'name': 'Web开发', 'color': 'magenta'}
        ]
        
        tags = []
        for tag_data in tags_data:
            tag = Tag(name=tag_data['name'], color=tag_data['color'])
            tags.append(tag)
            db.session.add(tag)
        
        db.session.flush()  # 获取标签ID
        
        # 创建示例文章
        articles_data = [
            {
                'title': 'Vue3 组合式API最佳实践',
                'content': '''
                <h2>引言</h2>
                <p>Vue3的组合式API为我们提供了更灵活、更强大的组件逻辑组织方式。本文将深入探讨组合式API的最佳实践，帮助你更好地构建现代化前端应用。</p>
                
                <h2>1. 响应式数据管理</h2>
                <p>在Vue3中，我们使用ref和reactive来创建响应式数据：</p>
                <pre><code>import { ref, reactive } from 'vue'

const count = ref(0)
const user = reactive({
  name: 'John',
  age: 25
})</code></pre>
                
                <h2>2. 计算属性</h2>
                <p>使用computed来创建计算属性：</p>
                <pre><code>const doubleCount = computed(() => count.value * 2)</code></pre>
                
                <h2>3. 生命周期钩子</h2>
                <p>组合式API提供了更直观的生命周期管理：</p>
                <pre><code>onMounted(() => {
  console.log('组件已挂载')
})

onUnmounted(() => {
  console.log('组件已卸载')
})</code></pre>
                
                <h2>4. 组合函数</h2>
                <p>创建可复用的逻辑组合：</p>
                <pre><code>function useCounter() {
  const count = ref(0)
  
  const increment = () => count.value++
  const decrement = () => count.value--
  
  return {
    count,
    increment,
    decrement
  }
}</code></pre>
                
                <h2>总结</h2>
                <p>组合式API让我们能够更好地组织代码逻辑，提高代码的可维护性和可复用性。通过合理使用这些特性，我们可以构建出更加优雅的Vue应用。</p>
                ''',
                'author_id': user1.id,
                'views': 1234,
                'likes_count': 89,
                'tags': ['Vue3', '前端']
            },
            {
                'title': 'Flask后端开发实战指南',
                'content': '''
                <h2>Flask框架简介</h2>
                <p>Flask是一个轻量级的Python Web框架，它提供了灵活性和可扩展性，是构建Web应用的理想选择。</p>
                
                <h2>1. 安装和配置</h2>
                <p>首先安装Flask：</p>
                <pre><code>pip install flask</code></pre>
                
                <h2>2. 基本应用结构</h2>
                <pre><code>from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()</code></pre>
                
                <h2>3. 路由和视图</h2>
                <p>Flask使用装饰器来定义路由：</p>
                <pre><code>@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'</code></pre>
                
                <h2>4. 模板系统</h2>
                <p>Flask使用Jinja2模板引擎：</p>
                <pre><code>from flask import render_template

@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)</code></pre>
                
                <h2>5. 数据库集成</h2>
                <p>使用Flask-SQLAlchemy进行数据库操作：</p>
                <pre><code>from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)</code></pre>
                
                <h2>总结</h2>
                <p>Flask是一个强大而灵活的Web框架，适合各种规模的Web应用开发。通过合理使用其特性，我们可以快速构建高质量的Web应用。</p>
                ''',
                'author_id': user2.id,
                'views': 987,
                'likes_count': 67,
                'tags': ['Flask', 'Python']
            },
            {
                'title': 'MySQL数据库优化技巧',
                'content': '''
                <h2>数据库性能优化的重要性</h2>
                <p>在Web应用中，数据库性能直接影响用户体验。本文将分享MySQL数据库优化的实用技巧。</p>
                
                <h2>1. 索引优化</h2>
                <p>合理使用索引是提升查询性能的关键：</p>
                <pre><code>-- 创建复合索引
CREATE INDEX idx_user_email_name ON users(email, name);

-- 避免在索引列上使用函数
-- 错误示例
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- 正确示例
SELECT * FROM users WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';</code></pre>
                
                <h2>2. 查询优化</h2>
                <p>优化SQL查询语句：</p>
                <pre><code>-- 使用EXPLAIN分析查询计划
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 避免SELECT *
SELECT id, name, email FROM users WHERE status = 'active';

-- 使用LIMIT限制结果集
SELECT * FROM articles ORDER BY created_at DESC LIMIT 10;</code></pre>
                
                <h2>3. 表结构优化</h2>
                <p>合理设计表结构：</p>
                <pre><code>-- 选择合适的数据类型
-- 使用TINYINT而不是INT存储布尔值
status TINYINT(1) DEFAULT 0

-- 使用VARCHAR而不是CHAR存储变长字符串
name VARCHAR(100) NOT NULL

-- 使用TEXT存储长文本
content TEXT</code></pre>
                
                <h2>4. 连接池配置</h2>
                <p>配置合适的连接池参数：</p>
                <pre><code>[mysqld]
max_connections = 200
innodb_buffer_pool_size = 1G
query_cache_size = 64M
query_cache_type = 1</code></pre>
                
                <h2>5. 监控和分析</h2>
                <p>使用MySQL慢查询日志：</p>
                <pre><code>-- 启用慢查询日志
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- 查看慢查询日志
SHOW VARIABLES LIKE 'slow_query_log%';</code></pre>
                
                <h2>总结</h2>
                <p>数据库优化是一个持续的过程，需要根据实际应用场景进行调整。通过合理使用这些技巧，可以显著提升数据库性能。</p>
                ''',
                'author_id': user3.id,
                'views': 756,
                'likes_count': 45,
                'tags': ['MySQL', '数据库']
            }
        ]
        
        # 添加文章和标签关联
        for article_data in articles_data:
            article = Article(
                title=article_data['title'],
                content=article_data['content'],
                excerpt=article_data['content'][:200] + '...',
                author_id=article_data['author_id'],
                views=article_data['views'],
                likes_count=article_data['likes_count']
            )
            db.session.add(article)
            db.session.flush()  # 获取文章ID
            
            # 添加标签关联
            for tag_name in article_data['tags']:
                tag = Tag.query.filter_by(name=tag_name).first()
                if tag:
                    article_tag = ArticleTag(article_id=article.id, tag_id=tag.id)
                    db.session.add(article_tag)
        
        # 添加一些示例点赞
        like_data = [
            (user1.id, 1),  # 用户1点赞文章1
            (user2.id, 1),  # 用户2点赞文章1
            (user3.id, 1),  # 用户3点赞文章1
            (user1.id, 2),  # 用户1点赞文章2
            (user2.id, 2),  # 用户2点赞文章2
            (user1.id, 3),  # 用户1点赞文章3
        ]
        
        for user_id, article_id in like_data:
            like = Like(user_id=user_id, article_id=article_id)
            db.session.add(like)
        
        # 提交所有更改
        db.session.commit()
        print("示例数据添加成功")
        print(f"创建了 {User.query.count()} 个用户")
        print(f"创建了 {Article.query.count()} 篇文章")
        print(f"创建了 {Tag.query.count()} 个标签")
        print(f"创建了 {Like.query.count()} 个点赞")

if __name__ == '__main__':
    init_database()
