(function(){
    angular.module('SrcApp')
        .controller('ModelsController', ModelsController);

    ModelsController.$inject = ['ApiModelsService', 'FileUploader', '$location'];
    function ModelsController(ApiModelsService, FileUploader, $location){
        var vm = this;
        var baseUrl = ApiModelsService.BaseUrl;

        vm.showLoadingGif = true;
        vm.selectedModelName = null;
        vm.classificationResults = null;
        vm.uploadDone = false;
        vm.classifiers = [];



        getModels();
        createUploader();

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

        function createUploader(){
            vm.uploader = new FileUploader({
             url: getFileUrl()
            });

            console.log(vm.uploader.url);

            vm.uploader.filters.push({
                name: 'imageFilter',
                fn: function(item /*{File|FileLikeObject}*/, options) {
                    var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                    return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
                }
            });

            vm.uploader.onCompleteItem = handleCompletion;
            vm.showLoadingGif = false;
        }

        vm.changeSelection = function(){
            vm.uploader.clearQueue();

            changeUploaderUrl();
            vm.uploadDone = false;
        }

        vm.uploadFile = function(item){
            vm.classificationResults = null;
            vm.showLoadingGif = true;
            item.upload();
        }

        vm.goToStats = function(modelName){
            $location.path('/models/' + modelName);
        }

        vm.clearUploader = function(){
            vm.uploader.clearQueue();
            vm.classificationResults = null;
            vm.uploadDone = false;
        }

        function getFileUrl(){
          var fileUrl = null;
            if(vm.selectedModelName != null){
                fileUrl =  baseUrl + '/classify/' + vm.selectedModelName;
            }
            else{
                fileUrl =  baseUrl + '/classify';
            }
           return fileUrl;
        }


        function changeUploaderUrl(){
            vm.classificationResults = null;
            vm.uploader.url = getFileUrl();
        }


        function handleCompletion(fileItem, response, status, headers) {
                 vm.classificationResults = response.prediction;
                 console.log(vm.classificationResults);
                 vm.showLoadingGif = false;
                 vm.uploadDone = true;
                 //vm.uploader.clearQueue();
        };

    }
})();