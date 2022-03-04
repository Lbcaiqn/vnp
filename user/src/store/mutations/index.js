export default {
  updateHomeMain(state,payload){
    state[payload.key] = payload.value
  },
  updateHomeOption(state,payload){
    state[payload.key] = payload.value
  }
}