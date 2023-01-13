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
                <div class="col-xs-12 window-height bg-black text-green-5 q-pa-sm log-box">
                  <q-scroll-area
                    ref="scroll"
                    class="fit"
                  >
                  <div v-for="log in logs" :key="log.id">
                    <p class="log-record q-mb-none">
                      {{log.message}}
                    </p>
                  </div>
                  </q-scroll-area>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');

.log-record {
  font-family: 'Roboto Mono', monospace;
  font-size: 12px;
  word-break: break-all;
}

</style>

<script>
import { useLogStore } from 'stores/log-store'
import { onMounted, ref } from 'vue'

const logStore = useLogStore()

export default {
  name: 'AppLogsPage',
  setup () {
    const scroll = ref(null)
    const logs = ref([])
    setInterval(() => {
      logStore.fetchLogs()
      logs.value = logStore.logs
      const scrollTarget = scroll.value?.getScrollTarget()
      const duration = 0
      scroll.value?.setScrollPosition('vertical', scrollTarget.scrollHeight, duration)
    }, 1000)
    onMounted(() => {
      logStore.fetchLogs()
      logs.value = logStore.logs
    })
    return { logs, scroll }
  }
}
</script>
