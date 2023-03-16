<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-6">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Xóa ứng dụng</div>
          </q-card-section>
          <q-separator/>
          <q-card-section>
            <div class="row">
              <div class="text-subtitle2">
                <q-icon name="warning" color="negative" size="md"/>
                <span class="q-ml-sm">Nếu bạn nhấn nút "Xóa ứng dụng", tất cả các dữ liệu liên quan đến ứng dụng này sẽ bị xóa.</span>
              </div>
              <div class="col-xs-12 q-mt-sm">
                <q-btn
                  color="negative"
                  label="Xóa ứng dụng"
                  @click="onDeleteApp"
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
import { useRoute, useRouter } from 'vue-router'
import { ref } from 'vue'
import { useAppStore } from 'stores/app-store'

export default {
  name: 'AppSettingPage',
  setup () {
    const $q = useQuasar()
    const route = useRoute()
    const router = useRouter()
    const appStore = useAppStore()
    const appId = ref(route.params.appId)
    const onDeleteApp = () => {
      $q.dialog({
        title: 'Xóa ứng dụng',
        message: 'Bạn có chắc chắn muốn xóa ứng dụng này?',
        cancel: true,
        persistent: true
      }).onOk(() => {
        appStore.deleteApp(appId.value, (err, data) => {
          if (err) {
            if (err.response.statusCode === 404) {
              // redirect to 404 page
              $q.notify({
                type: 'negative',
                message: 'Xóa ứng dụng thất bại. Lý do: Ứng dụng không tồn tại'
              })
              router.push({ name: 'index' })
            } else {
              $q.notify({
                type: 'negative',
                message: 'Xóa ứng dụng thất bại. Lý do: ' + err.response.data.detail.error || 'Không xác định'
              })
            }
          } else {
            $q.notify({
              type: 'positive',
              message: 'Xóa ứng dụng thành công',
              timeout: 1000
            })
            router.push({ name: 'project.apps' })
          }
        })
      })
    }
    return {
      onDeleteApp
    }
  }
}
</script>
