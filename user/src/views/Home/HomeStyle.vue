<template>
  <div id="HomeStyle">
    <div class="dropdown" @click="clickDropdown"><h2>样式选择 <i class="el-icon-arrow-right" v-show="!isDropdown"></i><i class="el-icon-arrow-down" v-show="isDropdown"></i></h2></div>
    <div class="dropdownBox" v-show="isDropdown">
      <div>
        <el-row><h3>图表的文本信息</h3></el-row>
        <el-row><el-checkbox v-model="desc.legend.useLegend">显示图例</el-checkbox></el-row>
        <el-row :gutter="20" v-for="i in desc" :key="i.iid" v-show="i.iid != '图例：' || desc.legend.useLegend">
          <el-col :span="2">{{i.iid}}</el-col>
          <el-col :span="4" v-for="(j,jIndex) in i.val" :key="jIndex"><el-input v-model="i.val[jIndex]"></el-input></el-col>
        </el-row>
        
        
      </div>
      <div>
        <el-row><h3>作图的样式</h3></el-row>
      </div>
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import EventBus from '../../EventBus/index.js'
export default {
  data(){
    return {
      isDropdown: false,
      desc:{
        title: {iid:'标题：',val:['']},
        xLabel: {iid:'X轴：',val:['']},
        yLabel: {iid:'Y轴：',val:['']},
        legend: {iid:'图例：',val:[''],useLegend: false},
      }
    }
  },
  methods:{
    clickDropdown(){
      this.isDropdown = !this.isDropdown
    }
  },
  mounted(){
    EventBus.$on('chartChange',(title)=>{
      this.desc.yLabel = {iid: 'Y轴：',val:[this.desc.yLabel.val[0]]}
      this.desc.legend = {iid: '图例：',val:[this.desc.legend.val[0]]}
      this.desc.title.val[0] = title
    })
    EventBus.$on('xyChange',(xy)=>{
      if(xy.xy == 'X轴：')  Vue.set(this.desc.xLabel.val,xy.sum-1,xy.isSl)
      else if(xy.xy == 'Y轴：'){
        if(xy.sum == 1)  Vue.set(this.desc.yLabel.val,.0,xy.isSl)
        Vue.set(this.desc.legend.val,xy.sum-1,xy.isSl)
      }
    })
    EventBus.$on('addY',()=>{
      this.desc.legend.val.push('')
    })
    EventBus.$on('redY',()=>{
      this.desc.legend.val.pop()
    })
  },
  watch:{
    'desc': {
      deep: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'desc',
          value: this.desc
        })
      }

    }
  }
  
}
</script>

<style scoped>
#HomeStyle {
  margin: 20px;
  padding: 20px;
}
.dropdown {
  height: 80px;
  line-height: 80px;
  cursor: pointer;
  border: 1px solid #fff;
}
.dropdown>h2 {
  padding-left: 30px;
}
.dropdownBox h3 {
  padding: 20px 0;
}
.el-col {
  height: 50px;
  line-height: 50px;
 
}

</style>
