<template>
  <v-app style="overflow: hidden">
    <v-row>
      <v-col
        col="2"
        style="background-color: #1a1a1a"
        class="pt-10 px-5 d-flex flex-column"
      >
        <div class="d-flex justify-center my-3 mb-15">
          <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
            transition="scale-transition"
            width="5vw"
          />
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>
        <div class="d-flex justify-center my-3">
          <v-btn
            text
            class="my-3 mx-3 primary--text font-weight-thin text-h5"
            x-large
            :disabled="!isLogin"
            @click="
              () => {
                this.$router.push('/');
              }
            "
            >Home</v-btn
          >
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>
        <div class="d-flex justify-center my-3">
          <v-btn
            text
            class="my-3 mx-3 primary--text font-weight-thin text-h5"
            x-large
            :disabled="!isLogin"
            @click="
              () => {
                this.$router.push('/song_list');
              }
            "
          >
            Song <br />list
          </v-btn>
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>

        <div class="d-flex justify-center my-3">
          <v-btn
            text
            class="my-3 mx-3 primary--text font-weight-thin text-h5"
            x-large
            :disabled="!isLogin"
            >Current <br />
            playing</v-btn
          >
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>

        <div class="d-flex justify-center my-3">
          <v-btn
            text
            class="my-3 mx-3 primary--text font-weight-thin text-h5"
            x-large
            :disabled="!isLogin"
            >Chat<br />
            room</v-btn
          >
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>

        <div class="mt-auto d-flex justify-center my-3" v-if="isLogin">
          <v-btn
            text
            class="my-3 mx-3 secondary--text font-weight-thin text-h5"
            x-large
            @click="signOut"
          >
            Sign out
          </v-btn>
        </div>
        <div class="mt-auto d-flex justify-center my-3" v-else>
          <v-btn
            text
            class="my-3 mx-3 secondary--text font-weight-thin text-h5"
            x-large
            @click="
              () => {
                this.$router.push('/login');
              }
            "
          >
            Login
          </v-btn>
        </div>
      </v-col>
      <!-- <v-col
        col="2"
        style="background-color: #1a1a1a"
        class="d-flex align-start flex-column"
      >
        <div class="pa-2">test</div>
        <div class="mt-auto"><v-img></v-img></div>
      </v-col> -->
      <v-col cols="10" class="pa-0 ma-3">
        <v-main>
          <div class="home">
            <v-container class="pa-0 ma-0">
              <v-row
                style="height: 89vh; width: 85vw; overflow: hidden"
                justify="center"
              >
                <router-view style="overflow: hidden" />
              </v-row>

              <v-row
                style="height: 13vh; width: 90vw"
                justify="center"
                class="grey darken-4 pa-4"
              >
                <div style="width: 60vw">
                  <audio-player
                    ref="audioPlayer"
                    :audio-list="audioList.map((elm) => elm.url)"
                    theme-color="#9df07d"
                    :pause="initChart"
                    :ended="initChart"
                    :play-prev="initChart"
                    :play-next="initChart"
                    :before-prev="startNewSong"
                    :before-next="startNewSong"
                  />
                </div>
              </v-row>
            </v-container>
          </div>
        </v-main>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
import { clearUserInformationCookies } from "@/jsLibrary/cookies.js";
import AudioPlayer from "@liripeng/vue-audio-player";
import { apiAddress } from "@/config.js";

export default {
  name: "App",
  components: {
    AudioPlayer,
  },
  async mounted() {
    console.log(apiAddress);
    // console.log(BarChart.chartData);
    // this.chartData.labels = as
  },
  data: () => ({
    currentAudioName: "",
    audioList: [
      {
        name: "audio1",
        url: apiAddress + "/static/one_last_kiss.wav",
      },
      {
        name: "audio2",
        url: apiAddress + "/static/the_edge.wav",
      },
    ],
  }),

  computed: {
    isLogin: {
      get() {
        if (this.$cookies.isKey("username") == false) return false;
        else return true;
      },
    },
  },

  methods: {
    signOut: function () {
      clearUserInformationCookies(this);
      this.$toast.info("Successfully logged out", {
        position: "top-center",
        timeout: 2000,
      });
      setTimeout(() => {
        this.$router.push("/login");
      }, 2000);
    },

    startNewSong(next) {
      this.$refs.audioPlayer.pause();
      setTimeout(next, 700);
    },
    initChart() {
      this.chartData = this.getEmptyChart();
    },
    getEmptyChart() {
      return {
        labels: Array(100).fill(0.01),
        datasets: [
          {
            backgroundColor: "#c774f7",
            data: Array(100).fill(0.01),
          },
        ],
      };
    },
  },
};
</script>
