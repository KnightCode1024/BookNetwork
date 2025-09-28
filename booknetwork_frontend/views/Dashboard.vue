<template>
  <div class="dashboard">
    <h1>Добро пожаловать в Dashboard!</h1>
    <p v-if="authStore.user">Вы вошли как: {{ authStore.user.username }}</p>
    <button @click="handleLogout" class="btn-logout">Выйти</button>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const handleLogout = () => {
      authStore.logout()
      router.push('/login')
    }

    return {
      authStore,
      handleLogout
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  text-align: center;
}

.btn-logout {
  background: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}

.btn-logout:hover {
  background: #c82333;
}
</style>