<template>
  <div class="theme-toggle">
    <a-tooltip :title="tooltipText" placement="bottom">
      <a-button
        type="text"
        shape="round"
        size="small"
        class="theme-btn"
        @click="handleToggle"
        :loading="isLoading"
      >
        {{ isDark ? '☀️' : '🌙' }}
      </a-button>
    </a-tooltip>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark, toggleTheme, currentTheme } = useTheme()

// 计算属性
const tooltipText = computed(() => {
  return isDark.value ? '切换到亮色模式' : '切换到暗色模式'
})

const isLoading = computed(() => false) // 可以根据需要添加加载状态

// 调试信息
onMounted(() => {
  console.log('ThemeToggle组件加载，当前主题状态:', isDark.value)
  console.log('当前主题类型:', currentTheme.value)
})

// 监听主题变化
const handleToggle = () => {
  console.log('点击主题切换按钮')
  console.log('切换前主题状态:', isDark.value)
  toggleTheme()
  console.log('切换后主题状态:', isDark.value)
}
</script>

<style scoped>
.theme-toggle {
  display: flex;
  align-items: center;
}

.theme-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  transition: var(--transition);
  box-shadow: var(--shadow-light);
  font-size: 16px;
}

.theme-btn:hover {
  background: var(--primary-color);
  color: white;
  transform: translateY(-2px);
  box-shadow: var(--shadow-medium);
}

/* 暗色主题下的特殊样式 */
.theme-dark .theme-btn {
  background: var(--bg-secondary);
  border-color: var(--border-color);
  color: var(--text-primary);
}

.theme-dark .theme-btn:hover {
  background: var(--primary-color);
  color: white;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .theme-btn {
    width: 36px;
    height: 36px;
    font-size: 14px;
  }
}

/* 动画效果 */
@keyframes themeSwitch {
  0% {
    transform: scale(1) rotate(0deg);
  }
  50% {
    transform: scale(1.1) rotate(180deg);
  }
  100% {
    transform: scale(1) rotate(360deg);
  }
}

.theme-btn:active {
  animation: themeSwitch 0.3s ease-in-out;
}
</style>
