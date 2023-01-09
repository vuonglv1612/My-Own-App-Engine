<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-6">
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
        <div class="row q-py-md">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Giao dịch gần đây</div>
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
                label="Chi tiết giao dịch"
                icon="arrow_forward"
                :to="{ name: 'project.billing.transactions' }"
              />
            </q-card-section>
          </q-card>
        </div>
      </div>
      <div class="col-xs-12 col-md-3 q-px-md">
        <div class="row">

          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Tài Khoản</div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <div class="text-caption"><b>Số dư:</b> {{ account.balance.toLocaleString() }} VND</div>
              <span class="text-caption"><b>Chi phí chưa thanh toán:</b> {{
                  account.unpaid_amount.toLocaleString()
                }} VND</span>
              <span><q-icon name="help">
                <q-tooltip class="tooltip-style" :offset="[10, 10]">{{ tooltipContent }}</q-tooltip>
              </q-icon></span>
              <div class="text-caption"><b>Trạng thái tài khoản:</b> {{ account.status }}</div>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <q-btn
                flat
                align="left"
                class="fit text-left text-weight-light"
                label="Nạp tiền"
                icon="arrow_forward"
                :to="{ name: 'project.billing.deposit' }"
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
  // name: 'PageName',
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
    return {
      tooltipContent,
      account,
      rows,
      columns
    }
  }
}
</script>
