<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer"/>

        <q-toolbar-title>
          <span class="q-ml-sm">App Engine</span>
        </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-drawer v-model="leftDrawerOpen" side="left" overlay bordered>
      <q-list padding class="rounded-borders text-black bg-white fit">
        <q-item
          v-ripple
        >
          <q-select
            v-model="project"
            :options="projects"
            @update:model-value="onChangeSelectedProject()"
            label="Dự án"
            outlined
            class="fit"
          />
        </q-item>
        <q-item
          clickable
          v-ripple
          :to="{ name: 'project.apps' }"
          :active="link === 'project.apps'"
          @click="link = 'project.apps'"
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon name="o_home"/>
          </q-item-section>

          <q-item-section>Danh sách ứng dụng</q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          :to="{ name: 'project.members' }"
          :active="link === 'project.members'"
          @click="link = 'project.members'"
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon name="o_supervisor_account"/>
          </q-item-section>

          <q-item-section>Thành Viên Dự Án</q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          :to="{ name: 'project.billing' }"
          :active="link.startsWith('project.billing')"
          @click="link = 'project.billing.overview'"
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon name="o_credit_card"/>
          </q-item-section>

          <q-item-section>Chi phí sử dụng</q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          :to="{ name: 'project.settings' }"
          :active="link === 'project.settings'"
          @click="link = 'project.settings'"
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon name="o_settings"/>
          </q-item-section>

          <q-item-section>Cài Đặt</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>

  </q-layout>
</template>

<style lang="scss">
.my-menu-link {
  background-color: $blue-1 !important;
  color: $primary !important;
}

.x-dashboard-page-title {
  margin-top: 0;
}

</style>

<script>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from 'stores/project-store'

export default {
  setup () {
    const projectStore = useProjectStore()
    projectStore.fetchProjects()

    const router = useRouter()
    const route = useRoute()
    const leftDrawerOpen = ref(false)
    const projects = ref(null)
    const project = ref(null)
    const link = ref('project.apps')

    projects.value = projectStore.listProjects.map((project) => {
      return {
        label: project.display_name,
        value: project.project_name
      }
    })

    const rawProject = projectStore.activeProject
    project.value = {
      label: rawProject.display_name,
      value: rawProject.project_name
    }
    link.value = route.name
    if (!link.value.startsWith('project.billing')) {
      leftDrawerOpen.value = true
    }

    const onChangeSelectedProject = () => {
      projectStore.setActiveProject(project.value.value)
      router.push({ name: link.value })
    }

    return {
      link,
      project,
      projects,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
        link.value = route.name
      },
      onChangeSelectedProject
    }
  }
}
</script>
