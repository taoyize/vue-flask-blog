<script setup>
import { ref, onMounted } from 'vue'
import { BookOutlined, EyeOutlined, LikeOutlined, FireOutlined } from '@ant-design/icons-vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { message } from 'ant-design-vue'

const router = useRouter()
const hotArticles = ref([])
const loading = ref(false)

const fetchHotArticles = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/articles/hot?limit=5')
    hotArticles.value = response.data
  } catch (error) {
    console.error('获取热门文章失败:', error)
    message.error('获取热门文章失败')
    // 使用模拟数据作为备用
    hotArticles.value = [
      {
        id: 1,
        title: 'Vue3 组合式API最佳实践',
        author: '技术达人',
        views: 1234,
        likes_count: 89,
        tags: ['Vue3', '前端'],
        excerpt: '深入探讨Vue3组合式API的使用技巧和最佳实践，帮助你更好地构建现代化前端应用...',
        isHot: true
      },
      {
        id: 2,
        title: 'Flask后端开发实战指南',
        author: 'Python专家',
        views: 987,
        likes_count: 67,
        tags: ['Flask', 'Python'],
        excerpt: '从零开始学习Flask框架，掌握Web开发的核心概念和实践技巧...',
        isHot: true
      },
      {
        id: 3,
        title: 'MySQL数据库优化技巧',
        author: '数据库工程师',
        views: 756,
        likes_count: 45,
        tags: ['MySQL', '数据库'],
        excerpt: '分享MySQL数据库性能优化的实用技巧，提升查询效率...',
        isHot: false
      }
    ]
  } finally {
    loading.value = false
  }
}

const handleArticleClick = (article) => {
  router.push(`/article/${article.id}`)
}

const handleAuthorClick = (author) => {
  console.log('查看作者:', author)
  // 这里可以跳转到作者页面
  // router.push(`/author/${author}`)
}

onMounted(() => {
  fetchHotArticles()
})
</script>

<template>
  <div class="hot-articles">
    <div class="hot-header">
      <FireOutlined class="hot-icon" />
      <span class="hot-title">今日热门</span>
    </div>
    
    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
      <p>加载中...</p>
    </div>
    
    <div v-else class="articles-list">
      <div 
        v-for="article in hotArticles" 
        :key="article.id"
        class="article-card"
        @click="handleArticleClick(article)"
      >
        <div class="article-header">
          <div class="article-title">
            <span class="title-text">{{ article.title }}</span>
            <FireOutlined v-if="article.views > 1000" class="hot-badge" />
          </div>
          <div class="article-meta">
            <span class="author" @click.stop="handleAuthorClick(article.author)">
              {{ article.author }}
            </span>
            <span class="divider">·</span>
            <span class="views">
              <EyeOutlined />
              {{ article.views }}
            </span>
            <span class="likes">
              <LikeOutlined />
              {{ article.likes_count }}
            </span>
          </div>
        </div>
        
        <div class="article-excerpt">
          {{ article.excerpt || article.content?.substring(0, 100) + '...' }}
        </div>
        
        <div class="article-tags">
          <a-tag 
            v-for="tag in article.tags" 
            :key="tag"
            color="blue"
            class="tag"
          >
            {{ tag }}
          </a-tag>
        </div>
      </div>
    </div>
    
    <div v-if="!loading && hotArticles.length === 0" class="empty-state">
      <BookOutlined class="empty-icon" />
      <p>暂无热门文章</p>
    </div>
  </div>
</template>

<style scoped>
.hot-articles {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.hot-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.hot-icon {
  font-size: 20px;
  color: #ff6b35;
}

.hot-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 16px;
}

.loading-container p {
  color: #7f8c8d;
  margin: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 12px;
}

.empty-icon {
  font-size: 48px;
  color: #bdc3c7;
}

.empty-state p {
  color: #7f8c8d;
  margin: 0;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-card {
  padding: 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.6));
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
}

.article-header {
  margin-bottom: 12px;
}

.article-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.title-text {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
}

.hot-badge {
  color: #ff6b35;
  font-size: 16px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #7f8c8d;
}

.author {
  color: #667eea;
  cursor: pointer;
  font-weight: 500;
}

.author:hover {
  text-decoration: underline;
}

.divider {
  color: #bdc3c7;
}

.views, .likes {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-excerpt {
  font-size: 14px;
  color: #5a6c7d;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  font-size: 11px;
  border-radius: 12px;
  padding: 2px 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hot-articles {
    padding: 16px;
  }
  
  .article-card {
    padding: 12px;
  }
  
  .title-text {
    font-size: 14px;
  }
  
  .article-excerpt {
    font-size: 13px;
  }
}
</style>
