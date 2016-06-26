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
          when('/build_phase_2', {
            templateUrl: 'templates/build_phase_2.html',
            controller: 'BuildModelController',
            controllerAs: 'vm'
          }).
          when('/', {
            templateUrl: 'templates/build.html',
            controller: 'BuildMainController',
            controllerAs: 'vm'
          }).
          otherwise({
            redirectTo: '/'
          });
    }]);


})();