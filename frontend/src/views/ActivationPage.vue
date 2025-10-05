<template>
  <div class="activation-page">
    <div class="activation-container">
      <div v-if="loading" class="loading-state">
        <p>Активация аккаунта...</p>
      </div>

      <div v-else-if="success" class="success-state">
        <h2>Аккаунт активирован</h2>
        <p>Вы можете вернуться в приложение</p>
      </div>

      <div v-else class="error-state">
        <h2>Ошибка активации</h2>
        <p>{{ errorMessage }}</p>
        <button @click="retryActivation">Попробовать снова</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

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
      error: false,
      errorMessage: ''
    }
  },
  mounted() {
    this.activateAccount()
  },
  methods: {
    async activateAccount() {
      try {
        this.loading = true
        this.error = false

        await api.post('auth/users/activation/', {
          uid: this.uid,
          token: this.token
        })

        this.success = true
        this.loading = false

      } catch (error) {
        this.loading = false
        this.success = false
        this.error = true

        if (error.response) {
          const status = error.response.status
          switch (status) {
            case 400:
              this.errorMessage = 'Неверные данные активации'
              break
            case 404:
              this.errorMessage = 'Ссылка активации не найдена'
              break
            default:
              this.errorMessage = 'Ошибка сервера'
          }
        } else if (error.request) {
          this.errorMessage = 'Нет соединения с сервером'
        } else {
          this.errorMessage = 'Произошла ошибка'
        }
      }
    },

    retryActivation() {
      this.activateAccount()
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
  background: white;
  padding: 20px;
}

.activation-container {
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.loading-state p {
  font-size: 18px;
  color: #666;
}

.success-state h2 {
  color: #000;
  margin-bottom: 15px;
  font-size: 24px;
}

.success-state p {
  color: #666;
  font-size: 16px;
  line-height: 1.5;
}

.error-state h2 {
  color: #000;
  margin-bottom: 15px;
  font-size: 24px;
}

.error-state p {
  color: #666;
  margin-bottom: 20px;
  font-size: 16px;
}

button {
  border: 1px solid #ddd;
  background: white;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background: #f5f5f5;
}
</style>