'use strict';

var HistoryService = function ($q, $log, $resource) {
    function historyAPI() {
        return $resource('/v1/url/:pk', {}, {
            'query': {'cache': true, 'isArray': false}
        });
    }

    return {
        history: function (url_pk) {
            var deferred = $q.defer();
            var api = historyAPI();

            api.get({'pk': url_pk},
                function success(data) {
                    deferred.resolve(data.toJSON());
                },
                function error(err) {
                    deferred.reject(err);
                }
            );
            return deferred.promise;
        }
    };
};

angular.module('example').service('HistoryService', ['$q', '$log', '$resource', HistoryService]);