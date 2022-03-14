<template>
  <div id="NavBar">
    <div class="NavBarBox">
      <ul>
        <li v-for="(i,iIndex) in item" :key="iIndex" @click="pageChange(iIndex)">{{i}}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      item: ['首页','使用案例']
    }
  },
  methods:{
    pageChange(i){
      if(i == 0 && this.$route.path != '/Home'){
        this.$router.push('/Home')
      }
      else if(i == 1 && this.$route.path != '/Show'){
        
        this.$router.push('/Show')
      }
    }
  }
}
</script>

<style scoped>
#NavBar {
  width: 1100px;
  height: 70px;
  margin: 0 auto;
  
  color: #fff;
  background-color: #000;
  
}
.NavBarBox {
  width: 400px;
}
ul {
  display: flex;
}
li {
  flex: 1;
  list-style: none;
  height: 70px;
  line-height: 70px;
  text-align: center;
  cursor: pointer;
}
li:hover {
  background-color: orange;
  transition: all 0.5s;
}
</style>