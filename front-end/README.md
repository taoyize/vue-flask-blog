# 理想主义者博客系统

一个基于 Vue3 + Flask + MySQL 的现代化博客系统，支持用户管理、文章发布、标签分类等功能。

## 项目结构

```
├── front-end/          # Vue3 前端项目
│   ├── src/           # 源代码
│   ├── public/        # 静态资源
│   └── package.json   # 前端依赖
├── back-end/          # Flask 后端项目
│   ├── main.py        # 主应用文件
│   ├── models.py      # 数据模型
│   ├── config.py      # 配置文件
│   └── requirements.txt # 后端依赖
└── README.md          # 项目说明
```

## 技术栈

### 前端 (Vue3)
- **框架**: Vue 3 + Composition API
- **UI库**: Ant Design Vue
- **路由**: Vue Router 4
- **构建工具**: Vite
- **HTTP客户端**: Axios

### 后端 (Flask)
- **框架**: Flask 2.3.3
- **数据库**: MySQL + SQLAlchemy
- **跨域**: Flask-CORS
- **密码加密**: Werkzeug
- **数据库驱动**: PyMySQL

## 功能特性

### 用户系统
- ✅ 用户注册、登录、管理
- ✅ 管理员权限控制
- ✅ 用户状态管理

### 文章系统
- ✅ 文章发布、编辑、删除
- ✅ 标签管理
- ✅ 点赞功能
- ✅ 热门文章推荐
- ✅ 文章列表分页

### 其他功能
- ✅ 网站统计信息
- ✅ 完整的错误处理
- ✅ 数据验证和安全
- ✅ 响应式设计

## 快速开始

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd flask+vue+mysql通信
```

### 2. 后端设置
```bash
cd back-end

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置数据库
# 修改 config.py 中的数据库连接信息

# 初始化数据库
python db_init.py

# 启动后端服务
python main.py
```

### 3. 前端设置
```bash
cd front-end

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 默认账号

初始化时会自动创建以下示例账号：

- **管理员**: admin / admin123
- **技术达人**: tech_author / 123456
- **Python专家**: python_expert / 123456
- **数据库工程师**: db_engineer / 123456

## API 文档

### 用户相关
- `POST /api/register` - 用户注册
- `POST /api/login` - 用户登录
- `GET /api/users` - 获取用户列表
- `POST /api/addusers` - 添加用户（管理员）

### 文章相关
- `GET /api/articles` - 获取文章列表
- `POST /api/articles` - 创建文章
- `GET /api/articles/:id` - 获取文章详情
- `GET /api/articles/hot` - 获取热门文章
- `PUT /api/articles/:id` - 更新文章
- `DELETE /api/articles/:id` - 删除文章

### 标签相关
- `GET /api/tags` - 获取所有标签
- `POST /api/tags` - 创建标签

### 点赞相关
- `POST /api/articles/:id/like` - 点赞/取消点赞文章

## 开发说明

### 添加新的API接口
1. 在 `back-end/main.py` 中添加新的路由函数
2. 在 `back-end/models.py` 中添加相应的数据模型（如需要）
3. 更新数据库结构（如需要）
4. 添加相应的错误处理

### 数据库迁移
当修改数据模型时，需要更新数据库结构：
1. 删除现有数据库表
2. 重新运行 `python db_init.py`

## 许可证

MIT License
