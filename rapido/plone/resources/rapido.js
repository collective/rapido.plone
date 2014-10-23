angular.module('rapido',['schemaForm'])
.service('DatabaseService', function($http, $q){
  var _api = './api';
  var _token;
  var _data = {}; 

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
    $http.get(this.getApi() + resource)
    .then(function(result) {
      deferred.resolve(result);
    });
    return deferred.promise;
  };

  this.loadMenu = function() {
    return this.load('/database');
  };

  this.loadForm = function(resource) {
    return this.load(resource)
    .then(function(result) {
      result.data.layout = result.data.layout.replace(/data-rapido-field/g, 'sf-insert-field');
      _data = result.data;
    });
  };

  this.save = function(form_id, model) {
    var deferred = $q.defer();
    model.Form = form_id;
    if(model.docid) {
      $http.post(
        this.getApi() + '/' + model.docid,
        model,
        {headers: {'X-CSRF-TOKEN': _token}})
      .then(function(result) {
        _data.model = result.data.model;
        deferred.resolve(result.data.model);
      });
    } else {
      $http.put(this.getApi() + '/document', model)
      .then(function(result) {
        _data.model = result.data.model;
        deferred.resolve(result.data.model);
      });
    }
    return deferred.promise;
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
.controller('DatabaseCtrl', function($rootScope) {
  $rootScope.state = "menu";
})
.controller('MenuCtrl', function($scope, $rootScope, DatabaseService) {
  DatabaseService.loadMenu().then(function(result) {
    $scope.forms = result.data.forms;
  })
  $scope.openForm = function(formId) {
    $rootScope.state = "form";
    $rootScope.formId = formId;
  };
  $scope.openMenu = function() {
    $rootScope.state = "menu";
    delete $rootScope.formId;
  };
  $scope.openView = function() {
    $rootScope.state = "view";
    delete $rootScope.formId;
  };
})
.controller('FormCtrl', function($scope, $rootScope, $http, DatabaseService){

  $scope.decorator = 'bootstrap-decorator';

  var resource = '/form/' + $scope.formId;
  if($rootScope.docId) {
    resource = $scope.docId + '/_full';
  }
  DatabaseService.loadForm(resource).then(function() {
    $scope.model = DatabaseService.getData().model || {};
    $scope.layout = DatabaseService.getLayout();
    $scope.schema = DatabaseService.getData().schema;
    $scope.form = DatabaseService.getData().form;
  });

  $scope.submitForm = function(form, model) {
    // First we broadcast an event so all fields validate themselves
    $scope.$broadcast('schemaFormValidate');
    // Then we check if the form is valid
    if (form.$valid) {
      DatabaseService.save($rootScope.formId, model).then(function(data) {
        $rootScope.docId = data.docid;
        $scope.model = data;
      });
    }
  }
});
