var app = new Vue({

  el: '#app',

  data: {
    search: '',
    checked: false,
    initialWidth: window.innerWidth,
    screenWidth: 0,
    mobileState: true,
    mobileSelectState: 0,
    col: 'col',
    requestData: [0],
    dataCode: '',
    letterCode: '',
    post: [],
    url_endpoint: '',
    ptypes: [],
    form: {
      fname: '',
      lname: '',
      address: '',
      policy_number: '',
      policy_type: ''
    },
    ids: [false],

    addresslist: []

  },
  watch: {
    search: _.debounce(function() {
      this.url_endpoint = this.basicSearch(this.search)
      this.getData(this.url_endpoint)

    }, 500),

    form: {
      handler: _.debounce(function(newValue, oldValue) {
        console.log(newValue)
        this.url_endpoint = this.advancedSearch(newValue)
        this.getData(this.url_endpoint)
      }, 500),
      deep: true
    },

    screenWidth: function(newWidth) {
      if (newWidth > 576) {
        this.mobileState = false
      } else {
        this.mobileState = true
      }
    },

    dataCode: function() {
      if (this.dataCode === "pt" || this.dataCode === "adv") {
        this.ptypes = this.requestData

      }
    },

    letterCode: function() {
      this.postData()
    }
  },
  created: function() {
    let vm = this;
    console.log(vm.mobileState)
    if (vm.initialWidth > 576) {
      vm.mobileState = false
    } else {
      vm.mobileState = true
    }

  },
  mounted: function() {
    this.$nextTick(function() {
      let vm = this;
      window.addEventListener('resize', function(e) {
        vm.screenWidth = window.innerWidth
      });
    })
  },

  filters: {
    capitalize: function(value) {
      if (!value) {
        return ''
      }
      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    },
    title: function(value) {
      if (!value) {
        return ''
      }
      var stringPieces = value.toString().split(" ");
      var result = '';
      for (var x = 0; x < stringPieces.length; x++) {
        result += stringPieces[x].charAt(0).toUpperCase() + stringPieces[x].slice(1) + " "
      }
      return result
    },
    address: function(value) {
      if (!value) {
        return ''
      }
      var addressPieces = value.toString().split(" ");
      var result = '';
      for (var x = 0; x < addressPieces.length; x++) {
        if (x === 4) {
          result += addressPieces[x].toUpperCase() + " ";
          continue;
        }
        result += addressPieces[x].charAt(0).toUpperCase() + addressPieces[x].slice(1) + " ";

      }
      return result
    }
  },

  methods: {

    basicSearch: function(searchResult) {
      var commercialTest = /^(commercial)$/ig;
      var dwellersTest = /\b(dwellers)(?:(\sf|\sfi|\sfir|\sfire)?)\b$/ig;
      var homeTest = /\b(home)(?:(o|ow|own|owne|owner|owners)?)\b$/ig;
      var nameTest = /^[a-z ,.'-]+$/ig;
      var policynumberTest = /^[0-9]+$/g;

      if (commercialTest.test(searchResult) || dwellersTest.test(searchResult) || homeTest.test(searchResult)) {
        console.log("We're searching for policy type");
        var base_url = "https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev/JSON/policytype/"
        console.log(dwellersTest.test(searchResult))
        if (dwellersTest.test(searchResult) === true) {
          base_url += "dwellers " + "fire";
          console.log(base_url)
          return base_url
        } else if (homeTest.test(searchResult) === true) {
          base_url += "homeowners";
          return base_url
        } else {
          base_url += searchResult.toLowerCase()
          return base_url
        }


      } else if (nameTest.test(searchResult)) {
        var namelist = searchResult.split(" ")
        var url = "https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev/JSON/contacts" + "?fname=" + namelist[0].toLowerCase()
        if (namelist[1] === undefined) {
          return url
        }
        url += "&lname=" + namelist[1].toLowerCase()
        console.log(url)
        return url

      } else if (policynumberTest.test(searchResult)) {
        console.log("We're searching for policy number");
        var url = "https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev/JSON/policy/" + searchResult
        console.log(url)
        return url

      } else {
        console.log("We're searching for address");
        var url = "https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev/JSON/address/" + searchResult.toLowerCase()
        return url
      }


    },

    advancedSearch: function(formData) {
      var base_url = "https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev/JSON/advanced";
      var first_name_arg = "?fname=" + formData.fname.toLowerCase()
      var last_name_arg = "&lname=" + formData.lname.toLowerCase()
      var address_arg = "&address=" + formData.address.toLowerCase()
      var pnum_arg = "&pnum=" + formData.policy_number.toLowerCase()
      var ptype_arg = "&ptype=" + formData.policy_type.toLowerCase()
      var url = base_url + first_name_arg + last_name_arg + address_arg + pnum_arg + ptype_arg
      return url

    },
    stateHandler: function() {
      if (this.mobileSelectState === 2) {
        this.mobileSelectState += -1;
        return
      }
      this.post = [];
      this.mobileSelectState += -1;
      return
    },

    getData: function(endpoint) {
      var vm = this;
      return fetch(endpoint).then((response) => {
        return response.json()
      }).then((data) => {
        vm.dataCode = data.Policy.pop();
        vm.requestData = data.Policy;
      }).catch(function(error) {
        vm.requestData = error
      });
    },

    postData: function() {
      var postResult = this.post;
      var letter = this.letterCode;
      var vm = this;
      return fetch("https://d1apf2cvs5.execute-api.us-east-1.amazonaws.com/dev/", {
        method: "POST",
        body: JSON.stringify({
          "data": postResult,
          "letter_id": letter
        }),
        headers: new Headers({
          'Content-Type': 'application/json'
        })
      }).then(function(response) {
        return response.json()
      }).then(function(data) {
        urls = data.Url
        for (var i = 0; i < urls.length; i++) {
          window.open(urls[i], "_blank");
        }
      }).catch(function(error) {
        console.log(error)
      });
    }

  },
  computed: {
    selectAll: {
      get: function() {
        if (this.post.length === this.ptypes.length) {
          for (var i = 0; i < this.ptypes.length; i++) {
            if (this.post[i] !== this.ptypes[i].policy_number) {
              return false
            }
            return true
          }
        }

        return false

      },
      set: function(value) {
        var post = [];
        if (value === true) {
          for (var i = 0; i < this.ptypes.length; i++) {
            post.push(this.ptypes[i].policy_number);
          }
          this.post = post;
        }
        this.post = post;
      }
    }

  }

})
