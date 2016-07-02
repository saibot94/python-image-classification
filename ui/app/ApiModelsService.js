(function(){

		angular.module('SrcApp')
			.factory('ApiModelsService', ApiModelsService);

		ApiModelsService.$inject = ['$http', '$location'];
		function ApiModelsService($http, $location){
            var baseUrl = 'http://' + $location.host() + ':' + $location.port() + '/api/models'
            var service = {
                CreateModel: createModel,
                GetModels: getModels,
                DeleteModel: deleteModel,
                GetStats: getStats,
                BaseUrl: baseUrl
            }

            return service;

            function createModel(modelObject){
                return $http({
                    data: modelObject,
                    method: 'POST',
                    url: baseUrl + '/'
                });
            }

            function getModels(){
                return $http({
                    method: 'GET',
                    url: baseUrl + '/'
                });
            }

            function deleteModel(id){
                return $http({
                    url: baseUrl + '/' + id,
                    method: 'DELETE'
                })
            }

            function getStats(name){
                return $http({
                    url: baseUrl + '/stats/' + encodeURIComponent(name),
                    method: 'GET'
                })
            }
		}


})();