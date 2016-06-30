(function(){
    angular.module('SrcApp')
        .controller('ModelStatsController', ModelStatsController);

    ModelStatsController.$inject = ['ApiModelsService', '$location'];
    function ModelStatsController(ApiModelsService, $location){

    }

})();