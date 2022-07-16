<template>
  <div class="d-flex justify-center align-center" style="height: 100vh">
    <v-card class="my-auto">
      <div v-if="wantLogin" style="width: 30vw">
        <login-form
          @closeSignInUpInterface="$emit('closeSignInUpInterface')"
          @wantToSignUp="wantLogin = false"
        />
      </div>
      <div v-else style="width: 30vw">
        <register-form
          @closeSignInUpInterface="$emit('closeSignInUpInterface')"
          @wantToSignIn="wantLogin = true"
        />
      </div>
    </v-card>
  </div>
</template>

<script>
import LoginForm from "@/components/form/user/LoginForm.vue";
import RegisterForm from "@/components/form/user/RegisterForm.vue";

export default {
  name: "SignInUpInterface",
  components: { LoginForm, RegisterForm },
  data: () => ({ wantLogin: true }),
};
</script>

<style>
.v-window__container {
  height: 50vh;
}
</style>
