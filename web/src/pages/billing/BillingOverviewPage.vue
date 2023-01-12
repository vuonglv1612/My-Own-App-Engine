<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12 col-md-9">
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
                    flat
                    :rows="rows"
                    :columns="columns"
                    row-key="payment_id"
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
      <div class="col-xs-12 col-md-3 q-pl-md">
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
                :to="{ name: 'project.billing.deposit', hash: '#deposit-box' }"
              />
            </q-card-section>
          </q-card>
        </div>

        <div class="row q-py-md">
          <q-card class="my-card fit">
            <q-card-section>
              <div class="text-h6">Hóa đơn gần đây</div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <span v-if="!invoices">Bạn chưa có hóa đơn</span>
              <q-list v-else class="q-pa-none">
                <q-item v-for="invoice in invoices" :key="invoice.id" clickable :to="invoice.url">
                  <q-item-section>
                    <q-item-label>{{ invoice.name }}</q-item-label>
                    <q-item-label caption>{{ invoice.date }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-item-label>{{ invoice.amount.toLocaleString() }} VND</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
            <q-separator/>
            <q-card-section class="q-pa-none">
              <q-btn
                flat
                align="left"
                class="fit text-left text-weight-light"
                label="Toàn bộ hóa đơn"
                icon="arrow_forward"
                :to="{ name: 'project.billing.invoices', hash: '#invoices-box' }"
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
import { date } from 'quasar'

export default {
  // name: 'PageName',
  setup () {
    const formatDate = (strDate) => {
      const timeStamp = Date(strDate)
      return date.formatDate(timeStamp, 'HH:mm:ss DD/MM/YYYY Z')
    }
    const columns = [
      {
        name: 'created_at',
        required: true,
        label: 'Ngày Tạo',
        align: 'left',
        sortable: true,
        field: row => formatDate(row.created_at)
      },
      { name: 'payment_id', align: 'left', label: 'Mã biên lai', field: 'payment_id' },
      { name: 'payment_method', align: 'left', label: 'Phương thức nạp tiền', field: 'payment_method' },
      {
        name: 'payment_amount',
        align: 'left',
        label: 'Số tiền nạp',
        field: (row) => {
          return Number(row.payment_amount).toLocaleString() + ' VND'
        },
        sortable: true
      },
      { name: 'payment_status', align: 'left', label: 'Trạng thái', field: 'payment_status' }
    ]

    const rows = [
      {
        created_at: '2022-12-12T12:00:00Z',
        payment_id: 'PM-01',
        payment_method: 'Chuyển Khoản',
        payment_amount: 10000,
        payment_status: 'Thành công'
      },
      {
        created_at: '2022-12-12T12:00:00Z',
        payment_id: 'PM-02',
        payment_method: 'Chuyển Khoản',
        payment_amount: 20000,
        payment_status: 'Thành công'
      },
      {
        created_at: '2022-12-12T12:00:00Z',
        payment_id: 'PM-03',
        payment_method: 'MoMo',
        payment_amount: 25000,
        payment_status: 'Thất bại'
      },
      {
        created_at: '2022-12-10T12:00:00Z',
        payment_id: 'PM-04',
        payment_method: 'MoMo',
        payment_amount: 25000,
        payment_status: 'Thất bại'
      },
      {
        created_at: '2022-12-11T12:00:00Z',
        payment_id: 'PM-05',
        payment_method: 'MoMo',
        payment_amount: 25000,
        payment_status: 'Thành công'
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
    return {
      tooltipContent,
      account,
      rows,
      columns,
      invoices: invoices.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)),
      formatDate
    }
  }
}
</script>
