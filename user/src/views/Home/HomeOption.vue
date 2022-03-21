<template>
  <div id="HomeOption">
    <div class="dropdown" @click="clickDropdown"><h2>高级选项 <i class="el-icon-arrow-right" v-show="!isDropdown"></i><i class="el-icon-arrow-down" v-show="isDropdown"></i></h2></div>
    <div class="dropdownBox" v-show="isDropdown">
      
        <div id="dataFilter">
          
          <el-row>
            <el-col :span="12"><h3>数据筛选</h3></el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="2">
              <el-checkbox v-model="que.useQue">使用</el-checkbox>
            </el-col>
            
            <el-col :span="10">
              </span><el-input type="text" placeholder="帅选条件" v-model="que.que" :disabled="!que.useQue" />
            </el-col>
          </el-row>
          
        </div>


        <div>
          
           <el-row>
             <el-col :span="12"><h3>数值型数据转为类别型数据</h3></el-col>
           </el-row>
           <el-row :gutter="20">
             <el-col :span="2"><el-checkbox v-model="cut.useCut" @change="gro.useType = $event ? 'cut':'default'">使用</el-checkbox></el-col>
             <el-col :span="10"><el-input type="text" placeholder="设置区间" :disabled="!cut.useCut" v-model="cut.cutBins" /></el-col>
             <el-col :span="10"><el-input type="text" placeholder="对应的类别" :disabled="!cut.useCut" v-model="cut.cutLabels" /></el-col>
           </el-row>
        </div>

        <div>
          <el-row><el-col><h3>数据分组</h3></el-col></el-row>
          <el-row>
            <el-col :span="4" style="text-align: left;"><el-checkbox v-model="gro.useGro">使用</el-checkbox></el-col>
        </el-row>

        <el-radio-group v-model="gro.useType" v-show="gro.useGro">
          <el-radio :label="gro.groType[0].iid" v-show="!cut.useCut && $store.state.mode!='pie' || $store.state.mode=='pie'">{{gro.groType[0].text}}</el-radio>
          <el-radio :label="gro.groType[1].iid" v-show="!cut.useCut && $store.state.mode!='pie'">{{gro.groType[1].text}}</el-radio>
          <el-radio :label="gro.groType[2].iid" v-show="cut.useCut && $store.state.mode!='pie'">{{gro.groType[2].text}}</el-radio>
        </el-radio-group>
        
        <el-row v-show="gro.useGro && gro.useType == 'double'">
          <el-col :span="3">二级分组项：</el-col>
          <el-col :span="4">
            <el-select v-model="gro.doubleCol">
              <el-option :value="opt.iid" :label="opt.text" v-for="(opt, optIndex) in cols" :key="optIndex"></el-option>
            </el-select>
          </el-col>
        </el-row>

        <el-row :gutter="20" v-show="gro.useGro">
        <el-col :span="3">Y处理：</el-col>
        <el-col :span="4" v-for="(groSel, index) in gro.isSl" :key="index">
          <el-select v-model="gro.isSl[index]">
            <el-option v-for="i,iIndex in gro.opt" :key="iIndex" :value="i.iid" :label="i.text"></el-option>
          </el-select>
        </el-col>
        </el-row>

        
        


        </div>

        <div v-show="$store.state.y.length > 1">
          <el-row>
            <el-col><h3>Y轴数据转化成比例</h3></el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="3"><el-checkbox v-model="rate.useRate">使用</el-checkbox></el-col>
            <el-col :span="4" v-show="rate.useRate">保留几位小数：</el-col>
            <el-col :span="3" v-show="rate.useRate"><el-input v-model="rate.tail" size="mini" type="number"></el-input></el-col>
          </el-row>
          <el-row v-show="rate.useRate">
            <el-col :span="3" v-for="i in rate.radio.opt" :key="i.iid">
              <el-radio v-model="rate.radio.isSl" :label="i.iid">{{i.text}}</el-radio>
            </el-col>
          </el-row>
        </div>

        

        <div v-show="this.$store.state.mode != 'pie'">
          <el-row>
            <el-col><h3>设置xy轴刻度</h3></el-col>
          </el-row>
          
            <el-row :gutter="40" v-for="(i, index) in ticks" :key="index">
              <el-col :span="6">{{ i.title }}</el-col>
              <el-col :span="3" v-for="(j,jIndex) in i.opt" :key="jIndex">
                <input type="radio" :id="j.iid" :value="j.iid" v-model="i.isSl" @click="i.isSl = $event.target.value"  />
                <label :for="j.iid">{{ j.text }}</label>
              </el-col>
              <el-col :span="6"></el-col>
              <el-col :span="4" v-for="(k,kIndex) in i.min_max_in" :key="k.iid" v-show="i.isSl == 'setting' + index">
                <el-input type="number" v-model="k.text" :placeholder="i.min_max_in_text[kIndex]" />
              </el-col>
            </el-row>

          
        </div> 


      
    </div>
  </div>
</template>

<script>
import EventBus from '../../EventBus/index.js'

export default {
  props:{
    cols:{
      type:Array,
      default(){
        return []
      }
    }
  },
  data(){
    return {
      isDropdown: false,
      //query
      que:{
        useQue: false,
        que: "",
      },
      //gro
      gro: {
          useGro: false,
          groType: [
            {iid:'default',text:'按X轴数据进行分组'},
            {iid:'double',text:'先按X轴数据进行分组，再按自定义进行分组'},
            {iid:'cut',text:'先按X轴数据进行分组，再按转换的类别数据进行分组'},
          ],
          useType: 'default',
          isSl: ["mean"],
          doubleCol:'',
          opt: [
            { iid: "mean", text: "平均值" },
            { iid: "min", text: "最小值" },
            { iid: "max", text: "最大值" },
            { iid: "count", text: "计数" },
          ],
        },
      //cut
      cut:{
        useCut:false,
        cutBins:'',
        cutLabels:''
      },
      rate:{
        useRate: false,
        tail: '2',
        radio:{
          isSl:'0',
          opt:[
            {iid:'0',text:'转成百分比'},
            {iid:'1',text:'转成小数比'},
          ]
        }
      },
      ticks: [
        {
          iid: 0,
          title: "X轴刻度:下限-上限-间隔：",
          isSl: "default0",
          min_max_in_text:['X轴的下限','X轴的上限','刻度最小值','刻度最大值','刻度的间隔'],
          min_max_in:[
            {iid:'xt0',text:''},
            {iid:'xt1',text:''},
            {iid:'xt2',text:''},
            {iid:'xt3',text:''},
            {iid:'xt4',text:''},
           ],
          opt: [
            { iid: "default0", text: "默认" },
            { iid: "none0", text: "不显示" },
            { iid: "setting0", text: "自定义" },
          ],
        },
        {
          iid: 1,
          title: "Y轴刻度:下限-上限-间隔：",
          isSl: "default1",
          min_max_in_text:['Y轴的下限','Y轴的上限','刻度最小值','刻度最大值','刻度的间隔'],
          min_max_in:[
            {iid:'yt0',text:''},
            {iid:'yt1',text:''},
            {iid:'yt2',text:''},
            {iid:'yt3',text:''},
            {iid:'yt4',text:''},
          
          ],
          opt: [
            { iid: "default1", text: "默认" },
            { iid: "none1", text: "不显示" },
            { iid: "setting1", text: "自定义" },
          ],
        }
      ]
    
    }
  },
  methods:{
    clickDropdown(){
      this.isDropdown = !this.isDropdown
    }
  },
  mounted(){
    EventBus.$on('chartChange',mode => {
      this.que.useQue = false
      this.que.que = ''
      this.cut.useCut = false
      this.cut.cutBins = ''
      this.cut.cutLabels = ''
      this.gro.useGro = false
      this.gro.isSl = ["mean"]
      this.gro.useType = 'default'
      this.rate.useRate = false
      this.rate.tail = '2'
      this.rate.radio.isSl = '0'

      for(let i in this.ticks){
        this.ticks[i].isSl = 'default' + i
        for(let j in this.ticks[i].min_max_in){
          this.ticks[i].min_max_in[j].text = ''
        }
      }
      
    })
    EventBus.$on('addY',()=>{
      this.gro.isSl.push("mean")
    })
    EventBus.$on('redY',()=>{
      this.gro.isSl.pop()
    })
  },
  watch:{
    'que':{
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeOption',
          key: 'que',
          value: this.que
        })
      }
    },
    'gro':{
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'gro',
          value: {
            useGro: this.gro.useGro, 
            useType: this.gro.useType,
            doubleCol: this.gro.doubleCol,
            gro: this.gro.isSl
          }
        })
      }
    },
    'cut':{
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeOption',
          key: 'cut',
          value: this.cut
        })
      }
    },
    'rate':{
      deep:true,
      immediate:true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'rate',
          value: {
            useRate:this.rate.useRate,
            tail:this.rate.tail,
            isSl:this.rate.radio.isSl
          }
        })
      }
    },
    'ticks':{
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeOption',
          key: 'xt',
          value:{
            xtSl: this.ticks[0].isSl,
            xtStr: this.ticks[0].min_max_in
          }
        })
        this.$store.commit({
          type: 'updateHomeOption',
          key: 'yt',
          value:{
            ytSl: this.ticks[1].isSl,
            ytStr: this.ticks[1].min_max_in
          }
        })
      }
    }
  }   
}
</script>

<style scoped>
#HomeOption {
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
.el-col {
  height: 50px;
  line-height: 50px;
}
.el-radio-group {
  margin: 3px 0 8px 0;
}
</style>
