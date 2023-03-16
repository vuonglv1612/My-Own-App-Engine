<template>
  <q-layout>

    <q-drawer v-model="openDrawer" side="left" elevated>
      <q-list
        bordered
        link
        class="text-black"
      >
        <q-item
          v-for="item in items"
          :key="item.name"
          clickable
          v-ripple
          :to="item.to"
          :active="link === item.name"
          active-class="my-menu-link"
          @click="link = item.name"
        >
          <q-item-section avatar>
            <q-icon :name="item.icon"/>
          </q-item-section>
          <q-item-section>{{ item.label }}</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  // name: 'PageName',
  setup () {
    const route = useRoute()
    const link = ref(route.name)
    watch(() => route.name, (newVal) => {
      link.value = newVal
    })
    const items = [
      {
        name: 'project.apps.overview',
        label: 'Thông tin chung',
        icon: 'o_radar',
        to: { name: 'project.apps.overview' }
      },
      {
        name: 'project.apps.activity',
        label: 'Lịch sử hoạt động',
        icon: 'o_history',
        to: { name: 'project.apps.activity' }
      },
      {
        name: 'project.apps.logs',
        label: 'Logs',
        icon: 'o_manage_search',
        to: { name: 'project.apps.logs' }
      },
      {
        name: 'project.apps.env',
        label: 'Biến môi trường',
        icon: 'o_toggle_on',
        to: { name: 'project.apps.env' }
      },
      {
        name: 'project.apps.deploy',
        label: 'Triển khai',
        icon: 'o_rocket',
        to: { name: 'project.apps.deploy' }
      },
      {
        name: 'project.apps.settings',
        label: 'Cài đặt',
        icon: 'o_settings',
        to: { name: 'project.apps.settings' }
      }
    ]
    const openDrawer = ref(true)
    return {
      openDrawer,
      items,
      link
    }
  }
}
</script>
