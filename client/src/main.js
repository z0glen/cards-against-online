import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue'
import VueSocketIO from "vue-socket.io"
import io from "socket.io-client"

import Vue from 'vue'

import App from './App.vue'
import router from './router'
import store from "./store"

console.log(`//${window.location.host}`)
Vue.use(BootstrapVue)
Vue.use(new VueSocketIO({
  debug: true,
  connection: io("http://localhost:5000"),
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
