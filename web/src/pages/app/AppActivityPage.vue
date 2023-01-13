<template>
  <q-page padding>
    <div class="q-px-lg q-pb-md">
      <div class="text-h6">Lịch sử hoạt động</div>
      <ActivityHistoryComponent :activities="activities"/>
    </div>
  </q-page>
</template>

<script>
import { onMounted, ref } from 'vue'
import ActivityHistoryComponent from 'components/ActivityHistoryComponent.vue'
import { useActivityStore } from 'stores/activity-store'

export default {
  name: 'AppActivityPage',
  components: { ActivityHistoryComponent },
  setup () {
    const activityStore = useActivityStore()
    const activities = ref([])
    onMounted(() => {
      activityStore.fetchActivities()
      activities.value = activityStore.sortedActivities
    })
    return {
      activities
    }
  }
}
</script>
