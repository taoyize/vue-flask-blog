<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BookOutlined, EyeOutlined, LikeOutlined, FireOutlined } from '@ant-design/icons-vue'
import axios from 'axios'
import { message } from 'ant-design-vue'

const route = useRoute()
const router = useRouter()

const isHot = ref(route.query.type === 'hot')
const loading = ref(false)
const articles = ref([])

// 分页
const currentPage = ref(Number(route.query.page || 1))
const pageSize = ref(10)
const total = ref(0)

const fetchArticles = async () => {
  try {
    loading.value = true
    if (isHot.value) {
      const limit = pageSize.value
      const res = await axios.get(`/api/articles/hot?limit=${limit}`)
      articles.value = res.data || []
      total.value = res.data?.length || 0
    } else {
      const res = await axios.get('/api/articles', {
        params: { page: currentPage.value, per_page: pageSize.value }
      })
      articles.value = res.data?.articles || []
      total.value = res.data?.total || 0
    }
  } catch (err) {
    console.error('获取文章列表失败:', err)
    message.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  const q = { ...route.query, page }
  router.replace({ path: '/articles', query: q })
  fetchArticles()
}

const goDetail = (id) => {
  router.push(`/article/${id}`)
}

watch(() => route.query, (q) => {
  isHot.value = q.type === 'hot'
  currentPage.value = Number(q.page || 1)
  fetchArticles()
})

onMounted(fetchArticles)
</script>

<template>
  <div class="article-list-page">
    <div class="page-header">
      <div class="title">
        <component :is="isHot ? FireOutlined : BookOutlined" class="title-icon" />
        <span>{{ isHot ? '热门文章' : '全部文章' }}</span>
      </div>
    </div>

    <a-spin :spinning="loading">
      <a-list :data-source="articles" item-layout="vertical">
        <template #renderItem="{ item }">
          <a-list-item class="list-item" @click="goDetail(item.id)">
            <a-list-item-meta :title="item.title" :description="item.author" />
            <div class="meta">
              <span class="views"><EyeOutlined /> {{ item.views }}</span>
              <span class="likes"><LikeOutlined /> {{ item.likes_count }}</span>
            </div>
            <div class="excerpt">{{ item.excerpt || (item.content ? item.content.slice(0, 120) + '...' : '') }}</div>
            <div class="tags">
              <a-tag v-for="tag in (item.tags || [])" :key="tag" color="blue">{{ tag }}</a-tag>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </a-spin>

    <div v-if="!isHot" class="pagination">
      <a-pagination
        :current="currentPage"
        :pageSize="pageSize"
        :total="total"
        @change="handlePageChange"
        show-less-items
      />
    </div>
  </div>
  
</template>

<style scoped>
.article-list-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
}

.title-icon {
  color: #667eea;
  font-size: 20px;
}

.list-item {
  cursor: pointer;
}

.list-item:hover {
  background: var(--bg-secondary);
}

.meta {
  display: flex;
  gap: 12px;
  color: var(--text-secondary);
  font-size: 12px;
  margin-bottom: 8px;
  transition: var(--transition);
}

.views, .likes {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.excerpt {
  color: var(--text-secondary);
  margin-bottom: 8px;
  transition: var(--transition);
}

.tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 16px;
}
</style>


