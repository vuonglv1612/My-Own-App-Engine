<template>
  <q-page padding>
    <div class="row q-mt-md">
      <div id="invoices-box" class="col-xs-12">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Hóa đơn chưa thanh toán</div>
          </q-card-section>
          <q-separator/>
          <q-card-section class="q-pa-xs">
            <div class="row">
              <div class="col-xs-12">
                <q-table
                  flat
                  :rows="debRows"
                  :columns="debColumns"
                  row-key="invoice_id"
                />
              </div>
            </div>
          </q-card-section>
          <q-separator/>
        </q-card>
      </div>
    </div>
    <div class="row q-mt-md">
      <div id="invoices-box" class="col-xs-12">
        <q-card class="my-card fit">
          <q-card-section>
            <div class="text-h6">Danh sách hóa đơn</div>
          </q-card-section>
          <q-separator/>
          <q-card-section class="q-pa-xs">
            <div class="row">
              <div class="col-xs-12">
                <q-table
                  flat
                  :rows="rows"
                  :columns="columns"
                  row-key="invoice_id"
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

<script>
import { date } from 'quasar'

export default {
  name: 'BillingInvoicePage',
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
      { name: 'invoice_id', align: 'left', label: 'Mã Hóa Đơn', field: 'invoice_id' },
      { name: 'invoice_due', align: 'left', label: 'Hạn hóa đơn', field: row => formatDate(row.invoice_due) },
      {
        name: 'subtotal',
        align: 'left',
        label: 'Chi phí trước chiết khấu',
        field: (row) => {
          return Number(row.subtotal).toLocaleString() + ' VND'
        },
        sortable: true
      },
      {
        name: 'discount_amount',
        align: 'left',
        label: 'Chiết khấu',
        field: (row) => {
          return Number(row.discount).toLocaleString() + ' VND'
        },
        sortable: true
      },
      {
        name: 'total',
        align: 'left',
        label: 'Chi phí',
        field: (row) => {
          return Number(row.total).toLocaleString() + ' VND'
        },
        sortable: true
      },
      { name: 'invoice_status', align: 'left', label: 'Trạng thái', field: 'status' }
    ]

    const rows = [
      {
        created_at: '2022-12-12T12:00:00Z',
        invoice_id: 'INVOICE-01-01',
        invoice_due: '2022-12-12T12:00:00Z',
        subtotal: 120000,
        discount: 20000,
        total: 100000,
        status: 'Đã thanh toán'
      },
      {
        created_at: '2022-12-12T12:00:00Z',
        invoice_id: 'INVOICE-01-02',
        invoice_due: '2022-12-12T12:00:00Z',
        subtotal: 220000,
        discount: 40000,
        total: 180000,
        status: 'Đã thanh toán'
      },
      {
        created_at: '2022-12-15T12:00:00Z',
        invoice_id: 'INVOICE-01-03',
        invoice_due: '2022-12-12T12:00:00Z',
        subtotal: 20000,
        discount: 4000,
        total: 16000,
        status: 'Chưa thanh toán'
      }
    ]

    const debColumns = [
      {
        name: 'created_at',
        required: true,
        label: 'Ngày Tạo',
        align: 'left',
        sortable: true,
        field: row => formatDate(row.created_at)
      },
      { name: 'invoice_id', align: 'left', label: 'Mã Hóa Đơn', field: 'invoice_id' },
      { name: 'invoice_due', align: 'left', label: 'Hạn hóa đơn', field: row => formatDate(row.invoice_due) },
      {
        name: 'subtotal',
        align: 'left',
        label: 'Chi phí trước chiết khấu',
        field: (row) => {
          return Number(row.subtotal).toLocaleString() + ' VND'
        },
        sortable: true
      },
      {
        name: 'discount_amount',
        align: 'left',
        label: 'Chiết khấu',
        field: (row) => {
          return Number(row.discount).toLocaleString() + ' VND'
        },
        sortable: true
      },
      {
        name: 'total',
        align: 'left',
        label: 'Chi phí',
        field: (row) => {
          return Number(row.total).toLocaleString() + ' VND'
        },
        sortable: true
      },
      { name: 'due_status', align: 'left', label: 'Trạng thái', field: 'due_status' }
    ]

    const debRows = [
      {
        created_at: '2022-12-12T12:00:00Z',
        invoice_id: 'INVOICE-01-01',
        invoice_due: '2022-12-12T12:00:00Z',
        subtotal: 120000,
        discount: 20000,
        total: 100000,
        due_status: 'Đã quá hạn'
      }
    ]
    return {
      rows,
      columns,
      debRows,
      debColumns
    }
  }
}
</script>
