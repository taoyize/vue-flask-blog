import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css' // 导入主题样式

const app = createApp(App)

app.use(router)

app.use(Antd).mount('#app')
