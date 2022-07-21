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
            <v-btn
              class="mx-3"
              color="secondary"
              outlined
              rounded
              @click="addFavoriteListToQueue"
            >
              Add all music to queue
            </v-btn>
          </v-col>
        </v-row>
      </div>
    </v-row>
    <div class="my-5" v-for="_id in favoriteList" :key="_id">
      <div class="pa-5 pl-15 pr-15 mr-15 my-0">
        <v-row>
          <v-col cols="2">
            <v-img
              :src="apiAddress + '/music/cover/' + _id"
              :aspect-ratio="1 / 1"
              width="15vh"
            ></v-img>
          </v-col>
          <v-col cols="10" justify="center">
            <v-container fill-height fluid class="pa-0">
              <v-row style="width: 60vw" class="pa-0">
                <v-col cols="9" justify="center" class="pa-0">
                  <div class="font-weight-thin text-h3">
                    {{ musicInfo[_id].music_name }}
                  </div>
                  <div class="font-weight-thin text-h5">
                    {{ musicInfo[_id].nickname }}
                  </div>
                </v-col>
                <v-col cols="3" justify="end" align="end">
                  <!-- <v-btn color="primary" outlined rounded>Add new music</v-btn> -->
                  <div>
                    <v-btn
                      :color="favoriteColor(_id)"
                      dark
                      small
                      fab
                      class=""
                      @click="toggleFavorite(_id)"
                      style="height: 1em; width: 1em; font-size: 50px"
                    >
                      <v-icon size="20">mdi-heart</v-icon>
                    </v-btn>
                    <v-btn
                      color="#78cc58"
                      dark
                      small
                      fab
                      class="mx-8"
                      @click="addToQueue(_id)"
                      style="height: 1em; width: 1em; font-size: 50px"
                    >
                      <v-icon size="20">mdi-plus</v-icon>
                    </v-btn>
                    <v-btn
                      color="primary"
                      dark
                      small
                      fab
                      @click="cutInQueue(_id)"
                      style="height: 1em; width: 1em; font-size: 50px"
                    >
                      <v-icon size="20">mdi-play</v-icon>
                    </v-btn>
                  </div>
                </v-col>
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </div>
      <v-divider></v-divider>
    </div>
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
    let _this = this;

    await this.$axios
      .get(apiAddress + "/user/favorite_list")
      .then(async (response) => {
        // console.log(response.data);
        // console.log(_this);
        if (response.data.success == 1) {
          _this.favoriteList = response.data.data;
          for (const _id of _this.favoriteList) {
            _this.musicInfo[_id] = await this.returnMusicInfo(_id);
            _this.musicInfo[_id].favorite = true;
          }
          this.$forceUpdate();
        } else {
          if (response.data.msg.indexOf("auth") != -1) {
            this.$router.push("/login");

            this.$toast.error(response.data.msg, {
              position: "top-center",
              timeout: 2000,
            });
          }
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
  data() {
    return {
      currentAudioName: "",
      chartData: this.getEmptyChart(),
      username: "",
      nickname: "",
      favoriteList: [],
      musicInfo: {},
      apiAddress: apiAddress,
    };
  },
  methods: {
    favoriteColor: function (id) {
      // console.log(this.musicInfo[id]);
      if (!this.musicInfo[id].favorite) return "pink lighten-4";
      else return "pink";
    },
    toggleFavorite: async function (id) {
      let data = this.musicInfo[id];
      data.favorite = !data.favorite;
      this.$forceUpdate();

      await this.$axios
        .post(apiAddress + "/user/update_favorite_music", {
          method: data.favorite ? "add" : "remove",
          music_id: id,
        })
        .then((response) => {
          if (
            response.data.success != 1 &&
            response.data.msg.indexOf("auth") != -1
          ) {
            this.$router.push("/login");

            this.$toast.error(response.data.msg, {
              position: "top-center",
              timeout: 2000,
            });
          }
        })
        .catch((error) => {
          console.log(error);
        });

      this.musicInfo[id] = data;
    },
    addFavoriteListToQueue() {
      for (let i = 0; i < this.favoriteList.length; i++)
        this.$parent.$parent.$parent.addToQueue(this.favoriteList[i]);
    },
    addToQueue: function (id) {
      this.$parent.$parent.$parent.addToQueue(id);
    },
    cutInQueue: function (id) {
      this.$parent.$parent.$parent.cutInQueue(id);
    },
    returnMusicInfo: async function (id) {
      let data = null;
      await this.$axios
        .get(apiAddress + "/music/info/" + id.toString())
        .then(async (response) => {
          // console.log(response.data);
          data = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      return data;
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
