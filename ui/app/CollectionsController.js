(function(){
    angular.module('SrcApp')
        .controller('CollectionsController', CollectionsController);

    CollectionsController.$inject = ['ApiCollectionsService']
    function CollectionsController(ApiCollectionsService){
        var vm = this;
        vm.collapsed = [];

        ApiCollectionsService.GetCollections().then(function(response){
            vm.collections = response.data.result
            angular.forEach(vm.collections, function(col){
                vm.collapsed[col.name] = true;
            });
        });

        vm.getImage = function(imagePath){
            return ApiCollectionsService.GetImage(imagePath);
        }

        vm.removeImage = function(imagePath, collectionName){
            ApiCollectionsService.RemoveImage(imagePath).then(function(res){
                angular.forEach(vm.collections, function(collection){
                    if(collection.name == collectionName){
                        indexOfImage = collection.items.indexOf(imagePath);
                        collection.items.splice(indexOfImage, 1);
                    }
                });
            });
        }
    }

})();