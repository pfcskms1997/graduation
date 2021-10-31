<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="posts"
      sort-by="name"
      class="elevation-1"
      :items-per-page="5"
      @click:row="serverPage"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>ScrapList</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>
      </template>
      <template v-slot:[`item.actions`]="{ item }">
        <v-icon small @click.stop="deletePost(item)"> mdi-minus </v-icon>
      </template>

      <template v-slot:no-data>
        <v-btn color="primary" @click="fetchPostList"> Reset </v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import axios from "axios";
import EventBus from "./event_bus";
export default {
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "ID",
        align: "start",
        sortable: false,
        value: "id",
      },
      { text: "제 목", value: "title" },
      { text: "요 약", value: "description" },
      { text: "수정일", value: "modify_dt" },
      { text: "작성자", value: "owner" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    posts: [],
    editedIndex: -1,
    editedItem: {},
    defaultItem: {},
    actionKind: "",
    me: { user: "Anonymous" },
  }),
  computed: {
  },
  created() {
      EventBus.$on("me_change", (val) => {
      this.me = val;
      console.log("EventBus()...", this.me.username);
    });
    this.fetchPostList();

  },

  methods: {
    fetchPostList() {
      console.log("fetchPostList()...");
      axios
        .get(`/api/post/scrap/`)
        .then((res) => {
          console.log("POST SCRAPLIST GET RES!!", res);
          this.posts = res.data;
        })
        .catch((err) => {
          console.log("POST SCRAPLIST ERR RES!!", err.response);
          alert(err.response.status + "" + err.response.statusText);
        });
    },

    serverPage(item) {
      console.log("serverPage()...", item);
      location.href = `/blog/post/${item.id}`;
    },

    deletePost(item) {
      console.log("deletePost()...", item);
      if (this.me.username === "Anonymous") {
        alert("Please login first!");
        return;
      }
      if (!confirm("Are you sure to delete ?")) return;
      axios
        .get(`/api/post/${item.id}/scrap/delete`)
        .then((res) => {
          console.log("POST SCRAP DEL GET RES!!", res);
          const index = this.posts.indexOf(item);
          this.posts.splice(index, 1);
          alert("Scrap is canceled!");
        })
        .catch((err) => {
          console.log("POST SCRAP DEL GET ERR.RESPONSE", err.response);
          alert(err.response.status + "" + err.response.statusText);
        });
    },
  },
};
</script>

<style scoped>
.v-data-table >>> tbody > tr {
  cursor: pointer;
}
</style>