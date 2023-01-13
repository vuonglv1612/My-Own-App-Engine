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

export default {
  name: 'PageName',
  setup () {
    const $q = useQuasar()
    const onDeleteApp = () => {
      $q.dialog({
        title: 'Xóa ứng dụng',
        message: 'Bạn có chắc chắn muốn xóa ứng dụng này?',
        cancel: true,
        persistent: true
      }).onOk(() => {
        // TODO: delete app
        alert('delete app')
      })
    }
    return {
      onDeleteApp
    }
  }
}
</script>
