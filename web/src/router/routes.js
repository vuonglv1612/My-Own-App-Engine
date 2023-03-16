import { authGuard } from '@auth0/auth0-vue'

const routes = [
  {
    name: 'index',
    path: '',
    component: () => import('pages/LandingPage.vue')
  },
  {
    name: 'callback',
    path: '/callback',
    component: () => import('pages/CallBackPage.vue')
  },
  {
    name: 'project',
    path: '/dashboard',
    redirect: { name: 'project.apps' },
    beforeEnter: authGuard,
    component: () => import('layouts/ProjectLayout.vue'),
    children: [
      // { name: 'project.index', path: '', component: () => import('pages/ProjectIndexPage.vue') },
      {
        name: 'project.new_app',
        path: 'new-app',
        beforeEnter: authGuard,
        component: () => import('pages/ProjectNewAppPage.vue')
      },
      {
        name: 'project.apps',
        path: 'apps',
        beforeEnter: authGuard,
        component: () => import('pages/ProjectAppsPage.vue')
      },
      {
        name: 'project.apps.detail',
        path: '/dashboard/apps/:appId',
        beforeEnter: authGuard,
        component: () => import('layouts/AppManageLayout.vue'),
        redirect: { name: 'project.apps.overview' },
        children: [
          {
            name: 'project.apps.overview',
            path: '/dashboard/apps/:appId/overview',
            beforeEnter: authGuard,
            component: () => import('pages/app/AppOverview.vue')
          },
          {
            name: 'project.apps.activity',
            path: '/dashboard/apps/:appId/activity',
            beforeEnter: authGuard,
            component: () => import('pages/app/AppActivityPage.vue')
          },
          {
            name: 'project.apps.logs',
            path: '/dashboard/apps/:appId/logs',
            beforeEnter: authGuard,
            component: () => import('pages/app/AppLogsPage.vue')
          },
          {
            name: 'project.apps.env',
            path: '/dashboard/apps/:appId/env',
            beforeEnter: authGuard,
            component: () => import('pages/app/AppEnvPage.vue')
          },
          {
            name: 'project.apps.deploy',
            path: '/dashboard/apps/:appId/deploy',
            beforeEnter: authGuard,
            component: () => import('pages/app/DeployPage.vue')
          },
          {
            name: 'project.apps.settings',
            path: '/dashboard/apps/:appId/settings',
            beforeEnter: authGuard,
            component: () => import('pages/app/AppSettingsPage.vue')
          }
        ]
      },
      {
        name: 'project.members',
        path: 'members',
        beforeEnter: authGuard,
        component: () => import('pages/ProjectMembersPage.vue')
      },
      {
        name: 'project.settings',
        path: 'settings',
        beforeEnter: authGuard,
        component: () => import('pages/ProjectSettingsPage.vue')
      },
      {
        name: 'project.billing',
        path: 'billing',
        beforeEnter: authGuard,
        component: () => import('layouts/ProjectBillingPageLayout.vue'),
        redirect: { name: 'project.billing.overview' },
        children: [
          {
            name: 'project.billing.overview',
            path: 'overview',
            beforeEnter: authGuard,
            component: () => import('pages/billing/BillingOverviewPage.vue')
          },
          {
            name: 'project.billing.invoices',
            path: 'invoices',
            beforeEnter: authGuard,
            component: () => import('pages/billing/BillingInvoicePage.vue')
          },
          {
            name: 'project.billing.transactions',
            path: 'transactions',
            beforeEnter: authGuard,
            component: () => import('pages/billing/BillingTransactionsPage.vue')
          },
          {
            name: 'project.billing.deposit',
            path: 'deposit',
            beforeEnter: authGuard,
            component: () => import('pages/billing/BillingDepositPage.vue')
          }
        ]
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    name: 'notfound',
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
