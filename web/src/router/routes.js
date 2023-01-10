const routes = [
  {
    name: 'project',
    path: '/',
    component: () => import('layouts/ProjectLayout.vue'),
    children: [
      { name: 'project.index', path: '', component: () => import('pages/ProjectIndexPage.vue') },
      { name: 'project.apps', path: 'apps', component: () => import('pages/ProjectAppsPage.vue') },
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
