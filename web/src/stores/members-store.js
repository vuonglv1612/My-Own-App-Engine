import { defineStore } from 'pinia'
import { auth0 } from 'app/auth0'
import { api } from 'boot/axios'

export const useMemberStore = defineStore('members', {
  state: () => ({
    listMembers: [],
    totalMembers: 0,
    pageSize: 10
  }),

  getters: {
    numberOfPages (state) {
      return Math.ceil(state.totalMembers / state.pageSize)
    }
  },

  actions: {
    fetchMembers (projectId, page, searchText, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const url = '/projects/' + projectId + '/members'
          const params = {
            page,
            page_size: this.pageSize
          }
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.get(url, { params, headers }).then(
            response => {
              this.listMembers = response.data.items.map(member => {
                return {
                  id: member.id,
                  user_id: member.user_id,
                  name: member.user.name,
                  email: member.user.email,
                  role: member.role,
                  join_at: member.created_at
                }
              })
              this.totalMembers = response.data.meta.total
              callback()
            }
          )
            .catch(error => {
              console.log(error)
              callback()
            })
        })
    },
    addMember (projectId, email, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const url = '/projects/' + projectId + '/members'
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.post(url, { email }, { headers }).then(
            response => {
              callback(null, response)
            }
          )
            .catch(error => {
              callback(error, null)
            })
        }
      )
    },
    deleteMember (projectId, userId, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const url = '/projects/' + projectId + '/members/' + userId
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.delete(url, { headers }).then(
            response => {
              callback(null, response)
            }
          )
            .catch(error => {
              callback(error, null)
            })
        }
      )
    },
    updateMember (projectId, userId, role, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const url = '/projects/' + projectId + '/members/' + userId
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.put(url, { role }, { headers }).then(
            response => {
              callback(null, response)
            }
          )
            .catch(error => {
              callback(error, null)
            })
        }
      )
    },
    deleteProject (projectId, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const url = '/projects/' + projectId
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.delete(url, { headers }).then(
            response => {
              callback(null, response)
            }
          )
            .catch(error => {
              callback(error, null)
            })
        }
      )
    },
    leaveProject (projectId, callback) {
      auth0.getAccessTokenSilently().then(
        token => {
          const url = '/projects/' + projectId + '/members/me'
          const headers = {
            Authorization: 'Bearer ' + token
          }
          api.delete(url, { headers }).then(
            response => {
              callback(null, response)
            })
            .catch(error => {
              callback(error, null)
            }
            )
        })
    }
  }
})
