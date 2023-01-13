<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-8 offset-md-2">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Tạo ứng dụng</div>
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
                  title="Chọn nền tảng"
                  icon="settings"
                  :done="step > 1"
                >
                  Ứng dụng của bạn đang chạy trên nền tảng nào? Chúng tôi sẽ cung cấp cho bạn một số nền tảng phổ biến để bắt đầu.

                  <q-stepper-navigation>
                    <div class="row">
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-python" size="4em" color="primary"  @click="selectPlatform('python')"/>
                      </div>
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-golang" size="4em" color="primary" @click="selectPlatform('golang')"/>
                      </div>
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-java" size="4em" color="primary"/>
                      </div>
                      <div class="col-xs-6 col-md-3 cursor-pointer">
                        <q-icon name="fa-brands fa-node" size="4em" color="primary"/>
                      </div>
                    </div>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="2"
                  title="Create an ad group"
                  caption="Optional"
                  icon="create_new_folder"
                  :done="step > 2"
                >
                  An ad group contains one or more ads which target a shared set of keywords.

                  <q-stepper-navigation>
                    <q-btn @click="step = 4" color="primary" label="Continue"/>
                    <q-btn flat @click="step = 1" color="primary" label="Back" class="q-ml-sm"/>
                  </q-stepper-navigation>
                </q-step>

                <q-step
                  :name="3"
                  title="Ad template"
                  icon="assignment"
                  disable
                >
                  This step won't show up because it is disabled.
                </q-step>

                <q-step
                  :name="4"
                  title="Create an ad"
                  icon="add_comment"
                >
                  Try out different ad text to see what brings in the most customers, and learn how to
                  enhance your ads using features like ad extensions. If you run into any problems with
                  your ads, find out how to tell if they're running and how to resolve approval issues.

                  <q-stepper-navigation>
                    <q-btn color="primary" label="Finish"/>
                    <q-btn flat @click="step = 2" color="primary" label="Back" class="q-ml-sm"/>
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

export default {
  setup () {
    const step = ref(1)
    const selectPlatform = (platform) => {
      alert('Selected platform: ' + platform)
      step.value = 2
    }
    return {
      step,
      selectPlatform
    }
  }
}
</script>
