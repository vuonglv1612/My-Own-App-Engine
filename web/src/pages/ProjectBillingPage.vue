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
        name: 'project.billing.overview',
        label: 'Tổng Quan',
        icon: 'o_home',
        to: { name: 'project.billing.overview' }
      },
      {
        name: 'project.billing.deposit',
        label: 'Nạp tiền',
        icon: 'o_atm',
        to: { name: 'project.billing.deposit' }
      },
      {
        name: 'project.billing.invoices',
        label: 'Hóa đơn',
        icon: 'o_receipt_long',
        to: { name: 'project.billing.invoices' }
      },
      {
        name: 'project.billing.transactions',
        label: 'Giao dịch',
        icon: 'o_payments',
        to: { name: 'project.billing.transactions' }
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
