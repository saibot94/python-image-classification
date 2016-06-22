(function(){
    angular.module('SrcApp')
        .controller('CollectionsController', CollectionsController);

    CollectionsController.$inject = ['ApiCollectionsService']
    function CollectionsController(ApiCollectionsService){
        var vm = this;
        vm.collapsed = [];
        vm.formOptions = {};
        vm.showLoadingGif = false;

        // Init phase
        getCollections();

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

        vm.deleteCollection = function(name){
            ApiCollectionsService.DeleteCollection(name).then(function(res){
                getCollections();
            });
        }

        vm.createCollection = function(){
            vm.showLoadingGif = true;
            if(vm.formOptions.numberOfResults == 0){
                vm.formOptions.numberOfResults = 200;
            }
            var name = vm.formOptions.collectionName;
            var query = vm.formOptions.query;
            var nrResults = vm.formOptions.numberOfResults;

            ApiCollectionsService.CreateCollection(name, query, nrResults).then(function(res){
                console.log(res);
                getCollections();
            });

        }


        function getCollections(){
            vm.showLoadingGif = true;
            ApiCollectionsService.GetCollections().then(function(response){
                vm.collections = response.data.result
                angular.forEach(vm.collections, function(col){
                    vm.collapsed[col.name] = true;
                });
                vm.showLoadingGif = false;
            });
        }
    }

})();