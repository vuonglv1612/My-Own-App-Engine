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
                            <q-btn class="fit" label="Thêm" color="positive" @click="onSaveEnv(newEnv)"/>
                          </template>
                        </q-input>
                      </div>
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useEnvStore } from 'stores/env-store'

const envStore = useEnvStore()

export default {
  name: 'AppEnvPage',
  setup () {
    const envs = ref([])
    const newEnv = ref({ name: null, value: null, show: false })

    onMounted(() => {
      envStore.fetchEnvs()
      envs.value = envStore.envs
      envs.value = envs.value.map(env => {
        return {
          id: env.id,
          name: env.name,
          value: env.value,
          show: false
        }
      })
    })

    const onSaveEnv = (env) => {
      // envStore.updateEnv(env.id, env.value)
      alert('Lưu thành công ' + env.name)
    }

    const onDeleteEnv = (env) => {
      // envStore.deleteEnv(env.id)
      alert('Xóa thành công ' + env.name)
    }

    return {
      envs,
      newEnv,

      onSaveEnv,
      onDeleteEnv
    }
  }
}
</script>
