import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "/login",
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/LoginView.vue"),
  },
  {
    path: "/favorite_playlist",
    name: "/favorite_playlist",
    component: () =>
      import(
        /* webpackChunkName: "about" */ "@/views/FavoritePlaylistView.vue"
      ),
  },
  {
    path: "/current_playing",
    name: "/current_playing",
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/CurrentPlayingView.vue"),
  },
  {
    path: "/chat_room",
    name: "/chat_room",
    component: () =>
      import(/* webpackChunkName: "about" */ "@/views/ChatRoomView.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
