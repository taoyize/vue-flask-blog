<script setup>
import UserStatus from "@/components/userStatus.vue";
import LogoutButton from "@/components/LogoutButton.vue";
import ShowPassages from "@/components/ShowPassages.vue";
import HotArticles from "@/components/HotArticles.vue";
import { 
  BookOutlined, 
  UserOutlined, 
  EyeOutlined, 
  LikeOutlined,
  TrophyOutlined,
  FireOutlined,
  ArrowRightOutlined
} from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';

const router = useRouter();

// 用户状态
const user = ref(null);
const loading = ref(true);

// 检查用户登录状态
const checkUserStatus = () => {
  try {
    const storedUser = localStorage.getItem("user");
    if (storedUser && storedUser !== "undefined" && storedUser !== "null") {
      user.value = JSON.parse(storedUser);
    } else {
      user.value = null;
    }
  } catch (error) {
    console.error('解析用户数据失败:', error);
    user.value = null;
  } finally {
    loading.value = false;
  }
};

// 页面加载时检查用户状态
onMounted(() => {
  checkUserStatus();
});

// 开始阅读功能
const handleStartReading = () => {
  router.push('/article/1');
};

// 加入我们功能
const handleJoinUs = () => {
  if (user.value) {
    router.push('/submit');
  } else {
    router.push('/register');
  }
};

// 查看全部文章
const handleViewAllArticles = () => {
  router.push({ path: '/articles' })
};

// 查看热门文章
const handleViewHotArticles = () => {
  router.push({ path: '/articles', query: { type: 'hot' } })
};
</script>

<template>
  <div v-if="loading" class="loading-container">
    <a-spin size="large" />
    <p>加载中...</p>
  </div>
  
  <div v-else class="home-container">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1 class="welcome-title">
            <FireOutlined class="title-icon" />
            欢迎来到理想主义者
          </h1>
          <p class="welcome-subtitle">
            在这里分享你的想法，探索无限可能
          </p>
          <div class="welcome-actions">
            <a-button 
              type="primary" 
              size="large" 
              class="primary-btn"
              @click="handleStartReading"
            >
              <template #icon><BookOutlined /></template>
              开始阅读
              <ArrowRightOutlined class="arrow-icon" />
            </a-button>
            <a-button 
              size="large" 
              class="secondary-btn"
              @click="handleJoinUs"
            >
              <template #icon><UserOutlined /></template>
              {{ user ? '发布文章' : '加入我们' }}
            </a-button>
          </div>
        </div>
        <div class="welcome-image">
          <div class="floating-card" @click="handleViewHotArticles">
            <TrophyOutlined class="trophy-icon" />
            <span>今日热门</span>
            <ArrowRightOutlined class="card-arrow" />
          </div>
        </div>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <a-row :gutter="[24, 24]">
        <a-col :xs="24" :sm="12" :md="6">
          <div class="stat-card">
            <div class="stat-icon users">
              <UserOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-number">1,234</div>
              <div class="stat-label">活跃用户</div>
            </div>
          </div>
        </a-col>
        <a-col :xs="24" :sm="12" :md="6">
          <div class="stat-card">
            <div class="stat-icon articles">
              <BookOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-number">567</div>
              <div class="stat-label">文章总数</div>
            </div>
          </div>
        </a-col>
        <a-col :xs="24" :sm="12" :md="6">
          <div class="stat-card">
            <div class="stat-icon views">
              <EyeOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-number">89,012</div>
              <div class="stat-label">总浏览量</div>
            </div>
          </div>
        </a-col>
        <a-col :xs="24" :sm="12" :md="6">
          <div class="stat-card">
            <div class="stat-icon likes">
              <LikeOutlined />
            </div>
            <div class="stat-content">
              <div class="stat-number">12,345</div>
              <div class="stat-label">总点赞数</div>
            </div>
          </div>
        </a-col>
      </a-row>
    </div>

    <!-- 用户状态和操作 -->
    <div class="user-section">
      <a-row :gutter="[24, 24]">
        <a-col :xs="24" :md="8">
          <div class="user-card">
            <user-status />
          </div>
        </a-col>
        <a-col :xs="24" :md="16">
          <div class="action-card">
            <logout-button />
          </div>
        </a-col>
      </a-row>
    </div>

    <!-- 今日热门文章 -->
    <div class="hot-articles-section">
      <div class="section-header">
        <h2 class="section-title">
          <FireOutlined class="section-icon" />
          今日热门
        </h2>
        <a-button type="link" class="view-all-btn" @click="handleViewHotArticles">
          查看全部
          <template #icon><ArrowRightOutlined /></template>
        </a-button>
      </div>
      <hot-articles />
    </div>

    <!-- 最新文章展示区域 -->
    <div class="articles-section">
      <div class="section-header">
        <h2 class="section-title">
          <BookOutlined class="section-icon" />
          最新文章
        </h2>
        <a-button type="link" class="view-all-btn" @click="handleViewAllArticles">
          查看全部
          <template #icon><ArrowRightOutlined /></template>
        </a-button>
      </div>
      <show-passages />
    </div>
  </div>
</template>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
}

.home-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* 欢迎区域 */
.welcome-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  border-radius: 20px;
  padding: 40px;
  position: relative;
  overflow: hidden;
}

.welcome-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.welcome-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  color: #667eea;
  font-size: 2rem;
}

.welcome-subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 32px;
  line-height: 1.6;
}

.welcome-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.arrow-icon {
  font-size: 14px;
  transition: transform 0.3s ease;
}

.primary-btn:hover .arrow-icon {
  transform: translateX(4px);
}

.secondary-btn {
  border: 2px solid #667eea;
  color: #667eea;
  background: transparent;
  transition: all 0.3s ease;
}

.secondary-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

.welcome-image {
  position: relative;
}

.floating-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 12px;
  animation: float 3s ease-in-out infinite;
  cursor: pointer;
  transition: all 0.3s ease;
}

.floating-card:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

.trophy-icon {
  font-size: 24px;
  color: #f39c12;
}

.card-arrow {
  font-size: 14px;
  color: #667eea;
  transition: transform 0.3s ease;
}

.floating-card:hover .card-arrow {
  transform: translateX(4px);
}

/* 统计卡片 */
.stats-section {
  margin-top: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

.stat-icon.users {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.stat-icon.articles {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.stat-icon.views {
  background: linear-gradient(135deg, #4facfe, #00f2fe);
}

.stat-icon.likes {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

/* 用户区域 */
.user-section {
  margin-top: 24px;
}

.user-card, .action-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* 热门文章区域 */
.hot-articles-section {
  margin-top: 24px;
}

/* 文章区域 */
.articles-section {
  margin-top: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.section-icon {
  color: #667eea;
}

.view-all-btn {
  color: #667eea;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.view-all-btn:hover {
  color: #5a6fd8;
}

.view-all-btn :deep(.anticon) {
  transition: transform 0.3s ease;
}

.view-all-btn:hover :deep(.anticon) {
  transform: translateX(4px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    text-align: center;
    gap: 24px;
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-actions {
    justify-content: center;
  }
  
  .floating-card {
    display: none;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}
</style>
