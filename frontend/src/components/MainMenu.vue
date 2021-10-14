<template>
  <div>
    <v-navigation-drawer v-model="drawer" app clipped>
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>dashboard</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-cog</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Settings</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left color="indigo" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Application</v-toolbar-title>

      <v-toolbar-title>Vue.js-Django Web Programming</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn text href="/">HOME</v-btn>
      <v-btn text href="/blog/post/list/">Article</v-btn>
      <v-btn text href="/admin/">Admin</v-btn>
      <v-btn text>/</v-btn>
      <v-btn text href="/post_list.html">PostList</v-btn>
      <v-btn text href="/post_detail.html">PostDetail</v-btn>
      <v-spacer></v-spacer>

      <v-menu offset-y left bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn text v-bind="attrs" v-on="on">
            <v-icon>mdi-account</v-icon>
            {{me.username}}
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <!-- 로그인 메뉴를 클릭했을때 클릭이벤트가 상위에있는 v-list 컴포넌트로 전달되도록 stop을 지워줌, 상위에있는 컴포넌트에서 click이벤트가 필요하기 때문-->
        <!-- 태그의 그룹에 v-if라는 디렉티브를 적용하려면 template로 태그들을 감싼다. -->
        <v-list>
          <!-- 로그인을 안한경우 유저이름이 익명일때는 v-if 쪽 탬플릿을 랜더링한다. -->
          <template v-if="me.username === 'Anonymous'">
            <v-list-item @click="dialogOpen('login')">
              <v-list-item-title>Login</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title @click="dialogOpen('register')">Register</v-list-item-title>
            </v-list-item>
          </template>
          <!-- 로그인을 했다면 v-else 쪽 탬플릿을 랜더링한다. -->
          <template v-else>
            <v-list-item @click="logout">
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-title @click="dialogOpen('pwdchg')">Password change</v-list-item-title>
            </v-list-item>
          </template>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- v-dialog 로그인을 위한 팝업창 -->
    <!-- vue를 이용하여 form을 만들때는 name속성이 중요하다 아예 디비의 컬럼이름과 같게한다고 생각한다. -->
    <!-- id 속성은 있어도 상관없지만 사용하지 않으므로 없엔다. -->
    <v-dialog v-model="dialog.login" max-width="600">
      <v-card class="elevation-12">
        <v-toolbar dark color="primary">
          <v-toolbar-title>Login form</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-form id="login-form" ref="loginForm">
            <v-text-field
              prepend-icon="person"
              name="username"
              label="Username"
              type="text"
            ></v-text-field>
            <v-text-field
              prepend-icon="lock"
              name="password"
              label="Password"
              type="password"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="grey" @click="cancel('login')">Cancel</v-btn>
          <v-btn color="primary" class="mr-5" @click="save('login')"
            >Login</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- v-dialog 회원가입을 위한 팝업창 -->
    <v-dialog v-model="dialog.register" max-width="600">
      <v-card class="elevation-12">
        <v-toolbar dark color="success">
          <v-toolbar-title>Resgister form</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-form id="register-form" ref="registerForm">
            <v-text-field
              prepend-icon="person"
              name="username"
              label="Username"
              type="text"
            ></v-text-field>
            <v-text-field
              prepend-icon="lock"
              name="password1"
              label="Password"
              type="password"
            ></v-text-field>
            <v-text-field
              prepend-icon="lock"
              name="password2"
              label="Password again"
              type="password"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="grey" @click="cancel('register')">Cancel</v-btn>
          <v-btn color="success" class="mr-5" @click="save('register')">Register</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- v-dialog 비번변경을 위한 팝업창 -->
    <v-dialog v-model="dialog.pwdchg" max-width="600">
      <v-card class="elevation-12">
        <v-toolbar dark color="warning">
          <v-toolbar-title>Password change form</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <v-form id="pwdchg-form" ref="pwdchgForm">
            <v-text-field
              id="password"
              prepend-icon="lock"
              name="old_password"
              label="Old password"
              type="password"
            ></v-text-field>
            <v-text-field
              id="password"
              prepend-icon="lock"
              name="new_password1"
              label="New password"
              type="password"
            ></v-text-field>
            <v-text-field
              id="password"
              prepend-icon="lock"
              name="new_password2"
              label="New password again"
              type="password"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="grey" @click="cancel('pwdchg')">Cancel</v-btn>
          <v-btn color="warning" class="mr-5" @click="save('pwdchg')"
            >Password change</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";

// 이 두 라인의 의미는 axios로 두 요청을 보낼때, csrftoken이라는 이름을가진 쿠키를 읽어서 요청헤더인 X-CSRFToken에 넣어서 보내라는 의미이다.
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";


export default {
  data: () => ({
    drawer: null,
    dialog: {
      login: false,
      register: false,
      pwdchg: false,
    },
    me: {username:'Anonymous'},
  }),
  created(){
    this.getUserInfo();
  },
  methods: {
    dialogOpen(kind){
      console.log("diallogOpen()...", kind);
      if (kind === "login"){ 
        this.dialog.login = true;
      }
      else if (kind === "register") {
        this.dialog.register = true;
      }
      else if (kind === "pwdchg") {
        this.dialog.pwdchg = true;
      }
    },

    cancel(kind) {
      console.log("cancel()...", kind);
      if (kind === "login"){ 
        this.dialog.login = false;
        this.$refs.loginForm.reset();
      }
      else if (kind === "register") {
        this.dialog.register = false;
        this.$refs.registerForm.reset();
      }
      else if (kind === "pwdchg") {
        this.dialog.pwdchg = false;
        this.$refs.pwdchgForm.reset();
      }
    },

    save(kind) {
      console.log("save()...", kind);
      if (kind === "login") {
        this.login();
        this.dialog.login = false;
        this.$refs.loginForm.reset();
      } else if (kind === "register") {
        this.register();
        this.dialog.register = false;
        this.$refs.registerForm.reset();
      } else if (kind === "pwdchg") {
        this.pwdchg();
        this.dialog.pwdchg = false;
        this.$refs.pwdchgForm.reset();
      }
    },

    login() {
      console.log("login()...");
      // es6 문법으로 var대신 const사용
      const postData = new FormData(document.getElementById("login-form"));
      axios.post("/api/login/", postData)
        .then((res) => {
          console.log("LOGIN POST RES", res);
          // alert(`user: ${res.data.username} login OK`);
          this.me = res.data;
        })
        .catch((err) => {
          console.log("LOGIN POST ERR.RESPONSE", err.response);
          alert("login NOK");
        });
    },
    register() {
      console.log("register()...");
      // es6 문법으로 var대신 const사용
      const postData = new FormData(document.getElementById("register-form"));
      axios.post("/api/register/", postData)
        .then((res) => {
          console.log("REGISTER POST RES", res);
          alert(`user: ${res.data.username} created OK`);
          // this.me = res.data;
        })
        .catch((err) => {
          console.log("REGISTER POST ERR.RESPONSE", err.response);
          alert("register NOK");
        });
    },
    logout(){
      console.log("logout()...");
      axios.get('/api/logout/')
        .then((res) => {
          console.log("LOGOUT GET RES", res);
          alert(`user: ${this.me.username} logout OK`);
          this.me = {username:'Anonymous'};
        })
        .catch((err) => {
          console.log("LOGOUT GETT ERR.RESPONSE", err.response);
          alert("LOGOUT NOK");
        });
    },
    pwdchg(){
      console.log("pwdchg()...");
      // es6 문법으로 var대신 const사용
      const postData = new FormData(document.getElementById("pwdchg-form"));
      axios.post("/api/pwdchg/", postData)
        .then((res) => {
          console.log("PWDCHG GET RES", res);
          alert(`user: ${this.me.username} password change OK`);
        })
        .catch((err) => {
          console.log("PWDCHG GET ERR.RESPONSE", err.response);
          alert("PASSWORD CHANGE NOK");
        });
    },
      getUserInfo(){
    console.log("getUserInfo()...");
    axios.get('/api/me/')
    .then(res =>{
      console.log("GET USER INFO GET", res);
      this.me = res.data;
    })
    .catch(err =>{
      console.log("GET USER INFO GET ERR.RESPONSE", err.response);
      alert(err.response.status + '' + err.response.statusText);
    });
  },
  },
};
</script>

<style>
</style>