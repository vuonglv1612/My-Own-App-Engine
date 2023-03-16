<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12">
        <div class="row">
          <q-card id="deposit-box" class="my-card fit">
            <q-card-section>
              <div class="text-h6">Logs</div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <div class="row">
                <div class="col-xs-12 window-height text-green-5 q-pa-sm log-box">
                  <iframe
                    class="fit"
                    :src="src"
                    frameborder="0"
                  />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'AppLogsPage',
  setup () {
    const route = useRoute()
    const appId = ref(route.params.appId)
    appId.value = route.params.appId
    const src = ref('https://grafana.autoinfra.tech/d/JVfuy7A4z/app-log?orgId=1&var-appname=' + appId.value + '&refresh=10s&from=now-1h&to=now&kiosk=embedded&theme=light')
    return { src }
  }
}
</script>
