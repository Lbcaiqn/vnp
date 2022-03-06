<template>
  <div id="app">
    <section style="height: 400px;"></section>
    <!-- <Home></Home> -->
    <router-view></router-view>
    
  </div>
</template>

<script>
import Home from './views/Home/Home.vue'

export default {
  components:{
    Home
  }
}
</script>


<style lang="less">
* {
  margin: 0;
  padding: 0;
}
body {
  background: url(./assets/img/a.png) no-repeat fixed;
  background-size: 100%;
}
#app {
  color: #fff;
  
}
</style>
