import { ref, onMounted } from 'vue'

// 主题类型
export const THEME_TYPES = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto'
}

// 组合式函数
export function useTheme() {
  // 主题状态 - 每个组件实例独立
  const currentTheme = ref(THEME_TYPES.LIGHT)
  const isDark = ref(false)

  // 从localStorage获取保存的主题
  const getStoredTheme = () => {
    try {
      const stored = localStorage.getItem('theme')
      console.log('从 localStorage 获取主题:', stored)
      return stored || THEME_TYPES.LIGHT
    } catch (error) {
      console.error('获取存储主题失败:', error)
      return THEME_TYPES.LIGHT
    }
  }

  // 保存主题到localStorage
  const saveTheme = (theme) => {
    try {
      localStorage.setItem('theme', theme)
    } catch (error) {
      console.error('保存主题失败:', error)
    }
  }

  // 应用主题到DOM
  const applyTheme = (theme) => {
    const root = document.documentElement
    const body = document.body
    
    // 移除所有主题类
    root.classList.remove('theme-light', 'theme-dark')
    body.classList.remove('theme-light', 'theme-dark')
    
    // 根据主题类型应用相应的类
    if (theme === THEME_TYPES.DARK || 
        (theme === THEME_TYPES.AUTO && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      root.classList.add('theme-dark')
      body.classList.add('theme-dark')
      isDark.value = true
      console.log('应用暗色主题')
    } else {
      root.classList.add('theme-light')
      body.classList.add('theme-light')
      isDark.value = false
      console.log('应用亮色主题')
    }
  }

  // 切换主题
  const toggleTheme = () => {
    console.log('切换主题，当前主题:', currentTheme.value)
    console.log('切换前 isDark 状态:', isDark.value)
    
    const newTheme = currentTheme.value === THEME_TYPES.LIGHT ? THEME_TYPES.DARK : THEME_TYPES.LIGHT
    console.log('新主题:', newTheme)
    
    setTheme(newTheme)
    
    console.log('切换后 isDark 状态:', isDark.value)
  }

  // 设置主题
  const setTheme = (theme) => {
    console.log('设置主题:', theme)
    console.log('设置前 currentTheme:', currentTheme.value)
    console.log('设置前 isDark:', isDark.value)
    
    currentTheme.value = theme
    applyTheme(theme)
    saveTheme(theme)
    
    console.log('设置后 currentTheme:', currentTheme.value)
    console.log('设置后 isDark:', isDark.value)
  }

  // 获取系统主题偏好
  const getSystemTheme = () => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? THEME_TYPES.DARK : THEME_TYPES.LIGHT
  }

  // 监听系统主题变化
  const watchSystemTheme = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    
    const handleChange = (e) => {
      if (currentTheme.value === THEME_TYPES.AUTO) {
        applyTheme(THEME_TYPES.AUTO)
      }
    }
    
    mediaQuery.addEventListener('change', handleChange)
    
    // 返回清理函数
    return () => mediaQuery.removeEventListener('change', handleChange)
  }

  // 初始化主题
  onMounted(() => {
    const storedTheme = getStoredTheme()
    console.log('初始化主题:', storedTheme)
    console.log('初始化前 isDark 状态:', isDark.value)
    
    // 先设置主题类型
    currentTheme.value = storedTheme
    // 然后应用主题
    applyTheme(storedTheme)
    
    console.log('初始化后 isDark 状态:', isDark.value)
    console.log('初始化后 currentTheme:', currentTheme.value)
    
    // 监听系统主题变化
    watchSystemTheme()
  })
  
  return {
    currentTheme,
    isDark,
    toggleTheme,
    setTheme,
    getSystemTheme,
    THEME_TYPES
  }
}
