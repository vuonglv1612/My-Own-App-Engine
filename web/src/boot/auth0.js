import { boot } from 'quasar/wrappers'
import { auth0 } from 'app/auth0'

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({ app }) => {
  app.use(auth0)
})
