<template>
  <div id="HomeUpload">
    <div class="uploadBox">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-upload action="" size="" :show-file-list="false" :http-request="upload">
            <el-button title="目前仅支持.csv文件的上传，且确保文件的第一行为列名" size="medium" type="primary" v-show="!isUpload">点击上传</el-button>
            <el-button size="medium" type="primary" :loading="true"  v-show="isUpload">上传中...</el-button>
          </el-upload>
        </el-col>
        <el-col :span="15" v-show="isUpload">
          <div class="uploadBar">
            <div ref="uploadBarBox"></div>
          </div>
        </el-col>
        <el-col :span="4" v-show="isUpload">{{uploadWidth}}</el-col>
    </el-row>
    <el-row>
      <p>{{tipText}}</p>
    </el-row>
    </div>
  </div>
</template>

<script>

import {req} from '../../network/index.js'

export default {
  data(){
    return {
      isUpload: false,
      tipText: '',
      uploadWidth: '0%'
    }
  },
  methods:{
    upload(files){
      this.$emit('beforeUpload')
      this.isUpload = true
      this.uploadWidth = '0%'
      this.$refs.uploadBarBox.style.width = 0
      this.tipText = ''
      let file = files.file
      if(file.name.split('.')[file.name.split('.').length-1] != 'csv'){
        this.isUpload = false
        this.tipText = '上传失败，目前只支持csv文件哦'
      }
      else {
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
        onUploadProgress: progress => {
          this.$refs.uploadBarBox.style.width = Math.round((progress.loaded*100)/progress.total) + '%'        
          this.uploadWidth = this.$refs.uploadBarBox.style.width != '100%' ? this.$refs.uploadBarBox.style.width : '文件配置中...'
        }
      }).then(res=>{
          this.$emit('afterUpload',{
            cols,
            filePath: res.data
          })
          this.isUpload = false
          this.tipText = '文件上传成功！'
        })
      

      }
      }
    },
   
  }
}


</script>

<style scoped>
#HomeUpload {
  margin-left: 20px;
  padding: 20px;
}
.uploadBox {
  margin-top: 20px ;
}
.el-col {
  height: 40px;
  line-height: 50px;
}
.uploadBar {
  height: 50px;
  border: 1px solid #fff;
}
.uploadBar>div {
  width: 0;
  height: 50px;
  background-color: blue;
}
p {
  margin-top: 20px;
}
</style>