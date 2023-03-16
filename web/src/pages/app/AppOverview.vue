<template>
  <q-page padding>
    <div class="row">
      <q-inner-loading :showing="loading">
        <div class="row">
          <q-spinner-ios
            color="primary"
            size="4em"
          />
        </div>
      </q-inner-loading>
      <div class="col-xs-12 col-md-8 q-pa-sm">
        <div class="row">
          <q-card id="deposit-box" class="my-card fit">
            <q-card-section>
              <div class="text-h6">Thông tin ứng dụng</div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <div class="row">
                <div v-for="field in appFields" :key="field.name" class="col-xs-12 col-md-6 q-pa-sm">
                  <div class="text-subtitle1 q-pl-sm">{{ field.label }}</div>
                  <div class="text-subtitle2 q-pl-sm">{{ field.value }}</div>
                </div>
              </div>
            </q-card-section>
            <q-card-section class="q-pa-none">
              <q-btn
                v-if="app.status === 'running'"
                flat
                class="fit"
                color="primary"
                align="left"
                label="Thay đổi số lượng"
                icon="scale"
                @click="onScale"
              />
              <q-btn
                v-if="app.status !== 'created'"
                flat
                class="fit"
                color="primary"
                align="left"
                label="Khởi động lại ứng dụng"
                icon="restart_alt"
                @click="onRestart"
              />
              <q-btn
                flat
                v-if="app.status === 'running'"
                class="fit"
                color="negative"
                align="left"
                label="Tắt ứng dụng"
                icon="power_off"
                @click="onPowerOff"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
      <div class="col-xs-12 col-md-4 q-pa-sm">
        <div class="row">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Hoạt động gần đây</div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <div class="row">
                <ActivityHistoryComponent :activities="lastActivities"/>
              </div>
            </q-card-section>
            <q-card-section class="q-pa-none">
              <q-btn
                flat
                align="left"
                class="fit text-left text-weight-light"
                label="Toàn bộ hoạt động"
                icon="arrow_forward"
                :to="{ name: 'project.apps.activity' }"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>

import { useActivityStore } from 'stores/activity-store'
import { onMounted, ref } from 'vue'
import ActivityHistoryComponent from 'components/ActivityHistoryComponent.vue'
import { useRoute } from 'vue-router'
import { useProjectStore } from 'stores/project-store'
import { useAppStore } from 'stores/app-store'
import { useQuasar } from 'quasar'

export default {
  name: 'AppOverViewPage',
  components: { ActivityHistoryComponent },
  setup () {
    const $q = useQuasar()
    const route = useRoute()
    const projectStore = useProjectStore()
    const appStore = useAppStore()
    const activityStore = useActivityStore()
    const lastActivities = ref([])
    const appId = ref(route.params.appId)
    const app = ref({})
    const appFields = ref([])
    const imageFields = ref([])
    const loading = ref(false)
    const replicas = ref(app.value?.replicas || 1)

    onMounted(() => {
      projectStore.fetchProjects(() => {
        loadData()
      })
    })
    const loadData = () => {
      loading.value = true
      activityStore.fetchActivities(projectStore.activeProject?.id, appId.value, () => {
        lastActivities.value = activityStore.latestActivities
      })
      appStore.getApp(projectStore.activeProject?.id, appId.value, (data) => {
        app.value = data
        replicas.value = app.value?.replicas || 1
        appFields.value = [
          {
            name: 'name',
            label: 'Tên ứng dụng',
            value: app.value.name
          },
          {
            name: 'platform',
            label: 'Nền tảng',
            value: app.value.platform
          },
          {
            name: 'address',
            label: 'Địa chỉ',
            value: app.value.address
          },
          {
            name: 'status',
            label: 'Trạng thái',
            value: app.value.status
          },
          {
            name: 'created_at',
            label: 'Ngày tạo',
            value: app.value.created_at
          },
          {
            name: 'cpu',
            label: 'CPU',
            value: (app.value.cpu / 1000) + ' vCPU'
          },
          {
            name: 'cpu',
            label: 'RAM',
            value: app.value.memory + 'MB'
          },
          {
            name: 'replicas',
            label: 'Số lượng',
            value: app.value.replicas
          }
        ]
        imageFields.value = [
          {
            name: 'registry',
            label: 'Registry',
            value: app.value.image?.registry
          },
          {
            name: 'repository',
            label: 'Repository',
            value: app.value.image?.repository
          },
          {
            name: 'tag',
            label: 'Tag',
            value: app.value.image?.tag
          },
          {
            name: 'digest',
            label: 'Digest',
            value: app.value.image?.digest
          }
        ]
        loading.value = false
      })
    }

    const onScale = () => {
      $q.dialog({
        title: 'Cài đặt số lượng ứng dụng',
        message: 'Số lượng ứng dụng',
        prompt: {
          model: replicas.value,
          type: 'number',
          min: 1,
          max: 100
        },
        cancel: true,
        persistent: true
      }).onOk((data) => {
        if (data < 1) {
          $q.notify({
            message: 'Số lượng ứng dụng phải lớn hơn 0',
            color: 'negative',
            position: 'top',
            timeout: 2000,
            icon: 'warning'
          })
          return
        }
        appStore.scaleApp(appId.value, data, (err, response) => {
          if (err) {
            $q.notify({
              message: 'Không thể cài đặt số lượng ứng dụng',
              color: 'negative',
              position: 'top',
              timeout: 2000,
              icon: 'warning'
            })
          } else {
            $q.notify({
              message: 'Đã cài đặt số lượng ứng dụng',
              color: 'positive',
              position: 'top',
              timeout: 2000,
              icon: 'check'
            })
            loadData()
          }
        })
      })
    }

    const onRestart = () => {
      appStore.restartApp(appId.value, (err, response) => {
        if (err) {
          $q.notify({
            message: 'Không thể khởi động lại ứng dụng',
            color: 'negative',
            position: 'top',
            timeout: 2000,
            icon: 'warning'
          })
        } else {
          $q.notify({
            message: 'Đã khởi động lại ứng dụng',
            color: 'positive',
            position: 'top',
            timeout: 2000,
            icon: 'check'
          })
          loadData()
        }
      })
    }

    const onPowerOff = () => {
      appStore.stopApp(appId.value, (err, response) => {
        if (err) {
          $q.notify({
            message: 'Không thể tắt ứng dụng',
            color: 'negative',
            position: 'top',
            timeout: 2000,
            icon: 'warning'
          })
        } else {
          $q.notify({
            message: 'Đã tắt ứng dụng',
            color: 'positive',
            position: 'top',
            timeout: 2000,
            icon: 'check'
          })
          loadData()
        }
      })
    }

    return {
      lastActivities,
      appFields,
      imageFields,
      loading,
      app,

      onScale,
      onRestart,
      onPowerOff
    }
  }
}
</script>
