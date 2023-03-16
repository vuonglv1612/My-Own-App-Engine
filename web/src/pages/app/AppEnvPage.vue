<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12">
        <div class="row">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Quản lý biến môi trường</div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <q-list
                bordered
                separator
                link
                class="text-black"
              >
                <q-item
                  v-for="env in envs"
                  :key="env.id"
                >
                  <q-item-section>
                    <div class="row">
                      <div class="col-md-6 q-pa-sm">
                        <q-input
                          filled
                          v-model="env.name"
                          disable
                          outlined
                          class="my-input text-uppercase text-weight-bold"
                        />
                      </div>
                      <div class="col-md-6 q-pa-sm">
                        <q-input outlined v-model="env.value" :type="env.show ? 'password' : 'text'">
                          <template v-slot:append>
                            <q-icon
                              :name="env.show ? 'visibility_off' : 'visibility'"
                              class="cursor-pointer"
                              @click="env.show = !env.show"
                            />
                          </template>
                          <template v-slot:after>
                            <q-btn rounded flat icon="o_save" color="positive" @click="onSaveEnv(env)"/>
                            <q-btn rounded flat icon="o_delete" color="negative" @click="onDeleteEnv(env)"/>
                          </template>
                        </q-input>
                      </div>
                    </div>
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>
                    <div class="row">
                      <div class="col-md-6 q-pa-sm">
                        <q-input
                          filled
                          v-model="newEnv.name"
                          outlined
                          class="my-input text-uppercase text-weight-bold"
                        />
                      </div>
                      <div class="col-md-6 q-pa-sm">
                        <q-input outlined v-model="newEnv.value" :type="newEnv.show ? 'password' : 'text'">
                          <template v-slot:append>
                            <q-icon
                              :name="newEnv.show ? 'visibility_off' : 'visibility'"
                              class="cursor-pointer"
                              @click="newEnv.show = !newEnv.show"
                            />
                          </template>
                          <template v-slot:after>
                            <q-btn class="fit" label="Thêm" color="positive" @click="onAddEnv"/>
                          </template>
                        </q-input>
                      </div>
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
            <q-inner-loading :showing="loading"/>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useEnvStore } from 'stores/env-store'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'

const envStore = useEnvStore()

export default {
  name: 'AppEnvPage',
  setup () {
    const $q = useQuasar()
    const envs = ref([])
    const newEnv = ref({ name: null, value: null, show: false })
    const route = useRoute()
    const appId = ref(route.params.appId)
    const loading = ref(false)

    const fetchEnvs = () => {
      loading.value = true
      envStore.fetchEnvs(appId.value, () => {
        newEnv.value = { name: null, value: null, show: false }
        envs.value = envStore.envs
        envs.value = envs.value.map(env => {
          return {
            id: env.id,
            name: env.name,
            value: env.value,
            show: false
          }
        })
        loading.value = false
      })
    }

    onMounted(() => {
      fetchEnvs()
    })

    const onSaveEnv = (env) => {
      loading.value = true
      envStore.updateEnv(appId.value, env.id, env, (err, response) => {
        if (err) {
          const reason = err.response.data.detail?.error
          $q.notify({
            message: reason || 'Cập nhật biến môi trường thất bại',
            color: 'negative',
            position: 'top',
            timeout: 2000
          })
        } else {
          fetchEnvs()
          $q.notify({
            message: 'Cập nhật biến môi trường thành công',
            color: 'positive',
            position: 'top',
            timeout: 2000
          })
        }
        loading.value = false
      })
    }

    const onAddEnv = () => {
      if (!newEnv.value.name || !newEnv.value.value) {
        $q.notify({
          message: 'Vui lòng nhập dữ liệu',
          color: 'negative',
          position: 'top',
          timeout: 2000
        })
        return
      }
      loading.value = true
      envStore.addEnv(appId.value, newEnv.value, (err, response) => {
        if (err) {
          const reason = err.response.data.detail?.error
          const msg = reason || 'Thêm biến môi trường thất bại'
          $q.notify({
            message: msg,
            color: 'negative',
            position: 'top',
            timeout: 2000
          })
        } else {
          fetchEnvs()
          $q.notify({
            message: 'Cập nhật biến môi trường thành công',
            color: 'positive',
            position: 'top',
            timeout: 2000
          })
        }
        loading.value = false
      })
    }

    const onDeleteEnv = (env) => {
      loading.value = true
      envStore.deleteEnv(appId.value, env.id, (err, response) => {
        if (err) {
          const reason = err.response.data.detail?.error
          $q.notify({
            message: reason || 'Xóa biến môi trường thất bại',
            color: 'negative',
            position: 'top',
            timeout: 2000
          })
        } else {
          fetchEnvs()
          $q.notify({
            message: 'Xóa biến môi trường thành công',
            color: 'positive',
            position: 'top',
            timeout: 2000
          })
        }
        loading.value = false
      })
    }

    return {
      envs,
      newEnv,
      loading,

      onSaveEnv,
      onDeleteEnv,
      onAddEnv
    }
  }
}
</script>
