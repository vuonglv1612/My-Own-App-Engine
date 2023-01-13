import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid'

export const useLogStore = defineStore('logs', {
  state: () => ({
    logs: []
  }),

  getters: {
  },

  actions: {
    fetchLogs () {
      const newLogs = { id: uuidv4(), message: '2023-01-11T04:58:41,121.268749 - 1 - MainThread - audit_billing_v4.services.consumer - _callback:91 - INFO - Message processed: b\'{"name": "audit_vod", "payload": {"audit_id": "2c72b0f52d6347cdbc417c90dd3d1586", "tenant_id": "f59e5a2e2ac540519706b8dbcc155ec5", "store_id": "1d4066319f57e02ab4e115319bc5da02", "store_name": "airclass", "start_time": "2023-01-11T02:00:00+00:00", "end_time": "2023-01-11T03:00:00+00:00"}, "issued_at": "2023-01-11T04:58:01.109090"}\' | context={}' }
      // const newLogs = { id: uuidv4(), message: uuidv4() }
      this.logs.push(newLogs)
    }
  }
})
