<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer"/>

        <q-toolbar-title>
          <q-avatar>
            <img src="https://appengine.hn.ss.bfcplatform.vn/logo.png">
          </q-avatar>
          <span class="q-ml-sm text-uppercase">Auto Infra</span>
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
          @click="onCreateProject"
          active-class="my-menu-link"
          class="bg-primary text-white"
        >
          <q-item-section avatar>
            <q-icon name="add_circle"/>
          </q-item-section>

          <q-item-section>Tạo dự án mới</q-item-section>
        </q-item>
        <q-item
          clickable
          v-ripple
          :to="{ name: 'project.apps' }"
          :active="link.startsWith('project.apps')"
          @click="link = 'project.apps'"
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon name="o_apps"/>
          </q-item-section>

          <q-item-section>Danh sách ứng dụng</q-item-section>
        </q-item>

        <q-item
          clickable
          v-ripple
          :to="{ name: 'project.members' }"
          :active="link.startsWith('project.members')"
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
          :active="link.startsWith('project.settings')"
          @click="link = 'project.settings'"
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon name="o_settings"/>
          </q-item-section>

          <q-item-section>Cài Đặt</q-item-section>
        </q-item>
        <q-item
          v-if="isAuthenticated"
          clickable
          v-ripple
          @click="logoutHandler"
        >
          <q-item-section avatar>
            <q-icon name="o_logout"/>
          </q-item-section>

          <q-item-section>Đăng Xuất</q-item-section>
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
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from 'stores/project-store'
import { useAuth0 } from '@auth0/auth0-vue'
import { useQuasar } from 'quasar'

export default {
  setup () {
    const $q = useQuasar()
    const projectStore = useProjectStore()

    const auth0 = useAuth0()
    const router = useRouter()
    const route = useRoute()
    const leftDrawerOpen = ref(false)
    const projects = ref(null)
    const project = ref(null)
    const link = ref('project.apps')
    const { isAuthenticated } = auth0

    onMounted(() => {
      projectStore.fetchProjects(() => {
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
      })
    })

    link.value = route.name
    if (!link.value.startsWith('project.billing') || !link.value.startsWith('project.apps')) {
      leftDrawerOpen.value = true
    }
    if (link.value.startsWith('project.new_app')) {
      leftDrawerOpen.value = true
    }

    const onChangeSelectedProject = () => {
      projectStore.setActiveProject(project.value.value)
      router.push({ name: link.value })
    }

    const logoutHandler = () => {
      auth0.logout(
        {
          returnTo: window.location.origin
        }
      )
    }

    const onCreateProject = () => {
      $q.dialog({
        title: 'Tạo dự án mới',
        message: 'Bạn có muốn tạo dự án mới không?',
        prompt: {
          model: '',
          type: 'text',
          label: 'Tên dự án',
          lazyRules: true,
          rules: [
            val => !!val || 'Vui lòng nhập tên dự án',
            val => (val && val.length <= 50) || 'Tên dự án không được quá 50 ký tự'
          ]
        },
        cancel: true,
        persistent: true
      }).onOk((data) => {
        projectStore.createProject(data, (err, response) => {
          if (err) {
            $q.notify({
              type: 'negative',
              message: 'Tạo dự án mới thất bại'
            })
            return
          }
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
        })
      })
    }

    return {
      link,
      project,
      projects,
      leftDrawerOpen,
      isAuthenticated,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
        link.value = route.name
      },
      onChangeSelectedProject,
      logoutHandler,
      onCreateProject
    }
  }
}
</script>
