<template>
  <div class="home">
    <v-row
      style="height: 40vh; width: 90vw"
      align="center"
      class="primary_dark pl-15"
    >
      <v-img
        src="@/assets/image/dj.jpg"
        min-width="15vw"
        max-width="15vw"
        max-height="15vw"
        min-height="15vw"
        :aspect-ratio="1 / 1"
      ></v-img>
      <div
        class="d-flex align-start flex-column pl-10"
        style="height: 12vw; width: 50vw"
      >
        <div class="font-weight-thin text-h1 mb-auto">Favorite Playlist</div>
        <v-row style="width: 60vw" class="d-flex align-end">
          <v-col cols="3">
            <div class="font-weight-thin text-h3">{{ nickname }}</div>
            <div class="font-weight-thin text-h6">@{{ username }}</div>
          </v-col>
          <v-col cols="9" class="d-flex align-end justify-end">
            <!-- <v-btn color="primary" outlined rounded>Add new music</v-btn> -->
            <v-btn class="mx-3" color="secondary" outlined rounded>
              Add all music to queue
            </v-btn>
          </v-col>
        </v-row>
      </div>
    </v-row>
  </div>
</template>

<script>
import { apiAddress } from "@/config.js";

export default {
  name: "FavoritePlaylistView",
  components: {},
  async mounted() {
    this.nickname = this.$cookies.get("nickname");
    this.username = this.$cookies.get("username");
  },
  data() {
    return {
      currentAudioName: "",
      chartData: this.getEmptyChart(),
      username: "",
      nickname: "",
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
    };
  },
  methods: {
    startNewSong(next) {
      this.$refs.audioPlayer.pause();
      setTimeout(next, 700);
    },
    initChart() {
      this.chartData = this.getEmptyChart();
    },
    getEmptyChart() {
      return {
        labels: Array(100).fill(0.005),
        datasets: [
          {
            backgroundColor: "#c774f7",
            data: Array(100).fill(0.005),
          },
        ],
      };
    },
    handleBeforePlay(next) {
      // There are a few things you can do here...
      this.currentAudioName =
        this.audioList[this.$refs.audioPlayer.currentPlayIndex].name;

      next(); // Start playing
    },
  },
};
</script>

<style>
.main {
  min-height: 70vh;
}
</style>
