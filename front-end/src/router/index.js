import { createRouter, createWebHistory } from 'vue-router'
import { message } from 'ant-design-vue'
import Home from "../views/Home.vue"
import userLogin from '../views/userLogin.vue'
import UserManage from "@/views/UserManage.vue";
import SubmitPassage from "@/views/SubmitPassage.vue";
import UserRegister from "@/views/UserRegister.vue";
import ArticleReader from "@/views/ArticleReader.vue";
import ArticleList from "@/views/ArticleList.vue";
import My from "@/views/My.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/me',
      name: 'me',
      component: My,
      meta: { requiresAuth: true }
    },
    {
      path:'/articles',
      name:'articles',
      component: ArticleList,
    },
    {
      path:'/login',
      name:'login',
      component:userLogin
    },
    {
      path:'/register',
      name:'register',
      component:UserRegister
    },
    {
      path:'/users',
      name:'users',
      component:UserManage,
      meta: { requiresAdmin: true }
    },
    {
      path:'/submit',
      name:'submit',
      component:SubmitPassage,
    },
    {
      path:'/article/:id',
      name:'article',
      component:ArticleReader,
    }
  ],
})

// 全局前置守卫：滚动置顶 + 管理员权限校验
router.beforeEach((to, from, next) => {
  window.scrollTo(0, 0);

  // 需要登录的页面
  if (to.meta?.requiresAuth) {
    const raw = localStorage.getItem('user')
    let user = null
    try { user = raw ? JSON.parse(raw) : null } catch (_) { user = null }
    if (!user) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }
  }

  if (to.meta?.requiresAdmin) {
    const raw = localStorage.getItem('user')
    let user = null
    try { user = raw ? JSON.parse(raw) : null } catch (_) { user = null }

    if (!user) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }
    if (Number(user.authority) !== 1) {
      message.error('无权限访问该页面')
      return next('/')
    }
  }

  next()
})

// 全局后置钩子 - 清理可能的缓存问题
router.afterEach((to, from) => {
  // 确保DOM更新完成
  setTimeout(() => {
    // 触发一个小的DOM更新来确保渲染
    const event = new Event('resize');
    window.dispatchEvent(event);
  }, 100);
});

export default router
