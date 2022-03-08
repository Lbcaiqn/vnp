<template>
  <div id="ShowContent">
    <div v-for="(i,iIndex) in content" :key="iIndex">
      <h1>{{i.title}}</h1>
      <div v-for="(j,jIndex) in i.content" :key="jIndex">
        <p>{{j.text}}</p>
        <img v-for="(k,kIndex) in j.img" :key="kIndex" :src=k>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  props:{
    content:{
      type: Object,
      default(){
        return {}
      }
    }
  }
}
</script>

<style scoped>
#ShowContent {
  margin: 20px;
  padding: 20px;
}
h1 {
  padding: 20px;
  border-bottom: solid 1px #fff;
}
p {
  padding: 20px;
  font-size: 20px;
}
img {
  margin: 0 25px 10px 25px;
  width: 970px;
}
</style>