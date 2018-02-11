

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
      this.searchRedirect();
      //this.getData()
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
    /*getData:  _.debounce(function (){
      var searchResult= this.search;
      var vm=this;
      return fetch("https://api.bart.gov/api/stn.aspx?cmd=stninfo&key=MW9S-E7SL-26DU-VV8V&json=y&orig=" +searchResult).then((response)=>{
        return response.json()
      }).then((data)=>{
        console.log(data);

      });
    }, 500),
*/
    searchRedirect: _.debounce(function(){
      var searchResult= this.search;
      var vm=this;
      var commercialTest = /^(commercial)$/ig;
      var dwellersTest = /^(dwellers fire)$/ig;
      var homeTest = /^(homeowners)$/ig;
      var nameTest = /^[a-z ,.'-]+$/ig;
      var policynumberTest = /^[0-9]+$/g;

      if (commercialTest.test(searchResult) || dwellersTest.test(searchResult) || homeTest.test(searchResult)){
        console.log("We're searching for policy type");
        return fetch("https://api.bart.gov/api/stn.aspx?cmd=stninfo&key=MW9S-E7SL-26DU-VV8V&json=y&orig=" +searchResult).then((response)=>{
          return response.json()
        }).then((data)=>{
          console.log(data);

        });
      }
      else if (nameTest.test(searchResult)){
        console.log("We're searching for a name");
        return fetch("https://api.bart.gov/api/stn.aspx?cmd=stninfo&key=MW9S-E7SL-26DU-VV8V&json=y&orig=" +searchResult).then((response)=>{
          return response.json()
        }).then((data)=>{
          console.log(data);

        });
      }

      else if (policynumberTest.test(searchResult)){
        console.log("We're searching for policy number");
        return fetch("http://localhost:5000/JSON/policy/"+ searchResult).then((response)=>{
          return response.json()
        }).then((data)=>{
          console.log(data);

        });
      }

      else{
        console.log("We're searching for address");
        return fetch("http://localhost:5000/JSON/address/" +searchResult).then((response)=>{
          return response.json()
        }).then((data)=>{
          console.log(data);

        });
      }


    },500)



  }
})
