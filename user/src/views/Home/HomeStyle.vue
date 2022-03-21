<template>
  <div id="HomeStyle">
    <div class="dropdown" @click="clickDropdown"><h2>样式选择 <i class="el-icon-arrow-right" v-show="!isDropdown"></i><i class="el-icon-arrow-down" v-show="isDropdown"></i></h2></div>
    <div class="dropdownBox" v-show="isDropdown">
      
      <div>
        <el-row :span="4"><h3>主题</h3></el-row>
        <el-row>
          <el-select v-model="theme.isSl" @change="themeChange">
            <el-option :value="i.iid" :label="i.text" v-for="i in theme.opt" :key="i.iid"></el-option>
          </el-select>
        </el-row>
      </div>
      
      <div>
        <el-row><h3>图表的文本信息</h3></el-row>
        <el-row>
          <el-col :span="3"><el-checkbox v-model="desc.legend.useLegend">显示图例</el-checkbox></el-col>
          <el-col :span="3"><el-checkbox v-model="desc.useText" v-show="$store.state.mode=='plot' || $store.state.mode=='bar'">显示标注</el-checkbox></el-col>
        </el-row>
        <el-row :gutter="20" v-for="i in desc" :key="i.iid" v-show="i.iid != '图例：' || desc.legend.useLegend">
          <el-col v-if="i.iid=='标题：' || $store.state.mode!='pie'" :span="2">{{i.iid}}</el-col>
          <el-col v-if="i.iid=='标题：' || $store.state.mode!='pie'" :span="4" v-for="(j,jIndex) in i.val" :key="jIndex"><el-input v-model="i.val[jIndex]"></el-input></el-col>
        </el-row>
        
        
      </div>
      <div>
        <el-row v-show="$store.state.mode != ''"><h3>作图的样式</h3></el-row>
        <table v-if="$store.state.mode != '' && $store.state.mode != 'pie'">
          <tr v-for="(i,iIndex) in style[$store.state.mode]" :key="iIndex">

            <td v-if="$store.state.mode == 'scatter'">散点：</td>
            <td v-if="$store.state.mode == 'plot'">线{{iIndex+1}}：</td>
            <td v-if="$store.state.mode == 'bar'">柱{{iIndex+1}}：</td>
            
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
        <div v-if="$store.state.mode == 'pie'">
          <div v-for="(p,pIndex) in style.pie">
          <div class="pieStyle">
            
            <div class="pieStyleBox" v-for="(i,iIndex) in p.pie" :key="iIndex">
              <h4>{{i.title}}</h4>
              <el-row :gutter="10">
                <el-col style="display:flex;" :span="12" v-for="j in i.val" :key="j.iid">
                  <p style="width: 50%;">{{j.text}}</p>
                  <div v-if="typeof j.val == 'string' && j.iid != 'color'"><el-input v-model="j.val" size="mini"></el-input></div>
                  <div v-if="typeof j.val == 'boolean'">
                    <el-select v-model="j.val">
                      <el-option :value="true" label="逆时针"></el-option>
                      <el-option :value="false" label="顺时针"></el-option>
                    </el-select>
                  </div>
                  <div v-if="j.iid == 'color'"><el-color-picker v-model="j.val"></el-color-picker></div>
                </el-col>
              </el-row>
            </div>
          </div>
          <div>
            <el-row>
              <el-col :span="5"><h4>给单独的饼块设置样式：</h4></el-col>
              <el-col :span="10">
                <el-button @click="redBlock(pIndex)"><i class="el-icon-minus"></i></el-button>
                <el-button @click="addBlock(pIndex)"><i class="el-icon-plus"></i></el-button>
              </el-col>
            </el-row>
            <el-row v-for="(i,iIndex) in p.block" :key="iIndex">
              <el-col :span="2">第几块：</el-col>
              <el-col :span="4"><el-input v-model="i.index" size="mini"></el-input></el-col>
              <el-col :span="2" :offset="2">颜色：</el-col>
              <el-col :span="2"><el-color-picker v-model="i.color"></el-color-picker></el-col>
              <el-col :span="2" :offset="2">距圆心：</el-col>
              <el-col :span="4"><el-input v-model="i.explode" size="mini"></el-input></el-col>
            
            </el-row>
           
          </div>
        </div>
        </div>
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
      theme:{
        isSl: 'default',
        opt:[
          {iid:'default',text:'默认'},
          {iid:'dark_background',text:'黑色模式'},
        ]
      },
      desc:{
        title: {iid:'标题：',val:['']},
        xLabel: {iid:'X轴：',val:['']},
        yLabel: {iid:'Y轴：',val:['']},
        legend: {iid:'图例：',val:[''],useLegend: false},
        useText: false
      },
      style: {
        scatter: [
          {
            color: {iid:'颜色：',val:'#000000'},
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
            color: {iid:'颜色：',val:'#000000'},
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
        pie: [{
          pie:{
            radius:{
              title:'半径大小：',
              val:{
                radius:{iid:'radius',text:'半径：',val:'1'},
                occupyRadius: {iid:'occupyRadius',text:'实占半径：',val:'1'}
              }
            },
            distance:{
              title:'文本距圆心位置(值为半径倍数)：',
              val:{
                pctdistance:{iid:'pctdistance',text:'百分比：',val:'0.65'},
                labeldistance:{iid:'labeldistance',text:'标签：',val:'1.2'}
              }
            },
            method:{
              title:'绘制方式：',
              val:{
                startangle:{iid:'startangle',text:'起始角度：',val:'0'},
                counterclock:{iid:'counterclock',text:'方向：',val:true}
              }
            },
            border:{
              title:'边框设置：',
              val:{
                linewidth:{iid:'linewidth',text:'线宽：',val:'0'},
                color:{iid:'color',text:'颜色：',val:'#000000'}
              }
            }
          },
          block:[]
        }]
      }
    }
  },
  
  methods:{
    clickDropdown(){
      this.isDropdown = !this.isDropdown
    },
    themeChange(i){
      if(i == 'dark_background'){
        for(let index in this.style.scatter){
          if(this.style.scatter[index].color.val == '#000000') this.style.scatter[index].color.val = '#ffffff'
        }
        for(let index in this.style.plot){
          if(this.style.plot[index].color.val == '#000000') this.style.plot[index].color.val = '#ffffff'
        }
      }
      else if(i != 'dark_background'){
        for(let index in this.style.scatter){
          if(this.style.scatter[index].color.val == '#ffffff') this.style.scatter[index].color.val = '#000000'
        }
        for(let index in this.style.plot){
          if(this.style.plot[index].color.val == '#ffffff') this.style.plot[index].color.val = '#000000'
        }
      }
    },
    checkWid(e,i){
      if(e[e.length-1] < '0' || e[e.length-1] > '9')
        this.style.plot[i].linewidth.val = this.style.plot[i].linewidth.val.substr(0,this.style.plot[i].linewidth.val.length-1)
    },
    addBlock(i){
      if(this.style.pie[i].block.length < 10){
        this.style.pie[i].block.push({index:'1',color:'#ff0000',explode:'0'})
      }
    },
    redBlock(i){
      if(this.style.pie[i].block.length > 0){
        this.style.pie[i].block.pop()
      }
    }
  },
  
  mounted(){
    EventBus.$on('chartChange',(title)=>{
      this.desc.yLabel = {iid: 'Y轴：',val:[this.desc.yLabel.val[0]]}
      this.desc.legend = {iid: '图例：',val:[this.desc.legend.val[0]],useLegend: false}
      this.desc.title.val[0] = title
      this.desc.useText = false
      this.theme.isSl = 'default'
      this.style = {
        scatter: [
          {
            color: {iid:'颜色：',val:'#000000'},
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
            color: {iid:'颜色：',val:'#000000'},
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
          pie: [{
            pie:{
              radius:{
                title:'半径大小：',
                val:{
                  radius:{iid:'radius',text:'半径：',val:'1'},
                  occupyRadius: {iid:'occupyRadius',text:'实占半径：',val:'1'}
                }
              },
              distance:{
                title:'文本距圆心位置(值为半径倍数)：',
                val:{
                  pctdistance:{iid:'pctdistance',text:'百分比：',val:'0.65'},
                  labeldistance:{iid:'labeldistance',text:'标签：',val:'1.2'}
                }
              },
              method:{
                title:'绘制方式：',
                val:{
                  startangle:{iid:'startangle',text:'起始角度：',val:'0'},
                  counterclock:{iid:'counterclock',text:'方向：',val:true}
                }
              },
              border:{
                title:'边框设置：',
                val:{
                  linewidth:{iid:'linewidth',text:'线宽：',val:'0'},
                  color:{iid:'color',text:'颜色：',val:'#000000'}
                }
              }
            },
            block:[]
          }]
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
        let c = this.theme.isSl == 'dark_background' ? "#ffffff" : '#000000'
        this.style['plot'].push({
            color: {iid:'颜色：',val:c},
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

      let w = this.style['bar'].length == 2 ? '0.8' : '0.4'
      for(let i in this.style['bar']){
        this.style['bar'][i].barwidth.val = w
      }

      this.style[this.$store.state.mode].pop()
    })
  },
  watch:{
    'theme.isSl':{
      immediate: true,
      handler(newVal){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'theme',
          value: newVal
        })
      }
    },
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
  },
  
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

.pieStyle {
  display:flex;
  flex-wrap: wrap;
}
.pieStyleBox {
  width: 45%;
  padding: 5px;
  margin-bottom: 10px;
  
  
}
</style>
