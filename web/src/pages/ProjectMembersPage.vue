<template>
  <q-page padding>
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <div class="row">
          <h5 class="x-dashboard-page-title">Danh sách thành viên</h5>
        </div>
        <!--        <div class="row">-->
        <!--          <div class="col-md-6">-->
        <!--            <q-input outlined bottom-slots v-model="searchText" ref="searchTextRef" :rules="searchTextRules"-->
        <!--                     label="Tìm kiếm">-->
        <!--              <template v-slot:after>-->
        <!--                <q-btn round dense flat icon="search" type="submit" @click="searchApp"/>-->
        <!--                <q-btn round dense flat icon="restart_alt" type="reset" @click="onReset"/>-->
        <!--              </template>-->
        <!--            </q-input>-->
        <!--          </div>-->
        <!--        </div>-->
        <div class="row">
          <q-btn
            color="primary"
            unelevated
            label="Thêm mới thành viên"
            @click="showAddMemberDialog"
          />
        </div>
        <!--        <q-separator spaced/>-->
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
            <MemberListItem
              v-for="member in listMembers"
              :key="member.id"
              :member="member"
              :active-project="activeProject"
              :currentRole="currentRole"
              :current-user="currentUser"
              :on-delete-member="onDeleteMember"
              :on-change-role="onChangeRole"
              :on-leave-project="onLeaveProject"
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
            @update:model-value="reloadMembers"
          />
        </div>
      </div>
    </div>
    <q-dialog v-model="showAddMember" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Thêm thành viên</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input label="Email" dense v-model="inviteEmail" autofocus/>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Hủy" v-close-popup/>
          <q-btn color="primary" label="Thêm" @click="onAddMemberRequest"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { onMounted, ref, watch } from 'vue'
import { useProjectStore } from 'stores/project-store'
import { storeToRefs } from 'pinia'
import MemberListItem from 'components/MemberListItem.vue'
import { useMemberStore } from 'stores/members-store'
import { useQuasar } from 'quasar'
import { useAuth0 } from '@auth0/auth0-vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ProjectMembersPage',
  components: { MemberListItem },
  setup () {
    const auth0 = useAuth0()
    const router = useRouter()
    const searchText = ref(null)
    const currentPage = ref(1)
    const loading = ref(true)
    const searchTextRef = ref(null)
    const searchTextRules = [
      (v) => !!v || 'Vui lòng nhập từ khóa tìm kiếm'
    ]

    const projectStore = useProjectStore()
    const memberStore = useMemberStore()
    const q = useQuasar()

    const currentUser = ref(auth0.user)
    const { activeProject } = storeToRefs(projectStore)
    const { listMembers, numberOfPages } = storeToRefs(memberStore)

    onMounted(() => {
      return reloadMembers()
    })

    const reloadMembers = () => {
      loading.value = true
      memberStore.fetchMembers(activeProject.value.id, currentPage.value, searchText.value, () => {
        loading.value = false
      })
    }

    const getCurrentRole = () => {
      const currentMember = listMembers.value.find(member => member.user_id === currentUser.value.sub)
      if (currentMember) {
        return currentMember.role
      }
      return null
    }
    const currentRole = ref(getCurrentRole())
    watch(listMembers, () => {
      currentRole.value = getCurrentRole()
    })

    watch(activeProject, () => {
      return reloadMembers()
    })

    const searchApp = () => {
      searchTextRef.value.validate()
      if (searchTextRef.value.hasError) {
        return
      }
      return reloadMembers()
    }

    const onReset = () => {
      searchTextRef.value.resetValidation()
      searchText.value = null
    }

    const inviteEmail = ref(null)
    const showAddMember = ref(false)
    const showAddMemberDialog = () => {
      showAddMember.value = true
    }
    const onAddMemberRequest = () => {
      memberStore.addMember(activeProject.value.id, inviteEmail.value, (err, response) => {
        if (err) {
          const reason = err?.response.data?.detail?.error || 'Đã có lỗi xảy ra'
          q.notify({
            message: reason,
            color: 'negative',
            position: 'top',
            timeout: 2000,
            icon: 'error'
          })
          inviteEmail.value = null
          showAddMember.value = true
          return
        }
        q.notify({
          message: 'Mời thành công',
          color: 'positive',
          position: 'top',
          timeout: 2000,
          icon: 'check_circle'
        })
        showAddMember.value = false
        inviteEmail.value = null
        reloadMembers()
      })
    }

    const onDeleteMember = (member) => {
      memberStore.deleteMember(activeProject.value.id, member.user_id, (err, response) => {
        if (err) {
          q.notify({
            message: 'Có lỗi xảy ra',
            type: 'negative',
            icon: 'error',
            position: 'top'
          })
        } else {
          q.notify({
            message: 'Xóa thành viên thành công',
            type: 'positive',
            icon: 'check_circle',
            position: 'top'
          })
        }
        reloadMembers()
      })
    }

    const onChangeRole = (member, role) => {
      memberStore.updateMember(activeProject.value.id, member.user_id, role, (err, response) => {
        if (err) {
          q.notify({
            message: 'Có lỗi xảy ra',
            type: 'negative',
            icon: 'error',
            position: 'top'
          })
        } else {
          q.notify({
            message: 'Thay đổi vai trò thành công',
            type: 'positive',
            icon: 'check_circle',
            position: 'top'
          })
        }
        reloadMembers()
      })
    }

    const onLeaveProject = () => {
      memberStore.leaveProject(activeProject.value.id, (err, response) => {
        if (err) {
          q.notify({
            message: 'Có lỗi xảy ra',
            type: 'negative',
            icon: 'error',
            position: 'top'
          })
        } else {
          q.notify({
            message: 'Rời khỏi dự án thành công',
            type: 'positive',
            icon: 'check_circle',
            position: 'top'
          })
        }
        projectStore.fetchProjects(() => {
          router.push({ name: 'project' })
        })
      })
    }

    return {
      currentPage,
      searchText,
      searchTextRef,
      searchTextRules,
      loading,
      listMembers,
      numberOfPages,
      reloadMembers,
      searchApp,
      onReset,
      showAddMemberDialog,
      showAddMember,
      inviteEmail,
      onAddMemberRequest,
      currentRole,
      currentUser,
      activeProject,
      onDeleteMember,
      onChangeRole,
      onLeaveProject
    }
  }
}
</script>
