const routes = [
  {
    path: "/",
    redirect: "/signin",
    component: () => import("layouts/EmptyLayout.vue"),
    children: [
      { path: "/signin", component: () => import("pages/Signin.vue") },
      { path: "/signup", component: () => import("pages/Signup.vue") },
      {
        path: "/resetpassword",
        component: () => import("pages/ResetPassword.vue"),
      },
    ],
  },
  {
    path: "/e",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "/home", component: () => import("pages/IndexPage.vue") },
      { path: "/profile", component: () => import("pages/Profile.vue") },
      { path: "/users", component: () => import("pages/UsersPage.vue") },
      { path: "/survey", component: () => import("pages/SamplePage.vue") },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
