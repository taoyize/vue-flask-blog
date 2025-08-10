# 理想主义者后端API服务

这是一个基于Flask的RESTful API后端服务，为前端提供完整的用户管理、文章管理、标签管理等功能。

## 功能特性

- ✅ 用户注册、登录、管理
- ✅ 文章发布、编辑、删除
- ✅ 标签管理
- ✅ 点赞功能
- ✅ 热门文章推荐
- ✅ 网站统计信息
- ✅ 完整的错误处理
- ✅ 数据验证和安全

## 技术栈

- **框架**: Flask 2.3.3
- **数据库**: MySQL + SQLAlchemy
- **跨域**: Flask-CORS
- **密码加密**: Werkzeug
- **数据库驱动**: PyMySQL

## 安装和运行

### 1. 环境要求

- Python 3.8+
- MySQL 5.7+

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 数据库配置

1. 创建MySQL数据库：
```sql
CREATE DATABASE test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `config.py` 中的数据库连接信息：
```python
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_HOST = 'localhost'
DB_NAME = 'test'
```

### 4. 初始化数据库

```bash
python db_init.py
```

### 5. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:5000` 启动。

## API接口文档

### 用户相关

#### 用户注册
```
POST /api/register
Content-Type: application/json

{
  "username": "test_user",
  "email": "test@example.com",
  "password": "password123",
  "real_name": "测试用户",
  "phone": "13800138000"
}
```

#### 用户登录
```
POST /api/login
Content-Type: application/json

{
  "username": "test_user",
  "password": "password123"
}
```

#### 获取用户列表
```
GET /api/users
```

#### 获取单个用户
```
GET /api/users/{user_id}
```

### 文章相关

#### 获取文章列表
```
GET /api/articles?page=1&per_page=10&tag=Vue3&author=tech_author
```

#### 获取单篇文章
```
GET /api/articles/{article_id}
```

#### 创建文章
```
POST /api/articles
Content-Type: application/json

{
  "title": "文章标题",
  "content": "文章内容",
  "author_id": 1,
  "tags": ["Vue3", "前端"]
}
```

#### 更新文章
```
PUT /api/articles/{article_id}
Content-Type: application/json

{
  "title": "更新后的标题",
  "content": "更新后的内容"
}
```

#### 删除文章
```
DELETE /api/articles/{article_id}
```

### 热门文章

#### 获取热门文章
```
GET /api/articles/hot?limit=10
```

### 标签相关

#### 获取所有标签
```
GET /api/tags
```

#### 创建标签
```
POST /api/tags
Content-Type: application/json

{
  "name": "新标签",
  "color": "blue"
}
```

### 点赞相关

#### 点赞/取消点赞文章
```
POST /api/articles/{article_id}/like
Content-Type: application/json

{
  "user_id": 1
}
```

#### 检查点赞状态
```
GET /api/articles/{article_id}/like?user_id=1
```

### 统计信息

#### 获取网站统计
```
GET /api/stats
```

## 数据库结构

### 用户表 (users)
- id: 主键
- username: 用户名（唯一）
- email: 邮箱（唯一）
- password_hash: 密码哈希
- real_name: 真实姓名
- phone: 手机号
- authority: 权限级别（0: 普通用户, 1: 管理员）
- avatar: 头像URL
- created_at: 创建时间
- updated_at: 更新时间

### 文章表 (articles)
- id: 主键
- title: 文章标题
- content: 文章内容
- excerpt: 文章摘要
- author_id: 作者ID（外键）
- status: 状态（draft, published, archived）
- views: 浏览量
- likes_count: 点赞数
- created_at: 创建时间
- updated_at: 更新时间

### 标签表 (tags)
- id: 主键
- name: 标签名称（唯一）
- color: 标签颜色
- created_at: 创建时间

### 文章标签关联表 (article_tags)
- id: 主键
- article_id: 文章ID（外键）
- tag_id: 标签ID（外键）
- created_at: 创建时间

### 点赞表 (likes)
- id: 主键
- user_id: 用户ID（外键）
- uid: 文章ID（外键）
- created_at: 创建时间

## 示例数据

初始化数据库时会自动创建以下示例数据：

### 用户
- 管理员: admin/admin123
- 技术达人: tech_author/123456
- Python专家: python_expert/123456
- 数据库工程师: db_engineer/123456

### 文章
- Vue3 组合式API最佳实践
- Flask后端开发实战指南
- MySQL数据库优化技巧

### 标签
- Vue3, 前端, Flask, Python, MySQL, 数据库, JavaScript, Web开发

## 错误处理

API使用标准HTTP状态码：

- 200: 成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权
- 404: 资源不存在
- 500: 服务器内部错误

错误响应格式：
```json
{
  "error": "错误类型",
  "message": "错误描述"
}
```

## 开发说明

### 添加新的API接口

1. 在 `main.py` 中添加新的路由函数
2. 在 `models.py` 中添加相应的数据模型（如需要）
3. 更新数据库结构（如需要）
4. 添加相应的错误处理

### 数据库迁移

当修改数据模型时，需要更新数据库结构：

1. 删除现有数据库表
2. 重新运行 `python db_init.py`

### 安全注意事项

- 所有用户密码都使用Werkzeug进行哈希加密
- 输入数据进行了验证和清理
- 使用参数化查询防止SQL注入
- 实现了适当的错误处理

## 许可证

MIT License
