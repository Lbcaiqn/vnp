<template>
  <div id="HomeMain">
    
    <el-row :gutter="20">
      <el-col :span="2">{{ chart.text }}</el-col>
      <el-col :span="4">
        <el-select v-model="chart.isSelectChart" @change="chartChange">
          <el-option v-for="c in chart.chart" :key="c.iid" :value="c.iid" :label="c.text"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4" v-if="chart.isSelectChart == 'plot' || chart.isSelectChart == 'bar'">
        <el-button @click="redPlotY"><i class="el-icon-minus"></i></el-button>
        <el-button @click="addPlotY"><i class="el-icon-plus"></i></el-button>
      </el-col>
      <el-col :span="2" v-if="this.chart.isSelectChart == 'bar'">方向：</el-col>
      <el-col :span="4" v-if="this.chart.isSelectChart == 'bar'">
        <el-select v-model="barStyle.orientation.isSl">
          <el-option v-for="i in barStyle.orientation.opt" :key="i.iid" :value="i.iid" :label="i.text"></el-option>
        </el-select>
      </el-col>
      <el-col :span="2" v-if="this.chart.isSelectChart == 'bar' && xy.y.sel.isSl.length >= 2">排列：</el-col>
      <el-col :span="4" v-if="this.chart.isSelectChart == 'bar' && xy.y.sel.isSl.length >= 2" >
        <el-select v-model="barStyle.fold.isSl">
          <el-option v-for="i in barStyle.fold.opt" :key="i.iid" :value="i.iid" :label="i.text"></el-option>
        </el-select>
      </el-col>

    </el-row>
        
    <el-row :gutter="20" v-for="(xory, xoryIndex) in xy" :key="xoryIndex" v-show="xoryIndex == 'x' || chart.isSelectChart != 'pie'">
      <el-col :span="2" v-if="chart.isSelectChart != 'pie'">{{ xory.text }}</el-col>
      <el-col :span="2" v-if="chart.isSelectChart == 'pie'">展示：</el-col>
      <el-col :span="4" v-for="sum in xory.sel.sum" :key="sum">
        <el-select v-model="xory.sel.isSl[sum-1]" @change="xyChange(xory, sum)">
          <el-option :value="opt.iid" :label="opt.text" v-for="(opt, optIndex) in cols" :key="optIndex"></el-option>
        </el-select>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" v-show="chart.isSelectChart != 'pie'">
      <el-col :span="2"></el-col>
      <el-col :span="4" v-for="(cal, calIndex) in calculateNewColumn" :key="calIndex">
        <el-input v-if="cal.isShow" type="text" v-model="cal.str" @input="checkCalStr(cal.str, calIndex)" />
      </el-col>
    </el-row>

    <div class="tipDiv">
      <h3>提示：</h3>
      <p v-if="chart.isSelectChart == 'pie'">
      绘制饼图需要类别型数据，若选择的是数值型数据，可在【高级选项】中转换成类别型数据
    </p>
    <p>若选择的数据是一个x值对应多个y值，则需要在【高级选项】中对x进行分组，并将多个y合并成一个值</p>
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
        chart: {
          isSelectChart: '',
          text: "图表：",
          chart: {
            scatter: { iid: "scatter", text: "散点图" },
            plot: { iid: "plot", text: "折线图" },
            bar: { iid: "bar", text: "柱状图" },
            pie: { iid: "pie", text: "饼图" }
          },
        },
        xy: {
          x: { text: "X轴：", sel: { sum: 1, isSl: [""] } },
          y: { text: "Y轴：", sel: { sum: 1, isSl: [""] } },
        },
        barStyle:{
          fold: {
            isSl:'transverse',
            opt:[
              {iid:'transverse',text:'并列'},
              {iid:'vertical',text:'堆叠'}
            ]
          },
          orientation: {
            isSl:'vertical',
            opt:[
              {iid:'vertical',text:'垂直'},
              {iid:'horizontal',text:'水平'}
            ]
          }
        },
        calculateNewColumn: [{ str: "", isShow: false }],
        
      }
  },
  methods:{
      chartChange(){
        this.xy = {
          x: { text: "X轴：", sel: { sum: 1, isSl: [this.xy.x.sel.isSl[0]] } },
          y: { text: "Y轴：", sel: { sum: 1, isSl: [this.xy.y.sel.isSl[0]] } },
        }
        this.calculateNewColumn = [this.calculateNewColumn[0]];
        
        this.barStyle.orientation.isSl = 'vertical'
        this.barStyle.fold.isSl = 'transverse'

        EventBus.$emit('chartChange',this.chart.isSelectChart)
      },
      xyChange(xy, sum) {
        let isSl = ''
        if(xy.sel.isSl[sum-1] != 'calculate') isSl = this.cols[parseInt(xy.sel.isSl[sum-1]) + 1].text.substr(2)
        EventBus.$emit('xyChange',{
          xy: xy.text,
          sum,
          isSl,
        })
        
        if (xy.text == "Y轴：") {
          if (xy.sel.isSl[sum-1] == "calculate") {
            this.calculateNewColumn[sum - 1].isShow = true;
          } 
          else {
            this.calculateNewColumn[sum - 1].isShow = false;
            this.calculateNewColumn[sum - 1].str = "";
          }
        }
      },
      addPlotY() {
        let sum = this.xy.y.sel.sum + 1;
        if (sum <= 5 && this.$store.state.mode == 'plot' || sum <= 3 && this.$store.state.mode == 'bar') {
          this.xy.y.sel.sum = sum;
          this.xy.y.sel.isSl.push('');
          this.calculateNewColumn.push({ str: "", isShow: false });
          EventBus.$emit('addY')
        }
         
      },
      redPlotY() {
        let sum = this.xy.y.sel.sum - 1;
        if (sum >= 1) {
          this.xy.y.sel.sum = sum;
          this.xy.y.sel.isSl.pop();
          this.calculateNewColumn.pop();

          if(sum == 1) this.barStyle.fold.isSl = 'transverse'

          EventBus.$emit('redY')
        }
      },
      checkCalStr(str, i) {
      let newChar = str[str.length - 1];
      let last2Char =
        this.calculateNewColumn[i].str[
          this.calculateNewColumn[i].str.length - 2
        ];
      if (
        //限制输入的字符
        newChar != "+" &&
        newChar != "-" &&
        newChar != "*" &&
        newChar != "/" &&
        newChar != "c" &&
        newChar != "(" &&
        newChar != ")" &&
        !(newChar >= "0" && newChar <= "9")
      ) {
        this.calculateNewColumn[i].str = this.calculateNewColumn[i].str.substr(
          0,
          str.length - 1
        );
      }
    },
  },
  watch:{
    'chart.isSelectChart'(newVal){
      this.$store.commit({
        type: 'updateHomeMain',
        key: 'mode',
        value: newVal
      })
    },
    'xy.x.sel.isSl'(newVal){
      this.$store.commit({
        type: 'updateHomeMain',
        key: 'x',
        value: newVal
      })
    },
    'xy.y.sel.isSl'(newVal){
      this.$store.commit({
        type: 'updateHomeMain',
        key: 'y',
        value: newVal
      })
    },
    'barStyle': {
      deep: true,
      immediate: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'barStyle',
          value: {
            fold: this.barStyle.fold.isSl,
            orientation: this.barStyle.orientation.isSl
          }
        })
      }
    },
    'calculateNewColumn'(newVal){
      this.$store.commit({
        type:'updateHomeMain',
        key:'cal',
        value:newVal
      })
    },
  },
  beforeDestory(){
    EventBus.$off('chartChange')
    EventBus.$off('xyChange')
    EventBus.$off('addY')
    EventBus.$off('redY')
  }
}
</script>

<style scoped>
#HomeMain {
  margin: 20px;
  padding: 20px;
}
.el-col {
  height: 50px;
  line-height: 50px;
  text-align: center;
}
.tipDiv {
  margin-top: 60px;
}
.tipDiv p {
  margin: 10px 0;
}
</style>