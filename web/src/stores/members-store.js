import { defineStore } from 'pinia'

export const useMemberStore = defineStore('members', {
  state: () => ({
    listMembers: [],
    totalMembers: 0,
    pageSize: 2
  }),

  getters: {
    numberOfPages (state) {
      return Math.ceil(state.totalMembers / state.pageSize)
    }
  },

  actions: {
    fetchMembers (projectId, page, searchText) {
      // const response = this.$api.get('/api/apps')
      const members = [
        {
          id: 1,
          user_id: 'user1',
          name: 'Vuong Le Van',
          email: 'vuonglv@gmail.com',
          role: 'admin',
          description: 'Vuonglv description',
          avatar: 'https://cdn.quasar.dev/img/avatar4.jpg',
          join_at: '2021-01-01 00:00:00'
        },
        {
          id: 2,
          user_id: 'user2',
          name: 'Nguyen Tu Tung',
          email: 'tung24@gmail.com',
          role: 'member',
          description: 'Tungnt description',
          avatar: 'https://cdn.quasar.dev/img/avatar1.jpg',
          join_at: '2021-01-01 00:00:00'
        },
        {
          id: 3,
          user_id: 'user3',
          name: 'Nguyen Tu Tung 2',
          email: 'tung24@gmail.com',
          role: 'admin',
          description: 'Tungnt description',
          avatar: 'https://cdn.quasar.dev/img/avatar2.jpg',
          join_at: '2021-01-01 00:00:00'
        }
      ]
      this.listMembers = members.slice((page - 1) * this.pageSize, page * this.pageSize)
      this.totalMembers = members.length
    }
  }
})
