<template>
  <div class="register-page">
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h1>Регистрация</h1>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="register" class="register-form">
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
              <label for="username">Имя пользователя</label>
              <input
                id="username"
                v-model="username"
                type="text"
                required
                placeholder="Введите имя пользователя"
                :class="{ 'error': usernameError }"
                @input="clearErrors"
              >
              <span v-if="usernameError" class="error-text">{{ usernameError }}</span>
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
                minlength="8"
              >
              <span v-if="passwordError" class="error-text">{{ passwordError }}</span>
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">Подтвердите пароль</label>
              <input
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                required
                placeholder="Подтвердите пароль"
                :class="{ 'error': confirmPasswordError }"
                @input="validatePasswordMatch"
              >
              <span v-if="confirmPasswordError" class="error-text">{{ confirmPasswordError }}</span>
            </div>
            
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="loading || !passwordsMatch"
            >
              <span v-if="loading">Регистрация...</span>
              <span v-else>Зарегистрироваться</span>
            </button>
          </form>
          
          <div class="links">
            <router-link to="/login" class="link">Уже есть аккаунт? Войти</router-link>
          </div>
          
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
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
  name: 'RegisterPage',
  data() {
    return {
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
      loading: false,
      emailError: '',
      usernameError: '',
      passwordError: '',
      confirmPasswordError: '',
      errorMessage: '',
      successMessage: '',
      passwordsMatch: false
    }
  },
  methods: {
    async register() {
      if (!this.validateForm()) {
        return
      }

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        await api.post('/auth/users/', {
          email: this.email,
          username: this.username,
          password: this.password
        })
        
        this.successMessage = 'Регистрация успешна! Проверьте вашу почту для активации аккаунта.'
        this.clearForm()
      } catch (error) {
        console.error('Registration error:', error)
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
      } else if (!this.isValidEmail(this.email)) {
        this.emailError = 'Введите корректный email'
        isValid = false
      } else {
        this.emailError = ''
      }

      if (!this.username) {
        this.usernameError = 'Имя пользователя обязательно'
        isValid = false
      } else if (this.username.length < 3) {
        this.usernameError = 'Имя пользователя должно содержать минимум 3 символа'
        isValid = false
      } else {
        this.usernameError = ''
      }

      if (!this.password) {
        this.passwordError = 'Пароль обязателен'
        isValid = false
      } else if (this.password.length < 8) {
        this.passwordError = 'Пароль должен содержать минимум 8 символов'
        isValid = false
      } else {
        this.passwordError = ''
      }

      if (!this.confirmPassword) {
        this.confirmPasswordError = 'Подтверждение пароля обязательно'
        isValid = false
      } else if (this.password !== this.confirmPassword) {
        this.confirmPasswordError = 'Пароли не совпадают'
        isValid = false
      } else {
        this.confirmPasswordError = ''
      }

      return isValid
    },

    validatePasswordMatch() {
      if (this.confirmPassword && this.password !== this.confirmPassword) {
        this.confirmPasswordError = 'Пароли не совпадают'
        this.passwordsMatch = false
      } else {
        this.confirmPasswordError = ''
        this.passwordsMatch = true
      }
    },

    isValidEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return emailRegex.test(email)
    },

    clearErrors() {
      this.emailError = ''
      this.usernameError = ''
      this.passwordError = ''
      this.confirmPasswordError = ''
      this.errorMessage = ''
    },

    clearForm() {
      this.email = ''
      this.username = ''
      this.password = ''
      this.confirmPassword = ''
      this.passwordsMatch = false
    },

    getErrorMessage(error) {
      if (error.response?.data) {
        const data = error.response.data
        if (data.email) {
          return `Email: ${data.email[0]}`
        } else if (data.username) {
          return `Имя пользователя: ${data.username[0]}`
        } else if (data.password) {
          return `Пароль: ${data.password[0]}`
        } else if (data.detail) {
          return data.detail
        }
      }
      return 'Произошла ошибка при регистрации'
    }
  }
}
</script>

<style scoped>
.register-page {
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

.success-message {
  margin-top: 15px;
  padding: 10px;
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 4px;
  text-align: center;
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
