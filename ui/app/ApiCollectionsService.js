(function(){

		angular.module('SrcApp')
			.factory('ApiCollectionsService', ApiCollectionsService);

		ApiCollectionsService.$inject = ['$http', '$location'];
		function ApiCollectionsService($http, $location){
            var baseUrl = 'http://' + $location.host() + ':' + $location.port() + '/api/collections'
            var service = {
                GetCollections: getCollections,
                GetImage: getImage,
                RemoveImage: removeImage,
                DeleteCollection: deleteCollection,
                CreateCollection: createCollection
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

            function deleteCollection(collectionName){
                return $http({
                    method: 'DELETE',
                    url: baseUrl + '/' + collectionName
                });
            }

            function createCollection(name, query, nrResults){
                return $http({
                    method: 'POST',
                    url: baseUrl + '/' + encodeURIComponent(name) + '/' +
                             encodeURIComponent(query) + '/' + encodeURIComponent(nrResults)
                });
            }
		}


})();