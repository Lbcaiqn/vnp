<template>
  <div id="ShowNav">
    <div class="showSelect">
      <el-row :gutter="20">
        <el-col :span="4">
          <el-select v-model="dataSelect.isSl" @change="pageChange">
            <el-option v-for="i in dataSelect.opt" :key="i.iid" :value="i.iid" :label="i.text"></el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>
    
  </div>
</template>

<script>

export default {
  data(){
    return {
      dataSelect: {
        isSl: 'population',
        opt:[
          {iid:'population',text:'中国人口数据'},
          {iid:'temperature',text:'世界气温数据'}
        ]
      },
      
      
     
    }
  },
  methods: {
    pageChange(i){
      this.$emit('dataChange',i)
    }
  }
}
</script>

<style scoped>
#ShowNav {
  padding: 40px;
  border-bottom: 1px solid #fff;
}

</style>