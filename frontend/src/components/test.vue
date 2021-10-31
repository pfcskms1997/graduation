<template>
  <v-container fluid>
    <!-- 얼라인속성은 위아래, 저스티파이는 좌우에 관여한다. 상하 좌우 가운데로 정렬된다. v-container 속성에 fluid를 넣어주면 화면을 꽉 채울수 있다.-->
    <v-row align="center" justify="center">
      <v-col cols="12" lg="10">
        <v-card class="pa-2" outlined tile>
          <h1>Post title here</h1>
          <p>2020-07-10, written by shkim</p>
        </v-card>
      </v-col>
    </v-row>
    <!-- 컬럼간의 간격을 없애주기 위해서 no-gutters 옵션을 없애준다. -->
    <v-row align="start" justify="center">
      <v-col cols="12" sm="8" lg="7">
        <p>
          I study Vue.js and Django. <br />
          <br /><br /><br /><br /><br /><br /><br />
          And more Vuetify.
        </p>
        <strong>TAGS:</strong>
        <v-chip class="ma-2" outlined> Python </v-chip>
        <v-chip class="ma-2" outlined> django </v-chip>
      </v-col>
      <v-col cols="12" sm="4" lg="3">
        <!-- 카드간에 간격을 주기 위해 marginbotton을 준다. mb-5 outlined 속성을 지우면 음영이 들어간다-->
        <v-card class="pa-2 mb-5" tile>
          <p>prev post</p>
          <h2>Previous title here</h2>
        </v-card>

        <v-card class="pa-2 mb-5" tile>
          <p>next post</p>
          <h2>Next title here</h2>
        </v-card>

        <v-card class="pa-2 mb-5" tile>
          <h2>Tag cloud</h2>
          <v-chip class="ma-2" color="green" text-color="white">
            <v-avatar left class="green darken-4"> 1 </v-avatar>
            Python
          </v-chip>
          <v-chip class="ma-2" color="green" text-color="white">
            <v-avatar left class="green darken-4"> 3 </v-avatar>
            django
          </v-chip>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>