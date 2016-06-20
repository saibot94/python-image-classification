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
    }

})();