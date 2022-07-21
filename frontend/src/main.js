import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import vuetify from "./plugins/vuetify";
// import VueSocketIO from "vue-socket.io";
import VueSocketIOExt from "vue-socket.io-extended";
import { io } from "socket.io-client";

import { apiAddress } from "@/config.js";

Vue.config.productionTip = false;
axios.defaults.withCredentials = true;
Vue.prototype.$axios = axios;

const socket = io(apiAddress + "/chatroom");

Vue.use(VueSocketIOExt, socket);
// Vue.use(
//   new VueSocketIO({
//     debug: true,
//     connection: apiAddress + "/chatroom",
//   })
// );

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
