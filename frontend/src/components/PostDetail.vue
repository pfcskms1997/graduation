<template>
  <v-container fluid>
    <!-- 얼라인속성은 위아래, 저스티파이는 좌우에 관여한다. 상하 좌우 가운데로 정렬된다. v-container 속성에 fluid를 넣어주면 화면을 꽉 채울수 있다.-->
    <v-row align="center" justify="center">
      <v-col cols="12" lg="10">
        <v-card class="pa-2" outlined tile>
          <h1>{{post.title}}</h1>
          <p>{{post.modify_dt}}, written by {{post.owner}}</p>
        </v-card>
      </v-col>
    </v-row>
    <!-- 컬럼간의 간격을 없애주기 위해서 no-gutters 옵션을 없애준다. -->
    <!-- white-space: pre-wrap; css 문법을 사용하게 되면 단어의 개행을 인식하고 줄이 넘칠것 같으면 자동으로 줄넘김을 해준다. -->
    <v-row align="start" justify="center">
      <v-col cols="12" sm="8" lg="7">
        <p style="white-space: pre-wrap;">{{post.content}}</p>
        <strong>TAGS:</strong>
        <!-- post.tags에서 tag이 스트링이다. 그러므로 tags.name을 하면 안된다. -->
        <v-chip class="ma-2 my-hover" outlined v-for="(tag, index) in post.tags" :key="index"
        @click="serverPage(tag)"> {{tag}}</v-chip>
        <!-- <v-chip class="ma-2" outlined> django </v-chip> -->
      </v-col>
      <v-col cols="12" sm="4" lg="3">
        <!-- 카드간에 간격을 주기 위해 marginbotton을 준다. mb-5 outlined 속성을 지우면 음영이 들어간다-->
        <v-card class="pa-2 mb-5" tile>
          <p>prev post</p>
          <h2 v-if="post.prev" @click="fetchPostDetail(post.prev.id)" class="my-hover">{{post.prev.title}}</h2>
        </v-card>
 
        <v-card class="pa-2 mb-5" tile>
          <p>next post</p>
          <h2 v-if="post.next" @click="fetchPostDetail(post.next.id)" class="my-hover">{{post.next.title}}</h2>
        </v-card>

        <v-card class="pa-2 mb-5" tile>
          <h2>Tag cloud</h2>
          <!-- color 부분에 tag.color를 넣어서 색을 지정한다. 근본이 자바스크립트 문법이므로 color앞에 :를 붙여준다.-->
          <v-chip v-for="(tag, index) in tagCloud" :key="index" @click="serverPage(tag.name)"
          class="ma-2 my-hover" :color="tag.color" text-color="white">
            <v-avatar left :class="tag.color + ' darken-4'"> {{tag.count}} </v-avatar>
            {{tag.name}}
          </v-chip>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios';
  export default {
    name: 'HelloWorld',

    data: () => ({
      //json 형식의 데이터가 들어갈 수 있도록 빈 변수를 객체 형태롤 만들어준다.
      post: {},
      tagCloud: [],
    }),
    created() {
      console.log("created()...");
      const postId = location.pathname.split('/')[3] || 2;
      this.fetchPostDetail(postId);
      this.fetchTagCloud();
    },
    methods:{
      fetchPostDetail(postId){
        console.log("fetchPostDetail()..", postId);
        axios.get(`/api/post/${postId}/`)
        .then(res => {
          console.log("POST DETAIL GET RES", res);
          this.post = res.data;
        })
        .catch(err => {
          console.log("POST DETAIL GET ERR.RESPONSE", err.response);
          alert(err.response.status+ ''+ err.response.statusText);
        });
      },
      fetchTagCloud(){
        console.log("fetchTagCloud()..");
        axios.get('/api/tag/cloud/')
        .then(res => {
          console.log("POST CLOUD GET RES", res);
          this.tagCloud = res.data;
          //tag.weight
          //배열의 각 원소에 조작하려면 forEach 매서드를 사용할 수 있다.
          this.tagCloud.forEach(element =>{
            //등호는 2개만 써도 상관없음, 각 웨이트에 따라서 element에 color속성을 생성하여 값을 넣어준다.
            if(element.weight === 3) element.color = 'green';
            else if(element.weight ===2) element.color = 'blue-grty';
            else if(element.weight ===1) element.color = 'grey';
          })
        })
        .catch(err => {
          console.log("TAG CLOUD GET ERR.RESPONSE", err.response);
          alert(err.response.status+ ''+ err.response.statusText);
        });
      },
      serverPage(tagname){
        console.log("serverPage()...", tagname);
        // location.herf = `/blog/post/list/?tagname=${tagname}`;
        location.href = `/blog/post/list/?tagname=${tagname}`;
      },
    },
  }
</script>

<style scoped>
/* css 문법을 이용하여 정의한 객체가 마우스 호버가 일어나면 커서는 pointer 형태 글자스타일은 기울임이 되게 된다 */
.my-hover:hover{
  cursor: pointer;
  font-style: italic;
}
</style>
