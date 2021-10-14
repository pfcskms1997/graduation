const FileManagerPlugin = require('filemanager-webpack-plugin-fixed'); //파일메니저 플러그인을 import 시키는 코드


module.exports = {
  transpileDependencies: [
    'vuetify'
  ],

  // 개발서버에서 localhost:8080으로 들어가면, index.html을 찾게 된다. 이 설정을 하게 되면, 다른 html을 찾게 해준다.
  devServer: {
    index: 'home.html',
    proxy: 'http://127.0.0.1:8000', //xhr, axios 요청을 해야하면 여기로 보내라는 뜻
  },
  //outputDir: 빌드한 결과 디렉토리, publicPath: 웹펙 결과물에 해당하는 루트 디렉토리 설정, assetsDir: static 파일이 들어가는 디렉토리 설정
  //assetsDir외 나머지는 디폴트와 같다.
  //만약에 publicPath를 'aa'라고 하면, index.html의 경로는 /aa/index.html 이 된다.
  outputDir: 'dist',
  publicPath: '/',
  assetsDir: 'static',

  //빌드를 하면 한개의 페이지만 나오는데 이 설정을 해주면 여러 페이지를 아웃풋으로 내놓게 된다.
  pages:{
    home: {
      template: 'public/index.html', // 만들때 참조하는 템플릿
      entry: 'src/pages/main_home.js', // 웹팩 빌드작업의 시작포인트, 프로젝트를 만들면 main.js로 되어있다.
      filename: 'home.html', //최종 결과물
      title: 'VueDjangoPhoto/home.html', //제목은 임의로 넣어주면 된다.
      minify: false, //최종 결과물을 쉽게 보기 위해서 minify 기능은 사용하지 않는다.
    },
    post_list: {
      template: 'public/index.html', 
      entry: 'src/pages/main_post_list.js', 
      filename: 'post_list.html', 
      title: 'VueDjangoPhoto/post_list.html', 
      minify: false, 
    },
    post_detail:{
      template: 'public/index.html', 
      entry: 'src/pages/main_post_detail.js', 
      filename: 'post_detail.html', 
      title: 'VueDjangoPhoto/post_detail.html', 
      minify: false, 
    },
  },

  //vue.config.js에서 외부 플러그인의 설정을 하려면 아래 오브젝트 안에서 해야한다. 외부 플러그인 추가 
  configureWebpack: {
    plugins: [
      new FileManagerPlugin({//파일을 옮기거나 복사 삭제해주는 플러그인 
        onStart: {// 웹팩빌드가 시작되기 직전에 실행되는 이벤트, 현재 이벤트는 백엔드 폴더의 static과 templates폴더를 지우는 것이다. *하나는 폴더의 하위 파일, **는 폴더의 하위 파일 및 폴더
          delete: [
            '../backend/static/**/',
            '../backend/templates/**/',
          ],
        },

        onEnd: { //빌드가 끝나고 시작하는 이벤트들 dis/static의 내용들을 backend/static에 복사해준다. favicon을 backend/static/img 폴더 안에 넣어준다.
          copy: [
            { source: 'dist/static', destination: '../backend/static/' },
            { source: 'dist/favicon.ico', destination: '../backend/static/img/' },
            { source: 'dist/home.html', destination: '../backend/templates/' },
            { source: 'dist/post*.html', destination: '../backend/templates/blog/' },
          ],
        }
      }),
    ]    
  },
}
