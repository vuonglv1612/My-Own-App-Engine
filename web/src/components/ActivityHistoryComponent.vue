<template>
  <q-timeline>
    <q-timeline-entry :color="iconMapping(activity.activity_type).color" v-for="activity in activities"
                      :key="activity.id" :icon="iconMapping(activity.activity_type).icon">
      <template v-slot:title>
        {{ activity.activity_content }}
      </template>
      <template v-slot:subtitle>
        <div class="row">
          {{ formatDate(activity.activity_time) }}
        </div>
        <div class="row">
          Thực hiện bởi: {{ activity.user?.username }}
        </div>
      </template>
    </q-timeline-entry>
  </q-timeline>
</template>

<script>
import { date } from 'quasar'

export default {
  name: 'ActivityHistoryComponent',
  props: {
    activities: {
      type: Array,
      required: true
    }
  },
  setup (props) {
    const formatDate = (strDate) => {
      const timeStamp = Date.parse(strDate)
      return date.formatDate(timeStamp, 'HH:mm:ss DD/MM/YYYY Z')
    }
    const iconMapping = (type) => {
      switch (type) {
        case 'app.created':
          return { icon: 'fiber_new', color: 'primary' }
        case 'app.deployed':
          return { icon: 'rocket_launch', color: 'positive' }
        default:
          return ''
      }
    }
    return {
      formatDate,
      iconMapping
    }
  }
}
</script>
