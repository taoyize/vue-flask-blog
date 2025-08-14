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
  ArrowRightOutlined,
  ReloadOutlined
} from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';
import { ref, onMounted, onUnmounted } from 'vue';
import axios from 'axios';
import { message } from 'ant-design-vue';

const router = useRouter();

// 用户状态
const user = ref(null);
const loading = ref(true);

// 统计数据
const stats = ref({
  total_users: 0,
  total_articles: 0,
  total_views: 0,
  total_likes: 0
});

const statsLoading = ref(false);
const lastUpdateTime = ref(null);
const statsUpdated = ref(false);

// 自动刷新定时器
let autoRefreshTimer = null;

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

// 获取统计数据
const fetchStats = async () => {
  try {
    statsLoading.value = true;
    const response = await axios.get('/api/stats');
    if (response.data) {
      stats.value = response.data;
      lastUpdateTime.value = new Date();
      statsUpdated.value = true;
      console.log('获取统计数据成功:', stats.value);
      
      // 重置更新状态
      setTimeout(() => {
        statsUpdated.value = false;
      }, 600);
    }
  } catch (error) {
    console.error('获取统计数据失败:', error);
    message.error('获取统计数据失败');
  } finally {
    statsLoading.value = false;
  }
};

// 刷新统计数据
const refreshStats = () => {
  fetchStats();
  message.success('统计数据已刷新');
};

// 启动自动刷新
const startAutoRefresh = () => {
  // 每5分钟自动刷新一次统计数据
  autoRefreshTimer = setInterval(() => {
    console.log('自动刷新统计数据...');
    fetchStats();
  }, 5 * 60 * 1000); // 5分钟
};

// 停止自动刷新
const stopAutoRefresh = () => {
  if (autoRefreshTimer) {
    clearInterval(autoRefreshTimer);
    autoRefreshTimer = null;
  }
};

// 格式化数字显示
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
};

// 格式化时间显示
const formatTime = (date) => {
  if (!date) return '';
  const now = new Date();
  const diff = now - date;
  
  if (diff < 60000) { // 小于1分钟
    return '刚刚';
  } else if (diff < 3600000) { // 小于1小时
    return `${Math.floor(diff / 60000)}分钟前`;
  } else if (diff < 86400000) { // 小于1天
    return `${Math.floor(diff / 3600000)}小时前`;
  } else {
    return date.toLocaleDateString();
  }
};

// 页面加载时检查用户状态和获取统计数据
onMounted(() => {
  checkUserStatus();
  fetchStats();
  startAutoRefresh();
});

// 页面卸载时清理定时器
onUnmounted(() => {
  stopAutoRefresh();
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
              <div class="stat-number">
                <a-spin v-if="statsLoading" size="small" />
                <span v-else :class="{ 'updated': statsUpdated }">{{ formatNumber(stats.total_users) }}</span>
              </div>
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
              <div class="stat-number">
                <a-spin v-if="statsLoading" size="small" />
                <span v-else :class="{ 'updated': statsUpdated }">{{ formatNumber(stats.total_articles) }}</span>
              </div>
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
              <div class="stat-number">
                <a-spin v-if="statsLoading" size="small" />
                <span v-else :class="{ 'updated': statsUpdated }">{{ formatNumber(stats.total_views) }}</span>
              </div>
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
              <div class="stat-number">
                <a-spin v-if="statsLoading" size="small" />
                <span v-else :class="{ 'updated': statsUpdated }">{{ formatNumber(stats.total_likes) }}</span>
              </div>
              <div class="stat-label">总点赞数</div>
            </div>
          </div>
        </a-col>
      </a-row>
      <div class="refresh-stats-btn">
        <a-button type="dashed" @click="refreshStats" :loading="statsLoading">
          <template #icon><ReloadOutlined /></template>
          刷新统计
        </a-button>
        <span class="last-update-time">最后更新: {{ formatTime(lastUpdateTime) }}</span>
      </div>
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
  transition: all 0.3s ease;
}

.stat-number span {
  display: inline-block;
  transition: all 0.3s ease;
}

.stat-number span.updated {
  animation: numberUpdate 0.6s ease-out;
}

@keyframes numberUpdate {
  0% {
    transform: scale(1);
    color: #2c3e50;
  }
  50% {
    transform: scale(1.1);
    color: #667eea;
  }
  100% {
    transform: scale(1);
    color: #2c3e50;
  }
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

.refresh-stats-btn {
  text-align: center;
  margin-top: 24px;
}

.refresh-stats-btn .ant-btn {
  border-style: dashed;
  border-color: #d9d9d9;
  color: #666;
  transition: all 0.3s ease;
}

.refresh-stats-btn .ant-btn:hover {
  border-color: #667eea;
  color: #667eea;
  background: rgba(102, 126, 234, 0.05);
}

.refresh-stats-btn .ant-btn:active {
  transform: scale(0.95);
}

.last-update-time {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-left: 16px;
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
