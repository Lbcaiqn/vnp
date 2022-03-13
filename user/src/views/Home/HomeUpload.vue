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
      tipText: ''
    }
  },
  methods:{
    upload(files){
      this.$emit('beforeUpload')
      this.isUpload = true
      this.tipText = ''
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
          this.tipText = '文件上传成功！'
        })
      

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
  margin-top: 50px ;
}
.el-col {
  height: 50px;
  line-height: 50px;
}
p {
  margin-top: 20px;
}
</style>