<template>
  <div class="login-page">
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h1>Вход в систему</h1>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="login" class="login-form">
            <div class="form-group">
              <label for="email">Email</label>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                placeholder="Введите ваш email"
                :class="{ 'error': emailError }"
                @input="clearErrors"
              >
              <span v-if="emailError" class="error-text">{{ emailError }}</span>
            </div>
            
            <div class="form-group">
              <label for="password">Пароль</label>
              <input
                id="password"
                v-model="password"
                type="password"
                required
                placeholder="Введите пароль"
                :class="{ 'error': passwordError }"
                @input="clearErrors"
              >
              <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="loading"
            >
              <span v-if="loading">Вход...</span>
              <span v-else>Войти</span>
            </button>
          </form>
          
          <div class="links">
            <router-link to="/register" class="link">Нет аккаунта? Зарегистрироваться</router-link>
            <router-link to="/password-reset" class="link">Забыли пароль?</router-link>
          </div>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      emailError: '',
      passwordError: '',
      errorMessage: ''
    }
  },
  methods: {
    async login() {
      if (!this.validateForm()) {
        return
      }

      this.loading = true
      this.errorMessage = ''

      try {
        const response = await api.post('/auth/jwt/create/', {
          email: this.email,
          password: this.password
        })
        
        // Сохраняем токены
        localStorage.setItem('access_token', response.data.access)
        localStorage.setItem('refresh_token', response.data.refresh)

        this.$router.push('/')
      } catch (error) {
        console.error('Login error:', error)
        this.errorMessage = this.getErrorMessage(error)
      } finally {
        this.loading = false
      }
    },

    validateForm() {
      let isValid = true

      if (!this.email) {
        this.emailError = 'Email обязателен'
        isValid = false
      } else {
        this.emailError = ''
      }

      if (!this.password) {
        this.passwordError = 'Пароль обязателен'
        isValid = false
      } else {
        this.passwordError = ''
      }

      return isValid
    },

    clearErrors() {
      this.emailError = ''
      this.passwordError = ''
      this.errorMessage = ''
    },

    getErrorMessage(error) {
      if (error.response?.data) {
        const data = error.response.data
        if (data.detail) {
          return data.detail
        } else if (data.non_field_errors) {
          return data.non_field_errors[0]
        }
      }
      return 'Произошла ошибка при входе в систему'
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #f5f5f5;
}

.container {
  width: 100%;
  max-width: 400px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.card-header h1 {
  margin: 0;
  font-size: 24px;
  color: #333;
  text-align: center;
}

.card-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-group input.error {
  border-color: #dc3545;
}

.error-text {
  color: #dc3545;
  font-size: 14px;
  margin-top: 5px;
  display: block;
}

.btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.links {
  margin-top: 20px;
  text-align: center;
}

.link {
  display: block;
  color: #007bff;
  text-decoration: none;
  margin-bottom: 10px;
}

.link:hover {
  text-decoration: underline;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  text-align: center;
}
</style>
