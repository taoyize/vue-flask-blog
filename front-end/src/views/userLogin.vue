<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'

const name = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const router = useRouter()

const handleLogin = async () => {
  if (!name.value || !password.value) {
    error.value = '请输入用户名和密码'
    return
  }
  try {
    loading.value = true
    error.value = ''
    
    const res = await axios.post('/api/login', {
      username: name.value,
      password: password.value
    })
    
    if (res.data.code === 200) {
      const userInfo = res.data.user
      localStorage.setItem('user', JSON.stringify(userInfo))
      router.push('/')
      console.log('登录成功')
    } else {
      error.value = res.data.message
      console.warn('登录失败:', error.value)
    }
  } catch (err) {
    error.value = '登录请求失败，请稍后重试'
    console.error('异常:', err)
  } finally {
    loading.value = false
  }
}

const handleRegister = () => {
  router.push('/register')
}

const handleBack = () => {
  router.back()
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <!-- 返回按钮 -->
      <div class="back-button" @click="handleBack">
        <span>← 返回</span>
      </div>
      
      <!-- 登录表单 -->
      <div class="form-header">
        <h1 class="form-title">欢迎回来</h1>
        <p class="form-subtitle">登录您的账户，继续您的创作之旅</p>
      </div>
      
      <a-form layout="vertical" class="login-form">
        <a-form-item label="用户名">
          <a-input
            v-model:value="name"
            placeholder="请输入用户名"
            size="large"
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <UserOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item label="密码">
          <a-input-password
            v-model:value="password"
            placeholder="请输入密码"
            size="large"
            @keyup.enter="handleLogin"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>
        
        <a-form-item>
          <a-button
            type="primary"
            @click="handleLogin"
            :loading="loading"
            size="large"
            class="login-btn"
            block
          >
            {{ loading ? '登录中...' : '登录' }}
          </a-button>
        </a-form-item>

        <!-- 错误提示 -->
        <a-alert
          v-if="error"
          :message="error"
          type="error"
          show-icon
          closable
          class="error-alert"
        />
      </a-form>
      
      <!-- 注册链接 -->
      <div class="register-link">
        还没有账户？
        <a @click="handleRegister" class="link-text">立即注册</a>
      </div>
      
      <!-- 其他登录方式 -->
      <div class="other-login">
        <div class="divider">
          <span>或</span>
        </div>
        
        <div class="social-login">
          <a-button class="social-btn wechat">
            <template #icon>
              <span class="social-icon">微信</span>
            </template>
            微信登录
          </a-button>
          
          <a-button class="social-btn qq">
            <template #icon>
              <span class="social-icon">QQ</span>
            </template>
            QQ登录
          </a-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px;
}

.login-card {
  width: 420px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
}

.back-button {
  position: absolute;
  top: 20px;
  left: 20px;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.back-button:hover {
  transform: translateX(-4px);
}

.form-header {
  text-align: center;
  margin-bottom: 32px;
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-subtitle {
  color: #7f8c8d;
  font-size: 16px;
  margin: 0;
}

.login-form {
  margin-bottom: 24px;
}

.login-form :deep(.ant-form-item-label > label) {
  font-weight: 600;
  color: #2c3e50;
}

.login-form :deep(.ant-input) {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
  height: 48px;
}

.login-form :deep(.ant-input:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.login-form :deep(.ant-input-prefix) {
  color: #7f8c8d;
  margin-right: 8px;
}

.login-btn {
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #5a6fd8, #6a5acd);
}

.error-alert {
  margin-top: 16px;
  border-radius: 8px;
}

.register-link {
  text-align: center;
  margin-bottom: 24px;
  color: #7f8c8d;
  font-size: 14px;
}

.link-text {
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.link-text:hover {
  color: #5a6fd8;
  text-decoration: underline;
}

.other-login {
  margin-top: 24px;
}

.divider {
  position: relative;
  text-align: center;
  margin-bottom: 24px;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #e9ecef;
}

.divider span {
  background: rgba(255, 255, 255, 0.95);
  padding: 0 16px;
  color: #7f8c8d;
  font-size: 14px;
}

.social-login {
  display: flex;
  gap: 12px;
}

.social-btn {
  flex: 1;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
  background: white;
  color: #2c3e50;
  font-weight: 500;
  transition: all 0.3s ease;
}

.social-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.social-btn.wechat:hover {
  border-color: #07c160;
  color: #07c160;
}

.social-btn.qq:hover {
  border-color: #12b7f5;
  color: #12b7f5;
}

.social-icon {
  font-size: 12px;
  margin-right: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: 16px;
  }
  
  .login-card {
    width: 100%;
    max-width: 400px;
    padding: 24px;
  }
  
  .form-title {
    font-size: 1.5rem;
  }
  
  .form-subtitle {
    font-size: 14px;
  }
  
  .back-button {
    position: static;
    margin-bottom: 16px;
    text-align: left;
  }
  
  .social-login {
    flex-direction: column;
  }
}

/* 添加进入动画 */
.login-card {
  animation: slideInUp 0.6s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
