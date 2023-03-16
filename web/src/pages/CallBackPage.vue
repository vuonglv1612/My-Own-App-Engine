<template>
  <div class="col">
    <div class="row items-center">
      <div class="col">
        <q-spinner-dots size="64px" color="primary"/>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue'
import { useRouter } from 'vue-router'

export default {
  // name: 'PageName',
  setup () {
    // Auth
    const auth0 = useAuth0()
    const router = useRouter()

    if (auth0.isAuthenticated) {
      router.push({ name: 'project' })
    } else {
      auth0.loginWithRedirect(
        {
          target: '/dashboard'
        }
      )
    }

    return {}
  }
}
</script>
