<template>
  <div v-if="hasError" class="error-overlay">
    <div class="error-modal">
      <h3>页面出现错误</h3>
      <p>{{ errorMessage }}</p>
      <div class="error-actions">
        <a-button type="primary" @click="retry">重试</a-button>
        <a-button @click="goHome" style="margin-left: 12px;">返回首页</a-button>
        <a-button @click="refresh" style="margin-left: 12px;">刷新页面</a-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const hasError = ref(false)
const errorMessage = ref('')

onErrorCaptured((error, instance, info) => {
  console.error('全局错误:', error, info)
  errorMessage.value = error.message || '未知错误'
  hasError.value = true
  return false
})

const retry = () => {
  hasError.value = false
  errorMessage.value = ''
  // 重新加载当前路由
  router.go(0)
}

const goHome = () => {
  hasError.value = false
  errorMessage.value = ''
  router.push('/')
}

const refresh = () => {
  window.location.reload()
}
</script>

<style scoped>
.error-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.error-modal {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  text-align: center;
}

.error-modal h3 {
  color: #ff4d4f;
  margin-bottom: 16px;
}

.error-modal p {
  color: #666;
  margin-bottom: 24px;
}

.error-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}
</style>
