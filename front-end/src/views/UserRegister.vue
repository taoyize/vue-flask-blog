<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { UserOutlined, LockOutlined, MailOutlined, PhoneOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import axios from 'axios'

const router = useRouter()

const formRef = ref()
const loading = ref(false)

const formState = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value) => {
        if (value !== formState.password) {
          return Promise.reject('两次输入的密码不一致')
        }
        return Promise.resolve()
      },
      trigger: 'blur'
    }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
    loading.value = true
    
    // 准备注册数据
    const registerData = {
      username: formState.username,
      password: formState.password
    }
    
    // 如果填写了邮箱，则添加到注册数据中
    if (formState.email.trim()) {
      registerData.email = formState.email.trim()
    }
    
    // 如果填写了手机号，则添加到注册数据中
    if (formState.phone.trim()) {
      registerData.phone = formState.phone.trim()
    }
    
    // 调用注册API
    const response = await axios.post('/api/register', registerData)
    
    if (response.data) {
      message.success('注册成功！欢迎加入理想主义者社区')
      router.push('/login')
    }
    
  } catch (error) {
    console.error('注册失败:', error)
    if (error.response?.data?.error) {
      message.error(error.response.data.error)
    } else {
      message.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}

const handleLogin = () => {
  router.push('/login')
}

const handleBack = () => {
  router.back()
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <!-- 返回按钮 -->
      <div class="back-button" @click="handleBack">
        <span>← 返回</span>
      </div>
      
      <!-- 注册表单 -->
      <div class="form-header">
        <h1 class="form-title">加入理想主义者</h1>
        <p class="form-subtitle">创建您的账户，开始分享您的想法</p>
      </div>
      
      <a-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        layout="vertical"
        class="register-form"
      >
        <a-form-item label="用户名" name="username">
          <a-input
            v-model:value="formState.username"
            placeholder="请输入用户名"
            size="large"
          >
            <template #prefix>
              <UserOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item label="邮箱地址（可选）" name="email">
          <a-input
            v-model:value="formState.email"
            placeholder="请输入邮箱地址（可选）"
            size="large"
          >
            <template #prefix>
              <MailOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item label="手机号码（可选）" name="phone">
          <a-input
            v-model:value="formState.phone"
            placeholder="请输入手机号码（可选）"
            size="large"
          >
            <template #prefix>
              <PhoneOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item label="密码" name="password">
          <a-input-password
            v-model:value="formState.password"
            placeholder="请输入密码"
            size="large"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>
        
        <a-form-item label="确认密码" name="confirmPassword">
          <a-input-password
            v-model:value="formState.confirmPassword"
            placeholder="请再次输入密码"
            size="large"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>
        
        <a-form-item>
          <a-button
            type="primary"
            html-type="submit"
            size="large"
            :loading="loading"
            @click="handleSubmit"
            class="submit-btn"
            block
          >
            {{ loading ? '注册中...' : '立即注册' }}
          </a-button>
        </a-form-item>
      </a-form>
      
      <!-- 登录链接 -->
      <div class="login-link">
        已有账户？
        <a @click="handleLogin" class="link-text">立即登录</a>
      </div>
      
      <!-- 用户协议 -->
      <div class="agreement">
        <p class="agreement-text">
          注册即表示您同意我们的
          <a class="link-text">用户协议</a>
          和
          <a class="link-text">隐私政策</a>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 24px;
}

.register-card {
  width: 480px;
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

.register-form {
  margin-bottom: 24px;
}

.register-form :deep(.ant-form-item-label > label) {
  font-weight: 600;
  color: #2c3e50;
}

.register-form :deep(.ant-input),
.register-form :deep(.ant-input-password) {
  border-radius: 12px;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
  height: 48px;
}

.register-form :deep(.ant-input:focus),
.register-form :deep(.ant-input-password:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.register-form :deep(.ant-input-prefix) {
  color: #7f8c8d;
  margin-right: 8px;
}

.submit-btn {
  height: 48px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #5a6fd8, #6a5acd);
}

.login-link {
  text-align: center;
  margin-bottom: 16px;
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

.agreement {
  text-align: center;
}

.agreement-text {
  font-size: 12px;
  color: #95a5a6;
  margin: 0;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    padding: 16px;
  }
  
  .register-card {
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
}

/* 添加进入动画 */
.register-card {
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
