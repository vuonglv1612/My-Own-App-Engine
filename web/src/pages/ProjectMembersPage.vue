<template>
  <q-page padding>
    <div class="row">
      <div class="col-md-8 offset-md-2">
        <div class="row">
          <h5 class="x-dashboard-page-title">Danh sách thành viên</h5>
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
        <div class="row">
          <q-btn
            color="primary"
            unelevated
            label="Thêm mới thành viên"
            @click="showAddMemberDialog"
          />
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
            <MemberListItem
              v-for="member in listMembers"
              :key="member.id"
              :member="member"
              :currentRole="currentRole"
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
          <q-btn flat label="Gửi yêu cầu" @click="onAddMemberRequest"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { ref, watch } from 'vue'
import { useProjectStore } from 'stores/project-store'
import { storeToRefs } from 'pinia'
import MemberListItem from 'components/MemberListItem.vue'
import { useMemberStore } from 'stores/members-store'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth-store'

export default {
  name: 'ProjectMembersPage',
  components: { MemberListItem },
  setup () {
    const searchText = ref(null)
    const currentPage = ref(1)
    const loading = ref(true)
    const searchTextRef = ref(null)
    const searchTextRules = [
      (v) => !!v || 'Vui lòng nhập từ khóa tìm kiếm'
    ]

    const projectStore = useProjectStore()
    const memberStore = useMemberStore()
    const authStore = useAuthStore()
    const q = useQuasar()

    const { currentUser } = storeToRefs(authStore)
    const { activeProject } = storeToRefs(projectStore)
    const { listMembers, numberOfPages } = storeToRefs(memberStore)
    memberStore.fetchMembers(activeProject.value.id, currentPage.value, searchText.value)
    loading.value = false

    const reloadMembers = () => {
      loading.value = true
      memberStore.fetchMembers(activeProject.value.id, currentPage.value, searchText.value)
      setTimeout(() => {
        loading.value = false
      }, 1000)
    }

    const getCurrentRole = () => {
      const currentMember = listMembers.value.find(member => member.user_id === currentUser.value.id)
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
      q.notify({
        message: 'Đã gửi yêu cầu thành công',
        color: 'positive',
        position: 'top',
        timeout: 2000
      })
      setTimeout(() => {
        showAddMember.value = false
      }, 2000)
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
      currentRole
    }
  }
}
</script>
