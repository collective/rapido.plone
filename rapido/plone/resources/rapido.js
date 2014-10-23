angular.module('rapido',['schemaForm'])
.service('DatabaseService', function($http, $q){
  var _api;
  var _data = {};

  // HARD-CODED FOT NOW
  _api = 'http://localhost:8080/test1/testdb/api';

  this.getApi = function() {
    return _api;
  };
  this.setApi = function(api) {
    _api = api;
  };
  this.getLayout = function() {
    return _data.layout;
  };
  this.getData = function() {
    return _data;
  };
  this.load = function(resource) {
    var deferred = $q.defer();
    if(!resource) {
      resource = '/form/frmtest';
    }
    $http.get(this.getApi() + resource)
    .then(function(result) {
      _data = result.data;
      deferred.resolve();
    });
    return deferred.promise;
  };

})
.directive('rapidoApi', function(DatabaseService) {
  return {
    restrict: 'A',
    scope: true,
    link: function (scope, iElement, iAttrs) {
      // console.log(iAttrs.rapidoApi);
      // DatabaseService.setApi(iAttrs.rapidoApi);
      // DatabaseService.load();
    }
  }
})
.controller('DatabaseCtrl', function($scope, DatabaseService){
  console.log('api='+DatabaseService.getApi());
    // $http.get(val.data).then(function(res){
    //     $scope.schema = res.data.schema;
    //     $scope.form   = res.data.form;
    //   });

    $scope.service = DatabaseService;
    DatabaseService.load().then(function() {
      $scope.model = {};
      $scope.layout = DatabaseService.getLayout();
      $scope.schema = DatabaseService.getData().schema;
      $scope.form = DatabaseService.getData().form;
    });

  //   $scope.schema = {
  //   "type": "object",
  //   "title": "Comment",
  //   "properties": {
  //     "name":  {
  //       "title": "Name",
  //       "type": "string"
  //     },
  //     "email":  {
  //       "title": "Email",
  //       "type": "string",
  //       "pattern": "^\\S+@\\S+$",
  //       "description": "Email will be used for evil."
  //     },
  //     "comment": {
  //       "title": "Comment",
  //       "type": "string",
  //       "maxLength": 20,
  //       "validationMessage": "Don't be greedy!"
  //     }
  //   },
  //   "required": ["name","email","comment"]
  // };
  // $scope.form = [
  //   "name",
  //   "email",
  //   {
  //     "key": "comment",
  //     "type": "textarea"
  //   },
  //   {
  //     "type": "submit",
  //     "style": "btn-info",
  //     "title": "OK"
  //   }
  // ];

});
