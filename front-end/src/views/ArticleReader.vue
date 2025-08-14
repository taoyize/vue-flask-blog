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
    
    // 检查用户是否已点赞
    await checkUserLikeStatus()
  } catch (error) {
    console.error('获取文章失败:', error)
    message.error('获取文章失败')
    router.push('/articles')
  } finally {
    isLoading.value = false
  }
}

// 检查用户点赞状态
const checkUserLikeStatus = async () => {
  const userStr = localStorage.getItem('user')
  if (!userStr) {
    isLiked.value = false
    console.log('用户未登录，点赞状态设为false')
    return
  }
  
  let user = null
  try { user = JSON.parse(userStr) } catch { user = null }
  if (!user || !user.id) {
    isLiked.value = false
    console.log('用户信息无效，点赞状态设为false')
    return
  }
  
  try {
    console.log('检查用户点赞状态，用户ID:', user.id, '文章ID:', article.value.id)
    const response = await axios.get(`/api/articles/${article.value.id}/like?user_id=${user.id}`)
    isLiked.value = response.data.is_liked
    console.log('点赞状态检查结果:', response.data.is_liked)
  } catch (error) {
    console.error('检查点赞状态失败:', error)
    isLiked.value = false
  }
}

const handleLike = async () => {
  // 检查用户是否登录
  const userStr = localStorage.getItem('user')
  if (!userStr) {
    message.warning('请先登录')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }
  
  let user = null
  try { user = JSON.parse(userStr) } catch { user = null }
  if (!user || !user.id) {
    message.warning('请先登录')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }

  console.log('执行点赞操作，用户ID:', user.id, '文章ID:', article.value.id, '当前点赞状态:', isLiked.value)

  try {
    // 调用后端API
    const response = await axios.post(`/api/articles/${article.value.id}/like`, {
      user_id: user.id
    })
    
    console.log('点赞API响应:', response.data)
    
    if (response.data) {
      // 更新前端状态
      isLiked.value = response.data.is_liked
      article.value.likes = response.data.likes_count
      
      console.log('更新后的点赞状态:', isLiked.value, '点赞数:', article.value.likes)
      
      if (isLiked.value) {
        message.success('点赞成功')
      } else {
        message.info('取消点赞成功')
      }
    }
  } catch (error) {
    console.error('点赞操作失败:', error)
    message.error('点赞操作失败，请稍后重试')
    // 恢复原状态
    isLiked.value = !isLiked.value
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
              {{ isLiked ? '已点赞' : '点赞' }}
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
