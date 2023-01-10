<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12">
        <div class="row">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Chi phí sử dụng</div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <div class="row">
                <div class="col-xs-12 col-md-6">
                  <div class="text-weight-bolder">Chi phí đã sử dụng</div>
                  <div class="text-caption text-italic">(Từ 1/1 - 9/1/2023)</div>
                  <div class="text-caption text-weight-medium">0.00 VND</div>
                </div>
                <div class="col-xs-12 col-md-6">
                  <div class="text-weight-bolder">Chi phí ước tính tới cuối tháng</div>
                  <div class="text-caption text-weight-medium">0.00 VND</div>
                </div>
              </div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <q-btn
                flat
                align="left"
                class="fit text-left text-weight-light"
                label="Chi tiết chi phí"
                icon="arrow_forward"
                :to="{ name: 'project.billing.invoices' }"
              />
            </q-card-section>
          </q-card>
        </div>
        <div class="row q-pt-md">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Nạp tiền</div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <div class="row q-ma-xs">
                <div v-for="option in depositOptions" :key="option.index" class="col-md-3 q-pa-xs">
                  <q-btn
                    flat
                    align="left"
                    class="fit bg-grey-2"
                    unelevated
                    color="primary"
                    :label="option.number.toLocaleString() + ' VND'"
                  />
                </div>
                <div class="col-md-3 q-pa-xs">
                  <q-input bottom-slots v-model="text" label="Label" counter maxlength="12" :dense="dense">
                    <template v-slot:before>
                      <q-avatar>
                        <img src="https://cdn.quasar.dev/img/avatar5.jpg">
                      </q-avatar>
                    </template>

                    <template v-slot:append>
                      <q-icon v-if="text !== ''" name="close" @click="text = ''" class="cursor-pointer"/>
                      <q-icon name="schedule"/>
                    </template>

                    <template v-slot:hint>
                      Field hint
                    </template>

                    <template v-slot:after>
                      <q-btn round dense flat icon="send"/>
                    </template>
                  </q-input>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="row q-pt-md">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Lịch sử nạp tiền</div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-xs">
              <div class="row">
                <div class="col-xs-12">
                  <q-table
                    :rows="rows"
                    :columns="columns"
                    row-key="name"
                    :separator="separator"
                    hide-pagination
                  />
                </div>
              </div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <q-btn
                flat
                align="left"
                class="fit text-left text-weight-light"
                label="Toàn bộ giao dịch"
                icon="arrow_forward"
                :to="{ name: 'project.billing.transactions' }"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style>
.tooltip-style {
  font-size: 12px;
  line-height: 1.5;
  color: #fff;
  background-color: #000;
  border-radius: 4px;
  padding: 8px;
  max-width: 200px;
}

</style>

<script>
import { ref } from 'vue'

export default {
  name: 'BillingDepositPage',
  setup () {
    const columns = [
      {
        name: 'name',
        required: true,
        label: 'Dessert (100g serving)',
        align: 'left',
        field: row => row.name,
        format: val => `${val}`,
        sortable: true
      },
      { name: 'calories', align: 'center', label: 'Calories', field: 'calories', sortable: true },
      { name: 'fat', label: 'Fat (g)', field: 'fat', sortable: true },
      { name: 'carbs', label: 'Carbs (g)', field: 'carbs' },
      { name: 'protein', label: 'Protein (g)', field: 'protein' },
      { name: 'sodium', label: 'Sodium (mg)', field: 'sodium' },
      {
        name: 'calcium',
        label: 'Calcium (%)',
        field: 'calcium',
        sortable: true,
        sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
      },
      {
        name: 'iron',
        label: 'Iron (%)',
        field: 'iron',
        sortable: true,
        sort: (a, b) => parseInt(a, 10) - parseInt(b, 10)
      }
    ]

    const rows = [
      {
        name: 'Frozen Yogurt',
        calories: 159,
        fat: 6.0,
        carbs: 24,
        protein: 4.0,
        sodium: 87,
        calcium: '14%',
        iron: '1%'
      },
      {
        name: 'Ice cream sandwich',
        calories: 237,
        fat: 9.0,
        carbs: 37,
        protein: 4.3,
        sodium: 129,
        calcium: '8%',
        iron: '1%'
      },
      {
        name: 'Eclair',
        calories: 262,
        fat: 16.0,
        carbs: 23,
        protein: 6.0,
        sodium: 337,
        calcium: '6%',
        iron: '7%'
      },
      {
        name: 'Cupcake',
        calories: 305,
        fat: 3.7,
        carbs: 67,
        protein: 4.3,
        sodium: 413,
        calcium: '3%',
        iron: '8%'
      },
      {
        name: 'Gingerbread',
        calories: 356,
        fat: 16.0,
        carbs: 49,
        protein: 3.9,
        sodium: 327,
        calcium: '7%',
        iron: '16%'
      },
      {
        name: 'Jelly bean',
        calories: 375,
        fat: 0.0,
        carbs: 94,
        protein: 0.0,
        sodium: 50,
        calcium: '0%',
        iron: '0%'
      },
      {
        name: 'Lollipop',
        calories: 392,
        fat: 0.2,
        carbs: 98,
        protein: 0,
        sodium: 38,
        calcium: '0%',
        iron: '2%'
      },
      {
        name: 'Honeycomb',
        calories: 408,
        fat: 3.2,
        carbs: 87,
        protein: 6.5,
        sodium: 562,
        calcium: '0%',
        iron: '45%'
      },
      {
        name: 'Donut',
        calories: 452,
        fat: 25.0,
        carbs: 51,
        protein: 4.9,
        sodium: 326,
        calcium: '2%',
        iron: '22%'
      },
      {
        name: 'KitKat',
        calories: 518,
        fat: 26.0,
        carbs: 65,
        protein: 7,
        sodium: 54,
        calcium: '12%',
        iron: '6%'
      }
    ]
    const tooltipContent = 'Chi phí chưa thanh toán là chi phí bạn đã sử dụng, ' +
      'nhưng chi phí này chưa chạm ngưỡng thanh toán. ' +
      'Mặc định, nếu cho tới cuối tháng chi phí vẫn chưa chạm ngưỡng thì sẽ tự động được trừ tiền '
    const account = ref({
      balance: 100000,
      unpaid_amount: 100000,
      status: 'Bình thường'
    })
    const invoices = ref([
      {
        id: 1,
        amount: 100000,
        name: 'Hóa đơn từ 1/1/2021 đến 31/1/2021',
        status: 'Đã thanh toán',
        created_at: '2021-02-01',
        url: '#'
      },
      {
        id: 2,
        amount: 100000,
        name: 'Hóa đơn từ 1/2/2021 đến 28/2/2021',
        status: 'Đã thanh toan',
        created_at: '2021-03-01',
        url: '#'
      },
      {
        id: 3,
        amount: 100300,
        name: 'Hóa đơn từ 1/3/2021 đến 31/3/2021',
        status: 'Chưa thanh toán',
        created_at: '2021-04-01',
        url: '#'
      },
      {
        id: 4,
        amount: 600000,
        name: 'Hóa đơn từ 1/4/2021 đến 30/4/2021',
        status: 'Chưa thanh toán',
        created_at: '2021-05-01',
        url: '#'
      },
      {
        id: 5,
        amount: 90000,
        name: 'Hóa đơn từ 1/5/2021 đến 31/5/2021',
        status: 'Chưa thanh toán',
        created_at: '2021-06-01',
        url: '#'
      }
    ])
    const depositOptions = ref([
      {
        index: 1,
        number: 100000,
        active: true
      },
      {
        index: 2,
        number: 200000,
        active: false
      },
      {
        index: 3,
        number: 500000,
        active: false
      },
      {
        index: 4,
        number: 1000000,
        active: false
      },
      {
        index: 5,
        number: 2000000,
        active: false
      },
      {
        index: 6,
        number: 5000000,
        active: false
      },
      {
        index: 7,
        number: 10000000,
        active: false
      }
    ])
    const customDeposit = ref(0)
    const customDepositInput = ref(null)
    const resetCustomDeposit = () => {
      customDeposit.value = null
      customDepositInput.value.resetValidation()
    }
    return {
      tooltipContent,
      account,
      rows,
      columns,
      invoices: invoices.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
      depositOptions,
      customDeposit,
      resetCustomDeposit
    }
  }
}
</script>
