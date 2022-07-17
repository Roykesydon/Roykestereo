import Vue from "vue";
import Vuetify from "vuetify/lib/framework";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import VueCookies from "vue-cookies-reactive";

Vue.use(Vuetify);

Vue.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
});
Vue.use(VueCookies);
Vue.$cookies.config("1d");

export default new Vuetify({
  theme: {
    dark: true,
    themes: {
      dark: {
        // primary: "#ff6fb9",
        // secondary: "#9782ff",
        primary: "#c774f7",
        primary_dark: "#2D1839",
        secondary: "#9df07d",
        secondary_dark: "#56993D",
        accent: "#8c9eff",
        error: "#b71c1c",
        customBackground: "#212121",
      },
    },
  },
});
