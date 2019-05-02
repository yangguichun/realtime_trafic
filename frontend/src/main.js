import Vue from 'vue'
import VueResource from 'vue-resource'
import App from './App.vue'
import './plugins/element.js'

// import ECharts from 'vue-echarts' // refers to components/ECharts.vue in webpack

// // import ECharts modules manually to reduce bundle size
// import 'echarts/lib/chart/bar'
// import 'echarts/lib/component/tooltip'

// import 'echarts-gl'

// register component to use
// Vue.component('v-chart', ECharts)

// var VueResource = require('vue-resource');
Vue.use(VueResource);
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
