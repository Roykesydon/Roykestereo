<template>
  <div class="home pa-15" style="overflow-y: scroll">
    <v-row
      style="height: 85vh; width: 80vw; overflow-x: hidden"
      justify="center"
      class="d-flex flex-column"
    >
      <div
        class="d-flex align-start justify-center pa-0 ma-10 flex-column"
        style="height: 60vh; width: 10vw"
      >
        <div class="logo-wall" style="width: 30vw">
          <div class="logo-wrapper first">
            <div
              class="mt-0 mb-10 font-weight-thin text-h2"
              style="white-space: nowrap"
            >
              <span class="mr-5" v-for="i in 20" :key="i">
                {{ musicName }} / {{ authorName }}
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              </span>
            </div>
          </div>
        </div>

        <div class="mb-0">
          <div class="d-flex align-center justify-center">
            <v-img
              style="background-color: #222222"
              :src="musicCover"
              min-width="20vw"
              max-width="20vw"
              max-height="20vw"
              min-height="20vw"
              :aspect-ratio="1 / 1"
            ></v-img>

            <bar-chart
              style="height: 30vh; width: 55vw"
              class="my-auto px-10"
              :chartData="chartData"
            />
          </div>
        </div>
        <div class="mt-5 mb-10 font-weight-thin text-h5"></div>
      </div>
    </v-row>
  </div>
</template>

<script>
import BarChart from "@/components/BarChart.vue";
import { apiAddress } from "@/config.js";

export default {
  name: "CurrentPlayingView",
  components: {
    BarChart,
  },
  props: {
    currentMusicId: {
      type: String,
    },
  },
  async mounted() {
    // console.log(apiAddress);
    if (this.currentMusicId != "") {
      this.musicCover =
        apiAddress + "/music/cover/" + this.currentMusicId.toString();

      let musicInfo = await this.returnMusicInfo(this.currentMusicId);
      this.musicName = musicInfo["music_name"];
      this.authorName = musicInfo["nickname"];

      await this.$axios
        .get(apiAddress + "/music/wave/" + this.currentMusicId.toString())
        .then((response) => {
          this.musicWave = response.data.wave;
        })
        .catch((error) => {
          console.log(error);
        });
    }

    let _this = this;
    let frameCount = 0;
    let secondFreq = 20;

    function updateWaveChart() {
      setTimeout(function () {
        if (
          _this.$parent.$parent.$parent.$refs.audioPlayer.currentTime === "" ||
          _this.currentMusicId == "" ||
          _this.updateDataFlag
        ) {
          _this.initChart();
          updateWaveChart();
          return;
        }

        if (_this.$parent.$parent.$parent.$refs.audioPlayer.isPlaying != true) {
          _this.initChart();
          updateWaveChart();
          return;
        }
        // console.log(
        //   _this.$parent.$parent.$parent.$refs.audioPlayer.currentTime
        // );
        let currentTime = Math.floor(
          _this.$parent.$parent.$parent.$refs.audioPlayer.currentTime
        );

        frameCount =
          Math.floor(
            (Math.floor(
              _this.$parent.$parent.$parent.$refs.audioPlayer.currentTime * 1000
            ) %
              1000) /
              (1000 / secondFreq)
          ) + 1;

        if (currentTime * secondFreq + frameCount >= _this.musicWave.length) {
          updateWaveChart();
          return;
        }

        let wave = _this.musicWave[currentTime * secondFreq + frameCount];

        for (let index = 0; index < wave.length; ++index) wave[index] += 0.005;

        _this.chartData.labels = wave;
        _this.chartData.datasets = [{ data: wave }];

        updateWaveChart();
      }, 1000 / secondFreq);
    }

    updateWaveChart();
  },
  watch: {
    currentMusicId: async function (newVal, oldVal) {
      console.log("oldVal", oldVal, "newVal", newVal);
      this.updateDataFlag = true;
      this.initChart();
      if (newVal != "") {
        this.musicCover = apiAddress + "/music/cover/" + newVal.toString();

        let musicInfo = await this.returnMusicInfo(newVal);

        this.musicName = musicInfo["music_name"];
        this.authorName = musicInfo["nickname"];
        let _this = this;

        await this.$axios
          .get(apiAddress + "/music/wave/" + newVal.toString())
          .then((response) => {
            if (_this.currentMusicId == newVal)
              _this.musicWave = response.data.wave;
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        this.initChart();
        this.musicCover = "";
        this.musicName = "Music Name";
        this.authorName = "Musician Name";
      }
      this.updateDataFlag = false;
    },
  },
  data() {
    return {
      musicWave: [],
      currentAudioName: "",
      chartData: this.getEmptyChart(),
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
      musicCover: "",
      musicName: "Music Name",
      authorName: "Musician Name",
      updateDataFlag: false,
    };
  },
  methods: {
    returnMusicInfo: async function (id) {
      let data = null;
      await this.$axios
        .get(apiAddress + "/music/info/" + id.toString())
        .then(async (response) => {
          data = response.data;
        })
        .catch((error) => {
          console.log(error);
        });

      return data;
    },
    startNewSong(next) {
      this.$parent.$parent.$parent.$refs.audioPlayer.pause();
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

<style lang="scss">
@keyframes scroll {
  from {
    transform: translateX(0%);
  }
  to {
    transform: translateX(-50%);
  }
}

.logo-wall {
  display: flex;

  .logo-wrapper {
    display: flex;
    animation: scroll 100s linear infinite;
  }
}
</style>
