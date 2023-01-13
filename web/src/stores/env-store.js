import { defineStore } from 'pinia'

export const useEnvStore = defineStore('envs', {
  state: () => ({
    envs: []
  }),

  getters: {
  },

  actions: {
    fetchEnvs () {
      const newEnvs = [{ id: 1, name: 'ENV_1', value: '111111', description: 'Development environment' },
        { id: 2, name: 'ENV_2', value: '222222', description: 'Development environment' },
        { id: 3, name: 'ENV_3', value: '333333', description: 'Development environment' }
      ]
      this.envs = newEnvs
    }
  }
})
