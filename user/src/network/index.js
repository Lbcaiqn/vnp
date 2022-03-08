import axios from 'axios'
export function req(config){
  //对该实例进行全局配置
  const instance1=axios.create({
    baseURL:'http://39.108.187.254:8000'
  })
  return instance1(config)
}
