import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    currentUser: {
      id: 'user1',
      name: 'Vuong Le Van'
    }
  }),

  getters: {},

  actions: {}
})
