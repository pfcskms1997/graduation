const FileManagerPlugin = require('filemanager-webpack-plugin-fixed'); //파일메니저 플러그인을 import 시키는 코드


module.exports = {
  transpileDependencies: [
    'vuetify'
  ],

  devServer: {
    index: 'home.html',
    proxy: 'http://127.0.0.1:8000',
  },

  outputDir: 'dist',
  publicPath: '/',
  assetsDir: 'static',


  pages:{
    home: {
      template: 'public/index.html',
      entry: 'src/pages/main_home.js',
      filename: 'home.html',
      title: 'VueDjangoPhoto/home.html',
      minify: false,
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
    post_scrap: {
      template: 'public/index.html', 
      entry: 'src/pages/main_post_scrap.js', 
      filename: 'post_scrap.html', 
      title: 'VueDjangoPhoto/post_scrap.html', 
      minify: false, 
    },
  },

  
  configureWebpack: {
    plugins: [
      new FileManagerPlugin({
        onStart: {
          delete: [
            '../backend/static/**/',
            '../backend/templates/**/',
          ],
        },

        onEnd: {
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
