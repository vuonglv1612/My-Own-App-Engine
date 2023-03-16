<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-8 offset-md-2">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Tạo ứng dụng</div>
          </q-card-section>
          <q-separator/>
          <q-card-section class="q-pa-none">
            <div>
              <q-stepper
                v-model="step"
                vertical
                color="primary"
                animated
                flat
              >
                <q-step
                  :name="1"
                  title="Chọn nền tảng"
                  icon="settings"
                  :done="step > 1"
                >
                  Ứng dụng của bạn đang chạy trên nền tảng nào? Chúng tôi sẽ cung cấp cho bạn một số nền tảng phổ biến
                  để bắt đầu.

                  <q-stepper-navigation>
                    <div class="row">
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-python" size="4em" color="primary"
                                @click="selectPlatform('python')"/>
                      </div>
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-golang" size="4em" color="primary"
                                @click="selectPlatform('go')"/>
                      </div>
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-docker" size="4em" color="primary"
                                @click="selectPlatform('static')"/>
                      </div>
                    </div>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="2"
                  title="Chọn cấu hình"
                  icon="create_new_folder"
                  :done="step > 2"
                >
                  Chọn cấu hình cho ứng dụng của bạn.
                  Cấu hình này sẽ ảnh hưởng đến khả năng xử lý của ứng dụng của bạn.
                  Ứng dụng của bạn có thể chạy trên nhiều đơn vị xử lý cùng một lúc. Việc chọn cấu hình dưới đây sẽ cài
                  đặt cấu hình cho mỗi đơn vị.
                  <div class="units">
                    <div class="row">
                      <div v-for="u in units" :key="u.id" class="col-xs-6 col-md-3 q-pa-md cursor-pointer">
                        <q-card class="my-card fit" @click="selectUnit(u)">
                          <q-card-section>
                            <div class="text-h6">Cấu hình: {{ u.name }}</div>
                          </q-card-section>
                          <q-separator/>
                          <q-card-section>
                            <div class="text-h6">Giá: {{ u.price }} VND/h</div>
                          </q-card-section>
                        </q-card>
                      </div>
                    </div>
                  </div>
                  <q-stepper-navigation>
                    <q-btn flat @click="step = 1" color="primary" label="Trở lại" class="q-ml-sm"/>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="3"
                  title="Đặt tên cho ứng dụng"
                  icon="add_comment"
                  :done="step > 3"
                >
                  <div class="name">
                    <q-input ref="nameRef" label="Tên ứng dụng" maxlength="100" hint="Ví dụ: app-cua-toi"
                             :rules="appNameRules"
                             v-model="name" outlined/>
                  </div>
                  <div class="name q-mt-md">
                    <q-input label="Mô tả" v-model="description" outlined/>
                  </div>
                  <q-stepper-navigation>
                    <q-btn @click="requestConfirm" :disable="!name" color="primary" label="Tiếp tục"/>
                    <q-btn flat @click="step = 2" color="primary" label="Quay lại" class="q-ml-sm"/>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="4"
                  title="Xác nhận thông tin"
                  icon="add_comment"
                >
                  <div class="confirm">
                    <div class="row">
                      <div class="col-xs-12 col-md-12">
                        <div class="text-caption">Tên ứng dụng: {{ name }}</div>
                      </div>
                      <div class="col-xs-12 col-md-12">
                        <div class="text-caption">Nền tảng: {{ platform }}</div>
                      </div>
                      <div class="col-xs-12 col-md-12">
                        <div class="text-caption">Cấu hình: {{ selectedUnit.name }}</div>
                      </div>
                    </div>
                  </div>
                  <q-stepper-navigation>
                    <q-btn @click="submitCreateApp" color="primary" label="Tạo ứng dụng"/>
                    <q-btn flat @click="step = 3" color="primary" label="Quay lại" class="q-ml-sm"/>
                  </q-stepper-navigation>
                </q-step>
              </q-stepper>
            </div>
          </q-card-section>
          <q-inner-loading :showing="loading"></q-inner-loading>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useProjectStore } from 'stores/project-store'
import { useRouter } from 'vue-router'
import { useAuth0 } from '@auth0/auth0-vue'
import { useQuasar } from 'quasar'

export default {
  setup () {
    const $q = useQuasar()
    const projectStore = useProjectStore()
    const auth0 = useAuth0()
    const router = useRouter()
    const step = ref(1)
    const platform = ref(null)
    const quantity = ref(1)
    const selectedUnit = ref(null)
    const name = ref(null)
    const description = ref(null)
    const loading = ref(false)
    const nameRef = ref(null)
    const selectPlatform = (p) => {
      platform.value = p
      step.value = 2
    }
    const selectUnit = (u) => {
      selectedUnit.value = u
      step.value = 3
    }

    const requestConfirm = () => {
      nameRef.value.validate()

      if (nameRef.value.hasError) {
        // form has error
      } else {
        step.value = 4
      }
    }
    const submitCreateApp = () => {
      loading.value = true
      auth0.getAccessTokenSilently().then(token => {
        api.post('/apps', {
          project_id: projectStore.activeProject?.id,
          name: name.value,
          platform: platform.value,
          description: description.value,
          unit: selectedUnit.value.id,
          replicas: quantity.value
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).then(res => {
          loading.value = false
          $q.notify({
            message: 'Tạo ứng dụng thành công',
            color: 'positive',
            position: 'top'
          })
          router.push({ name: 'project.apps.overview', params: { appId: name.value } })
        }).catch((err) => {
          loading.value = false
          $q.notify({
            message: 'Tạo ứng dụng thất bại. Lỗi: ' + err.response.data?.detail.error,
            color: 'negative',
            position: 'top'
          })
        })
      })
    }
    const units = [
      {
        id: 'c100_m100',
        name: '100MB RAM, 0.1 CPU',
        price: 100
      },
      {
        id: 'c200_m200',
        name: '200MB RAM, 0.2 CPU',
        price: 200
      },
      {
        id: 'c500_m500',
        name: '0.5GB RAM, 0.5 CPU',
        price: 500
      },
      {
        id: 'c1000_m1000',
        name: '1GB RAM, 1 CPU',
        price: 1000
      }
    ]
    return {
      step,
      platform,
      selectPlatform,
      selectUnit,
      submitCreateApp,
      requestConfirm,
      selectedUnit,
      units,
      name,
      description,
      loading,
      appNameRules: [
        value => !!value || 'Tên ứng dụng không được để trống',
        value => value.length <= 100 || 'Tên ứng dụng không được quá 100 ký tự',
        value => /^[a-z0-9-]+$/.test(value) || 'Tên ứng dụng chỉ được chứa các ký tự a-z, 0-9 và dấu -'
      ],
      nameRef
    }
  }
}
</script>
