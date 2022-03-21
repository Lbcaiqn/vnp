import axios from 'axios'
export function req(config){
  //对该实例进行全局配置
  const instance1=axios.create({
    // baseURL:'http://47.107.225.248:8000'
    baseURL:'http://localhost:8000'
  })
  return instance1(config)
}
