<template>
  <q-table
    ref="tableRef"
    :title="title"
    :rows="rows"
    :columns="columns"
    :row-key="rowKey"
    :loading="loading"
    hide-pagination
  >
    <template v-slot:bottom>
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
        @update:model-value="reloadTable"
      />
    </template>
  </q-table>
</template>

<script>
import { onMounted, ref } from 'vue'

export default {
  props: {
    columns: {
      type: Array,
      required: true
    },
    fetchFromServer: {
      type: Function
    },
    rowKey: {
      type: String,
      default: 'id'
    },
    title: {
      type: String,
      default: null
    }
  },
  setup (props) {
    const tableRef = ref()
    const rows = ref([])
    const loading = ref(false)
    const pageSize = ref(5)
    const currentPage = ref(1)
    const numberOfPages = ref(0)

    function reloadTable () {
      loading.value = true

      const sortBy = null
      const descending = null
      const pageOffset = (currentPage.value - 1) * pageSize.value

      // fetch data from "server"
      const { records, total } = props.fetchFromServer(pageOffset, pageSize.value, sortBy, descending)

      // clear out existing data and add new
      rows.value.splice(0, rows.value.length, ...records)
      numberOfPages.value = Math.ceil(total / pageSize.value)

      loading.value = false
    }

    onMounted(() => {
      reloadTable()
    })

    return {
      tableRef,
      loading,
      rows,
      currentPage,
      numberOfPages,

      reloadTable
    }
  }
}
</script>
