<template>
  <div class="home">
    <!-- <v-row
        style="height: 45vh; width: 90vw"
        justify="center"
        class="grey darken-4 pa-0"
      >
        <v-img
          src="@/assets/image/headphone.jpg"
          min-width="15vw"
          max-width="15vw"
          max-height="15vw"
          min-height="15vw"
          :aspect-ratio="1 / 1"
        ></v-img>
      </v-row> -->
    <v-row style="height: 89vh; width: 90vw" justify="center">
      <div class="d-flex align-end justify-center pb-3">
        <!-- {{ currentAudioName || audioList[0].name }} -->
        <bar-chart
          style="height: 40vh; width: 70vw; position: float; right: 0px"
          class="wave"
          :chartData="chartData"
        />
      </div>
    </v-row>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import BarChart from "@/components/BarChart.vue";
import { apiAddress } from "@/config.js";

export default {
  name: "SongListView",
  components: {
    // HelloWorld,
    BarChart,
  },
  async mounted() {
    console.log(apiAddress);
    await this.$axios
      .get(apiAddress + "/music/audio_wave/")
      .then((response) => {
        // console.log(response);
        // this.chartData.labels = response.data.wave[0];
        // this.chartData.datasets = [{ data: response.data.wave[0] }];
        let lastTime = NaN;

        let i = 0;
        let _this = this;
        let frameCount = 0;
        let secondFreq = 20;

        function myLoop() {
          //  create a loop function
          setTimeout(function () {
            if (_this.$refs.audioPlayer.currentTime === "") {
              _this.initChart();
              myLoop();
              return;
            }
            // console.log(_this.$refs.audioPlayer.isPlaying);
            if (_this.$refs.audioPlayer.isPlaying != true) {
              _this.initChart();
              myLoop();
              return;
            }
            //  call a 3s setTimeout when the loop is called
            // console.log(_this.chartData);
            let currentTime = Math.ceil(_this.$refs.audioPlayer.currentTime);
            if (isNaN(lastTime)) {
              lastTime = currentTime;
            } else if (lastTime != currentTime) {
              frameCount = 0;
            } else if (lastTime == currentTime) {
              frameCount++;
            }
            lastTime = currentTime;

            frameCount = Math.min(frameCount, secondFreq);

            // console.log(currentTime, frameCount);
            if (
              currentTime * secondFreq + frameCount >=
              response.data.wave.length
            ) {
              myLoop();
              return;
            }

            let wave =
              response.data.wave[currentTime * secondFreq + frameCount];
            // wave = wave.slice().reverse().concat(wave);

            for (let index = 0; index < wave.length; ++index)
              wave[index] += 0.005;

            _this.chartData.labels = wave;
            _this.chartData.datasets = [{ data: wave }];
            i++; //  increment the counter
            // console.log(lastTime[0]);

            // console.log(typeof _this.$refs.audioPlayer.currentTime);
            if (i < 10000) {
              //  if the counter < 10, call the loop function
              myLoop(); //  ..  again which will trigger another
            } //  ..  setTimeout()
          }, 1000 / secondFreq);
        }

        myLoop();
      })
      .catch((error) => {
        console.log(error);
      });

    // console.log(BarChart.chartData);
    // this.chartData.labels = as
  },
  data() {
    return {
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
