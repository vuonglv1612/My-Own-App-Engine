<template>
  <q-item clickable :to="{ name: 'project.apps.overview', params: { appId: app.id } }">
    <q-item-section avatar top>
      <q-icon :name="statusIcon" :color="statusColor" size="24px">
        <q-tooltip>
          {{ statusText }}
        </q-tooltip>
      </q-icon>
    </q-item-section>

    <q-item-section top class="col-2">
      <q-item-label>{{ app.name }}</q-item-label>
    </q-item-section>

    <q-item-section top>
      <q-item-label lines="1">
        <span class="text-weight-medium">[{{ app.slug }}]</span>
        <span class="text-grey-8 text-capitalize"> - {{ app.platform }}
        <q-icon class="p-ml-xl" v-if="platformIcon" :name="platformIcon" color="primary"/>
        </span>
      </q-item-label>
      <q-item-label caption lines="2">
        <span class="text-grey-8"><b>Mô tả: </b>
          {{ app.description }}</span>
      </q-item-label>
      <q-item-label caption lines="1">
        <span class="text-grey-8"><b>Ngày tạo:</b> {{ app.created_at }}</span>
      </q-item-label>
      <q-item-label v-if="app.latest_version" caption lines="1">
        <span class="text-grey-8"><b>Phiên bản hiện tại: </b> {{ app.latest_version }}</span>
      </q-item-label>

    </q-item-section>
  </q-item>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'AppListItem',
  props: {
    app: Object
  },
  setup (props) {
    const statusIcon = ref('hexagon')
    const statusColor = ref('positive')
    const statusText = ref('Đang hoạt động')
    const platformIcon = ref('')
    const platformIconMapping = {
      android: 'fa-brands fa-android',
      ios: 'fa-brands fa-apple',
      web: 'fa-brands fa-chrome',
      python: 'fa-brands fa-python',
      nodejs: 'fa-brands fa-node-js',
      java: 'fa-brands fa-java',
      php: 'fa-brands fa-php',
      ruby: 'fa-brands fa-ruby',
      golang: 'fa-brands fa-golang',
      image: 'fa-brands fa-docker'
    }
    if (props.app.status === 'running') {
      statusIcon.value = 'check_circle'
      statusColor.value = 'positive'
      statusText.value = 'Đang hoạt động'
    } else if (props.app.status === 'stopped') {
      statusIcon.value = 'error'
      statusColor.value = 'negative'
      statusText.value = 'Không hoạt động'
    } else if (props.app.status === 'created') {
      statusIcon.value = 'warning'
      statusColor.value = 'warning'
      statusText.value = 'Chưa Deploy'
    }
    platformIcon.value = platformIconMapping[props.app.platform]

    return { statusIcon, statusColor, statusText, platformIcon }
  }
}
</script>
