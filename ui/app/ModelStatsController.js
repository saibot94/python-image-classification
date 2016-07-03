(function(){
    angular.module('SrcApp')
        .controller('ModelStatsController', ModelStatsController);

    ModelStatsController.$inject = ['ApiModelsService', '$location', '$routeParams'];
    function ModelStatsController(ApiModelsService, $location, $routeParams){
        var vm = this;
        vm.modelNameComponents = $routeParams.modelName.split('~');
        vm.modelName = $routeParams.modelName;
        vm.table = {
            keys: []
        };
        vm.showLoadingGif = true;


        function buildKeys(key, value){
            vm.table.keys.push(key);
        }

        // Iterate over a map of values and apply the keyValueFunction to each pair
        function keyValueIteration(map, fct){
            for (var key in map) {
                  if (map.hasOwnProperty(key)) {
                  fct(key, map[key])
                  }
            }
       }


       // Init code to run
        ApiModelsService.GetStats(vm.modelName).then(function(res){
            vm.stats = res.data;
            keyValueIteration(vm.stats.matrix, function(key, val){ console.log(key + '->'); console.log(val);});
            keyValueIteration(vm.stats.matrix, buildKeys);
            vm.showLoadingGif = false;

        });

    }

})();