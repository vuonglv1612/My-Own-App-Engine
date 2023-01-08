<template>
  <q-page padding>
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <div class="row">
          <h5 class="x-dashboard-page-title">Danh sách ứng dụng</h5>
        </div>
        <div class="row">
          <div class="col-md-6">
            <q-input outlined bottom-slots v-model="searchText" ref="searchTextRef" :rules="searchTextRules"
                     label="Tìm kiếm">
              <template v-slot:after>
                <q-btn round dense flat icon="search" type="submit" @click="searchApp"/>
                <q-btn round dense flat icon="restart_alt" type="reset" @click="onReset"/>
              </template>
            </q-input>
          </div>
        </div>
        <q-separator spaced/>
        <div v-if="loading" class="column justify-center items-center">
          <q-spinner-ios
            color="primary"
            size="4em"
          />
        </div>
        <div v-else class="row">
          <q-list
            bordered
            separator
            link
            class="q-my-md fit"
          >
            <AppListItem
              v-for="app in apps"
              :key="app.id"
              :app="app"
            />
          </q-list>
        </div>
        <div class="row">
          <q-pagination
            v-if="numberOfPages !== 1"
            v-model="currentPage"
            :max="numberOfPages"
            direction-links
            boundary-links
            icon-first="skip_previous"
            icon-last="skip_next"
            icon-prev="fast_rewind"
            icon-next="fast_forward"
            @update:model-value="loadNewPage"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useAppStore } from 'stores/app-store'
import AppListItem from 'components/AppListItem.vue'
import { useProjectStore } from 'stores/project-store'
import { storeToRefs } from 'pinia'

export default {
  name: 'ListAppsPage',
  components: { AppListItem },
  setup () {
    const searchText = ref(null)
    const currentPage = ref(1)
    const loading = ref(true)
    const searchTextRef = ref(null)
    const searchTextRules = [
      (v) => !!v || 'Vui lòng nhập từ khóa tìm kiếm'
    ]

    const projectStore = useProjectStore()
    const appStore = useAppStore()

    const { activeProject } = storeToRefs(projectStore)

    console.log('projectStore.currentProject', activeProject.project_name)
    appStore.fetchApps(activeProject.id, currentPage.value, searchText.value)
    loading.value = false
    const numberOfPages = ref(appStore.numberOfPages)
    const apps = ref(appStore.listApps)

    const loadNewPage = () => {
      loading.value = true
      appStore.fetchApps(activeProject.id, currentPage.value, searchText.value)
      loading.value = false
      numberOfPages.value = appStore.numberOfPages
      apps.value = appStore.listApps
    }

    const searchApp = () => {
      searchTextRef.value.validate()
      if (searchTextRef.value.hasError) {
        return
      }
      loading.value = true
      appStore.fetchApps(activeProject.id, currentPage.value, searchText.value)
      setTimeout(() => {
        loading.value = false
      }, 1000)
      numberOfPages.value = appStore.numberOfPages
      apps.value = appStore.listApps
    }

    const onReset = () => {
      searchTextRef.value.resetValidation()
      searchText.value = null
    }

    return {
      currentPage,
      numberOfPages,
      searchText,
      apps,
      loading,
      searchTextRef,
      searchTextRules,
      loadNewPage,
      searchApp,
      onReset
    }
  }
}
</script>
