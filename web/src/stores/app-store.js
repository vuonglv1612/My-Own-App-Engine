import { defineStore } from 'pinia'

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
    fetchApps (projectId, page, searchText) {
      // const response = this.$api.get('/api/apps')
      const apps = [
        {
          id: 1,
          name: 'App 1',
          slug: 'app-1',
          description: 'App 1 description',
          platform: 'python',
          latest_version: '1.0.0',
          status: 'running',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        },
        {
          id: 2,
          name: 'App 2 (with a long name)',
          slug: 'app-2',
          description: 'App 2 description là một app có description rất dài, nhưng hầu như không để làm gì cả," ' +
            '"chỉ để test thôi, không có gì đặc biệt. Nếu viết thêm chắc phải mấy ngày',
          platform: 'python',
          latest_version: '1.0.0',
          status: 'down',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        },
        {
          id: 3,
          name: 'App 3',
          slug: 'app-3',
          description: 'App 3 description',
          platform: 'python',
          status: 'created',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        },
        {
          id: 4,
          name: 'App 4',
          slug: 'app-4',
          description: 'App 4 description',
          platform: 'golang',
          latest_version: '1.2.0',
          status: 'down',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        },
        {
          id: 5,
          name: 'App 5',
          slug: 'app-5',
          description: 'App 5 description',
          platform: 'image',
          latest_version: '1.2.0',
          status: 'running',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        },
        {
          id: 6,
          name: 'App 6',
          slug: 'app-6',
          description: 'App 6 description',
          platform: 'image',
          latest_version: '1.2.0',
          status: 'running',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        },
        {
          id: 7,
          name: 'App 7',
          slug: 'app-7',
          description: 'App 7 description',
          platform: 'python',
          latest_version: '1.2.0',
          status: 'down',
          created_at: '2021-01-01 00:00:00',
          updated_at: '2021-01-01 00:00:00'
        }
      ]
      this.totalApps = apps.length
      this.apps = apps.slice((page - 1) * this.pageSize, page * this.pageSize)
    }
  }
})
