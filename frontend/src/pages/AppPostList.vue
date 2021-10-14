<template>
  <v-app id="inspire">
    <main-menu />
    <v-main>
      <PostList />
    </v-main>

    <v-footer app>
      <span>&copy; 2020</span>
    </v-footer>
  </v-app>
</template>

<script>
import MainMenu from "../components/MainMenu.vue";
import PostList from "../components/PostList.vue";
export default {
  components: { PostList, MainMenu },
  props: {
    //source: String,
  },

  data: () => ({
    //drawer: null,
  }),

  created: () => {
    // this.$vuetify.theme.dark = true
  },
};
</script>