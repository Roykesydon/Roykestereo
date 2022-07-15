<template>
  <div class="home">
    <v-container class="pa-0 ma-0">
      <v-row style="height: 89vh; width: 85vw" justify="center">
        <div class="d-flex align-end justify-center pb-3">
          <!-- {{ currentAudioName || audioList[0].name }} -->
          <bar-chart
            style="height: 40vh; width: 70vw; position: float; right: 0px"
            class="wave"
            :chartData="chartData"
          />
        </div>
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
            :before-play="handleBeforePlay"
            theme-color="#9df07d"
          />
        </div>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import BarChart from "@/components/BarChart.vue";
import AudioPlayer from "@liripeng/vue-audio-player";

export default {
  name: "HomeView",
  components: {
    // HelloWorld,
    BarChart,
    AudioPlayer,
  },
  async mounted() {
    await this.$axios
      .get("http://192.168.100.158:5000/music/audio_wave")
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
              _this.chartData = _this.getEmptyChart();
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

            console.log(currentTime, frameCount);
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
          url: "http://192.168.100.158:5000/static/the_edge.wav",
        },
        {
          name: "audio2",
          url: "http://192.168.100.158:5000/static/the_edge.wav",
        },
      ],
    };
  },
  methods: {
    getEmptyChart() {
      return {
        labels: Array(100).fill(0),
        datasets: [
          {
            backgroundColor: "#c774f7",
            data: Array(100).fill(0),
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
