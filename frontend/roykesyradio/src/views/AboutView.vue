<template>
  <div class="about">
    <h1>This is an about page</h1>
    <marquee-text :repeat="10"> Short text =( </marquee-text>
  </div>
</template>
<script>
import MarqueeText from "vue-marquee-text-component";
export default { name: "AboatView", components: { MarqueeText } };
</script>
