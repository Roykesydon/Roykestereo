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
        <div
          class="d-flex justify-start my-3 pl-5 pointer"
          @click="
            () => {
              this.$router.push('/');
            }
          "
        >
          <v-icon color="primary">mdi-home</v-icon>
          <div class="my-3 ml-3 px-0 primary--text font-weight-thin text-h5">
            Home
          </div>
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>
        <div
          class="d-flex justify-start my-3 pl-5 pointer"
          @click="
            () => {
              this.$router.push('/favorite_playlist');
            }
          "
        >
          <v-icon color="primary">mdi-heart</v-icon>
          <div class="my-3 ml-3 px-0 primary--text font-weight-thin text-h5">
            Favorite <br />Playlist
          </div>
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>

        <div
          class="d-flex justify-start my-3 pl-5 pointer"
          @click="
            () => {
              this.$router.push('/current_playing');
            }
          "
        >
          <v-icon color="primary">mdi-disc</v-icon>
          <div class="my-3 ml-3 px-0 primary--text font-weight-thin text-h5">
            Current <br />
            Playing
          </div>
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>

        <div
          class="d-flex justify-start my-3 pl-5 pointer"
          @click="
            () => {
              this.$router.push('/');
            }
          "
        >
          <v-icon color="primary">mdi-party-popper</v-icon>
          <div class="my-3 ml-3 px-0 primary--text font-weight-thin text-h5">
            Chat<br />
            Room
          </div>
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

      <v-col cols="10" class="pa-0 ma-3">
        <v-main>
          <div class="">
            <v-container class="pa-0 ma-0">
              <v-row
                style="height: 89vh; width: 85vw; overflow-x: hidden"
                justify="center"
                class="route"
              >
                <router-view
                  :currentMusicId="currentMusicId"
                  style="overflow-y: hidden; overflow-x: hidden"
                />
              </v-row>

              <v-row
                style="height: 13vh; width: 90vw"
                justify="center"
                class="grey darken-4 pa-4"
              >
                <div style="width: 60vw">
                  <audio-player
                    ref="audioPlayer"
                    :progress-interval="1000 / 25"
                    :audio-list="audioList"
                    theme-color="#c774f7"
                    :pause="initChart"
                    :ended="nextMusic"
                    :before-prev="prevMusic"
                    :before-next="nextMusic"
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
// import Vue from "vue";

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
    musicNextQueue: [],
    musicPrevStack: [],
    currentMusicId: "",
    audioList: [],
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
    addToQueue(id) {
      if (id != this.currentMusicId) {
        this.musicNextQueue.push(id);
      }
      if (this.currentMusicId == "") {
        this.$refs.audioPlayer.playNext();
      }
    },

    cutInQueue(id) {
      if (id != this.currentMusicId) {
        this.musicNextQueue.unshift(id);
        this.$refs.audioPlayer.playNext();
      }
    },

    signOut: function () {
      clearUserInformationCookies(this);
      this.$toast.info("Successfully logged out", {
        position: "top-center",
        timeout: 2000,
      });

      this.$router.push("/login");
    },

    nextMusic(next) {
      if (this.currentMusicId != "")
        this.musicPrevStack.push(this.currentMusicId);
      console.log(this.musicNextQueue);
      if (this.musicNextQueue.length != 0) {
        this.currentMusicId = this.musicNextQueue[0];
        this.audioList = [
          apiAddress + "/music/audio/" + this.currentMusicId.toString(),
        ];
        // Vue.set(
        //   this.audioList,
        //   0,
        //   apiAddress + "/music/audio/" + this.musicNextQueue[0].toString()
        // );

        // this.musicPrevStack.push(this.musicNextQueue[0]);
        this.musicNextQueue.shift();

        this.$refs.audioPlayer.pause();
        this.$refs.audioPlayer.currentTime = 0;
        setTimeout(next, 700);
      } else {
        this.audioList = [""];
        this.currentMusicId = "";
      }
    },

    prevMusic(next) {
      if (this.currentMusicId != "")
        this.musicNextQueue.unshift(this.currentMusicId);
      if (this.musicPrevStack.length != 0) {
        this.currentMusicId =
          this.musicPrevStack[this.musicPrevStack.length - 1];

        this.audioList = [
          apiAddress + "/music/audio/" + this.currentMusicId.toString(),
        ];

        this.musicPrevStack.pop();
        this.$refs.audioPlayer.pause();
        this.$refs.audioPlayer.currentTime = 0;
        setTimeout(next, 700);
      } else {
        this.audioList = [""];
        this.currentMusicId = "";
      }
      console.log(
        this.musicPrevStack,
        this.currentMusicId,
        this.musicNextQueue
      );
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

<style scope>
.v-btn:before {
  opacity: 0 !important;
}

.v-ripple__container {
  opacity: 0 !important;
}

.route {
  /* background-image: linear-gradient(
    to right top,
    #2c1732,
    #23162b,
    #1b1523,
    #15131a,
    #0f0f0f
  ); */
  /* background-image: linear-gradient(
    to right top,
    #150a18,
    #110915,
    #0d0811,
    #08070c,
    #050505
  ); */
  background-image: linear-gradient(
    to right top,
    #0f0811,
    #0c070f,
    #09070c,
    #070609,
    #050505
  );
}

::-webkit-scrollbar {
  display: none;
}

.pointer {
  cursor: pointer;
}
.pointer:hover {
  border-radius: 25px;

  background-color: #2d1839;
}
</style>
