<template>
  <div class="home">
    <bar-chart :chartData="chartData" />
    {{ currentAudioName || audioList[0].name }}
    <audio-player
      ref="audioPlayer"
      :audio-list="audioList.map((elm) => elm.url)"
      :before-play="handleBeforePlay"
      theme-color="#ff2929"
    />
    <audio controls>
      <source
        src="http://192.168.100.158:5000/static/the_edge.wav"
        type="audio/mpeg"
      />
    </audio>
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import BarChart from "@/components/BarChart.vue";
import AudioPlayer from "@liripeng/vue-audio-player";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
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
        let secondFreq = 100;

        function myLoop() {
          //  create a loop function
          setTimeout(function () {
            if (_this.$refs.audioPlayer.currentTime === "") {
              this.chartData = {
                labels: Array(70).fill(0),
                datasets: [{ data: Array(70).fill(0) }],
              };
              myLoop();
              return;
            }
            //  call a 3s setTimeout when the loop is called
            // console.log(_this.chartData);
            let currentTime = Math.floor(_this.$refs.audioPlayer.currentTime);
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

        // for (;;) {
        //   let currentTime = Date.now();
        //   // console.log(startTime);
        //   // console.log((currentTime - startTime) % 1000);
        //   // console.log(((currentTime - startTime) % 1000) / 20);
        //   if (
        //     (currentTime - startTime) / 1000 == lastTime[0] &&
        //     ((currentTime - startTime) % 1000) / 20 == lastTime[1]
        //   )
        //     continue;

        //   lastTime = [
        //     (currentTime - startTime) / 1000,
        //     ((currentTime - startTime) % 1000) / 20,
        //   ];

        //   this.chartData.labels = response.data.wave[lastTime[0] + lastTime[1]];
        //   this.chartData.datasets = [
        //     { data: response.data.wave[lastTime[0] + lastTime[1]] },
        //   ];
        //   await setTimeout(() => {}, 1000);
        // }

        // for (let i = 0; i < response.data.wave.length; i++) {
        //   this.chartData.datasets = [{ data: response.data.wave[i] }];
        // }
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
      chartData: {
        labels: Array(70).fill(0),
        datasets: [{ data: Array(70).fill(0) }],
      },
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
    handleBeforePlay(next) {
      // There are a few things you can do here...
      this.currentAudioName =
        this.audioList[this.$refs.audioPlayer.currentPlayIndex].name;

      next(); // Start playing
    },
  },
};
</script>
