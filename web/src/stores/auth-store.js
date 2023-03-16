import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    accessToken: null,
    currentUser: {
      id: 'user1',
      name: 'Vuong Le Van'
    },
    currentAuthUser: null
  }),

  getters: {},

  actions: {
    setCurrentAuthUser (user) {
      this.currentAuthUser = user
    },
    setIsAuthenticated (isAuthenticated) {
      this.isAuthenticated = isAuthenticated
    }
  }
})
