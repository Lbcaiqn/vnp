<template>
  <div id="app">
    <section style="height: 400px;"></section>
    <NavBar></NavBar>
    <router-view></router-view>
    
  </div>
</template>

<script>
import NavBar from './components/NavBar/NavBar.vue'

export default {
  components: {
    NavBar,
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
