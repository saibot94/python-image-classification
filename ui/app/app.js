(function() {
	'use strict';

	var app = angular.module('SrcApp', ['nvd3', 'ui.bootstrap', 'ngRoute',
	 'ngAnimate', 'ngMaterial', 'ngAria', 'rzModule'])


	app.config(['$routeProvider',
      function($routeProvider) {
        $routeProvider.
          when('/models', {
            templateUrl: 'templates/models.html',
            controller: 'ModelsController',
            controllerAs: 'vm'
          }).
          when('/collections', {
            templateUrl: 'templates/collections.html',
            controller: 'CollectionsController',
            controllerAs: 'vm'
          }).
          when('/', {
            templateUrl: 'templates/build.html',
            controller: 'BuildModelController',
            controllerAs: 'vm'
          }).
          otherwise({
            redirectTo: '/'
          });
    }]);


})();