(function(){

		angular.module('SrcApp')
			.factory('ApiCollectionsService', ApiCollectionsService);

		ApiCollectionsService.$inject = ['$http', '$location'];
		function ApiCollectionsService($http, $location){
            var baseUrl = 'http://' + $location.host() + ':' + $location.port() + '/api/collections'
            var service = {
                GetCollections: getCollections,
                GetImage: getImage,
                RemoveImage: removeImage
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
                return baseUrl + '/image?name=' + imagePath
            }

            function removeImage(imagePath){
                return $http({
                    method: 'DELETE',
                    url: baseUrl + '/image',
                    params: {name: imagePath}
                });
            }
		}


})();