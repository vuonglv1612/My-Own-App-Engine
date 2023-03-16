<template>
  <q-btn v-if="isAuthenticated" label="Logout" @click="logout"/>
  <q-btn v-else label="Login" @click="login"/>
</template>

<script>
import { useAuth0 } from '@auth0/auth0-vue'

export default {
  name: 'LoginPage',
  setup () {
    const auth0 = useAuth0()
    const { isAuthenticated } = auth0
    const login = () => {
      auth0.loginWithRedirect({
        target: '/dashboard'
      })
    }
    const logout = () => {
      auth0.logout(
        {
          returnTo: window.location.origin
        }
      )
    }
    return { login, logout, isAuthenticated }
  }
}
</script>
