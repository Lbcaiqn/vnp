<template>
  <div id="HomeImg">
      <img v-show="this.$store.state.imgURL != '#'" :src="this.$store.state.imgURL" />
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
#HomeImg {
  margin: 20px;
  padding: 20px;
}
</style>