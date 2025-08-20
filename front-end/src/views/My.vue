<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { UserOutlined, LikeOutlined, BookOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'

const router = useRouter()

const user = ref(null)
const loading = ref(false)

// 资料编辑表单
const profileForm = reactive({
  username: '',
  email: '',
  phone: '',
  avatar: ''
})
const saving = ref(false)

const initProfile = () => {
  if (!user.value) return
  profileForm.username = user.value.username || ''
  profileForm.email = user.value.email || ''
  profileForm.phone = user.value.phone || ''
  profileForm.avatar = user.value.avatar || ''
}

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
  if (!user.value || !user.value.id) {
    message.warning('请先登录')
    router.push({ path: '/login', query: { redirect: '/me' } })
    return false
  }
  initProfile()
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

// 保存资料
const saveProfile = async () => {
  if (!ensureLogin()) return
  try {
    saving.value = true
    const payload = {
      username: profileForm.username?.trim(),
      email: profileForm.email?.trim() || null,
      phone: profileForm.phone?.trim() || '',
      avatar: profileForm.avatar?.trim() || ''
    }
    console.log('[profile] 提交更新 payload:', payload)
    const res = await axios.put(`/api/users/${user.value.id}`, payload)
    console.log('[profile] 更新响应:', res.data)
    // 防止后端中间件缓存或序列化问题，保存后主动拉取一次最新用户信息
    let updated = res.data?.user
    if (!updated) {
      try {
        const fresh = await axios.get(`/api/users/${user.value.id}`)
        updated = fresh.data
        console.log('[profile] 重新获取用户信息:', updated)
      } catch (re) {
        console.warn('[profile] 重新获取用户信息失败:', re)
      }
    }
    if (updated) {
      localStorage.setItem('user', JSON.stringify(updated))
      user.value = updated
      initProfile()
      try { window.dispatchEvent(new CustomEvent('user-updated', { detail: updated })) } catch {}
      message.success('资料已更新')
    } else {
      message.warning('更新成功，但未返回用户信息')
    }
  } catch (e) {
    const msg = e?.response?.data?.error || '更新失败，请稍后重试'
    message.error(msg)
    console.error('[profile] 更新失败:', e)
  } finally {
    saving.value = false
  }
}

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
      <!-- 个人资料已移动至页面底部 -->

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

      <!-- 个人资料（移动到底部） -->
      <div class="section">
        <h2 class="section-title"><UserOutlined /> 个人资料</h2>
        <a-card class="profile-card">
          <div class="profile">
            <div class="left">
              <a-avatar v-if="profileForm.avatar" :size="72" class="avatar" :src="profileForm.avatar" />
              <a-avatar v-else :size="72" class="avatar">
                <template #icon><UserOutlined /></template>
              </a-avatar>
            </div>
            <div class="right">
              <a-form layout="vertical">
                <div class="grid">
                  <a-form-item label="昵称（用户名）">
                    <a-input v-model:value="profileForm.username" placeholder="请输入昵称" allow-clear />
                  </a-form-item>
                  <a-form-item label="邮箱">
                    <a-input v-model:value="profileForm.email" placeholder="请输入邮箱（可选）" allow-clear />
                  </a-form-item>
                </div>
                <div class="grid">
                  <a-form-item label="手机号">
                    <a-input v-model:value="profileForm.phone" placeholder="请输入手机号（可选）" allow-clear />
                  </a-form-item>
                  <a-form-item label="头像URL">
                    <a-input v-model:value="profileForm.avatar" placeholder="请输入头像图片URL（可选）" allow-clear />
                  </a-form-item>
                </div>
                <div class="actions">
                  <a-button type="primary" :loading="saving" @click="saveProfile">保存资料</a-button>
                </div>
              </a-form>
            </div>
          </div>
        </a-card>
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

.profile-card { margin-bottom: 8px; }
.profile { display: flex; gap: 16px; align-items: flex-start; }
.profile .left { flex: 0 0 auto; }
.profile .right { flex: 1; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.actions { margin-top: 4px; }
</style>


