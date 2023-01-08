import { defineStore } from 'pinia'

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
    fetchProjects () {
      // const response = this.$api.get('/api/projects')
      this.projects = [
        { id: 1, display_name: 'Project 1', project_name: 'project-1', active: true },
        { id: 2, display_name: 'Project 2', project_name: 'project-2', active: false },
        { id: 3, display_name: 'Project 3', project_name: 'project-3', active: false },
        { id: 4, display_name: 'Project 4', project_name: 'project-4', active: false }
      ]
    },
    setActiveProject (projectName) {
      this.projects.forEach(project => {
        project.active = project.project_name === projectName
      })
    }
  }
})
