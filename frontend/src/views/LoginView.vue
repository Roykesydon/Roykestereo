<template>
  <div class="home">
    <sign-in-up-interface />
  </div>
</template>

<script>
import SignInUpInterface from "@/components/combinedForm/SignInUpInterface.vue";
export default {
  name: "LoginView",
  components: { SignInUpInterface },
  async mounted() {},
  data() {
    return {};
  },
  methods: {},
};
</script>

<style></style>
