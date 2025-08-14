<script setup>
import HeadMenu from "@/components/headMenu.vue";
import GlobalErrorHandler from "@/components/GlobalErrorHandler.vue";
import { ref, onErrorCaptured, computed } from 'vue';
import { useTheme } from '@/composables/useTheme';

const { isDark } = useTheme();

// 错误处理
onErrorCaptured((error, instance, info) => {
  console.error('组件错误:', error, info);
  return false;
});
</script>

<template>
  <div id="app" :class="{ 'theme-dark': isDark, 'theme-light': !isDark }">
    <global-error-handler />
    <a-layout class="main-layout">
      <a-layout-header class="main-header">
        <head-menu />
      </a-layout-header>
      
      <a-layout-content class="main-content">
        <div class="content-wrapper">
          <router-view v-slot="{ Component, route }">
            <transition name="fade" mode="out-in">
              <component :is="Component" :key="route.fullPath" />
            </transition>
          </router-view>
        </div>
      </a-layout-content>
      
      <a-layout-footer class="main-footer">
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
  background: var(--card-bg);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--shadow-heavy);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-color);
  position: relative;
  min-height: 300px;
  transition: var(--transition);
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
