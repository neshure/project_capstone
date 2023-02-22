const { createApp } = Vue;

const app = createApp({
  delimiters: ['[[', ']]'],
  data() {
    return {
      whiskey: [],
    }
  },
  methods: {
    getWhiskey() {
      axios.get('https://www.reddit.com/r/whiskey/.json')
        .then((data) => {
          this.whiskey = data.data.data.children
          console.log(data.data.data.children);
        })
      } 
    },
    created() {
      this.getWhiskey()
    }
  })
  app.mount('#app')