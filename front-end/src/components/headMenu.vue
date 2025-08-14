<template>
  <div class="header-container">
    <div class="logo-section">
      <div class="logo" @click="goHome">
        <BookOutlined class="logo-icon" />
        <span class="logo-text">理想主义者</span>
      </div>
    </div>
    
    <a-menu 
      v-model:selectedKeys="current" 
      mode="horizontal" 
      :items="filteredItems" 
      @click="handleClick"
      class="custom-menu"
    />
    
    <div class="header-actions">
      <a-button type="primary" shape="round" size="small" class="action-btn" @click="refreshPage">
        <template #icon><SettingOutlined /></template>
        刷新
      </a-button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { h, ref, watch, nextTick, computed } from 'vue';
import {
  AppstoreOutlined,
  SettingOutlined,
  BookOutlined,
  UserOutlined,
  HomeOutlined,
  PlusOutlined
} from '@ant-design/icons-vue';
import { MenuProps } from 'ant-design-vue';
import { useRouter, useRoute } from "vue-router";

const current = ref<string[]>(['/']);
const route = useRoute();
const router = useRouter();

const items = ref<MenuProps['items']>([
  {
    key: '/',
    label: '主页',
    title: '主页',
    icon: () => h(HomeOutlined),
  },
  {
    key: '/submit',
    label: '发布文章',
    title: '发布文章',
    icon: () => h(PlusOutlined),
  },
  {
    key: '/me',
    label: '我的',
    title: '我的',
    icon: () => h(UserOutlined),
  },
  
  {
    key: '/login',
    icon: () => h(UserOutlined),
    label: '用户登录',
    title: '用户登录',
  },
  {
    key: '/users',
    icon: () => h(AppstoreOutlined),
    label: '用户管理',
    title: '用户管理',
  },
]);

const isAdmin = computed(() => {
  const raw = localStorage.getItem('user')
  try {
    const u = raw ? JSON.parse(raw) : null
    return !!u && Number(u.authority) === 1
  } catch {
    return false
  }
})

const filteredItems = computed<MenuProps['items']>(() => {
  // 非管理员隐藏“用户管理”入口
  return items.value?.filter((it: any) => it?.key !== '/users' || isAdmin.value) || []
})

// 监听路由变化，更新选中状态
watch(() => route.path, (newPath) => {
  current.value = [newPath];
  console.log('路由变化:', newPath);
}, { immediate: true });

const handleClick: MenuProps['onClick'] = async (info) => {
  const path = String(info.key);
  if (route.path !== path) {
    console.log('导航到:', path);
    await router.push(path);
    // 强制更新DOM
    await nextTick();
  }
};

const goHome = async () => {
  await router.push('/');
  await nextTick();
};

const refreshPage = () => {
  window.location.reload();
};
</script>

<style scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 64px;
  max-width: 1200px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 24px;
  color: #667eea;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  letter-spacing: 0.5px;
}

.custom-menu {
  flex: 1;
  justify-content: center;
  background: transparent;
  border: none;
}

.custom-menu :deep(.ant-menu-item) {
  margin: 0 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.custom-menu :deep(.ant-menu-item:hover) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.custom-menu :deep(.ant-menu-item-selected) {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.custom-menu :deep(.ant-menu-item-selected:hover) {
  background: linear-gradient(135deg, #5a6fd8, #6a5acd);
  transform: translateY(-2px);
}

.custom-menu :deep(.ant-menu-item::before) {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.custom-menu :deep(.ant-menu-item:hover::before) {
  width: 80%;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #5a6fd8, #6a5acd);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
    flex-direction: column;
    height: auto;
    gap: 16px;
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .custom-menu {
    width: 100%;
    justify-content: space-around;
  }
  
  .custom-menu :deep(.ant-menu-item) {
    margin: 0 4px;
    padding: 0 8px;
  }
  
  .header-actions {
    width: 100%;
    justify-content: center;
  }
}

/* 添加一些微妙的动画 */
@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-container {
  animation: slideInDown 0.6s ease-out;
}
</style>

