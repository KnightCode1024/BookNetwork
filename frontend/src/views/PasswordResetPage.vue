<template>
  <div class="password-reset-page">
    <div class="container">
      <div class="card">
        <div class="card-header">
          <h1>Сброс пароля</h1>
        </div>
        
        <!-- Форма запроса сброса пароля -->
        <div v-if="!emailSent && !showResetForm" class="card-body">
          <p class="description">
            Введите ваш email адрес, и мы вышлем вам ссылку для сброса пароля.
          </p>
          
          <form @submit.prevent="requestPasswordReset" class="reset-form">
            <div class="form-group">
              <label for="email">Email адрес</label>
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
            
            <button 
              type="submit" 
              class="btn btn-primary"
              :disabled="loading"
            >
              <span v-if="loading">Отправка...</span>
              <span v-else>Отправить ссылку для сброса</span>
            </button>
          </form>
          
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
        
        <!-- Форма установки нового пароля -->
        <div v-if="showResetForm" class="card-body">
          <p class="description">
            Введите ваш новый пароль.
          </p>
          
          <form @submit.prevent="confirmPasswordReset" class="reset-form">
            <div class="form-group">
              <label for="newPassword">Новый пароль</label>
              <input
                id="newPassword"
                v-model="newPassword"
                type="password"
                required
                placeholder="Введите новый пароль"
                :class="{ 'error': passwordError }"
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
                placeholder="Подтвердите новый пароль"
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
              <span v-if="loading">Сброс пароля...</span>
              <span v-else>Установить новый пароль</span>
            </button>
          </form>
          
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
            <router-link to="/login" class="login-link">Войти в аккаунт</router-link>
          </div>
          
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </div>
        
        <!-- Сообщение после отправки email -->
        <div v-if="emailSent && !showResetForm" class="card-body">
          <div class="success-message">
            <h3>Письмо отправлено!</h3>
            <p>Мы отправили ссылку для сброса пароля на адрес <strong>{{ email }}</strong></p>
            <p>Пожалуйста, проверьте вашу почту и перейдите по ссылке в письме.</p>
            <button @click="resetForm" class="btn btn-secondary">
              Отправить еще раз
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'PasswordResetPage',
  props: {
    uid: {
      type: String,
      default: ''
    },
    token: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      email: '',
      newPassword: '',
      confirmPassword: '',
      loading: false,
      emailSent: false,
      showResetForm: false,
      emailError: '',
      passwordError: '',
      confirmPasswordError: '',
      errorMessage: '',
      successMessage: '',
      passwordsMatch: false
    }
  },
  mounted() {
    // Если есть uid и token в параметрах маршрута, показываем форму сброса
    if (this.uid && this.token) {
      this.showResetForm = true
    }
  },
  methods: {
    async requestPasswordReset() {
      if (!this.validateEmail()) {
        return
      }

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        await api.post('/auth/users/reset_password/', {
          email: this.email
        })
        
        this.emailSent = true
        this.successMessage = 'Ссылка для сброса пароля отправлена на ваш email'
      } catch (error) {
        console.error('Password reset request error:', error)
        this.errorMessage = this.getErrorMessage(error)
      } finally {
        this.loading = false
      }
    },

    async confirmPasswordReset() {
      if (!this.validatePasswords()) {
        return
      }

      this.loading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        await api.post('/auth/users/reset_password_confirm/', {
          uid: this.uid,
          token: this.token,
          new_password: this.newPassword
        })
        
        this.successMessage = 'Пароль успешно изменен! Теперь вы можете войти в систему с новым паролем.'
        this.showResetForm = false
      } catch (error) {
        console.error('Password reset confirmation error:', error)
        this.errorMessage = this.getErrorMessage(error)
      } finally {
        this.loading = false
      }
    },

    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.email)) {
        this.emailError = 'Пожалуйста, введите корректный email адрес'
        return false
      }
      this.emailError = ''
      return true
    },

    validatePasswords() {
      let isValid = true

      if (this.newPassword.length < 8) {
        this.passwordError = 'Пароль должен содержать минимум 8 символов'
        isValid = false
      } else {
        this.passwordError = ''
      }

      if (this.newPassword !== this.confirmPassword) {
        this.confirmPasswordError = 'Пароли не совпадают'
        isValid = false
      } else {
        this.confirmPasswordError = ''
      }

      return isValid
    },

    validatePasswordMatch() {
      if (this.confirmPassword && this.newPassword !== this.confirmPassword) {
        this.confirmPasswordError = 'Пароли не совпадают'
        this.passwordsMatch = false
      } else {
        this.confirmPasswordError = ''
        this.passwordsMatch = true
      }
    },

    clearErrors() {
      this.emailError = ''
      this.errorMessage = ''
    },

    resetForm() {
      this.emailSent = false
      this.email = ''
      this.errorMessage = ''
      this.successMessage = ''
    },

    getErrorMessage(error) {
      if (error.response?.data) {
        const data = error.response.data
        // Обработка различных форматов ошибок от Djoser
        if (data.email) {
          return data.email[0]
        } else if (data.new_password) {
          return data.new_password[0]
        } else if (data.uid) {
          return 'Неверная ссылка для сброса пароля'
        } else if (data.token) {
          return 'Неверный токен для сброса пароля'
        } else if (data.detail) {
          return data.detail
        } else if (typeof data === 'string') {
          return data
        }
      }
      return 'Произошла ошибка. Пожалуйста, попробуйте еще раз.'
    }
  }
}
</script>

<style scoped>
.password-reset-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  width: 100%;
  max-width: 450px;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.card-header {
  background: #4f46e5;
  color: white;
  padding: 30px;
  text-align: center;
}

.card-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.card-body {
  padding: 40px;
}

.description {
  text-align: center;
  color: #6b7280;
  margin-bottom: 30px;
  line-height: 1.5;
}

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 8px;
}

input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #4f46e5;
}

input.error {
  border-color: #ef4444;
}

.error-text {
  color: #ef4444;
  font-size: 14px;
  margin-top: 5px;
}

.btn {
  padding: 14px 20px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  text-decoration: none;
  display: block;
}

.btn-primary {
  background: #4f46e5;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #4338ca;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: #6b7280;
  color: white;
  margin-top: 15px;
}

.btn-secondary:hover {
  background: #4b5563;
}

.success-message {
  background: #d1fae5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
}

.success-message h3 {
  margin-bottom: 10px;
}

.error-message {
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 16px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
}

.login-link {
  display: inline-block;
  margin-top: 15px;
  color: #4f46e5;
  text-decoration: none;
  font-weight: 500;
}

.login-link:hover {
  text-decoration: underline;
}
</style>