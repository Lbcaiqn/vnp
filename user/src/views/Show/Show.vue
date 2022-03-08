<template>
  <div id="Show">
    <ShowNav @dataChange="dataChange"></ShowNav>
    <ShowContent :content="content[dataIsSl]"></ShowContent>
  </div>
</template>

<script>
import {req} from '../../network/index.js'
import ShowNav from './ShowNav.vue'
import ShowContent from './ShowContent.vue'

export default {
  components:{
    ShowNav,
    ShowContent
  },
  data(){
    return {
      dataIsSl: 'population',
      content: {}
    }
  },
  methods:{
    dataChange(i){
      this.dataIsSl = i
    }
  },
  created(){
    req({
      url: '/show',
      method: 'get'
    }).then(res => {
      this.content = res.data
    })
  }
}
</script>

<style scoped>
#Show {
  width: 1100px;
  margin: 0 auto;
  
  color: #fff;
  background-color: rgb(50,37,21);
}
</style>