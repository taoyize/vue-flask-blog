<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { UserOutlined, LikeOutlined, BookOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

const router = useRouter()

const user = ref(null)
const loading = ref(false)

// 分页状态
const myArticles = ref([])
const likedArticles = ref([])
const myCurrentPage = ref(1)
const likedCurrentPage = ref(1)
const pageSize = ref(10)
const myTotal = ref(0)
const likedTotal = ref(0)

const ensureLogin = () => {
  const raw = localStorage.getItem('user')
  try { user.value = raw ? JSON.parse(raw) : null } catch { user.value = null }
  if (!user.value) {
    message.warning('请先登录')
    router.push({ path: '/login', query: { redirect: '/me' } })
    return false
  }
  return true
}

const fetchMyArticles = async () => {
  if (!ensureLogin()) return
  try {
    loading.value = true
    console.log('获取用户文章，用户ID:', user.value.id)
    const res = await axios.get(`/api/users/${user.value.id}/articles`, {
      params: { page: myCurrentPage.value, per_page: pageSize.value }
    })
    console.log('我的文章API响应:', res.data)
    myArticles.value = res.data?.articles || []
    myTotal.value = res.data?.total || 0
    console.log('设置我的文章数据:', myArticles.value.length, '篇，总数:', myTotal.value)
  } catch (e) {
    console.error('获取我的文章失败:', e)
    message.error('获取我的文章失败')
  } finally {
    loading.value = false
  }
}

const fetchLikedArticles = async () => {
  if (!ensureLogin()) return
  try {
    loading.value = true
    console.log('获取用户点赞文章，用户ID:', user.value.id)
    const res = await axios.get(`/api/users/${user.value.id}/likes`, {
      params: { page: likedCurrentPage.value, per_page: pageSize.value }
    })
    console.log('点赞文章API响应:', res.data)
    likedArticles.value = res.data?.articles || []
    likedTotal.value = res.data?.total || 0
    console.log('设置点赞文章数据:', likedArticles.value.length, '篇，总数:', likedTotal.value)
  } catch (e) {
    console.error('获取我的点赞失败:', e)
    message.error('获取我的点赞失败')
  } finally {
    loading.value = false
  }
}

const goDetail = (id) => router.push(`/article/${id}`)

onMounted(() => {
  if (!ensureLogin()) return
  fetchMyArticles()
  fetchLikedArticles()
})
</script>

<template>
  <div class="my-page">
    <h1 class="title"><UserOutlined /> 我的</h1>

    <a-spin :spinning="loading">
      <div class="section">
        <h2 class="section-title"><BookOutlined /> 我的文章</h2>
        <div v-if="myArticles.length === 0" class="empty">暂无文章</div>
        <div v-else class="list">
          <a-card v-for="a in myArticles" :key="a.id" class="card" @click="goDetail(a.id)">
            <div class="card-title">{{ a.title }}</div>
            <div class="card-meta">{{ a.created_at }} · ❤ {{ a.likes_count }} · 👁 {{ a.views }}</div>
            <div class="card-excerpt">{{ a.excerpt }}</div>
          </a-card>
        </div>
        <div class="pager" v-if="myTotal > pageSize">
          <a-pagination :current="myCurrentPage" :total="myTotal" :pageSize="pageSize"
                        @change="p => { myCurrentPage = p; fetchMyArticles() }" />
        </div>
      </div>

      <div class="section">
        <h2 class="section-title"><LikeOutlined /> 我的点赞</h2>
        <div v-if="likedArticles.length === 0" class="empty">暂无点赞</div>
        <div v-else class="list">
          <a-card v-for="a in likedArticles" :key="a.id" class="card" @click="goDetail(a.id)">
            <div class="card-title">{{ a.title }}</div>
            <div class="card-meta">{{ a.created_at }} · ❤ {{ a.likes_count }} · 👁 {{ a.views }}</div>
            <div class="card-excerpt">{{ a.excerpt }}</div>
          </a-card>
        </div>
        <div class="pager" v-if="likedTotal > pageSize">
          <a-pagination :current="likedCurrentPage" :total="likedTotal" :pageSize="pageSize"
                        @change="p => { likedCurrentPage = p; fetchLikedArticles() }" />
        </div>
      </div>
    </a-spin>
  </div>
  
</template>

<style scoped>
.my-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}
.title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 16px;
}
.section { margin-top: 16px; }
.section-title { display: flex; align-items: center; gap: 6px; font-size: 18px; margin: 12px 0; }
.list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }
.card { cursor: pointer; }
.card-title { font-weight: 600; margin-bottom: 6px; }
.card-meta { font-size: 12px; color: #7f8c8d; margin-bottom: 8px; }
.card-excerpt { color: #2c3e50; }
.empty { color: #95a5a6; padding: 16px 0; }
.pager { display: flex; justify-content: center; margin-top: 12px; }
</style>


