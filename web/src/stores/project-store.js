import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import { auth0 } from 'app/auth0'

export const useProjectStore = defineStore('projects', {
  state: () => ({
    projects: null
  }),

  getters: {
    activeProject (state) {
      if (!state.projects) return null
      return state.projects.find(project => project.active)
    },
    listProjects (state) {
      if (!state.projects) return null
      return state.projects
    }
  },

  actions: {
    fetchProjects (callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.get('/users/me/projects', { headers }).then(
            response => {
              const items = response.data.items
              this.projects = items.map(item => {
                return {
                  id: item.id,
                  display_name: item.name,
                  project_name: item.id,
                  active: false
                }
              })
              this.projects[0].active = true
              if (callback) callback()
            }
          )
        })
    },
    setActiveProject (projectName) {
      if (!projectName) {
        this.projects[0].active = true
        return
      }
      this.projects.forEach(project => {
        project.active = project.project_name === projectName
      })
    },
    createProject (projectName, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.post('/projects', { name: projectName }, { headers }).then(
            response => {
              const item = response.data
              this.projects.push({
                id: item.id,
                display_name: item.name,
                project_name: item.id,
                active: false
              })
              if (callback) callback()
            }
          )
        })
    }
  }
})
