<template>
  <q-page padding>
    <div class="row">
      <div class="col-xs-12">
        <div class="row">
          <q-card id="deposit-box" class="my-card fit">
            <q-card-section>
              <div class="text-h6">Nạp tiền</div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <div class="text-subtitle1 q-pl-sm">Chọn nhanh số tiền cần nạp</div>
              <div class="row">
                <div v-for="option in predefinedDepositOptions" :key="option.amount"
                     class="col col-xs-12 col-md-4 q-pa-sm">
                  <q-btn flat class="fit deposit-option-box bg-grey-3 text-center justify-center q-pa-lg q-hoverable"
                         @click="requestTopUp(option.amount)">
                    {{ option.amount.toLocaleString() + ' VNĐ' }}
                  </q-btn>
                </div>
              </div>
            </q-card-section>
            <q-separator/>
            <q-card-section>
              <div class="text-subtitle1 q-pl-sm">Chọn số tiền muốn nạp</div>
              <div class="row">
                <q-input outlined type="number" suffix="VNĐ" v-model="customDeposit" class="q-pl-sm">
                  <template v-slot:append>
                    <div class="row">
                      <q-btn class="bg-primary text-white" flat label="Nạp tiền"
                             @click="requestTopUp(Number(customDeposit))"/>
                    </div>
                  </template>
                </q-input>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
    <div class="row q-mt-md">
      <div class="col-xs-12">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Lịch sử nạp tiền</div>
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
                />
              </div>
            </div>
          </q-card-section>
          <q-separator/>
        </q-card>
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
import { date, useQuasar } from 'quasar'
import TopUpComponent from 'components/TopUpComponent.vue'

export default {
  // name: 'PageName',
  setup () {
    const $q = useQuasar()
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
        label: 'Số tiền',
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
    const predefinedDepositOptions = [
      {
        amount: 50000
      },
      {
        amount: 100000
      },
      {
        amount: 200000
      },
      {
        amount: 500000
      },
      {
        amount: 1000000
      },
      {
        amount: 2000000
      }
    ]
    const depositAmount = ref(null)
    const requestTopUp = (depositAmount) => {
      $q.dialog({
        component: TopUpComponent,
        componentProps: {
          depositAmount
        },
        persistent: true
      })
    }

    const customDeposit = ref(0)
    return {
      rows,
      columns,
      customDeposit,
      predefinedDepositOptions,
      depositAmount,
      requestTopUp
    }
  }
}
</script>
