<template>
  <div class="activation-page">
    <div class="container">
      <div class="card">
        <div class="card-body">
          <div v-if="loading" class="loading">
            <h2>Активация аккаунта...</h2>
            <p>Пожалуйста, подождите</p>
          </div>
          
          <div v-else-if="success" class="success">
            <h2>Аккаунт активирован!</h2>
            <p>Ваш аккаунт успешно активирован. Теперь вы можете войти в систему.</p>
            <router-link to="/login" class="btn btn-primary">Войти в систему</router-link>
          </div>
          
          <div v-else class="error">
            <h2>Ошибка активации</h2>
            <p>{{ errorMessage }}</p>
            <button @click="retryActivation" class="btn btn-secondary">Попробовать снова</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'ActivationPage',
  props: {
    uid: {
      type: String,
      required: true
    },
    token: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      loading: true,
      success: false,
      errorMessage: ''
    }
  },
  async mounted() {
    await this.activateAccount()
  },
  methods: {
    async activateAccount() {
      try {
        await api.post('/auth/users/activation/', {
          uid: this.uid,
          token: this.token
        })
        this.success = true
      } catch (error) {
        console.error('Activation error:', error)
        this.errorMessage = this.getErrorMessage(error)
      } finally {
        this.loading = false
      }
    },
    
    retryActivation() {
      this.loading = true
      this.activateAccount()
    },
    
    getErrorMessage(error) {
      if (error.response?.data) {
        const data = error.response.data
        if (data.detail) {
          return data.detail
        } else if (data.uid) {
          return 'Неверная ссылка активации'
        } else if (data.token) {
          return 'Неверный токен активации'
        }
      }
      return 'Произошла ошибка при активации аккаунта'
    }
  }
}
</script>

<style scoped>
.activation-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #f5f5f5;
}

.container {
  width: 100%;
  max-width: 500px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-body {
  padding: 20px;
  text-align: center;
}

.loading h2,
.success h2,
.error h2 {
  margin-bottom: 15px;
  color: #374151;
}

.loading p,
.success p,
.error p {
  color: #6b7280;
  margin-bottom: 25px;
  line-height: 1.5;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover {
  background: #4338ca;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}
</style>