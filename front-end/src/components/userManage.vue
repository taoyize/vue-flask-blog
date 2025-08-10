<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { message, Modal } from 'ant-design-vue'
import { TeamOutlined } from "@ant-design/icons-vue"

const users = ref([])
const name = ref('')
const email = ref('')
const password = ref('')
const authority = ref(0)
const loading = ref(false)

const fetchUsers = async () => {
  try {
    loading.value = true
    const res = await axios.get('/api/users')
    users.value = res.data
  } catch (err) {
    console.error('加载用户失败:', err)
    message.error('加载用户失败')
  } finally {
    loading.value = false
  }
}

const addUser = async () => {
  if (!name.value.trim()) {
    message.warning('请输入用户名')
    return
  }
  // 邮箱改为可选；如果填写则一并提交
  
  try {
    loading.value = true
    console.log('发送数据:', {
      name: name.value.trim(),
      email: email.value.trim() || undefined,
      password: password.value.trim() || undefined,
      authority: authority.value,
    })
    
    const response = await axios.post('/api/addusers', {
      name: name.value.trim(),
      email: email.value.trim() || undefined,
      password: password.value.trim() || undefined,
      authority: authority.value,
    })
    
    console.log('响应:', response.data)
    message.success('添加成功')
    await fetchUsers()
    
    // 清空表单
    name.value = ''
    email.value = ''
    password.value = ''
    authority.value = 0
    
  } catch (err) {
    console.error('添加用户失败:', err)
    console.error('错误响应:', err.response?.data)
    console.error('错误状态:', err.response?.status)
    
    let errorMsg = '添加失败，请稍后重试'
    if (err.response?.data?.error) {
      errorMsg = err.response.data.error
    } else if (err.response?.status === 400) {
      errorMsg = '请求参数错误，请检查输入'
    } else if (err.response?.status === 500) {
      errorMsg = '服务器内部错误，请稍后重试'
    }
    
    message.error(errorMsg)
  } finally {
    loading.value = false
  }
}

const deleteUser = (id) => {
  Modal.confirm({
    title: '确认删除该用户？',
    content: '删除后无法恢复，请谨慎操作',
    onOk: async () => {
      try {
        await axios.post('/api/deleteusers', { id })
        message.success('删除成功')
        await fetchUsers()
      } catch (err) {
        console.error('删除用户失败:', err)
        const errorMsg = err.response?.data?.error || '删除失败，请稍后重试'
        message.error(errorMsg)
      }
    },
    okText: '删除',
    cancelText: '取消',
    okType: 'danger'
  })
}

onMounted(fetchUsers)
</script>

<template>
  <div class="user-manage-container">
    <a-card title="用户列表" class="mb-4">
      <a-spin :spinning="loading">
        <a-list bordered>
          <a-list-item v-for="user in users" :key="user.id">
            <a-list-item-meta 
              :title="user.username || user.name" 
              :description="user.email" 
            />
            <div class="user-authority">
              <a-tag v-if="user.authority == 1" color="red">管理员</a-tag>
              <a-tag v-else color="blue">普通用户</a-tag>
            </div>
            <template #actions>
              <a-button type="link" danger @click="deleteUser(user.id)">删除</a-button>
            </template>
          </a-list-item>
        </a-list>
      </a-spin>
    </a-card>

    <a-card title="添加用户">
      <template #extra>
        <TeamOutlined />
      </template>
      
      <a-form layout="inline" @submit.prevent>
        <a-form-item label="用户名" required>
          <a-input 
            v-model:value="name" 
            placeholder="请输入用户名" 
            style="width: 200px"
            :disabled="loading"
          />
        </a-form-item>
        
        <a-form-item label="邮箱">
          <a-input 
            v-model:value="email" 
            placeholder="请输入邮箱" 
            style="width: 240px"
            :disabled="loading"
          />
        </a-form-item>

        <a-form-item label="密码">
          <a-input-password
            v-model:value="password"
            placeholder="不填则默认为 123456"
            style="width: 220px"
            :disabled="loading"
          />
        </a-form-item>
        
        <a-form-item label="权限">
          <a-select 
            v-model:value="authority" 
            placeholder="选择权限" 
            style="width: 160px"
            :disabled="loading"
          >
            <a-select-option :value="0">普通用户</a-select-option>
            <a-select-option :value="1">管理员</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item>
          <a-button 
            type="primary" 
            @click="addUser"
            :loading="loading"
            :disabled="!name.trim()"
          >
            添加用户
          </a-button>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<style scoped>
.user-manage-container {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.user-authority {
  margin-right: 16px;
}
</style>
