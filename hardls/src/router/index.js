import Vue from 'vue'
import Router from 'vue-router'
import ChatRooms from '@/components/ChatRooms'
import Auth from '@/components/Auth'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
//Vue.use(IconsPlugin)
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
      /*{
        path: '/',
        name: 'Auth',
        component: Auth
    },*/
    {
      path: '/',
      name: 'ChatRooms',
      component: ChatRooms
    }
  ]
})
