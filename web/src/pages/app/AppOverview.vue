<template>
  <q-page padding>
    <div class="row">
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
          </q-card>
        </div>
        <div class="row q-mt-md">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Thông tin Image</div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-xs">
              <div class="row">
                <div class="row">
                  <div v-for="field in imageFields" :key="field.name" class="col-xs-12 q-pa-sm">
                    <div class="text-subtitle1 q-pl-sm">{{ field.label }}</div>
                    <div class="text-subtitle2 q-pl-sm">{{ field.value }}</div>
                  </div>
                </div>
              </div>
            </q-card-section>
            <q-separator/>
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

export default {
  name: 'AppOverViewPage',
  components: { ActivityHistoryComponent },
  setup () {
    const activityStore = useActivityStore()
    const lastActivities = ref([])

    onMounted(() => {
      activityStore.fetchActivities()
      lastActivities.value = activityStore.latestActivities
    })
    const app = ref({
      name: 'Vuonglv Test App',
      app_id: 'vuonglv-app',
      platform: 'Python',
      address: 'https://vuonglv-app.ipaas.site',
      status: 'Running',
      created_at: '2021-05-20T10:00:00Z',
      size: {
        cpu: 5,
        memory: 2560
      },
      image: {
        registry: 'registry.ipaas.site',
        repository: 'vuonglv-app',
        tag: 'production-1.0.0',
        digest: 'sha256:81587739dc6b02b0f7281a14018d9eae3a2a4edeedf307363c9943e8dd68136d'
      }
    })
    const appFields = ref([
      {
        name: 'name',
        label: 'Tên ứng dụng',
        value: app.value.name
      },
      {
        name: 'app_id',
        label: 'Mã ứng dụng',
        value: app.value.app_id
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
        label: 'CPU sử dụng',
        value: app.value.size.cpu + ' CPU'
      },
      {
        name: 'memory',
        label: 'Bộ nhớ sử dụng',
        value: app.value.size.memory + ' MB'
      }
    ])
    const imageFields = [
      {
        name: 'registry',
        label: 'Registry',
        value: app.value.image.registry
      },
      {
        name: 'repository',
        label: 'Repository',
        value: app.value.image.repository
      },
      {
        name: 'tag',
        label: 'Tag',
        value: app.value.image.tag
      },
      {
        name: 'digest',
        label: 'Digest',
        value: app.value.image.digest
      }
    ]
    return {
      lastActivities,
      appFields,
      imageFields
    }
  }
}
</script>
