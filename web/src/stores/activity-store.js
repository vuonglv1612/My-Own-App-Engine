import { defineStore } from 'pinia'
import { auth0 } from 'app/auth0'
import { api } from 'boot/axios'

const rawActivities = [
  {
    activity_id: 1,
    user: {
      username: 'vuonglv',
      full_name: 'Lê Văn Vương',
      avatar: 'https://i.pravatar.cc/150?img=1'
    },
    activity_type: 'create',
    activity_time: '2021-05-01T00:00:00.000Z',
    activity_content: 'Tạo ứng dụng'
  },
  {
    activity_id: 2,
    user: {
      username: 'vuonglv',
      full_name: 'Lê Văn Vương',
      avatar: 'https://i.pravatar.cc/150?img=1'
    },
    activity_type: 'release',
    activity_time: '2021-05-02T00:00:00.000Z',
    activity_content: 'Release V1'
  },
  {
    activity_id: 3,
    user: {
      username: 'vuonglv',
      full_name: 'Lê Văn Vương',
      avatar: 'https://i.pravatar.cc/150?img=1'
    },
    activity_type: 'release',
    activity_time: '2021-05-03T00:00:00.000Z',
    activity_content: 'Release V2'
  },
  {
    activity_id: 4,
    user: {
      username: 'vuonglv',
      full_name: 'Lê Văn Vương',
      avatar: 'https://i.pravatar.cc/150?img=1'
    },
    activity_type: 'release',
    activity_time: '2021-05-04T00:00:00.000Z',
    activity_content: 'Release V3'
  }
]

export const useActivityStore = defineStore('activityStore', {
  state: () => ({
    activities: []
  }),

  getters: {
    latestActivities () {
      return this.sortedActivities.slice(0, 5)
    },
    sortedActivities () {
      return this.activities.map(activity => activity).sort((a, b) => {
        return Date.parse(b.activity_time) - Date.parse(a.activity_time)
      })
    }
  },

  actions: {

    fetchActivities (projectId, appName, callback) {
      auth0.getAccessTokenSilently().then((token) => {
        const headers = {}
        api.get('/projects/' + projectId + '/apps/' + appName + '/activities', { headers }).then(
          response => {
            const items = response.data.items
            this.activities = items.map(item => {
              return {
                activity_id: item.id,
                user: {
                  username: item.actor.name,
                  full_name: item.actor.name
                },
                activity_type: item.event_type,
                activity_time: item.created_at,
                activity_content: item.event
              }
            })
            if (callback) callback()
          }
        )
        this.activities = rawActivities
      })
    }
  }
})
