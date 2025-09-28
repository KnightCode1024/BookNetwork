import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI, tokenUtils } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const accessToken = ref(localStorage.getItem('access_token'))
    const refreshToken = ref(localStorage.getItem('refresh_token'))
    const loading = ref(false)
    const error = ref('')

    const isAuthenticated = computed(() => {
        return !!accessToken.value && tokenUtils.isTokenValid()
    })

    const login = async (credentials) => {
        loading.value = true
        error.value = ''

        try {
            const response = await authAPI.login(credentials)
            const { access, refresh } = response.data

            // Сохраняем токены
            tokenUtils.saveTokens(access, refresh)
            accessToken.value = access
            refreshToken.value = refresh

            // Получаем данные пользователя
            await fetchProfile()

            return { success: true }
        } catch (err) {
            const errorMessage = err.response?.data?.detail || 'Ошибка авторизации'
            error.value = errorMessage
            return { success: false, error: errorMessage }
        } finally {
            loading.value = false
        }
    }

    const fetchProfile = async () => {
        try {
            if (!accessToken.value) return

            const response = await authAPI.getProfile()
            user.value = response.data
        } catch (err) {
            console.error('Ошибка получения профиля:', err)
            logout()
        }
    }

    const logout = () => {
        user.value = null
        accessToken.value = null
        refreshToken.value = null
        tokenUtils.clearTokens()
        error.value = ''
    }

    const refreshTokens = async () => {
        try {
            if (!refreshToken.value) throw new Error('No refresh token')

            const response = await authAPI.refreshToken(refreshToken.value)
            const { access } = response.data

            tokenUtils.saveTokens(access, refreshToken.value)
            accessToken.value = access

            return access
        } catch (err) {
            logout()
            throw err
        }
    }

    // Получение данных из токена
    const getTokenData = () => {
        return tokenUtils.getTokenData()
    }

    // Инициализация при загрузке приложения
    const initialize = async () => {
        if (accessToken.value && tokenUtils.isTokenValid()) {
            await fetchProfile()
        } else if (accessToken.value) {
            // Token истек, пытаемся обновить
            try {
                await refreshTokens()
                await fetchProfile()
            } catch (err) {
                logout()
            }
        }
    }

    return {
        user,
        accessToken,
        refreshToken,
        loading,
        error,
        isAuthenticated,
        login,
        logout,
        fetchProfile,
        refreshTokens,
        getTokenData,
        initialize
    }
})