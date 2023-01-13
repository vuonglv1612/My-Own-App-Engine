const routes = [
  {
    name: 'project',
    path: '/',
    redirect: { name: 'project.apps' },
    component: () => import('layouts/ProjectLayout.vue'),
    children: [
      { name: 'project.index', path: '', component: () => import('pages/ProjectIndexPage.vue') },
      { name: 'project.new_app', path: 'new-app', component: () => import('pages/ProjectNewAppPage.vue') },
      {
        name: 'project.apps',
        path: 'apps',
        component: () => import('pages/ProjectAppsPage.vue')
      },
      {
        name: 'project.apps.detail',
        path: '/apps/:appId',
        component: () => import('layouts/AppManageLayout.vue'),
        redirect: { name: 'project.apps.overview' },
        children: [
          { name: 'project.apps.overview', path: '/apps/:appId/overview', component: () => import('pages/app/AppOverview.vue') },
          { name: 'project.apps.activity', path: '/apps/:appId/activity', component: () => import('pages/app/AppActivityPage.vue') },
          { name: 'project.apps.logs', path: '/apps/:appId/logs', component: () => import('pages/app/AppLogsPage.vue') },
          { name: 'project.apps.env', path: '/apps/:appId/env', component: () => import('pages/app/AppEnvPage.vue') },
          { name: 'project.apps.settings', path: '/apps/:appId/settings', component: () => import('pages/app/AppSettingsPage.vue') }
        ]
      },
      { name: 'project.members', path: 'members', component: () => import('pages/ProjectMembersPage.vue') },
      { name: 'project.settings', path: 'settings', component: () => import('pages/ProjectSettingsPage.vue') },
      {
        name: 'project.billing',
        path: 'billing',
        component: () => import('layouts/ProjectBillingPageLayout.vue'),
        redirect: { name: 'project.billing.overview' },
        children: [
          {
            name: 'project.billing.overview',
            path: 'overview',
            component: () => import('pages/billing/BillingOverviewPage.vue')
          },
          {
            name: 'project.billing.invoices',
            path: 'invoices',
            component: () => import('pages/billing/BillingInvoicePage.vue')
          },
          {
            name: 'project.billing.transactions',
            path: 'transactions',
            component: () => import('pages/billing/BillingTransactionsPage.vue')
          },
          {
            name: 'project.billing.deposit',
            path: 'deposit',
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
