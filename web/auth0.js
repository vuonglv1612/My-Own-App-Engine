import { createAuth0 } from '@auth0/auth0-vue'

export const auth0 = createAuth0({
  domain: 'appengine.jp.auth0.com',
  clientId: '1cwEQPWCZw3AryA6rFRe8bfMxid9rvVe',
  authorizationParams: {
    redirect_uri: 'http://localhost:9000/callback',
    audience: 'http://localhost:8000/api'
  }
})
