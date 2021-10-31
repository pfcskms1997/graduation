import Vue from 'vue'
import AppPostScrap from './AppPostScrap.vue'
import vuetify from '../plugins/vuetify'

Vue.config.productionTip = false

new Vue({
  vuetify,
  render: h => h(AppPostScrap)
}).$mount('#app')
