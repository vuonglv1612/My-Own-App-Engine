import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import { auth0 } from 'app/auth0'

export const useAppStore = defineStore('appStore', {
  state: () => ({
    apps: null,
    selectedApp: null,
    totalApps: 0,
    pageSize: 5
  }),

  getters: {
    listApps (state) {
      if (!state.apps) return null
      return state.apps
    },
    getSelectedApp (state) {
      if (!state.selectedApp) return null
      return state.selectedApp
    },
    numberOfPages (state) {
      return Math.ceil(state.totalApps / state.pageSize)
    }
  },

  actions: {
    fetchApps (projectId, page, searchText, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.get('/projects/' + projectId + '/apps', {
            params: {
              page,
              page_size: this.pageSize
            },
            headers
          }).then(
            response => {
              this.apps = response.data.items.map(app => {
                return {
                  id: app.id,
                  name: app.name,
                  slug: app.name,
                  platform: app.platform,
                  description: app.description,
                  status: app.status,
                  created_at: app.created_at,
                  updated_at: app.updated_at
                }
              })
              this.totalApps = response.data.meta.total
              callback()
            }
          )
        }
      )
    },
    getApp (projectId, appId, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.get('/projects/' + projectId + '/apps/' + appId, {
          headers
        }).then(
          response => {
            const app = response.data
            api.get('/projects/' + projectId + '/apps/' + appId + '/active-scale', { headers }).then(
              response => {
                const scale = response.data
                const data = {
                  id: app.id,
                  name: app.name,
                  slug: app.name,
                  platform: app.platform,
                  status: app.status,
                  created_at: app.created_at,
                  updated_at: app.updated_at,
                  cpu: scale.unit?.cpu,
                  memory: scale.unit?.memory,
                  replicas: scale.replicas,
                  address: 'https://' + app.name + '.ipaas.site'
                }
                this.selectedApp = data
                callback(data)
              })
          }
        )
      }
      )
    },
    deployApp (projectId, appId, params, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        params = {
          ...params,
          project_id: projectId
        }
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.post('/apps/' + appId + '/deploy', params, { headers }).then(
          response => {
            callback(null, response.data)
          }
        ).catch(
          error => {
            callback(error, null)
          }
        )
      })
    },
    deleteApp (appId, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const url = '/apps/' + appId
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.delete(url, { headers }).then(
          response => {
            return callback(null, response.data)
          }
        ).catch(
          error => {
            return callback(error, null)
          }
        )
      })
    },
    stopApp (appId, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const url = '/apps/' + appId + '/stop'
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.post(url, {}, { headers }).then(
          response => {
            return callback(null, response.data)
          }
        ).catch(
          error => {
            return callback(error, null)
          })
      })
    },
    restartApp (appId, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const url = '/apps/' + appId + '/restart'
        const headers = {
          Authorization: 'Bearer ' + token
        }
        api.post(url, {}, { headers }).then(
          response => {
            return callback(null, response.data)
          }
        ).catch(
          error => {
            return callback(error, null)
          })
      })
    },
    scaleApp (appId, replicas, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const url = '/apps/' + appId + '/scale'
        const headers = {
          Authorization: 'Bearer ' + token
        }
        const params = {
          replicas
        }

        api.post(url, params, { headers }).then(
          response => {
            return callback(null, response.data)
          }
        ).catch(
          error => {
            return callback(error, null)
          }
        )
      })
    }
  }
})
