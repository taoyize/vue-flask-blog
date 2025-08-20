<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { UserOutlined, BookOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

const route = useRoute()
const router = useRouter()

const user = ref(null)
const loading = ref(false)
const articles = ref([])

const fetchData = async () => {
  try {
    loading.value = true
    const userId = route.params.id
    const ures = await axios.get(`/api/users/${userId}`)
    user.value = ures.data

    const ares = await axios.get(`/api/users/${userId}/articles`, {
      params: { page: 1, per_page: 10 }
    })
    articles.value = ares.data?.articles || []
  } catch (e) {
    message.error('加载用户资料失败')
  } finally {
    loading.value = false
  }
}

const goDetail = id => router.push(`/article/${id}`)

onMounted(fetchData)
</script>

<template>
  <div class="profile-page">
    <a-spin :spinning="loading">
      <div v-if="user" class="header">
        <a-avatar v-if="user.avatar" :size="80" :src="user.avatar" />
        <a-avatar v-else :size="80">
          <template #icon><UserOutlined /></template>
        </a-avatar>
        <div class="meta">
          <div class="name">{{ user.username }}</div>
          <div class="sub">加入于 {{ user.created_at }}</div>
        </div>
      </div>

      <div class="section">
        <h2 class="section-title"><BookOutlined /> 最近文章</h2>
        <div v-if="articles.length === 0" class="empty">暂无文章</div>
        <div v-else class="list">
          <a-card v-for="a in articles" :key="a.id" class="card" @click="goDetail(a.id)">
            <div class="card-title">{{ a.title }}</div>
            <div class="card-meta">{{ a.created_at }} · ❤ {{ a.likes_count }} · 👁 {{ a.views }}</div>
            <div class="card-excerpt">{{ a.excerpt }}</div>
          </a-card>
        </div>
      </div>
    </a-spin>
  </div>
</template>

<style scoped>
.profile-page { max-width: 900px; margin: 0 auto; padding: 24px; }
.header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
.meta .name { font-size: 20px; font-weight: 700; }
.meta .sub { color: #7f8c8d; font-size: 12px; }
.section { margin-top: 16px; }
.section-title { display: flex; align-items: center; gap: 6px; font-size: 18px; margin: 12px 0; }
.list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
.card { cursor: pointer; }
.card-title { font-weight: 600; margin-bottom: 6px; }
.card-meta { font-size: 12px; color: #7f8c8d; margin-bottom: 8px; }
.card-excerpt { color: #2c3e50; }
.empty { color: #95a5a6; padding: 16px 0; }
</style>
