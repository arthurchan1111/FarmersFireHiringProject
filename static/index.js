

var app = new Vue({

  el: '#app',

  data: {
     search: '',
     checked: false,
     selected: false,
     initialWidth: window.innerWidth,
     screenWidth: 0,
     mobileState: true,
     mobileSelectState: 0,
     col: 'col'

  },
  watch: {
    search: function() {
      this.getData()
    },
    screenWidth: function(newWidth){
       if (newWidth > 576){
         this.mobileState = false
       }
       else{
         this.mobileState = true
       }
    }


  },
  created: function(){
    let vm = this;
    console.log(vm.mobileState)
    if (vm.initialWidth > 576){
      vm.mobileState = false

    }
    else{
      vm.mobileState = true
    }
    console.log(vm.mobileState)
  },
  mounted: function(){
    this.$nextTick(function () {
      let vm= this;
      window.addEventListener('resize', function(e) {
        vm.screenWidth = window.innerWidth
      });
 })
  },

  methods: {
    getData:  _.debounce(function (){
      var searchResult= this.search;
      var vm=this;
      return fetch("https://api.bart.gov/api/stn.aspx?cmd=stninfo&key=MW9S-E7SL-26DU-VV8V&json=y&orig=" +searchResult).then((response)=>{
        return response.json()
      }).then((data)=>{
        console.log(data);

      });
    }, 500)

  }
})
  
