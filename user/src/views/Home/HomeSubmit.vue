<template>
  <div id="HomeSubmit">
    <el-row>
      <el-col :span="4">
        <el-button size="medium" type="primary" v-show="!isSubmit" @click="clickSubmit">开始绘制</el-button>
        <el-button size="medium" type="primary" :loading="true"  v-show="isSubmit">绘制中...</el-button>
      </el-col>
      <el-col :span="4">
        <span>{{tipsText}}</span>
      </el-col>
    </el-row>
    
  </div>
</template>

<script>
import { req } from "../../network/index.js";
import { mid2behind } from '../../myTool/mid2behind.js';

export default {
  data(){
    return {
      tipsText: '',
      isSubmit: false
    }
  },
  methods:{
    clickSubmit() {
      this.tipsText = ''
      this.$store.state.imgURL = "#"
      
      if (this.$store.state.fd.filePath == '') this.tipsText = "请先上传文件";
      else if (this.$store.state.mode == '') this.tipsText = "请选择要画的图";
      else {
        let flag = true;
        for(let i in  this.$store.state.y){
          if(this.$store.state.x[i] == '' || this.$store.state.y[i] == ''){
            flag = false
            this.tipsText = '请选择完X/Y数据'
            break
          }
        }
        
        
       
        if(this.$store.state.mode == 'pie' && this.$store.state.x[0] != ''){
          flag = true
          this.tipsText = ''
        }
        if (flag) {
          this.isSubmit = true
          
          let calArr = [],xtArr = [this.$store.state.xt.xtSl],ytArr = [this.$store.state.yt.ytSl]
          for (let i of this.$store.state.cal) {
            let cal = i.str
            if(cal != '') cal = mid2behind(cal)    
            calArr.push(cal)
          }
          for(let i of this.$store.state.xt.xtStr)  xtArr.push(i.text)
          for(let i of this.$store.state.yt.ytStr)  ytArr.push(i.text)
          let style = {scatter:[],plot:[],bar:[],pie:[]}
          for(let i in this.$store.state.style){
            for(let j in this.$store.state.style[i]){
              style[i].push([])
              for(let k in this.$store.state.style[i][j]){
                if(typeof this.$store.state.style[i][j][k].val == 'object') style[i][j].push(this.$store.state.style[i][j][k].val.isSl)
                else style[i][j].push(this.$store.state.style[i][j][k].val)
              }
            }
          }
          
          const submitData = {
            filePath: this.$store.state.fd.filePath,
            mode: this.$store.state.mode,
            x: this.$store.state.x,
            y: this.$store.state.y,
            barStyle: this.$store.state.barStyle,
            cal: calArr,
            que: this.$store.state.que,
            cut: this.$store.state.cut,
            gro: this.$store.state.gro,
            xt: xtArr,
            yt: ytArr,
            theme: this.$store.state.theme,
            desc:this.$store.state.desc,
            style
          }
          

          req({
            url: "/aaa",
            method: "post",
            data: {
              submitData,
              imgName: this.$store.state.mode
            },
          }).then((res) => {
            this.isSubmit = false
            this.$store.state.imgURL = res.data;
            if (res.data == "#") this.tipsText = "绘制失败";
            else this.tipsText = "绘制成功";
            
          });
        }
      }
    },
  }
}
</script>

<style scoped>
#HomeSubmit {
  margin: 20px;
  padding: 20px;
}
.el-col {
  height: 30px;
  line-height: 30px;
}
</style>