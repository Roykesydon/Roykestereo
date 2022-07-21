<template>
  <div class="pa-10 d-flex align-center flex-column" style="overflow-x: hidden">
    <v-card class="pa-0" fill-height elevation="12">
      <v-card-title
        class="primary_dark primary--text text-h4 pa-7 font-weight-bold d-flex align-center"
      >
        <v-icon color="primary" size="30" class="mr-5"
          >mdi-account-voice</v-icon
        >
        <div>Chat Room</div>
      </v-card-title>
      <!-- <v-divider></v-divider> -->
      <v-card-text
        class="text-h5 font-weight-thin pa-7"
        style="
          height: 63vh;
          width: 30vw;
          overflow-y: scroll;
          background-color: #0f0f0f;
        "
      >
        <v-row
          class="flex-column mx-5"
          v-for="(message, index) in messages"
          :align="messageAlign(message)"
          :key="index"
        >
          <div v-if="message.join == true" class="mb-4">
            <v-card
              class="grey darken-4 py-1 px-3 my-0 secondary--text text-subtitle-2 rounded-pill"
            >
              {{ message.nickname }}@{{ message.username }} joined
            </v-card>
          </div>
          <div v-if="message.join == false" class="mb-10">
            <v-row :class="idJustify(message.self)">
              <span class="text-h6 font-weight-thin primary--text">{{
                message.nickname
              }}</span>
              <span class="text-h6 font-weight-thin grey--text"
                >@{{ message.username }}</span
              >
            </v-row>
            <v-row :class="idJustify(message.self)">
              <v-card
                class="grey darken-4 py-1 px-3 primary--text text-wrap"
                max-width="20vw"
                >{{ message.msg }}</v-card
              >
            </v-row>
          </div>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-text-field
          v-model="message"
          label="Input Message"
          class="ml-2"
          color="primary"
          outlined
          dense
          hide-details
        ></v-text-field>
        <v-btn color="primary" outlined class="mx-3" @click="sendMessage">
          send</v-btn
        >
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import { apiAddress } from "@/config.js";

export default {
  name: "ChatRoomView",
  components: {},
  sockets: {
    connect() {
      console.log("socket connected");
    },
    test(val) {
      console.log(val);
      // console.log(
      //   'this method was fired by the socket server. eg: io.emit("customEmit", data)'
      // );
    },
  },

  async mounted() {
    console.log(this.$cookies.get("username"));
    if (!this.$cookies.get("username")) {
      this.$toast.error("Please Login", {
        position: "top-center",
        timeout: 2000,
      });
      this.$router.push("/login");
    }

    this.$socket.client.on("error", (errorMsg) => {
      this.$toast.error(errorMsg, {
        position: "top-center",
        timeout: 2000,
      });
      if (errorMsg.indexOf("auth") != -1) {
        this.$router.push("/login");
      }
      console.log(errorMsg);
    });

    this.$socket.client.on("join_success", async (data) => {
      let message = {
        username: data["username"],
        nickname: "",
        msg: "",
        join: true,
        self: false,
      };

      await this.$axios
        .get(apiAddress + "/user/nickname", {
          params: {
            username: data["username"],
          },
        })
        .then(async (response) => {
          if (response.data.success == 1) message.nickname = response.data.data;
          else {
            console.log(response.data);
          }
        })
        .catch((error) => {
          console.log(error);
        });

      this.messages.push(message);
    });

    this.$socket.client.on("get_msg", async (data) => {
      let message = {
        username: data["username"],
        nickname: "",
        msg: data["msg"],
        join: false,
        self: false,
      };

      await this.$axios
        .get(apiAddress + "/user/nickname", {
          params: {
            username: data["username"],
          },
        })
        .then(async (response) => {
          if (response.data.success == 1) message.nickname = response.data.data;
          else {
            console.log(response.data);
          }
        })
        .catch((error) => {
          console.log(error);
        });

      if (data["username"] == this.$cookies.get("username"))
        message.self = true;

      this.messages.push(message);
    });

    this.$socket.client.emit("join_chat", {
      username: this.$cookies.get("username"),
    });
    // this.$socket.client.emit("send_message", { msg: "hihi" });
  },
  data() {
    return { messages: [], message: "" };
  },
  methods: {
    idJustify: function (self) {
      if (self) return "d-flex justify-end";
      return "";
    },
    messageAlign: function (message) {
      if (message.join) return "center";

      if (message.self) return "end";

      return "start";
    },
    sendMessage: function () {
      if (this.message != "") {
        this.$socket.client.emit("send_message", {
          username: this.$cookies.get("username"),
          msg: this.message,
        });
        this.message = "";
      }
    },
  },
};
</script>

<style scope></style>
