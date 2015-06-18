'use strict';

var app = angular.module('example', [
  'ngSanitize',
  'ui.router',
  'ngResource',
  'angular-timeline',
  'angular-scroll-animate',
]);

app.config(function($stateProvider) {
  $stateProvider.state('user', {
    url:         '',
    controller: 'ExampleCtrl',
    templateUrl: '/static/monitor/history/example.html'
  });
});