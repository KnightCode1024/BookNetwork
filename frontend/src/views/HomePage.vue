<template>
  <div class="home-page">
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <h2>BookNetwork</h2>
        </div>
        <div class="nav-menu">
          <template v-if="isAuthenticated">
            <span class="user-info">Привет, {{ user.username }}!</span>
            <button @click="logout" class="btn btn-secondary">Выйти</button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-primary">Войти</router-link>
            <router-link to="/register" class="btn btn-outline">Регистрация</router-link>
          </template>
        </div>
      </div>
    </nav>

    <main class="main-content">
      <div class="container">
        <div v-if="isAuthenticated" class="welcome-section">
          <h1>Добро пожаловать в BookNetwork!</h1>
          <p>Вы успешно авторизованы в системе.</p>
        </div>
        <div v-else class="welcome-section">
          <h1>Добро пожаловать в BookNetwork!</h1>
          <p>Платформа для обмена книгами и обсуждения литературы.</p>
          <div class="auth-buttons">
            <router-link to="/login" class="btn btn-primary">Войти</router-link>
            <router-link to="/register" class="btn btn-outline">Зарегистрироваться</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      user: null
    }
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('access_token')
    }
  },
  mounted() {
    this.loadUser()
  },
  methods: {
    async loadUser() {
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          // Здесь можно загрузить данные пользователя
          // Пока используем данные из localStorage или дефолтные
          this.user = {
            username: localStorage.getItem('username') || 'Пользователь'
          }
        } catch (error) {
          console.error('Error loading user:', error)
          this.logout()
        }
      }
    },

    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('username')
      this.user = null
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 0;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.nav-brand h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info {
  color: #666;
  font-weight: 500;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.3s;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.main-content {
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.welcome-section h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 15px;
}

.welcome-section p {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

.auth-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.auth-buttons .btn {
  padding: 12px 24px;
  font-size: 16px;
}
</style>
