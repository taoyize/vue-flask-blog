<script setup>
import { h } from 'vue'
import router from "@/router/index.js";
import { LogoutOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { Modal } from 'ant-design-vue';

function handleLogout() {
  Modal.confirm({
    title: '确认登出',
    icon: h(ExclamationCircleOutlined),
    content: '您确定要退出登录吗？',
    okText: '确认',
    cancelText: '取消',
    okType: 'danger',
    onOk() {
      localStorage.removeItem('user');
      router.push('/');
      location.reload();
    },
  });
}
</script>

<template>
  <div class="logout-container">
    <a-button 
      @click="handleLogout" 
      type="primary" 
      danger 
      class="logout-btn"
      size="large"
    >
      <template #icon><LogoutOutlined /></template>
      退出登录
    </a-button>
    
    <div class="logout-info">
      <div class="info-item">
        <span class="info-label">安全提示：</span>
        <span class="info-text">退出后将清除本地登录状态</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logout-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
  padding: 20px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.logout-container:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.logout-btn {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  border: none;
  border-radius: 25px;
  height: 48px;
  padding: 0 32px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 4px 16px rgba(231, 76, 60, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logout-btn:hover {
  background: linear-gradient(135deg, #c0392b, #a93226);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
}

.logout-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
}

.logout-info {
  text-align: center;
  max-width: 300px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}

.info-label {
  font-size: 12px;
  font-weight: 600;
  color: #e74c3c;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-text {
  font-size: 13px;
  color: #7f8c8d;
  line-height: 1.4;
}

/* 添加脉冲动画效果 */
.logout-btn {
  position: relative;
  overflow: hidden;
}

.logout-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.logout-btn:hover::before {
  width: 300px;
  height: 300px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .logout-container {
    padding: 16px;
  }
  
  .logout-btn {
    width: 100%;
    justify-content: center;
    padding: 0 24px;
    height: 44px;
    font-size: 14px;
  }
  
  .logout-info {
    max-width: 100%;
  }
}

/* 添加进入动画 */
.logout-container {
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 添加警告图标动画 */
.logout-btn :deep(.anticon) {
  transition: transform 0.3s ease;
}

.logout-btn:hover :deep(.anticon) {
  transform: scale(1.1);
}
</style>
