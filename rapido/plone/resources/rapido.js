angular.module('rapido',['schemaForm'])
.service('DatabaseService', function($http, $q){
  var _api;
  var _token;
  var _data = {};

  // HARD-CODED FOT NOW
  _api = 'http://localhost:8080/test1/testdb/api';

  this.getApi = function() {
    return _api;
  };
  this.setParameters = function(api, token) {
    _api = api;
    _token = token;
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
      result.data.layout = result.data.layout.replace(/data-rapido-field/g, 'sf-insert-field');
      _data = result.data;
      deferred.resolve();
    });
    return deferred.promise;
  };
  this.save = function(form_id, model) {
    model.Form = form_id;
    if(model.docid) {
      return $http.post(
        this.getApi() + '/' + model.docid,
        model,
        {headers: {'X-CSRF-TOKEN': _token}})
      .then(function(result) {
        console.log(result);
      });
    } else {
      return $http.put(this.getApi() + '/document', model)
      .then(function(result) {
        console.log(result);
      });
    }
  }

})
.directive('rapidoApi', function(DatabaseService) {
  return {
    restrict: 'A',
    scope: false,
    link: function (scope, element, attrs) {
      DatabaseService.setParameters(attrs.rapidoApi, attrs.rapidoToken);
    }
  }
})
.controller('DatabaseCtrl', function($scope, $http, DatabaseService){

  $scope.decorator = 'bootstrap-decorator';

  DatabaseService.load('/8736169359445/_full').then(function() {
    $scope.model = DatabaseService.getData().items || {};
    $scope.layout = DatabaseService.getLayout();
    $scope.schema = DatabaseService.getData().schema;
    $scope.form = DatabaseService.getData().form;
  });

  $scope.submitForm = function(form, model) {
    // First we broadcast an event so all fields validate themselves
    $scope.$broadcast('schemaFormValidate');
    // Then we check if the form is valid
    if (form.$valid) {
      DatabaseService.save('frmtest', model);
    }
  }


});
