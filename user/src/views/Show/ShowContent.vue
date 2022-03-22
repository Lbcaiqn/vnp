<template>
  <div id="ShowContent">

    <div id="ShowNav" ref="ShowNav">
    <div class="showNav">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-select v-model="dataSelect.isSl">
            <el-option v-for="i in dataSelect.opt" :key="i.iid" :value="i.iid" :label="i.text"></el-option>
          </el-select>
        </el-col>
        <el-col :span="19">
          <ul>
            <li v-for="(i,iIndex) in navItem" :key="iIndex" @click="clickShowNavItem(iIndex)">
              <span :class="{'spanUnderline':navSpan[iIndex]}">{{i}}</span>
            </li>
          </ul>
        </el-col>
      </el-row>
    </div>
    
    <div v-show="this.isFix" class="showNav ShowNavFix">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-select v-model="dataSelect.isSl">
            <el-option v-for="i in dataSelect.opt" :key="i.iid" :value="i.iid" :label="i.text"></el-option>
          </el-select>
        </el-col>
        <el-col :span="19">
          <ul>
            <li v-for="(i,iIndex) in navItem" :key="iIndex" @click="clickShowNavItem(iIndex)">
              <span :class="{'spanUnderline':navSpan[iIndex]}">{{i}}</span>
            </li>
          </ul>
        </el-col>
      </el-row>
    </div>
  </div>

    <div ref="ShowContent">
      <div class="contentBox" v-for="(i,iIndex) in content[dataSelect.isSl]" :key="iIndex">
      <h1>{{i.title}}</h1>
      <div v-for="(j,jIndex) in i.content" :key="jIndex">
        <h2>{{j.title}}</h2>
        <p>{{j.text}}</p>
        <img v-for="(k,kIndex) in j.img" :key="kIndex" :src=k>
      </div>
    </div>
    </div>
    
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  props:{
    content:{
      type: Object,
      default(){
        return {}
      }
    }
  },
  data(){
    return {
      dataSelect: {
        isSl: 'population',
        opt:[
          {iid:'population',text:'中国人口数据'},
          {iid:'temperature',text:'世界气温数据'}
        ]
      },
      navItem: ['散点图','折线图','柱状图','饼图'],
      navSpan: [false,false,false,false],
      isFix: false,
      navY: 0
    }
  },
  methods:{
    scrollFun(){
      /*试过mounted和@load中获取nav的offwetTop，但是都不对，多了1000，
      最后干脆直接滚动事件中获取*/
      if(this.$refs.ShowNav != undefined)
        this.navY = this.$refs.ShowNav.offsetTop
      
      let top = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
      this.isFix = top >= this.navY ? true : false
      
      if(this.$refs.ShowContent != undefined){
        let tag = -1
        for(let i in this.$refs.ShowContent.children){
          if(i == 0) continue
          if(this.$refs.ShowContent.children.length > i){
            tag = top < this.$refs.ShowContent.children[i].children[0].offsetTop-500 ? tag : i-1
          }
        }
        for(let i in this.navSpan){
          Vue.set(this.navSpan,i,false)
      }
      if(tag != -1) Vue.set(this.navSpan,tag,true)
      }
    },
    clickShowNavItem(i){
      for(let index in this.navSpan){
        Vue.set(this.navSpan,index,false)
      }
      Vue.set(this.navSpan,i,true)
      
      if(this.$refs.ShowContent.children.length > i+1){
        let moveY = this.$refs.ShowContent.children[i+1].children[0].offsetTop
        // window.scroll(0,moveY-80)
        window.scrollTo({
          top: moveY-79,
          behavior: "smooth"
        })
      }
    }
  },
  watch:{
    'dataSelect.isSl'(newVal){
      this.navItem=[]
      for(let i in this.content[newVal]){
        if(i!='dataDesc'){
          this.navItem.push(this.content[newVal][i].title)
        }
      }
    }
  },
  mounted(){
    window.addEventListener('scroll',this.scrollFun)

  },
  destoryed(){
    window.removeEventListener('scroll', this.scrollFun)
  }
}

</script>

<style scoped>
.showNav {
  padding: 20px 10px 20px 40px;
  width: 1100px;
  background: url(../../assets/img/nav.png) no-repeat;
  background-size: 100%;
  border-top: 1px solid #fff;
  box-sizing: border-box;
}
.ShowNavFix {
  position: fixed;
  top: 0;
  z-index: 999;
}
ul {
  display: flex;
}
li {
  flex: 1;
  list-style: none;
  height: 40px;
  line-height: 40px;
  text-align: center;
}
li:hover {
  background-color: orange;
  cursor: pointer;
  transition: all 0.5s;
}
.spanUnderline {
  
  border-bottom: 3px solid #fff;
}




.contentBox {
  margin: 20px;
  padding: 20px;
  box-sizing: border-box;
}
h1 {
  padding: 20px;
  border-bottom: solid 1px #fff;
}
h2 {
  padding: 40px 20px 0 20px;
}
p {
  padding: 20px;
  font-size: 18px;
  line-height: 35px;
}
img {
  margin: 0 25px 10px 25px;
  width: 970px;
}
.contentBox {
  margin-bottom: 100px;
}
</style>