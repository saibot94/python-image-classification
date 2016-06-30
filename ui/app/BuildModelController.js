(function(){
    angular.module('SrcApp')
        .controller('BuildModelController', BuildModelController);

    BuildModelController.$inject = ['ApiCollectionsService', 'ApiModelsService', '$location'];
    function BuildModelController(ApiCollectionsService, ApiModelsService, $location){
        var vm = this;
        vm.modelRequest = {
            type: 'svc',
            collections: [],
            clusters: 50,
            trainPercentage: 0.5,
            limit: false
        };
        vm.showLoadingGif = false;
        vm.collections = [];
        vm.radioData = [
                { label: 'SVC', value: 'svc'},
                { label: 'LinearSVC', value: 'linearsvc'},
         ];
        vm.radioData2 = [
            {label: 'True', value: true},
            {label: 'False', value: false}
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
                console.log(response.data);
                $location.path('/models');
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