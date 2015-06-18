'use strict';

var ExampleCtrl = function($rootScope, $document, $timeout, $scope, HistoryService) {

  // var lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. " +
  //             "Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit. Donec et mollis dolor." +
  //             "Praesent et diam eget libero egestas mattis sit amet vitae augue. Nam tincidunt congue enim, " +
  //             "ut porta lorem lacinia consectetur. Donec ut libero sed arcu vehicula ultricies a non tortor." +
  //             "Lorem ipsum dolor sit amet, consectetur adipiscing elit.";

  // $scope.events = [{
  //   badgeClass: 'info',
  //   badgeIconClass: 'glyphicon-check',
  //   title: 'First heading',
  //   when: '11 hours ago via Twitter',
  //   content: 'Some awesome content.'
  // }, {
  //   badgeClass: 'warning',
  //   badgeIconClass: 'glyphicon-credit-card',
  //   title: 'Second heading',
  //   when: '12 hours ago via Twitter',
  //   content: 'More awesome content.'
  // }, {
  //   badgeClass: 'default',
  //   badgeIconClass: 'glyphicon-credit-card',
  //   title: 'Third heading',
  //   titleContentHtml: '<img class="img-responsive" src="http://www.freeimages.com/assets/183333/1833326510/wood-weel-1444183-m.jpg">',
  //   contentHtml: lorem,
  //   footerContentHtml: '<a href="">Continue Reading</a>'
  // }];
  $scope.events = [];

  HistoryService.history(13).then(function (data) {
    console.log(data)
    $scope.events = [];
    angular.forEach(data.history, function(row, index) {
      var row_item = {
            badgeClass: 'info',
            badgeIconClass: 'glyphicon-check',
            title: 'Changed: ' + data.url,
            when: row.date_of,
            content: row.content,
            //contentHtml: '<img id="fileA" src="data:image/png;base64,'+row.screenshot+'" alt="" title="" border="0" />'
          };
      $scope.events.push(row_item);
    });
  });

  // optional: not mandatory (uses angular-scroll-animate)
  $scope.animateElementIn = function($el) {
    $el.removeClass('hidden');
    $el.addClass('bounce-in');
  };

  // optional: not mandatory (uses angular-scroll-animate)
  $scope.animateElementOut = function($el) {
    $el.addClass('hidden');
    $el.removeClass('bounce-in');
  };
};

angular.module('example').controller('ExampleCtrl', ['$rootScope', '$document', '$timeout', '$scope', 'HistoryService', ExampleCtrl]);
