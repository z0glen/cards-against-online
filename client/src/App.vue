<template>
  <div id="app">
    <Nav/>
    <br>
    <router-view/>
  </div>
</template>

<script>

import Nav from "./components/Nav";

export default {
  name: 'App',
  components: {
    Nav,
  },
  watch: {
    '$route' (to) {
      document.title = to.meta.title || 'Cards Against Online'
    }
  }
}
</script>
