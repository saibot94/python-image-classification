(function(){
    angular.module('SrcApp')
        .controller('BuildModelController', BuildModelController);

    BuildModelController.$inject = ['ApiCollectionsService', 'ApiModelsService'];
    function BuildModelController(ApiCollectionsService, ApiModelsService){
        var vm = this;
        vm.modelRequest = {
            type: 'svc',
            collections: [],
            clusters: 50,
            trainPercentage: 0.5
        };
        vm.showLoadingGif = false;
        vm.collections = [];
        vm.radioData = [
                { label: 'SVC', value: 'svc'},
                { label: 'LinearSVC', value: 'linearsvc'},
         ];



        getCollections();


        vm.buildModel = function(){
            vm.showLoadingGif = true;
            angular.forEach(vm.collections, function(collection){
                if(collection.selected){
                    vm.modelRequest.collections.push(collection.name);
                }
            });

            ApiModelsService.CreateModel(vm.modelRequest).then(function(response){
                vm.showLoadingGif = false;
            });
        }
        function getCollections(){
            vm.showLoadingGif = true;
            ApiCollectionsService.GetCollections().then(function(response){
                vm.collections = response.data.result;
                angular.forEach(vm.collections, function(collection){
                    collection.selected = false;
                });
                vm.showLoadingGif = false;
            });
        }
    }

})();