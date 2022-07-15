import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    dark: true,
    themes: {
      dark: {
        // primary: "#ff6fb9",
        // secondary: "#9782ff",
        primary: "#c774f7",
        secondary: "#9df07d",
        accent: "#8c9eff",
        error: "#b71c1c",
      },
    },
  },
});
