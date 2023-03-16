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
import { useProjectStore } from 'stores/project-store'
import { useRoute } from 'vue-router'

export default {
  name: 'AppActivityPage',
  components: { ActivityHistoryComponent },
  setup () {
    const route = useRoute()
    const projectStore = useProjectStore()
    const activityStore = useActivityStore()
    const activities = ref([])
    const appId = ref(route.params.appId)
    onMounted(() => {
      activityStore.fetchActivities(projectStore.activeProject?.id, appId.value, () => {
        activities.value = activityStore.sortedActivities
      })
    })
    return {
      activities
    }
  }
}
</script>
