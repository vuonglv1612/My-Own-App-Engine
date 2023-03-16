import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import { auth0 } from 'app/auth0'

export const useEnvStore = defineStore('envs', {
  state: () => ({
    envs: []
  }),

  getters: {},

  actions: {
    fetchEnvs (appId, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        this.envs = []
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.get('/apps/' + appId + '/envs', {
          headers
        }).then(
          (response) => {
            this.envs = response.data.items.map((env) => {
              return {
                id: env.id,
                name: env.name,
                value: env.value
              }
            })
            callback()
          }
        )
      })
    },
    addEnv (appId, env, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const headers = {
          Authorization: 'Bearer ' + token
        }
        const params = {
          name: env.name,
          value: env.value
        }
        api.post('/apps/' + appId + '/envs', params, { headers }).then(
          (response) => {
            callback(null, response)
          }).catch((error) => {
          callback(error, null)
        })
      })
    },
    updateEnv (appId, envId, env, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const headers = {
          Authorization: 'Bearer ' + token
        }
        const params = {
          name: env.name,
          value: env.value
        }
        api.put('/apps/' + appId + '/envs/' + envId, params, { headers }).then(
          (response) => {
            callback(null, response)
          }).catch((error) => {
          callback(error, null)
        })
      })
    },
    deleteEnv (appId, envId, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.delete('/apps/' + appId + '/envs/' + envId, { headers }).then(
          (response) => {
            callback(null, response)
          }).catch((error) => {
          callback(error, null)
        })
      })
    }

  }
})
