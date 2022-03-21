<template>
  <div id="home">
    <HomeUpload @beforeUpload="beforeUpload" @afterUpload="afterUpload"></HomeUpload>
    <HomeMain :cols="cols"></HomeMain>
    <HomeOption :cols="cols"></HomeOption>
    <HomeStyle></HomeStyle>    
    <HomeSubmit></HomeSubmit>
    <HomeImg></HomeImg>
  </div>
</template>

<script>
import HomeUpload from './HomeUpload.vue'
import HomeMain from './HomeMain.vue'
import HomeOption from './HomeOption.vue'
import HomeStyle from './HomeStyle.vue'
import HomeSubmit from './HomeSubmit.vue'
import HomeImg from './HomeImg.vue'


export default {
  components:{
    HomeUpload,
    HomeMain,
    HomeOption,
    HomeStyle,
    HomeSubmit,
    HomeImg
  },
  data() {
    return {
      cols: [],
      desc: {
        title: { iid: "标题", text: "" },
        xName: { iid: "X标签", text: { sum: 1, val: [""] } },
        yName: { iid: "Y标签", text: { sum: 1, val: [""] } },
        legend: { iid: "图例", text: { sum: 1, val: [""] } },
      }
    };
  },
  methods: {
    beforeUpload(){
      this.cols = []
      this.$store.commit({
        type: 'updateHomeMain',
        key: 'fd',
        value: {filePath: '',isUpload: false}
      })
    },
    afterUpload(res){
      let cols = res.cols
      for(let i in cols)  cols[i].text = i + '-' + cols[i].text
      cols.unshift({iid:'calculate',text:'自定义列'})
      this.cols = cols
      this.$store.commit({
        type: 'updateHomeMain',
        key: 'fd',
        value: {filePath: res.filePath,isUpload: true}
      })
    }
  },
};
</script>

<style scoped>
#home {
  width: 1100px;
  margin: 0 auto;
  color: #fff;
  background-color: rgb(50,37,21);
  
}

</style>
