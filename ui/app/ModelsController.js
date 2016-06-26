(function(){
    angular.module('SrcApp')
        .controller('ModelsController', ModelsController);

    ModelsController.$inject = ['ApiModelsService'];
    function ModelsController(ApiModelsService){
        var vm = this;
        vm.showLoadingGif = false;
        vm.classifiers = [];

        getModels();

        // Implementation below
        function getModels(){
            vm.showLoadingGif = true;

            ApiModelsService.GetModels().then(function(response){
                vm.models = response.data.classifiers;
                vm.showLoadingGif = false;
            });
        }

        vm.deleteModel = function(name){
            console.log(name);
            vm.showLoadingGif = true;
             ApiModelsService.DeleteModel(name).then(function(response){
                vm.showLoadingGif = false;
                if(!angular.isDefined(response.data.error)){
                      getModels();
                } else{
                    console.log(response.data.error)
                }

            });
        }

    }
})();