import Vue from 'vue'
import VueRouter from 'vue-router'
import * as View from '@/views'
import session from '@/plugins/session'
import { Ndp_Community_Board } from "@/views";

async function rootAccess(to, from, next) {
  if (!session.authentication && to.query.uid) {
    try {
      await session.loginFromProp(to.query.uid)
      next({ name: 'ndp_task_status_manage' })
    }
    catch (e) {
      next({ name: 'ndp_task_status_manage' })
    }
  }
  else next({ name: 'ndp_task_status_manage' })
}

const beforeEnter = (to, from, next) => {
  if (session.authentication) next()
  else next({ name: 'login' })
}

Vue.use(VueRouter)

const routes = [{
  path: '/',
  name: 'home',
  template: '<router-view />',
  beforeEnter: rootAccess
},
{
  path: '/ndp_task_file_upload',
  name: 'ndp_task_file_upload',
  component: View.Ndp_Task_File_Upload,
  template: '<router-view />',
},
{
  path: '/ndp_task_test_date',
  name: 'ndp_task_test_date',
  component: View.Ndp_Task_Test_Date,
  template: '<router-view />',
},
{
  path: '/login',
  component: View.Login,
  children: [
    {
      path: '',
      name: 'login',
      component: View.Login_SignIn
    },
    {
      path: 'signup',
      name: 'signup',
      component: View.Login_SignUp
    },
    {
      path: 'find-password',
      name: 'find-password',
      component: View.Login_FindPassword
    }
  ]
},
{
  path: '/ndp_user',
  name: 'ndp_user',
  component: View.SubView,
  redirect: { name: 'user_manage' },
  beforeEnter,
  children: [
    {
      path: 'user_manage',
      name: 'user_manage',
      component: View.User_Manage,
      meta: { breadcrumb: [{ text: '사용자 관리', disabled: true }, { text: '사용자 관리', disabled: true }] },
      props: true,
      beforeEnter
    },
    {
      path: 'ndp_user_hist',
      name: 'ndp_user_hist',
      component: View.Ndp_User_Hist,
      meta: { breadcrumb: [{ text: '사용자 관리', disabled: true }, { text: '접속이력', disabled: true }] },
      props: true,
      beforeEnter
    },
  ]
},
{
  path: '/ndp_community',
  name: 'ndp_community',
  component: View.SubView,
  redirect: { name: 'ndp_community_board' },
  beforeEnter,
  children: [
    {
      path: 'ndp_community_board',
      name: 'ndp_community_board',
      component: View.Ndp_Community_Board,
      meta: { breadcrumb: [{ text: '커뮤니티', disabled: true }, { text: '게시판', disabled: true }] },
      beforeEnter
    },

  ]
},
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
