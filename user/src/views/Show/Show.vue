<template>
  <div id="Show">
    <ShowContent :content="content"></ShowContent>
  </div>
</template>

<script>
import {req} from '../../network/index.js'
import ShowContent from './ShowContent.vue'

export default {
  components:{
    ShowContent
  },
  data(){
    return {
      content: {}
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