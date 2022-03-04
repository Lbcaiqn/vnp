<template>
  <div id="HomeUpload">
    <el-upload action="" size="" :show-file-list="false" :http-request="upload">
  <el-button size="medium" type="primary" v-show="!isUpload">点击上传</el-button>
  <el-button size="medium" type="primary" :loading="true"  v-show="isUpload">上传中...</el-button>
  
</el-upload>
  </div>
</template>

<script>
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI);
import {req} from '../../network/index.js'

export default {
  data(){
    return {
      isUpload: false
    }
  },
  methods:{
    upload(files){
      this.$emit('beforeUpload')
      this.isUpload = true
      let file = files.file
      const fileReader = new FileReader();
      fileReader.readAsText(file, "utf8"); //编码要与csv文件的编码一致，否则中文乱码
      fileReader.onload = () => {
      //读取完成
      let res = fileReader.result,str = "";
      //取出首行
      for (let i of res) {
        if (i == "\n") break;
        str += i;
      }
      let resArr = str.split(","),cols=[];
      for (let i in resArr) {
        let data = {};
        data.iid = i;
        data.text = resArr[i];
        cols.push(data)
      }
      //获取FormData
      let data = new FormData(),fd = null;
      data.append(file.name, file);
      fd = data;
      
      //上传
      req({
        url: '/upload',
        method: "post",
        data: fd,
        headers: {"Content-Type": "multipart/form-data",},
      }).then(res=>{
          this.$emit('afterUpload',{
            cols,
            filePath: res.data
          })
          this.isUpload = false
        })
      

      }
    }
  }
}


</script>

<style scoped>
#HomeUpload {
  margin: 20px;
  padding: 20px;
}
</style>