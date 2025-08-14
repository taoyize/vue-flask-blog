<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  BookOutlined, 
  EyeOutlined, 
  LikeOutlined, 
  ShareAltOutlined,
  UserOutlined,
  CalendarOutlined,
  TagOutlined,
  ArrowLeftOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const article = ref({
  id: 0,
  title: '',
  author: '',
  authorAvatar: '',
  publishTime: '',
  readTime: '5分钟',
  views: 0,
  likes: 0,
  tags: [],
  content: '',
  relatedArticles: []
})

const isLiked = ref(false)
const isLoading = ref(false)

// 获取文章数据
const fetchArticle = async () => {
  try {
    isLoading.value = true
    const articleId = route.params.id
    console.log('正在获取文章ID:', articleId)
    
    const response = await axios.get(`/api/articles/${articleId}`)
    const articleData = response.data
    console.log('获取到的文章数据:', articleData)
    
    // 格式化文章数据
    article.value = {
      id: articleData.id,
      title: articleData.title,
      author: articleData.author || '未知作者',
      authorAvatar: '',
      publishTime: articleData.created_at ? new Date(articleData.created_at).toLocaleDateString('zh-CN') : '',
      readTime: '5分钟',
      views: articleData.views || 0,
      likes: articleData.likes_count || 0,
      tags: articleData.tags || [],
      content: articleData.content || '',
      relatedArticles: []
    }
    console.log('格式化后的文章数据:', article.value)
  } catch (error) {
    console.error('获取文章失败:', error)
    message.error('获取文章失败')
    router.push('/articles')
  } finally {
    isLoading.value = false
  }
}

const handleLike = () => {
  isLiked.value = !isLiked.value
  if (isLiked.value) {
    article.value.likes++
    message.success('已添加到收藏')
  } else {
    article.value.likes--
    message.info('已取消收藏')
  }
}

const handleShare = () => {
  navigator.clipboard.writeText(window.location.href).then(() => {
    message.success('链接已复制到剪贴板')
  })
}

const handleBack = () => {
  router.back()
}

const handleRelatedArticleClick = (relatedArticle) => {
  console.log('查看相关文章:', relatedArticle.title)
  // 这里可以跳转到相关文章
}

const handleAuthorClick = () => {
  console.log('查看作者:', article.value.author)
  // router.push(`/author/${article.value.author}`)
}

// 监听路由参数变化
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchArticle()
  }
})

// 组件挂载时获取文章数据
onMounted(() => {
  fetchArticle()
})
</script>

<template>
  <div class="article-reader">
    <!-- 返回按钮 -->
    <div class="back-button" @click="handleBack">
      <ArrowLeftOutlined />
      <span>返回</span>
    </div>
    
    <!-- 加载状态 -->
    <a-spin :spinning="isLoading" tip="加载中...">
      <div v-if="!isLoading && article.title">
        <!-- 文章主体 -->
        <div class="article-container">
          <!-- 文章头部 -->
          <div class="article-header">
            <h1 class="article-title">{{ article.title }}</h1>
            
            <div class="article-meta">
              <div class="author-info" @click="handleAuthorClick">
                <a-avatar :size="40" class="author-avatar">
                  <template #icon><UserOutlined /></template>
                </a-avatar>
                <div class="author-details">
                  <div class="author-name">{{ article.author }}</div>
                  <div class="publish-time">
                    <CalendarOutlined />
                    {{ article.publishTime }} · {{ article.readTime }}
                  </div>
                </div>
              </div>
              
              <div class="article-stats">
                <div class="stat-item">
                  <EyeOutlined />
                  <span>{{ article.views }}</span>
                </div>
                <div class="stat-item">
                  <LikeOutlined />
                  <span>{{ article.likes }}</span>
                </div>
              </div>
            </div>
            
            <div class="article-tags">
              <TagOutlined class="tag-icon" />
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
          
          <!-- 文章内容 -->
          <div class="article-content" v-html="article.content"></div>
          
          <!-- 文章操作 -->
          <div class="article-actions">
            <a-button 
              :type="isLiked ? 'primary' : 'default'"
              @click="handleLike"
              class="action-btn"
            >
              <template #icon><LikeOutlined /></template>
              {{ isLiked ? '已收藏' : '收藏' }}
            </a-button>
            
            <a-button @click="handleShare" class="action-btn">
              <template #icon><ShareAltOutlined /></template>
              分享
            </a-button>
          </div>
        </div>
        
        <!-- 相关文章 -->
        <div class="related-articles">
          <h3 class="related-title">
            <BookOutlined />
            相关文章
          </h3>
          
          <div class="related-list">
            <div 
              v-for="related in article.relatedArticles" 
              :key="related.id"
              class="related-item"
              @click="handleRelatedArticleClick(related)"
            >
              <div class="related-title-text">{{ related.title }}</div>
              <div class="related-views">
                <EyeOutlined />
                {{ related.views }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </a-spin>
  </div>
</template>

<style scoped>
.article-reader {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  cursor: pointer;
  margin-bottom: 24px;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  width: fit-content;
}

.back-button:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateX(-4px);
}

.article-container {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-heavy);
  margin-bottom: 24px;
  transition: var(--transition);
}

.article-header {
  margin-bottom: 32px;
}

.article-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 24px;
  line-height: 1.3;
  transition: var(--transition);
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.author-info:hover {
  transform: translateY(-2px);
}

.author-avatar {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.author-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
  transition: var(--transition);
}

.publish-time {
  font-size: 12px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
  transition: var(--transition);
}

.article-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--text-secondary);
  font-size: 14px;
  transition: var(--transition);
}

.article-tags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tag-icon {
  color: #667eea;
  font-size: 16px;
}

.tag {
  border-radius: 12px;
  padding: 4px 12px;
  font-size: 12px;
}

.article-content {
  font-size: 16px;
  line-height: 1.8;
  color: var(--text-primary);
  margin-bottom: 32px;
  transition: var(--transition);
}

.article-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 32px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--border-color);
  transition: var(--transition);
}

.article-content p {
  margin-bottom: 16px;
}

.article-content pre {
  background: var(--code-bg);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
  border-left: 4px solid var(--code-border);
  transition: var(--transition);
}

.article-content code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  color: var(--text-primary);
  transition: var(--transition);
}

.article-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.action-btn {
  min-width: 120px;
  height: 40px;
  border-radius: 20px;
  font-weight: 500;
}

.related-articles {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-medium);
  transition: var(--transition);
}

.related-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--border-color);
  transition: var(--transition);
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 8px;
  background: var(--bg-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
}

.related-item:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateX(4px);
}

.related-title-text {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  flex: 1;
  transition: var(--transition);
}

.related-views {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
  transition: var(--transition);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .article-reader {
    padding: 16px;
  }
  
  .article-container {
    padding: 20px;
  }
  
  .article-title {
    font-size: 1.8rem;
  }
  
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .article-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>
