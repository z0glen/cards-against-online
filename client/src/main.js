import 'bootstrap/dist/css/bootstrap.css'
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
import VueSocketIO from "vue-socket.io"
import io from "socket.io-client"

import Vue from 'vue'

import App from './App.vue'
import router from './router'
import store from "./store"

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(new VueSocketIO({
  debug: true,
  connection: io('127.0.0.1:5000'),
  // connection: io(`//${window.location.host}`),
  // connection: io('https://cahplayer-server.herokuapp.com'),
  vuex: {
    store,
    actionPrefix: 'SOCKET_',
    mutationPrefix: 'SOCKET_',
  }
}))

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
