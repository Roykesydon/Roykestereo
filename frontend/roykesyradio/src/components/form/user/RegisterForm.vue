<template>
  <v-card class="pa-10 vld-parent">
    <div class="ma-5">
      <loading
        :active.sync="isLoading"
        :can-cancel="false"
        :is-full-page="false"
        :color="$vuetify.theme.currentTheme.primary"
        :background-color="$vuetify.theme.currentTheme.customBackground"
      ></loading>
      <div class="text-h2 font-weight-thin text-center primary--text dark">
        Register
      </div>
      <div class="my-auto pa-10">
        <v-form ref="signUpForm" v-model="signUpValid" lazy-validation>
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="inputUsername"
                color="secondary"
                label="Username"
                :rules="[rules.required, rules.username]"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="inputNickname"
                color="secondary"
                label="Nickname"
                :rules="[rules.required, rules.nickname]"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="inputPassword"
                color="secondary"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.password]"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="confirmPassword"
                color="secondary"
                label="Confirm Password"
                :type="showConfirmPassword ? 'text' : 'password'"
                :rules="[
                  rules.required,
                  rules.password,
                  confirmPassword == inputPassword ||
                    'Confirm password is not same as password',
                ]"
                :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showConfirmPassword = !showConfirmPassword"
              ></v-text-field>
            </v-col>
          </v-row>
          <div class="d-flex justify-end">
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="$emit('closeSignInUpInterface')"
            >
              Close
            </v-btn>
            <v-btn color="primary" text @click="register()"> Register </v-btn>
          </div>
          <div class="d-flex justify-end my-5">
            <v-btn color="secondary" text @click="$emit('wantToSignIn')">
              already have acoount?
            </v-btn>
          </div>
        </v-form>
      </div>
    </div>
  </v-card>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { apiAddress } from "@/config.js";
import Loading from "vue-loading-overlay";
import "vue-loading-overlay/dist/vue-loading.css";

export default {
  name: "RegisterForm",
  components: {
    Loading,
  },
  data: () => ({
    inputUsername: "",
    inputNickname: "",

    inputPassword: "",
    showPassword: false,

    confirmPassword: "",
    showConfirmPassword: false,

    signUpValid: true,

    isLoading: false,

    rules: rules,
  }),
  methods: {
    requestRegister: async function () {
      await this.$axios
        .post(apiAddress + "/user/register", {
          username: this.inputUsername,
          nickname: this.inputNickname,
          password: this.inputPassword,
        })
        .then((response) => {
          if (response.data.success == 1) {
            this.$cookies.set("username", response.data.data.username);
            this.$cookies.set("nickname", response.data.data.nickname);
            this.$toast.success("Register Success!\nRedirecting to home page", {
              position: "top-center",
              timeout: 2000,
            });
            this.$router.push("/");
          } else {
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
    register: async function () {
      if (this.$refs.signUpForm.validate() == false) {
        return;
      }

      this.isLoading = true;
      await this.requestRegister();
      this.isLoading = false;
    },
  },
};
</script>
