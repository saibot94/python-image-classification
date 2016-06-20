(function(){

		angular.module('SrcApp')
			.factory('ApiCollectionsService', ApiCollectionsService);

		ApiCollectionsService.$inject = ['$http', '$location'];
		function ApiCollectionsService($http, $location){
            var baseUrl = 'http://' + $location.host() + ':' + $location.port() + '/api/collections'
            var service = {
                GetCollections: getCollections,
                GetImage: getImage
            }

            return service;


            function getCollections(){
                return $http({
                    method: 'GET',
                    url: baseUrl + '/',
                    isArray: true
                })
            }

            function getImage(imagePath){
                return baseUrl + '/get_image?name=' + imagePath
            }
		}


})();