<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-6 offset-md-3">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Xóa dự án</div>
          </q-card-section>
          <q-separator/>
          <q-card-section>
            <div class="row">
              <div class="text-subtitle2">
                <q-icon name="warning" color="negative" size="md"/>
                <span class="q-ml-sm">Nếu bạn nhấn nút "Xóa dự án", tất cả các dữ liệu liên quan đến dự án này sẽ bị xóa, bao gồm(ứng dụng, lịch sử thanh toán, hóa đơn)</span>
              </div>
              <div class="col-xs-12 q-mt-sm">
                <q-btn
                  color="negative"
                  label="Xóa dự án"
                  @click="onDeleteProject"
                />
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>

import { useQuasar } from 'quasar'
import { useMemberStore } from 'stores/members-store'
import { useProjectStore } from 'stores/project-store'
import { storeToRefs } from 'pinia'

export default {
  name: 'PageName',
  setup () {
    const $q = useQuasar()
    const projectStore = useProjectStore()
    const { activeProject } = storeToRefs(projectStore)
    const memberStore = useMemberStore()
    const onDeleteProject = () => {
      $q.dialog({
        title: 'Xóa dự án',
        message: 'Bạn có chắc chắn muốn xóa dự án này?',
        cancel: true,
        persistent: true
      }).onOk(() => {
        memberStore.deleteProject(activeProject.value.id, (err, response) => {
          if (err) {
            const reason = err.response.data.detail.error || 'Xóa dự án thất bại'
            $q.notify({
              type: 'negative',
              message: reason,
              position: 'top',
              timeout: 2000,
              icon: 'warning'
            })
          } else {
            $q.notify({
              type: 'positive',
              message: 'Xóa dự án thành công',
              position: 'top',
              timeout: 2000,
              icon: 'check_circle'
            })
            projectStore.fetchProjects(() => {
              projectStore.setActiveProject(null)
            })
          }
        })
      })
    }
    return {
      onDeleteProject
    }
  }
}
</script>
