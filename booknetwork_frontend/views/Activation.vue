<template>
  <div class="activation-container">
    <div v-if="loading" class="loading">
      Активация аккаунта...
    </div>
    
    <div v-else-if="success" class="success">
      <h2>✅ Аккаунт успешно активирован!</h2>
      <p>Теперь вы можете войти в систему.</p>
      <button @click="goToLogin" class="btn-primary">
        Перейти к входу
      </button>
    </div>
    
    <div v-else-if="error" class="error">
      <h2>❌ Ошибка активации</h2>
      <p>{{ error }}</p>
      <button @click="goToLogin" class="btn-secondary">
        Попробовать войти
      </button>
    </div>
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import { authAPI } from '@/api/auth'

export default {
  name: 'Activation',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(true)
    const success = ref(false)
    const error = ref('')

    const activateAccount = async () => {
      try {
        // Получаем uid и token из URL
        const uid = route.params.uid
        const token = route.params.token

        console.log('Активация аккаунта:', { uid, token })

        // Отправляем запрос активации
        await authAPI.activate(uid, token)
        
        success.value = true
        console.log('✅ Аккаунт успешно активирован')
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка активации аккаунта'
        console.error('❌ Ошибка активации:', err)
      } finally {
        loading.value = false
      }
    }

    const goToLogin = () => {
      router.push('/login')
    }

    onMounted(() => {
      activateAccount()
    })

    return {
      loading,
      success,
      error,
      goToLogin
    }
  }
}
</script>

<style scoped>
.activation-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  text-align: center;
}

.loading {
  font-size: 18px;
  color: #666;
}

.success {
  color: #28a745;
}

.error {
  color: #dc3545;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-secondary {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary:hover {
  background: #545b62;
}
</style>