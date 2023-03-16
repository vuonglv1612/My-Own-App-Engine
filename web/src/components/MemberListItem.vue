<template>
  <q-item clickable>
    <q-item-section avatar top>
      <q-avatar v-if="member.avatar">
        <img v-if="member.avatar" :src="member.avatar">
      </q-avatar>
      <q-avatar v-else color="primary" text-color="white">
        {{ member.name[0] }}
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
        <q-btn v-for="btn in buttons" :key="btn.id" class="gt-xs" size="12px" flat dense round :icon="btn.icon"
               :color="btn.color" @click="btn.handler">
          <q-tooltip>{{ btn.label }}</q-tooltip>
        </q-btn>
      </div>
    </q-item-section>
  </q-item>
</template>

<script>

export default {
  name: 'MemberListItem',
  props: {
    activeProject: Object,
    member: Object,
    currentRole: String,
    currentUser: Object,
    onDeleteMember: Function,
    onChangeRole: Function,
    onLeaveProject: Function
  },
  setup (props) {
    const buttons = []
    const deleteButton = {
      id: 1,
      label: 'Xóa',
      color: 'negative',
      icon: 'delete',
      handler: () => {
        props.onDeleteMember(props.member)
      }
    }
    const changeRoleToAdminButton = {
      id: 2,
      label: 'Chuyển thành admin',
      color: 'primary',
      icon: 'arrow_circle_up',
      handler: () => {
        props.onChangeRole(props.member, 'admin')
      }
    }
    const changeRoleToMemberButton = {
      id: 3,
      label: 'Chuyển thành member',
      color: 'primary',
      icon: 'arrow_circle_down',
      handler: () => {
        props.onChangeRole(props.member, 'member')
      }
    }
    const leaveButton = {
      id: 4,
      label: 'Rời khỏi dự án',
      color: 'negative',
      icon: 'exit_to_app',
      handler: () => {
        props.onLeaveProject()
      }
    }
    if (props.currentRole === 'member') {
      if (props.member.user_id === props.currentUser.sub) {
        buttons.push(leaveButton)
      }
    } else if (props.currentRole === 'admin') {
      if (props.member.user_id === props.currentUser.sub) {
        buttons.push(leaveButton)
      } else {
        buttons.push(deleteButton)
        if (props.member.role === 'member') {
          buttons.push(changeRoleToAdminButton)
        } else {
          buttons.push(changeRoleToMemberButton)
        }
      }
    } else if (props.currentRole === 'owner') {
      if (props.member.user_id !== props.currentUser.sub) {
        buttons.push(deleteButton)
        if (props.member.role === 'member') {
          buttons.push(changeRoleToAdminButton)
        } else {
          buttons.push(changeRoleToMemberButton)
        }
      }
    }
    return {
      buttons
    }
  }

}
</script>
