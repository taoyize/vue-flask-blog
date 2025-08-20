<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { UserOutlined, CrownOutlined, TeamOutlined, LoginOutlined } from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const user = ref(null);

const refreshFromStorage = () => {
  const storedUser = localStorage.getItem("user");
  if (storedUser && storedUser !== "undefined" && storedUser !== "null") {
    try {
      user.value = JSON.parse(storedUser);
    } catch (error) {
      console.error("解析 user 失败", error);
      user.value = null;
    }
  } else {
    user.value = null;
  }
};

onMounted(() => {
  refreshFromStorage();
  const handler = (e) => {
    refreshFromStorage();
  };
  window.addEventListener('user-updated', handler);
  // 卸载时移除监听
  onBeforeUnmount(() => window.removeEventListener('user-updated', handler));
});

const getUserRole = () => {
  if (!user.value) return '游客';
  return user.value.authority == 1 ? '管理员' : '普通用户';
};

const getRoleIcon = () => {
  if (!user.value) return LoginOutlined;
  return user.value.authority == 1 ? CrownOutlined : TeamOutlined;
};

const getRoleColor = () => {
  if (!user.value) return '#95a5a6';
  return user.value.authority == 1 ? '#f39c12' : '#3498db';
};

const handleLogin = () => {
  router.push('/login');
};
</script>

<template>
  <div class="user-status-container">
    <div v-if="user" class="user-card">
      <div class="user-avatar" @click="router.push(`/user/${user.id}`)" style="cursor: pointer;">
        <a-avatar v-if="user?.avatar" :size="48" class="avatar" :src="user.avatar" />
        <a-avatar v-else :size="48" class="avatar">
          <template #icon><UserOutlined /></template>
        </a-avatar>
        <div class="status-indicator online"></div>
      </div>
      
      <div class="user-info">
        <div class="user-name">{{ user.username }}</div>
        <div class="user-role">
          <component :is="getRoleIcon()" class="role-icon" :style="{ color: getRoleColor() }" />
          <span :style="{ color: getRoleColor() }">{{ getUserRole() }}</span>
        </div>
      </div>
      
      <div class="user-stats">
        <div class="stat-item">
          <div class="stat-value">12</div>
          <div class="stat-label">文章</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">89</div>
          <div class="stat-label">点赞</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">1.2k</div>
          <div class="stat-label">浏览</div>
        </div>
      </div>
    </div>
    
    <div v-else class="guest-card">
      <div class="guest-avatar">
        <a-avatar :size="48" class="avatar guest">
          <template #icon><LoginOutlined /></template>
        </a-avatar>
        <div class="status-indicator offline"></div>
      </div>
      
      <div class="guest-info">
        <div class="guest-title">欢迎游客</div>
        <div class="guest-subtitle">请登录以获取完整功能</div>
      </div>
      
      <div class="guest-actions">
        <a-button type="primary" size="small" class="login-btn" @click="handleLogin">
          <template #icon><LoginOutlined /></template>
          立即登录
        </a-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-status-container {
  width: 100%;
}

.user-card, .guest-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.user-card:hover, .guest-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.user-avatar, .guest-avatar {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.avatar.guest {
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.status-indicator.online {
  background: #2ecc71;
  animation: pulse 2s infinite;
}

.status-indicator.offline {
  background: #95a5a6;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0.7); }
  70% { box-shadow: 0 0 0 10px rgba(46, 204, 113, 0); }
  100% { box-shadow: 0 0 0 0 rgba(46, 204, 113, 0); }
}

.user-info, .guest-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
}

.role-icon {
  font-size: 14px;
}

.guest-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.guest-subtitle {
  font-size: 12px;
  color: #7f8c8d;
}

.user-stats {
  display: flex;
  gap: 16px;
  flex-shrink: 0;
}

.stat-item {
  text-align: center;
  min-width: 40px;
}

.stat-value {
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
}

.stat-label {
  font-size: 10px;
  color: #7f8c8d;
  margin-top: 2px;
}

.guest-actions {
  flex-shrink: 0;
}

.login-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  border-radius: 20px;
  font-size: 12px;
  height: 32px;
  padding: 0 16px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-card, .guest-card {
    flex-direction: column;
    text-align: center;
    gap: 12px;
    padding: 16px;
  }
  
  .user-stats {
    justify-content: center;
    gap: 24px;
  }
  
  .stat-item {
    min-width: 50px;
  }
  
  .user-info, .guest-info {
    text-align: center;
  }
}

/* 添加进入动画 */
.user-card, .guest-card {
  animation: slideInLeft 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
