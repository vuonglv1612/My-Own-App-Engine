<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-10">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Triển khai phiên bản mới</div>
          </q-card-section>
          <q-separator/>
          <q-card-section class="q-pa-none">
            <div>
              <q-stepper
                v-model="step"
                vertical
                color="primary"
                animated
                flat
              >
                <q-step
                  :name="1"
                  title="Chọn nguồn"
                  icon="settings"
                  :done="step > 1"
                >
                  Chọn cách thức triển khai phiên bản mới của ứng dụng của bạn.
                  Chúng tôi hỗ trợ 2 cách thức là triển khai từ mã nguồn hoặc triển khai từ Docker image.
                  <q-stepper-navigation>
                    <div class="row">
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-git" size="4em" color="primary"
                                @click="selectSource('git')"/>
                      </div>
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-docker" size="4em" color="primary"
                                @click="selectSource('image')"/>
                      </div>
                    </div>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="2"
                  title="Nhập đường dẫn"
                  icon="create_new_folder"
                  :done="step > 2"
                >
                  <div class="sources">
                    <div v-if="selectedSource === 'git'">
                      <q-input
                        v-model="gitUrl"
                        label="Git URL"
                        hint="Ví dụ: https://gitlab.com/vuonglv1612/test-python"
                        outlined
                        class="my-input q-mt-md"
                      />
                      <q-input
                        v-model="gitBranch"
                        label="Git Branch"
                        hint="Ví dụ: master"
                        outlined
                        class="my-input q-mt-md"
                      />
                    </div>
                    <div v-if="selectedSource === 'image'">
                      <q-input
                        v-model="dockerImage"
                        label="Docker Image"
                        hint="Ví dụ: vuonglv/sample-api:latest"
                        outlined
                        class="my-input q-mt-md"
                      />
                    </div>
                  </div>
                  <q-stepper-navigation>
                    <q-btn @click="step = 3" color="primary" label="Tiếp theo" class="q-ml-sm"/>
                    <q-btn flat @click="step = 1" color="primary" label="Trở lại" class="q-ml-sm"/>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="3"
                  title="Xác nhận thông tin"
                  icon="add_comment"
                >
                  <div class="confirm">
                    <div class="row">
                      <div class="col-xs-6 col-md-6">
                        <div class="text-caption">Nguồn triển khai: {{ selectedSource }}</div>
                      </div>
                      <div v-if="selectedSource === 'git'" class="col-xs-12 col-md-12">
                        <div class="text-caption">Git Url: {{ gitUrl }}</div>
                      </div>
                      <div v-if="selectedSource === 'git'" class="col-xs-12 col-md-12">
                        <div class="text-caption">Git Branch: {{ gitBranch }}</div>
                      </div>
                      <div v-if="selectedSource === 'image'" class="col-xs-12 col-md-12">
                        <div class="text-caption">Docker Image: {{ dockerImage }}</div>
                      </div>
                    </div>
                  </div>
                  <q-stepper-navigation>
                    <q-btn @click="submitDeployApp" color="primary" label="Triển khai"/>
                    <q-btn flat @click="step = 2" color="primary" label="Quay lại" class="q-ml-sm"/>
                  </q-stepper-navigation>
                </q-step>
              </q-stepper>
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectStore } from 'stores/project-store'
import { useAppStore } from 'stores/app-store'
import { useQuasar } from 'quasar'

export default {
  name: 'DeployPage',
  setup () {
    const $q = useQuasar()
    const route = useRoute()
    const step = ref(1)
    const selectedSource = ref(null)
    const version = ref('latest')
    const gitUrl = ref('')
    const gitBranch = ref('master')
    const dockerImage = ref('')
    const appId = ref(route.params.appId)
    const projectStore = useProjectStore()
    const appStore = useAppStore()
    const router = useRouter()

    const submitDeployApp = () => {
      const params = {
        source_url: gitUrl.value,
        source_type: selectedSource.value,
        version: version.value,
        git_branch: gitBranch.value
      }
      if (selectedSource.value === 'git') {
        params.source_url = gitUrl.value
        params.git_branch = gitBranch.value
      } else {
        params.source_url = dockerImage.value
      }
      appStore.deployApp(projectStore.activeProject.id, appId.value, params, (error, data) => {
        if (error) {
          $q.notify({
            message: 'Có lỗi xảy ra khi triển khai ứng dụng',
            color: 'negative',
            position: 'top',
            timeout: 2000
          })
        } else {
          $q.notify({
            message: 'Triển khai ứng dụng thành công',
            color: 'positive',
            position: 'top',
            timeout: 2000
          })
          step.value = 1
          router.push({ name: 'project.apps.logs', params: { appId: appId.value } })
        }
      })
    }

    const selectSource = (source) => {
      selectedSource.value = source
      step.value = 2
    }

    return {
      step,
      submitDeployApp,
      selectSource,
      selectedSource,
      gitUrl,
      gitBranch,
      dockerImage,
      version
    }
  }
}
</script>
