<template>
    <q-drawer v-model="openDrawer" side="left" elevated>
      <!-- drawer content -->
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
          active-class="my-menu-link"
        >
          <q-item-section avatar>
            <q-icon :name="item.icon"/>
          </q-item-section>
          <q-item-section>{{ item.label }}</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
</template>

<script>
import { ref } from 'vue'

export default {
  // name: 'PageName',
  setup () {
    const items = [
      {
        name: 'project.apps',
        label: 'Danh sách ứng dụng',
        icon: 'o_home',
        to: { name: 'project.apps' }
      },
      {
        name: 'project.members',
        label: 'Thành viên',
        icon: 'o_people',
        to: { name: 'project.members' }
      },
      {
        name: 'project.billing',
        label: 'Thanh toán',
        icon: 'o_credit_card',
        to: { name: 'project.billing' }
      }
    ]
    const openDrawer = ref(true)
    return {
      openDrawer,
      items
    }
  }
}
</script>
