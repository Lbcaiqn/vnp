<template>
  <div id="app">
    <section style="height: 400px;"></section>
    <NavBar></NavBar>
    <transition appear name="nav">
      <router-view></router-view>
    </transition>
    
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
  background: url(./assets/img/1.png) no-repeat fixed;
  background-size: 100%;
}
#app {
  color: #fff;
  
}

.nav-enter,
.nav-leave-to {
  opacity: 0;
}
.nav-enter-active,
.nav-leave-active {
  transition: 0.75s;
}

</style>
