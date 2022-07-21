<template>
  <div class="pa-10" style="overflow-y: hidden; overflow-x: hidden">
    <div style="overflow-y: hidden; overflow-x: hidden">
      <v-row class="mt-5 ml-10" style="width: 80vw">
        <v-col cols="12" class="font-weight-thin text-h2 py-10">
          <div class="mb-5">Music not in the platform?</div>
          <div class="text-h1 primary--text">Add it right now!</div>
        </v-col>
        <v-col cols="12" class="d-flex align-center pl-15 ma-0">
          <div class="arrow mr-0 my-auto">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <v-dialog v-model="addNewMusicDialog" width="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" x-large outlined v-bind="attrs" v-on="on">
                Add new music
              </v-btn>
            </template>

            <v-card class="pa-10">
              <div class="text-h4 pa-5 pb-0 primary--text">Add New Music</div>

              <v-divider class="my-5"></v-divider>

              <div>
                <v-form
                  ref="addMusicForm"
                  v-model="addMusicValid"
                  lazy-validation
                >
                  <v-row class="pa-3 d-flex align-center">
                    <v-col cols="6" class="text-h6 secondary--text">
                      Music name
                    </v-col>
                    <v-col cols="6">
                      <v-text-field
                        v-model="musicName"
                        label="Music Name"
                        :rules="[rules.required, rules.musicName]"
                        clearable
                      ></v-text-field
                    ></v-col>
                  </v-row>
                  <v-row class="pa-3 d-flex align-center">
                    <v-col cols="6" class="text-h6 secondary--text"
                      >Upload image</v-col
                    >
                    <v-col cols="6"
                      ><v-file-input
                        v-model="coverName"
                        accept="image/png, image/jpeg"
                        placeholder="Pick cover picture"
                        prepend-icon=""
                        append-icon="mdi-camera"
                        label="Cover Picture"
                        :rules="[rules.required]"
                        @change="uploadMusicImage"
                      ></v-file-input
                    ></v-col>
                  </v-row>
                  <v-row class="pa-3 d-flex align-center">
                    <v-col cols="6" class="text-h6 secondary--text"
                      >Upload file</v-col
                    >
                    <v-col cols="6"
                      ><v-file-input
                        v-model="fileName"
                        accept=".mp3, .wav"
                        placeholder="Pick cover picture"
                        prepend-icon=""
                        append-icon="mdi-music"
                        label="Music"
                        :rules="[rules.required]"
                        @change="uploadMusic"
                      ></v-file-input
                    ></v-col>
                  </v-row>
                </v-form>
              </div>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" text @click="addNewMusicDialog = false">
                  Cancel
                </v-btn>
                <v-btn
                  color="primary"
                  text
                  @click="addNewMusic"
                  :loading="isLoading"
                  >upload
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>
      <v-divider class="my-5"></v-divider>
      <div class="ma-0 pa-5">
        <v-row class="ma-15 mt-5">
          <v-col
            v-for="(value, key) in musicInfo"
            :key="key"
            cols="3"
            class="pa-5"
          >
            <v-card>
              <v-img
                :src="apiAddress + '/music/cover/' + key.toString()"
                :aspect-ratio="1 / 1"
              ></v-img>
              <v-card-title
                primary-title
                style="height: 100px; position: relative"
              >
                <div>
                  <div class="text-h6 text-truncate" style="width: 12vw">
                    {{ musicInfo[key].music_name }}
                  </div>
                  <div class="subtitle-1 text-truncate" style="width: 12vw">
                    {{ musicInfo[key].nickname }}
                  </div>
                  <div
                    style="position: absolute; right: 0px; top: -20px"
                    class="px-5"
                  >
                    <v-btn
                      :color="favoriteColor(key)"
                      dark
                      small
                      fab
                      class="mr-3"
                      @click="toggleFavorite(key)"
                    >
                      <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <v-btn
                      color="#78cc58"
                      dark
                      small
                      fab
                      class="mr-3"
                      @click="addToQueue(key)"
                    >
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                    <v-btn
                      color="primary"
                      dark
                      small
                      fab
                      @click="cutInQueue(key)"
                    >
                      <v-icon>mdi-play</v-icon>
                    </v-btn>
                  </div>
                </div>
              </v-card-title>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>
<script>
import { rules } from "@/jsLibrary/rules.js";
import { apiAddress } from "@/config.js";
import Vue from "vue";

export default {
  name: "HomeView",
  components: {},
  data() {
    return {
      rules: rules,
      addNewMusicDialog: false,
      addMusicValid: false,
      coverPicture: null,
      musicFile: null,
      musicName: "",
      isLoading: false,
      totalMusicCount: 0,
      apiAddress: apiAddress,
      musicInfo: {},
      coverName: "",
      fileName: "",
      idList: [],
    };
  },
  async mounted() {
    let _this = this;
    await this.$axios
      .get(apiAddress + "/music/all_id_list")
      .then(async (response) => {
        _this.idList = response.data;
        _this.musicInfo = {};
        for (let i = 0; i < _this.idList.length; i++) {
          _this.musicInfo[_this.idList[i]] = {
            username: "",
            nickname: "",
            music_name: "",
            favorite: false,
          };
          _this.musicInfo[this.idList[i]] = await this.returnMusicInfo(
            this.idList[i]
          );
          this.$forceUpdate();
        }
      })
      .catch((error) => {
        console.log(error);
      });

    // console.log("hey", this.musicInfo);

    await this.$axios
      .get(apiAddress + "/user/favorite_list")
      .then(async (response) => {
        // console.log(response.data);
        if (response.data.success == 1) {
          let favoriteList = response.data.data;
          for (let i = 0; i < favoriteList.length; i++) {
            let musicId = favoriteList[i];
            if (!(musicId in this.musicInfo)) continue;
            let data = this.musicInfo[musicId];
            data.favorite = true;
            Vue.set(this.musicInfo, musicId, data);
            // console.log("what", this.musicInfo);
            _this.$forceUpdate();
          }
        } else {
          if (response.data.msg.indexOf("auth") != -1) {
            this.$router.push("/login");

            this.$toast.error(response.data.msg, {
              position: "top-center",
              timeout: 2000,
            });
          }
        }
        // console.log(response.data);
        // this.musicInfo = Array(parseInt(response.data.data.length)).fill({
        //   username: "",
        //   nickname: "",
        //   music_name: "",
        //   favorite: false,
        // });
        // this.musicInfo
        this.totalMusicCount = parseInt(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
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

      Vue.set(this.musicInfo, id, data);
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
    uploadMusicImage: function (file) {
      const reader = new FileReader();
      reader.addEventListener("load", (e) => {
        this.coverPicture = e.target.result;
      });
      reader.addEventListener("error", () => {
        this.$toast.error("Uplaod image error", {
          position: "top-center",
          timeout: 2000,
        });
      });
      reader.readAsDataURL(file);
    },
    uploadMusic: function (file) {
      const reader = new FileReader();
      reader.addEventListener("load", (e) => {
        this.musicFile = e.target.result;
      });
      reader.addEventListener("error", () => {
        this.$toast.error("Uplaod file error", {
          position: "top-center",
          timeout: 2000,
        });
      });
      reader.readAsDataURL(file);
    },
    requestAddMusic: async function () {
      await this.$axios
        .post(
          apiAddress + "/music/upload_music",
          {
            music_name: this.musicName,
            cover: this.coverPicture,
            music: this.musicFile,
          },
          {
            timeout: 1000 * 60 * 10,
          }
        )
        .then((response) => {
          if (response.data.success == 1) {
            this.$toast.success("Upload Success!\n", {
              position: "top-center",
              timeout: 2000,
            });
          } else {
            if (response.data.msg.indexOf("auth") != -1) {
              this.$router.push("/login");
            }
            this.$toast.error(response.data.msg, {
              position: "top-center",
              timeout: 2000,
            });
          }
        })
        .catch((error) => {
          this.$toast.error(String(error), {
            position: "top-center",
            timeout: 2000,
          });
          console.log(error);
        });
    },
    addNewMusic: async function () {
      if (this.$refs.addMusicForm.validate() == false) {
        return;
      }

      this.requestAddMusic();
      this.addNewMusicDialog = false;
      this.coverPicture = null;
      this.musicFile = null;
      this.musicName = "";
      this.coverName = "";
      this.fileName = "";
      this.$refs.addMusicForm.reset();
      this.$toast.info(
        "Already send request\nMight take several minutes to upload to server",
        {
          position: "top-center",
          timeout: 2000,
        }
      );
    },
  },
};
</script>

<style scope>
.arrow {
  transform: translate(-50%, -50%);
}
.arrow span {
  display: inline-block;
  width: 30px;
  height: 30px;
  border-bottom: 5px solid #9df07d;
  border-right: 5px solid #c774f7;
  margin: -5px;
  position: relative;
  top: 17px;
  animation: animate 2s infinite;
}
.arrow span:nth-child(2) {
  animation-delay: -0.2s;
}
.arrow span:nth-child(3) {
  animation-delay: -0.4s;
}
@keyframes animate {
  0% {
    opacity: 0;
    transform: rotate(-45deg) translate(-20px, -20px);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: rotate(-45deg) translate(0px, 0px);
  }
}
</style>
