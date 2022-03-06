<template>
  <div id="HomeStyle">
    <div class="dropdown" @click="clickDropdown"><h2>样式选择 <i class="el-icon-arrow-right" v-show="!isDropdown"></i><i class="el-icon-arrow-down" v-show="isDropdown"></i></h2></div>
    <div class="dropdownBox" v-show="isDropdown">
      <div>
        <el-row><h3>图表的文本信息</h3></el-row>
        <el-row><el-checkbox v-model="desc.legend.useLegend">显示图例</el-checkbox></el-row>
        <el-row :gutter="20" v-for="i in desc" :key="i.iid" v-show="i.iid != '图例：' || desc.legend.useLegend">
          <el-col v-if="i.iid=='标题：' || $store.state.mode!='pie'" :span="2">{{i.iid}}</el-col>
          <el-col v-if="i.iid=='标题：' || $store.state.mode!='pie'" :span="4" v-for="(j,jIndex) in i.val" :key="jIndex"><el-input v-model="i.val[jIndex]"></el-input></el-col>
        </el-row>
        
        
      </div>
      <div>
        <el-row v-show="$store.state.mode != '' && $store.state.mode != 'pie'"><h3>作图的样式</h3></el-row>
        <table v-show="$store.state.mode == mIndex" v-for="(m,mIndex) in style" :key="mIndex">
          <tr v-for="(i,iIndex) in m" :key="iIndex">

            <td v-if="mIndex == 'scatter'">散点：</el-td>
            <td v-if="mIndex == 'plot'">线{{iIndex+1}}：</td>
            <td v-if="mIndex == 'bar'">柱{{iIndex+1}}：</td>
            
            <td v-for="(j,jIndex) in i" :key="jIndex">
              <div v-if="jIndex.substr(jIndex.length-5,jIndex.length) == 'color'">
                {{j.iid}}
                <el-color-picker v-model="j.val"></el-color-picker>
              </div>

              <div v-if="jIndex.substr(jIndex.length-5,jIndex.length) != 'color' && jIndex.substr(jIndex.length-5,jIndex.length) != 'width'">
                {{j.iid}}
                <el-select v-model="j.val.isSl">
                  <el-option :value="opt.iid" :label="opt.text" v-for="(opt, optIndex) in j.val.opt" :key="optIndex"></el-option>
                </el-select>
              </div>

              <div v-if="jIndex.substr(jIndex.length-5,jIndex.length) == 'width'">
                <el-col :span="6">{{j.iid}}</el-col>
                <el-col :span="8"><el-input v-model="j.val" size="mini" @input="checkWid($event,iIndex)" ></el-input></el-col>
              </div>

            </td>
          </tr>
        </table>
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
      },
      style: {
        scatter: [
          {
            color: {iid:'颜色：',val:'#ffffff'},
            marker: {iid:'点型：',val:{isSl: 'o',opt:[
              {iid:'o',text:'圆点'},
              {iid:'.',text:'小点'},
              {iid:'s',text:'正方形'},
              {iid:'p',text:'五角形'},
              {iid:'*',text:'*'},
            ]}}
          },
        ],
        plot: [{
            color: {iid:'颜色：',val:'#ffffff'},
            ilnestyle: {iid:'线型：',val:{isSl: '-',opt:[
              {iid:'-',text:'实线'},
              {iid:'--',text:'虚线'},
              {iid:'-.',text:'点线'},
            ]}},
            marker: {iid:'点型：',val:{isSl: 'default',opt:[
              {iid:'default',text:'不使用'},
              {iid:'.',text:'实点'},
              {iid:'o',text:'圆形'},

            ]}},
            linewidth: {iid:'线宽：',val:'1'}
          }],
        bar: [{
            color: {iid:'颜色：',val:'#00f'},
            barwidth: {iid:'柱宽：',val:'0.8'},
          }],
      }
    }
  },
  
  methods:{
    clickDropdown(){
      this.isDropdown = !this.isDropdown
    },
    checkWid(e,i){
      if(e[e.length-1] < '0' || e[e.length-1] > '9')
        this.style.plot[i].linewidth.val = this.style.plot[i].linewidth.val.substr(0,this.style.plot[i].linewidth.val.length-1)
    }
  },
  mounted(){
    EventBus.$on('chartChange',(title)=>{
      this.desc.yLabel = {iid: 'Y轴：',val:[this.desc.yLabel.val[0]]}
      this.desc.legend = {iid: '图例：',val:[this.desc.legend.val[0]],useLegend: false}
      this.desc.title.val[0] = title

      this.style = {
        scatter: [
          {
            color: {iid:'颜色：',val:'#ffffff'},
            marker: {iid:'点型：',val:{isSl: 'o',opt:[
              {iid:'o',text:'圆点'},
              {iid:'.',text:'小点'},
              {iid:'s',text:'正方形'},
              {iid:'p',text:'五角形'},
              {iid:'*',text:'*'},
            ]}}
          },
        ],
        plot: [{
            color: {iid:'颜色：',val:'#ffffff'},
            ilnestyle: {iid:'线型：',val:{isSl: '-',opt:[
              {iid:'-',text:'实线'},
              {iid:'--',text:'虚线'},
              {iid:'-.',text:'点线'},
            ]}},
            marker: {iid:'点型：',val:{isSl: 'default',opt:[
              {iid:'default',text:'不使用'},
              {iid:'.',text:'实点'},
              {iid:'o',text:'圆形'},

            ]}},
            linewidth: {iid:'线宽：',val:'1'}
          },
          
          
        ],
        bar: [{
            color: {iid:'颜色：',val:'#00f'},
            barwidth: {iid:'柱宽：',val:'0.8'},
          },
          
          
        ],
      }
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
      if(this.$store.state.mode == 'plot'){
        this.style['plot'].push({
            color: {iid:'颜色：',val:'#ffffff'},
            ilnestyle: {iid:'线型：',val:{isSl: '-',opt:[
              {iid:'-',text:'实线'},
              {iid:'--',text:'虚线'},
              {iid:'-.',text:'点线'},
            ]}},
            marker: {iid:'点型：',val:{isSl: 'default',opt:[
              {iid:'default',text:'不使用'},
              {iid:'.',text:'实点'},
              {iid:'o',text:'圆形'},

            ]}},
            linewidth: {iid:'线宽：',val:'1'}
          })
      }
      else if(this.$store.state.mode == 'bar'){
        let c = this.style['bar'].length == 2 ? '#0f0' : '#f00'
        let w = this.style['bar'].length == 2 ? '0.26' : '0.4'
        for(let i in this.style['bar']){
          this.style['bar'][i].barwidth.val = w
        }

        this.style['bar'].push({
            color: {iid:'颜色：',val: c},
            barwidth: {iid:'柱宽：',val:w},
          })
      }
      
    })
    EventBus.$on('redY',()=>{
      this.desc.legend.val.pop()

      let w = this.style['bar'].length == 2 ? '1' : '0.4'
      for(let i in this.style['bar']){
        this.style['bar'][i].barwidth.val = w
      }

      this.style[this.$store.state.mode].pop()
    })
  },
  watch:{
    'desc': {
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'desc',
          value: this.desc
        })
        
      }

    },
    'style': {
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'style',
          value: this.style
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

td {
  padding: 8px;
  height: 60px;
  line-height: 60px;
}

</style>
