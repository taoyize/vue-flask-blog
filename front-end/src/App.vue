<script setup>
import HeadMenu from "@/components/headMenu.vue";
import GlobalErrorHandler from "@/components/GlobalErrorHandler.vue";
import { ref, onErrorCaptured } from 'vue';

const footerStyle = {
  textAlign: 'center',
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: '#fff',
  padding: '20px 0',
  fontSize: '14px',
  fontWeight: '500',
  boxShadow: '0 -2px 10px rgba(0,0,0,0.1)',
  borderTop: '1px solid rgba(255,255,255,0.1)'
};

const contentStyle = {
  padding: '20px',
  background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  minHeight: 'calc(100vh - 120px)',
  position: 'relative'
};

const layoutStyle = {
  minHeight: '100vh',
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
};

const headerStyle = {
  background: 'rgba(255, 255, 255, 0.95)',
  backdropFilter: 'blur(10px)',
  borderBottom: '1px solid rgba(255,255,255,0.2)',
  boxShadow: '0 2px 20px rgba(0,0,0,0.1)',
  position: 'sticky',
  top: 0,
  zIndex: 1000
};

// 错误处理
onErrorCaptured((error, instance, info) => {
  console.error('组件错误:', error, info);
  return false;
});
</script>

<template>
  <div id="app">
    <global-error-handler />
    <a-layout :style="layoutStyle">
      <a-layout-header :style="headerStyle">
        <head-menu />
      </a-layout-header>
      
      <a-layout-content :style="contentStyle">
        <div class="content-wrapper">
          <router-view v-slot="{ Component, route }">
            <transition name="fade" mode="out-in">
              <component :is="Component" :key="route.fullPath" />
            </transition>
          </router-view>
        </div>
      </a-layout-content>
      
      <a-layout-footer :style="footerStyle">
        <div class="footer-content">
          <span>© 2025 idealist_taoyize</span>
          <span class="footer-divider">|</span>
          <span>Vue3 + Ant Design Vue</span>
        </div>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<style scoped>
.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  min-height: 300px;
}

.content-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
  border-radius: 16px 16px 0 0;
}

.footer-content {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.footer-divider {
  opacity: 0.6;
  font-weight: 300;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    margin: 0 16px;
    padding: 20px 16px;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 8px;
  }
  
  .footer-divider {
    display: none;
  }
}
</style>
