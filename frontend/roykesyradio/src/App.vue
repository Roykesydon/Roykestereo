<template>
  <v-app style="overflow: hidden">
    <v-row>
      <v-col col="2" style="background-color: #1a1a1a" class="pt-10 px-5">
        <div class="d-flex justify-center my-3">
          <v-btn text class="mx-3 primary--text font-weight-thin text-h5"
            >Home</v-btn
          >
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>
        <div class="d-flex justify-center my-3">
          <v-btn
            text
            class="mx-3 primary--text font-weight-thin text-h5"
            x-large
            >Song <br />list</v-btn
          >
        </div>
        <div>
          <v-divider class="secondary"></v-divider>
        </div>
        <v-divider></v-divider>
      </v-col>
      <!-- <v-col
        col="2"
        style="background-color: #1a1a1a"
        class="d-flex align-start flex-column"
      >
        <div class="pa-2">test</div>
        <div class="mt-auto"><v-img></v-img></div>
      </v-col> -->
      <v-col cols="10">
        <v-main>
          <router-view />
        </v-main>
      </v-col>
    </v-row>
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    //
  }),
};
</script>
