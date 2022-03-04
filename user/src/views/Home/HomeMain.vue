<template>
  <div id="HomeMain">
    <!-- <p>fd:{{this.$store.state.fd}}</p>
    <p>mode:{{this.$store.state.mode}}</p>
    <p>x:{{this.$store.state.x}}</p>
    <p>y:{{this.$store.state.y}}</p>
    <p>cal:{{this.$store.state.cal}}</p>
    <p>gro:{{this.$store.state.gro}}</p>
    <p>que:{{this.$store.state.que}}</p>
    <p>cut:{{this.$store.state.cut}}</p> -->
    
    <!-- <p>xt:{{this.$store.state.xt}}</p> -->
    <!-- <p>yt:{{this.$store.state.yt}}</p> -->
    



    <el-row :gutter="20">
      <el-col :span="2">{{ chart.text }}</el-col>
      <el-col :span="4">
        <el-select v-model="chart.isSelectChart" @change="chartChange">
          <el-option v-for="c in chart.chart" :key="c.iid" :value="c.iid" :label="c.text"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4" :offset="4" v-if="chart.isSelectChart == 'plot' || chart.isSelectChart == 'bar'">
        <el-button @click="redPlotY"><i class="el-icon-minus"></i></el-button>
        <el-button @click="addPlotY"><i class="el-icon-plus"></i></el-button>
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

    <el-row>
      <el-col style="text-align: left;"><el-checkbox v-model="gro.useGro">按X轴数据进行分组</el-checkbox></el-col>
    </el-row>
    <el-row :gutter="20" v-show="gro.useGro">
        <el-col :span="2">Y处理：</el-col>
        <el-col :span="4" v-for="(groSel, index) in gro.isSl" :key="index">
          <el-select v-model="gro.isSl[index]">
            <el-option v-for="i,iIndex in gro.opt" :key="iIndex" :value="i.iid" :label="i.text"></el-option>
          </el-select>
        </el-col>
      </el-row>


  </div>
</template>

<script>
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
        calculateNewColumn: [{ str: "", isShow: false }],
        
        gro: {
          useGro: false,
          isSl: ["mean"],
          opt: [
            { iid: "mean", text: "平均值" },
            { iid: "min", text: "最小值" },
            { iid: "max", text: "最大值" },
          ],
        },
      }
  },
  methods:{
      chartChange() {
        this.xy = {
          x: { text: "X轴：", sel: { sum: 1, isSl: [this.xy.x.sel.isSl[0]] } },
          y: { text: "Y轴：", sel: { sum: 1, isSl: [this.xy.y.sel.isSl[0]] } },
        }
        this.calculateNewColumn = [this.calculateNewColumn[0]];
        this.gro.isSl = ["mean"];
      },
      xyChange(xy, sum) {
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
        if (sum <= 5) {
          this.xy.y.sel.sum = sum;
          this.xy.y.sel.isSl.push('');
          this.calculateNewColumn.push({ str: "", isShow: false });
          this.gro.isSl.push("mean");
        }
      },
      redPlotY() {
        let sum = this.xy.y.sel.sum - 1;
        if (sum >= 1) {
          this.xy.y.sel.sum = sum;
          this.xy.y.sel.isSl.pop();
          this.calculateNewColumn.pop();
          this.gro.isSl.pop();
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
    'calculateNewColumn'(newVal){
      this.$store.commit({
        type:'updateHomeMain',
        key:'cal',
        value:newVal
      })
    },
    'gro':{
      deep: true,
      handler(){
        this.$store.commit({
          type: 'updateHomeMain',
          key: 'gro',
          value: {useGro: this.gro.useGro, gro: this.gro.isSl}
        })
      }
    }
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
</style>