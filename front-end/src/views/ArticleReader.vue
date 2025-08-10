<script setup>
import { ref, onMounted } from 'vue'
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

const route = useRoute()
const router = useRouter()

const article = ref({
  id: 1,
  title: 'Vue3 组合式API最佳实践',
  author: '技术达人',
  authorAvatar: '',
  publishTime: '2024-01-15',
  readTime: '8分钟',
  views: 1234,
  likes: 89,
  tags: ['Vue3', '前端', 'JavaScript'],
  content: `
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
  `,
  relatedArticles: [
    { id: 2, title: 'Vue3性能优化技巧', views: 856 },
    { id: 3, title: 'Vue Router 4 新特性', views: 743 },
    { id: 4, title: 'Pinia状态管理指南', views: 621 }
  ]
})

const isLiked = ref(false)
const isLoading = ref(false)

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
</script>

<template>
  <div class="article-reader">
    <!-- 返回按钮 -->
    <div class="back-button" @click="handleBack">
      <ArrowLeftOutlined />
      <span>返回</span>
    </div>
    
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
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.article-header {
  margin-bottom: 32px;
}

.article-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 24px;
  line-height: 1.3;
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
  color: #2c3e50;
  margin-bottom: 4px;
}

.publish-time {
  font-size: 12px;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #7f8c8d;
  font-size: 14px;
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
  color: #2c3e50;
  margin-bottom: 32px;
}

.article-content h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 32px 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #f0f0f0;
}

.article-content p {
  margin-bottom: 16px;
}

.article-content pre {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
  border-left: 4px solid #667eea;
}

.article-content code {
  background: #f1f3f4;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
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
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.related-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
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
  background: rgba(255, 255, 255, 0.6);
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
  color: #2c3e50;
  flex: 1;
}

.related-views {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #7f8c8d;
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
