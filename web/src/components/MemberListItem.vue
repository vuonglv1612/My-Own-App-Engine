<template>
  <q-item clickable>
    <q-item-section avatar top>
      <q-avatar>
        <img :src="member.avatar">
      </q-avatar>

    </q-item-section>

    <q-item-section top>
      <q-item-label caption lines="2">
        <span class="text-grey-8">{{ member.name }}</span>
        <span class="text-grey-8"> - </span>
        <span class="text-grey-8"><b>{{ member.role }}</b></span>
      </q-item-label>
      <q-item-label caption lines="1">
        <span><q-icon name="email" size="16px"></q-icon> {{ member.email }}</span>
      </q-item-label>

    </q-item-section>

    <q-item-section top side>
      <div class="text-grey-8 q-gutter-xs">
        <q-btn v-for="btn in buttons" :key="btn.id" class="gt-xs" size="12px" flat dense round :icon="btn.icon" :color="btn.color" @click="btn.handler" >
          <q-tooltip>{{ btn.label }}</q-tooltip>
        </q-btn>
      </div>
    </q-item-section>
  </q-item>
</template>

<script>

import { useAuthStore } from 'stores/auth-store'
import { storeToRefs } from 'pinia'

export default {
  name: 'MemberListItem',
  props: {
    member: Object,
    currentRole: String
  },
  setup (props) {
    const authStore = useAuthStore()
    const { currentUser } = storeToRefs(authStore)
    const buttons = []
    console.log(props.currentRole)
    if (currentUser.value.id !== props.member.user_id && props.currentRole !== 'member') {
      buttons.push({
        id: 1,
        label: 'Xóa',
        color: 'negative',
        icon: 'delete',
        handler: () => {
          console.log('delete')
        }
      })
      if (props.member.role === 'member') {
        buttons.push({
          id: 2,
          label: 'Chuyển thành admin',
          color: 'primary',
          icon: 'edit',
          handler: () => {
            console.log('change role')
          }
        })
      }
    }

    if (props.currentRole !== 'owner' && currentUser.value.id === props.member.user_id) {
      buttons.push({
        icon: 'logout',
        color: 'negative',
        label: 'Rời nhóm',
        handler: () => {
          console.log('leave')
        }
      })
    }
    return {
      buttons
    }
  }

}
</script>
