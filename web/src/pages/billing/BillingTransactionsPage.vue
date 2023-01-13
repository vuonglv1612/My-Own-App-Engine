<template>
  <q-page padding>
    <div class="row q-mt-md">
      <div id="invoices-box" class="col-xs-12">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Danh sách giao dịch</div>
          </q-card-section>
          <q-separator/>
          <q-card-section>
            <div class="row">
              <div class="col-xs-12">
                <q-input outlined :model-value="`${transactionRange.from} - ${transactionRange.to}`">
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-date v-model="transactionRange" range>
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat/>
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
              <div class="col-xs-12">
                <AjaxTableComponent flat :columns="columns" :fetch-from-server="fetchFromServer"/>
              </div>
            </div>
          </q-card-section>
          <q-separator/>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { date } from 'quasar'

import AjaxTableComponent from 'components/AjaxTableComponent.vue'
import { ref, watch } from 'vue'

export default {
  name: 'BillingTransactionPage',
  components: { AjaxTableComponent },
  setup () {
    const formatDate = (strDate) => {
      const timeStamp = Date.parse(strDate)
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
      { name: 'transaction_id', align: 'left', label: 'Mã Giao Dịch', field: 'transaction_id' },
      { name: 'transaction_type', align: 'left', label: 'Loại giao dịch', field: 'transaction_type' },
      {
        name: 'amount',
        align: 'left',
        label: 'Số tiền',
        field: (row) => {
          return Number(row.transaction_amount).toLocaleString() + ' VND'
        },
        sortable: true
      },
      { name: 'transaction_status', align: 'left', label: 'Trạng thái', field: 'transaction_status' }
    ]

    const rows = [
      {
        created_at: '2022-12-12T12:00:00Z',
        transaction_id: 'TRANS-01',
        transaction_type: 'Nạp tiền',
        transaction_amount: 10000,
        transaction_status: 'Thành công'
      },
      {
        created_at: '2022-12-12T12:00:00Z',
        transaction_id: 'TRANS-02',
        transaction_type: 'Nạp tiền',
        transaction_amount: 60000,
        transaction_status: 'Thành công'
      },
      {
        created_at: '2022-12-12T12:00:00Z',
        transaction_id: 'TRANS-03',
        transaction_type: 'Thanh toán hóa đơn',
        transaction_amount: 50000,
        transaction_status: 'Thất bại'
      },
      {
        created_at: '2022-12-10T12:00:00Z',
        transaction_id: 'TRANS-04',
        transaction_type: 'Thanh toán hóa đơn',
        transaction_amount: 30000,
        transaction_status: 'Thất bại'
      },
      {
        created_at: '2022-12-11T12:00:00Z',
        transaction_id: 'TRANS-05',
        transaction_type: 'Thanh toán hóa đơn',
        transaction_amount: 30000,
        transaction_status: 'Thành công'
      }
    ]

    function fetchFromServer (pageOffset, pageSize, filter, sortBy, descending) {
      const total = rows.length
      if (pageSize) {
        return { records: rows.slice(pageOffset, pageOffset + pageSize), total }
      } else {
        return { records: rows, total }
      }
    }

    const transactionRange = ref({ from: Date.now(), to: Date.now() })
    watch(transactionRange.value, () => {
      console.log(transactionRange)
    })

    return {
      rows,
      columns,
      fetchFromServer,
      transactionRange
    }
  }
}
</script>
