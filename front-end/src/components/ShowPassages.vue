<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { message } from 'ant-design-vue'

const passages = ref([])
const loading = ref(true)
const error = ref(false)

const fetchPassages = async () => {
  try {
    loading.value = true
    error.value = false
    const res = await axios.get('/api/passages')
    passages.value = res.data
  } catch (err) {
    console.error('获取文章失败:', err)
    error.value = true
    message.error('无法获取数据')
    // 使用模拟数据
    passages.value = [
      {
        id: 1,
        username: '测试用户',
        content: '这是一篇测试文章内容',
        time: '2024-01-01 12:00:00'
      },
      {
        id: 2,
        username: '另一个用户',
        content: '这是另一篇测试文章内容',
        time: '2024-01-02 14:30:00'
      }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(fetchPassages)
</script>

<template>
  <div class="passages-container">
    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-container">
      <p>加载失败，显示模拟数据</p>
    </div>
    
    <a-card v-else title="最新文章" class="passage-card" bordered>
      <a-list :data-source="passages" :renderItem="null">
        <template #renderItem="{ item }">
          <a-list-item :key="item.id">
            <a-list-item-meta :title="item.username" :description="`发表于：${item.time}`" />
            <div>{{ item.content }}</div>
          </a-list-item>
        </template>
      </a-list>
    </a-card>
  </div>
</template>

<style scoped>
.passages-container {
  width: 100%;
}

.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  gap: 16px;
}

.passage-card {
  max-width: 800px;
  margin: 0 auto;
}
</style>
