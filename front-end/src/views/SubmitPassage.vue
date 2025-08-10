<template>
  <div class="submit-container">
    <h1>发布文章</h1>

    <a-form layout="vertical" :model="form" @submit.prevent>
      <a-form-item label="标题" required>
        <a-input v-model:value="title" placeholder="请输入标题" :maxlength="200" />
      </a-form-item>

      <a-form-item label="标签">
        <a-select
          v-model:value="selectedTags"
          mode="tags"
          style="width: 100%"
          :options="tagOptions"
          placeholder="输入或选择标签，按回车确认"
        />
      </a-form-item>

      <a-form-item label="内容" required>
        <a-textarea v-model:value="content" placeholder="请输入正文内容" :rows="10" />
      </a-form-item>

      <a-form-item>
        <a-button type="primary" :loading="submitting" @click="handleSubmit">发布文章</a-button>
      </a-form-item>
    </a-form>

    <a-alert
      v-if="loginWarning"
      message="你还没有登录，请先登录后再发布文章"
      type="warning"
      closable
      @close="loginWarning=false"
    />

    <a-alert
      v-if="successVisible"
      message="发布成功，即将跳转"
      type="success"
      closable
      :after-close="handleClose"
    />
  </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import router from '@/router/index.js'
import { message } from 'ant-design-vue'

const title = ref('')
const content = ref('')
const selectedTags = ref([])
const tagOptions = ref([])
const submitting = ref(false)
const loginWarning = ref(false)
const successVisible = ref(false)

const fetchTags = async () => {
  try {
    const res = await axios.get('/api/tags')
    tagOptions.value = (res.data || []).map((t) => ({ label: t.name, value: t.name }))
  } catch (err) {
    // 忽略失败，用空选项
    tagOptions.value = []
  }
}

onMounted(fetchTags)

const handleSubmit = async () => {
  const userStr = localStorage.getItem('user')
  if (!userStr) {
    loginWarning.value = true
    return
  }

  let user = null
  try { user = JSON.parse(userStr) } catch { user = null }
  if (!user || !user.id) {
    loginWarning.value = true
    return
  }

  if (!title.value.trim()) {
    return message.warning('请输入标题')
  }
  if (!content.value.trim()) {
    return message.warning('请输入内容')
  }

  try {
    submitting.value = true
    const res = await axios.post('/api/articles', {
      title: title.value.trim(),
      content: content.value.trim(),
      author_id: user.id,
      tags: selectedTags.value
    })

    successVisible.value = true
    title.value = ''
    content.value = ''
    selectedTags.value = []

    const newId = res.data?.article?.id
    setTimeout(() => {
      if (newId) {
        router.push(`/article/${newId}`)
      } else {
        router.push('/')
      }
    }, 600)
  } catch (err) {
    console.error('发布文章失败:', err)
    message.error(err.response?.data?.error || '发布文章失败')
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  successVisible.value = false
  router.push('/')
}
</script>

<style scoped>
.submit-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

h1 {
  margin-top: 16px;
  margin-bottom: 24px;
  text-align: center;
}
</style>
